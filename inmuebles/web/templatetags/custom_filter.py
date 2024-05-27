from django import template

register = template.Library()

def format_rut(rut:str) -> str:
    body = rut[:-1]
    verifier = rut[-1]

    return f'{body[:-6]}.{body[:-3]}.{body[-3:]}-{verifier}'