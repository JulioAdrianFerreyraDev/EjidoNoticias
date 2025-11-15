# core/templatetags/custom_tags.py
from django import template
from django.utils.formats import number_format

register = template.Library()

@register.filter
def short_format(num):
    """
    Formatea un número en un formato corto y legible (ej: 1.5k, 2.1M).
    """
    try:
        num = int(num)
    except (ValueError, TypeError):
        return num

    if num < 1000:
        return str(num)
    
    if num < 1000000:
        k_val = num / 1000
        # number_format redondea a 1 decimal
        return f"{number_format(k_val, 1)}k"
        
    m_val = num / 1000000
    return f"{number_format(m_val, 1)}M"

@register.filter
def format_read_time(minutes):
    """
    Formatea el tiempo de lectura en un formato legible (ej: '5 min read').
    """
    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        return minutes

    if minutes == 1:
        return "1 min"
    elif minutes > 60:
        hours = minutes // 60
        return f"{hours} hrs"
    return f"{minutes} mins"