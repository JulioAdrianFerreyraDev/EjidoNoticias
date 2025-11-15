from django.db import models
import os
import io
from PIL import Image, ImageOps
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile # <--- Importación necesaria
from ckeditor_uploader.fields import RichTextUploadingField

# --- Modelo de Categorías ---
# Una noticia pertenece a UNA categoría (Relación Uno a Muchos)
# Ej: "Deportes", "Política", "Tecnología"
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            help_text="Usado para las URLs. Ej: 'deportes'")
    banner = models.ImageField(
        upload_to='categorias/%Y/%m/%d/',
        verbose_name="Banner Principal",
        help_text="Imagen principal de la categoría.",
        default="https://placehold.co/600x400.webp"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    # --- INICIO: LÓGICA DE PROCESAMIENTO DE IMAGEN ---

    def save(self, *args, **kwargs):
        """
        Sobrescribe el guardado para procesar el banner de la categoría.
        """
        try:
            instancia_db = Categoria.objects.get(pk=self.pk)
            banner_antiguo = instancia_db.banner
        except Categoria.DoesNotExist:
            instancia_db = None
            banner_antiguo = None

        procesar_imagen = False
        
        # Comprobamos que 'self.banner' tenga el atributo 'file'.
        # Esto es crucial para filtrar el 'default' (que es un string)
        # y procesar solo cuando se sube un archivo nuevo.
        if self.banner and hasattr(self.banner, 'file'):
            if not instancia_db or banner_antiguo != self.banner:
                procesar_imagen = True

        if procesar_imagen:
            self.procesar_banner_categoria()
            
            # Opcional: Borrar el banner antiguo si existía y era un archivo
            if instancia_db and banner_antiguo and banner_antiguo != self.banner:
                if hasattr(banner_antiguo, 'path'): # No intentar borrar el default
                    banner_antiguo.storage.delete(banner_antiguo.name)

        super().save(*args, **kwargs)

    def procesar_banner_categoria(self):
        """
        Redimensiona, recorta a 614x256 y convierte a WebP el banner.
        """
        if not self.banner or not hasattr(self.banner, 'file'):
            return

        img = Image.open(self.banner)
        
        # Definimos el tamaño exacto
        tamano_deseado = (614, 256)
        
        # --- 1. Redimensionar y Recortar ---
        # ImageOps.fit() escala y recorta la imagen para que coincida
        # exactamente con el tamaño, usando el centro como punto focal.
        # Esto evita que la imagen se estire o distorsione.
        img_procesada = ImageOps.fit(img, tamano_deseado, Image.Resampling.LANCZOS)

        # Obtenemos la ruta base y el nombre (sin extensión)
        ruta_base_nombre, _ = os.path.splitext(self.banner.name)
        
        # --- 2. Guardar como WebP ---
        buffer_banner = io.BytesIO()
        img_procesada.save(buffer_banner, format='WEBP', quality=85)
        
        # Generamos el nuevo nombre de archivo
        nombre_banner = f"{ruta_base_nombre}.webp"
        
        # Asignamos el nuevo archivo usando el método .save() del campo
        self.banner.save(nombre_banner, 
                         ContentFile(buffer_banner.getvalue()), 
                         save=False) # save=False para evitar bucle

    # --- FIN: LÓGICA DE PROCESAMIENTO ---

# --- Modelo de Tags ---
# Una noticia puede tener MUCHOS tags (Relación Muchos a Muchos)
# Ej: "IA", "Elecciones", "Apple"
class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=50, unique=True, db_index=True,
                            help_text="Usado para las URLs. Ej: 'inteligencia-artificial'")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# --- Modelo Principal: Noticia ---
