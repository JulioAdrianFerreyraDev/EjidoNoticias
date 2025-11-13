from django.db import models
from django.conf import settings
from django.utils import timezone
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
        default="https://placehold.co/616x256?text=Categoría"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

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
    # --- Contenido Principal ---
    titulo = models.CharField(max_length=255, verbose_name="Título")
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            help_text="URL amigable, autogenerada o manual. Ej: 'mi-gran-noticia-2025'")
    subtitulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtítulo")
    
    # --- El RichText Box ---
    # Este campo requiere 'django-ckeditor'
    contenido = RichTextUploadingField(verbose_name="Contenido")
    
    # --- Banner/Imagen Principal ---
    # Guarda las imágenes en 'media/noticias/banners/AÑO/MES/DIA/'
    banner = models.ImageField(
        upload_to='noticias/banners/%Y/%m/%d/',
        verbose_name="Banner Principal",
        help_text="Imagen principal que aparecerá en la parte superior de la noticia."
    )
    
    # --- Relaciones ---
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,  # No permite borrar una categoría si tiene noticias
        related_name="noticias",
        verbose_name="Categoría"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relacionado con el modelo User de Django
        on_delete=models.SET_NULL, # Si se borra el autor, la noticia permanece (autor=null)
        null=True,
        related_name="noticias_escritas",
        verbose_name="Autor"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,  # Una noticia puede no tener tags
        related_name="noticias",
        verbose_name="Tags"
    )
    
    # --- Metadatos ---
    vistas = models.PositiveIntegerField(default=0, verbose_name="Vistas",
                                       help_text="Contador de vistas")
    tiempo_lectura = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="Tiempo de lectura (min)",
        help_text="Tiempo estimado de lectura en minutos"
    )
    
    # --- Fechas ---
    fecha_publicacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de publicación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,  # Se actualiza automáticamente cada vez que se guarda
        verbose_name="Última actualización"
    )
    
    # --- Estado ---
    publicado = models.BooleanField(default=True, verbose_name="¿Publicado?")

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        # Ordena las noticias por defecto, de más nueva a más vieja
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo