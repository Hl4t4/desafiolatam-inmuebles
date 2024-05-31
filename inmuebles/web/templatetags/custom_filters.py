from django import template

register = template.Library()

@register.filter
def format_rut(rut:str) -> str:
    body = rut[:-1]
    verifier = rut[-1]

    return f'{body[:-6]}.{body[-6:-3]}.{body[-3:]}-{verifier}'

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def none_esp(value):
    if value is None:
        return 'No hay'
    else:
        return value

@register.filter(name='as_dict')
def as_dict(obj):
    if hasattr(obj, 'as_dict'):
        return obj.as_dict()
    else:
        return {}