class Noticia(models.Model):
    # ... (campos: titulo, slug, subtitulo, contenido) ...
    titulo = models.CharField(max_length=255, verbose_name="Título")
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            help_text="URL amigable, autogenerada o manual. Ej: 'mi-gran-noticia-2025'")
    subtitulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtítulo")
    contenido = RichTextUploadingField(verbose_name="Contenido")
    
    # --- Banner y Thumbnails ---
    banner = models.ImageField(
        upload_to='noticias/banners/%Y/%m/%d/',
        verbose_name="Banner Principal",
        help_text="Imagen principal. Se redimensionará a 1920x1080 si es más grande."
    )
    # --- NUEVOS CAMPOS PARA THUMBNAILS ---
    banner_medium = models.ImageField(
        upload_to='noticias/banners/%Y/%m/%d/',
        verbose_name="Thumbnail Mediano",
        blank=True, null=True,
        editable=False # Oculto en el admin, se genera solo
    )
    banner_small = models.ImageField(
        upload_to='noticias/banners/%Y/%m/%d/',
        verbose_name="Thumbnail Pequeño",
        blank=True, null=True,
        editable=False # Oculto en el admin, se genera solo
    )
    # --- Fin de nuevos campos ---
    
    # ... (campos: categoria, autor, tags) ...
    categoria = models.ForeignKey(
        'Categoria', # Asumiendo que 'Categoria' está en el mismo archivo o importada
        on_delete=models.PROTECT,
        related_name="noticias",
        verbose_name="Categoría"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="noticias_escritas",
        verbose_name="Autor"
    )
    tags = models.ManyToManyField(
        'Tag', # Asumiendo que 'Tag' está en el mismo archivo o importada
        blank=True,
        related_name="noticias",
        verbose_name="Tags"
    )

    # ... (campos: vistas, tiempo_lectura, fechas, publicado) ...
    vistas = models.PositiveIntegerField(default=0, verbose_name="Vistas",
                                       help_text="Contador de vistas")
    tiempo_lectura = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="Tiempo de lectura (min)",
        help_text="Tiempo estimado de lectura en minutos"
    )
    fecha_publicacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de publicación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    publicado = models.BooleanField(default=True, verbose_name="¿Publicado?")

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo

    # --- INICIO: LÓGICA DE PROCESAMIENTO DE IMÁGENES ---

    def save(self, *args, **kwargs):
        """
        Sobrescribe el guardado para procesar el banner.
        """
        try:
            instancia_db = Noticia.objects.get(pk=self.pk)
        except Noticia.DoesNotExist:
            instancia_db = None

        # Procesar solo si el banner es nuevo o cambió
        if not instancia_db or (instancia_db.banner != self.banner):
            if self.banner:
                self.procesar_banner()

        super().save(*args, **kwargs)

    def procesar_banner(self):
        """
        Redimensiona, convierte a WebP y crea thumbnails del banner.
        (Versión corregida usando el método .save() del campo)
        """
        if not self.banner:
            return

        img = Image.open(self.banner)
        
        # 1. Redimensionar Banner Principal
        if img.width > 1920 or img.height > 1080:
            img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)

        # Obtenemos el nombre base (sin extensión) y la ruta
        # Ej: 'noticias/banners/2025/11/14/mi-foto'
        ruta_base_nombre, _ = os.path.splitext(self.banner.name)
        
        # --- 2. Guardar Banner Principal como WebP ---
        buffer_banner = io.BytesIO()
        img.save(buffer_banner, format='WEBP', quality=80)
        
        # Generamos el nuevo nombre de archivo
        nombre_banner = f"{ruta_base_nombre}.webp"
        
        # Forma correcta:
        # Llama a .save() EN EL CAMPO, no en el modelo
        # (save=False evita que se guarde el modelo, solo asigna el archivo)
        self.banner.save(nombre_banner, 
                         ContentFile(buffer_banner.getvalue()), 
                         save=False)

        # --- 3. Crear Thumbnail Mediano (800px ancho) ---
        thumb_medium = img.copy()
        thumb_medium.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        buffer_medium = io.BytesIO()
        thumb_medium.save(buffer_medium, format='WEBP', quality=75)
        
        nombre_medium = f"{ruta_base_nombre}-medium.webp"
        self.banner_medium.save(nombre_medium, 
                                ContentFile(buffer_medium.getvalue()), 
                                save=False)

        # --- 4. Crear Thumbnail Pequeño (300px ancho) ---
        thumb_small = img.copy()
        thumb_small.thumbnail((300, 200), Image.Resampling.LANCZOS)
        
        buffer_small = io.BytesIO()
        thumb_small.save(buffer_small, format='WEBP', quality=70)
        
        nombre_small = f"{ruta_base_nombre}-small.webp"
        self.banner_small.save(nombre_small, 
                               ContentFile(buffer_small.getvalue()), 
                               save=False)

    # --- FIN: LÓGICA DE PROCESAMIENTO DE IMÁGENES ---