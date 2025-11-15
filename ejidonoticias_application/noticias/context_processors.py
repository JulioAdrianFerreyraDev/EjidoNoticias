from .models import RedSocial

def redes_sociales_context_processor(request):
    """
    Context processor para agregar las redes sociales a todas las plantillas.
    """
    redes = RedSocial.objects.all()
    return {
        'redes_sociales': redes
    }