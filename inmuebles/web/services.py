from web.models import Inmueble, Usuario, TipoUsuario, TipoInmueble, SolicitudArriendo, Comuna, Region
from django.core.exceptions import ValidationError


def get_all_inmuebles () -> list[Inmueble]:
    return Inmueble.objects.all()

def imprimir_all_inmuebles () -> None:
    inmuebles = get_all_inmuebles()
    for inmueble in inmuebles:
        print(f'Inmueble\n{inmueble}')

def insertar_inmueble (nombre:str, descripcion:str, m2_construidos:float, m2_terreno:float, estacionamientos:int, restrooms:int, habitaciones:int, direccion:str, comuna:Comuna, region:Region, tipo_inmueble:TipoInmueble, arriendo:int) -> Inmueble:
    inmueble = Inmueble(nombre = nombre, descripcion = descripcion, m2_construidos = m2_construidos, m2_terreno = m2_terreno, estacionamientos = estacionamientos, restrooms = restrooms, habitaciones = habitaciones, direccion = direccion, comuna = comuna, region = region, tipo_inmueble = tipo_inmueble, arriendo = arriendo)
    inmueble.save
    return inmueble

def actualizar_inmueble_aux (inmueble:Inmueble, **kargs):
    for key,value in kargs.items():
        if value is not None:
            inmueble[key] = value
            try:
                inmueble.save()
            except ValidationError as e:
                print(f'Ha ocurrido un error: {e}')
        

def actualizar_inmueble (inmueble:Inmueble, nombre:str = None, descripcion:str = None, m2_construidos:float = None, m2_terreno:float = None, estacionamientos:int = None, restrooms:int = None, habitaciones:int = None, direccion:str = None, comuna:Comuna = None, region:Region = None, tipo_inmueble:TipoInmueble = None, arriendo:int = None, arrendador:Usuario = None, arrendatario:Usuario = None):
    actualizar_inmueble_aux(inmueble, {'nombre':nombre, 'descripcion':descripcion, 'm2_construidos':m2_construidos, 'm2_terreno':m2_terreno, 'estacionamientos':estacionamientos, 'restrooms':restrooms, 'habitaciones':habitaciones, 'direccion':direccion, 'id_comuna':comuna, 'id_region':region, 'tipo_inmueble':tipo_inmueble, 'arriendo':arriendo, 'arrendador':arrendador, 'arrendatario':arrendatario})

def borrar_inmueble (inmueble:Inmueble):
    inmueble.delete()

def test ():
    
    pass