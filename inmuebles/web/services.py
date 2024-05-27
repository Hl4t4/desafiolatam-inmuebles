from web.models import Inmueble, Usuario, TipoUsuario, TipoInmueble, SolicitudArriendo, Comuna, Region
from django.core.exceptions import ValidationError
import sys, json


def get_all_inmuebles () -> list[Inmueble]:
    return Inmueble.objects.all()

def imprimir_all_inmuebles () -> None:
    inmuebles = get_all_inmuebles()
    for inmueble in inmuebles:
        print(f'Inmueble\n{inmueble}')

def insertar_inmueble (nombre:str, descripcion:str, m2_construidos:float, m2_totales:float, estacionamientos:int, restrooms:int, habitaciones:int, direccion:str, comuna:Comuna, region:Region, tipo_inmueble:TipoInmueble, arriendo:int, arrendatario:Usuario) -> Inmueble:
    inmueble = Inmueble(nombre = nombre, descripcion = descripcion, m2_construidos = m2_construidos, m2_totales = m2_totales, estacionamientos = estacionamientos, restrooms = restrooms, habitaciones = habitaciones, direccion = direccion, comuna = comuna, region = region, tipo_inmueble = tipo_inmueble, arriendo = arriendo, arrendatario = arrendatario)
    inmueble.save
    return inmueble

def actualizar_inmueble_aux (inmueble:Inmueble, **kargs) -> Inmueble:
    for key,value in kargs.items():
        if value is not None:
            setattr(inmueble, key, value)
            try:
                inmueble.save()
            except ValidationError as e:
                print(f'Ha ocurrido un error: {e}')
    return inmueble
        

def actualizar_inmueble (inmueble:Inmueble, nombre:str = None, descripcion:str = None, m2_construidos:float = None, m2_totales:float = None, estacionamientos:int = None, restrooms:int = None, habitaciones:int = None, direccion:str = None, comuna:Comuna = None, region:Region = None, tipo_inmueble:TipoInmueble = None, arriendo:int = None, arrendador:Usuario = None, arrendatario:Usuario = None) -> Inmueble:
    actualizar_inmueble_aux(inmueble, nombre = nombre, descripcion = descripcion, m2_construidos = m2_construidos, m2_totales = m2_totales, estacionamientos = estacionamientos, restrooms = restrooms, habitaciones = habitaciones, direccion = direccion, id_comuna = comuna, id_region = region, tipo_inmueble = tipo_inmueble, arriendo = arriendo, arrendador = arrendador, arrendatario = arrendatario)
    return inmueble

def borrar_inmueble (inmueble:Inmueble):
    if inmueble is not None:
        inmueble.delete()

def test ():
    usuarios = Usuario.objects.all()
    inmuebles = get_all_inmuebles()
    comunas = Comuna.objects.all()
    regiones = Region.objects.all()
    tipos_inmuebles = TipoInmueble.objects.all()
    tipos_usuarios = TipoUsuario.objects.all()

    original_stdout = sys.stdout
    file = open('output.txt', 'w', encoding='utf-8')
    sys.stdout = file

    print(usuarios)
    print(inmuebles)
    imprimir_all_inmuebles ()
    print('\n')
    print('\n')
    print('\n')

    arrendatario = Usuario.objects.filter(tipo_de_usuario = '5').first()

    inmueble1 = insertar_inmueble(nombre = 'nombre 1', descripcion = 'Descripcion 1', m2_construidos= 10.0, m2_totales = 15.0, estacionamientos = 5, restrooms = 3, habitaciones = 4, direccion = 'Direccion 1', comuna = comunas[3], region = regiones[3], tipo_inmueble = tipos_inmuebles[0], arriendo = 999000, arrendatario = arrendatario)
    inmueble2 = insertar_inmueble(nombre = 'nombre 2', descripcion = 'Descripcion 2', m2_construidos= 20.0, m2_totales = 25.0, estacionamientos = 1, restrooms = 1, habitaciones = 3, direccion = 'Direccion 2', comuna = comunas[4], region = regiones[4], tipo_inmueble = tipos_inmuebles[1], arriendo = 500000, arrendatario = arrendatario)
    inmueble3 = insertar_inmueble(nombre = 'nombre 3', descripcion = 'Descripcion 3', m2_construidos= 30.0, m2_totales = 35.0, estacionamientos = 2, restrooms = 2, habitaciones = 2, direccion = 'Direccion 3', comuna = comunas[5], region = regiones[5], tipo_inmueble = tipos_inmuebles[2], arriendo = 1500000, arrendatario = arrendatario)
    inmueble4 = insertar_inmueble(nombre = 'nombre 4', descripcion = 'Descripcion 4', m2_construidos= 40.0, m2_totales = 45.0, estacionamientos = 3, restrooms = 4, habitaciones = 1, direccion = 'Direccion 4', comuna = comunas[6], region = regiones[6], tipo_inmueble = tipos_inmuebles[1], arriendo = 50000, arrendatario = arrendatario)
    inmueble5 = insertar_inmueble(nombre = 'nombre 5', descripcion = 'Descripcion 5', m2_construidos= 50.0, m2_totales = 55.0, estacionamientos = 4, restrooms = 5, habitaciones = 5, direccion = 'Direccion 5', comuna = comunas[7], region = regiones[7], tipo_inmueble = tipos_inmuebles[2], arriendo = 405000, arrendatario = arrendatario)
    inmueble6 = insertar_inmueble(nombre = 'nombre 6', descripcion = 'Descripcion 6', m2_construidos= 60.0, m2_totales = 65.0, estacionamientos = 50, restrooms = 6, habitaciones = 6, direccion = 'Direccion 6', comuna = comunas[8], region = regiones[8], tipo_inmueble = tipos_inmuebles[0], arriendo = 800000, arrendatario = arrendatario)

    inmueble1.save()
    inmueble2.save()
    inmueble3.save()
    inmueble4.save()
    inmueble5.save()
    inmueble6.save()
    
    print(inmueble1)
    print(inmueble2)
    print(inmueble3)
    print(inmueble4)
    print(inmueble5)
    print(inmueble6)
    print('\n')
    print('\n')
    print('\n')

    inmueble1 = actualizar_inmueble(inmueble1, comuna = comunas[15])
    inmueble2 = actualizar_inmueble(inmueble2, region = regiones[2], arriendo = 420000)
    inmueble3 = actualizar_inmueble(inmueble3, tipo_inmueble = tipos_inmuebles[1])

    print(inmueble1)
    print(inmueble2)
    print(inmueble3)
    print('\n')
    print('\n')
    print('\n')

    print('\n')
    print('\n')
    imprimir_all_inmuebles()
    borrar_inmueble(inmueble5)    
    imprimir_all_inmuebles()
    print('\n')
    print('\n')
    
    borrar_inmueble(inmueble1)    
    borrar_inmueble(inmueble2)    
    borrar_inmueble(inmueble3)    
    borrar_inmueble(inmueble4)    
    borrar_inmueble(inmueble6)    


    sys.stdout = original_stdout
    file.close()

def get_fixtures():
    comunas = Comuna.objects.all().values()
    regiones = Region.objects.all().values()

    with open(f'web/fixtures/comunas.json', 'w', encoding = 'utf-8') as file:
        serialized_data = []
        for comuna in comunas:
            serialized_obj = {
                "model": "web.Comuna",  # Replace with the actual app_label and model_name
                "pk": comuna["id"],  # Assuming 'id' is the primary key field
                "fields": comuna  # Add all other fields of the object
            }
            serialized_data.append(serialized_obj)
        # file.write(serialized_data)
        json.dump(serialized_data, file, indent=4, ensure_ascii=False)
    with open(f'web/fixtures/regiones.json', 'w', encoding = 'utf-8') as file:
        serialized_data = []
        for region in regiones:
            serialized_obj = {
                "model": "web.Region",  # Replace with the actual app_label and model_name
                "pk": region["id"],  # Assuming 'id' is the primary key field
                "fields": region  # Add all other fields of the object
            }
            serialized_data.append(serialized_obj)
        json.dump(serialized_data, file, indent=4, ensure_ascii=False)
        # file.write(serialized_data)
def get_inmuebles(nombre:str, descripcion:str) -> list[Inmueble]:
    raw_query = f"""
        SELECT * 
        FROM web_inmueble
        WHERE web_inmueble.nombre = '{nombre}' AND web_inmueble.descripcion = '{descripcion}'
        ORDER BY web_inmueble.comuna_id;
    """
    inmuebles = Inmueble.objects.raw(raw_query)
    # inmuebles = Inmueble.objects.filter(descripcion = descripcion).filter(nombre = nombre).raw(raw_query)
    for inmueble in inmuebles:
        print(f'Inmueble: {inmueble}')
    return inmuebles

def get_inmuebles(nombre:str, descripcion:str) -> list[Inmueble]:
    raw_query = f"""
        SELECT * 
        FROM web_inmueble
        WHERE web_inmueble.nombre = '{nombre}' AND web_inmueble.descripcion = '{descripcion}'
        ORDER BY web_inmueble.comuna_id;
    """
    inmuebles = Inmueble.objects.raw(raw_query)
    # inmuebles = Inmueble.objects.filter(descripcion = descripcion).filter(nombre = nombre).raw(raw_query)
    old_comuna = ''
    with open('outputs/inmuebles_punto2.txt', 'w', encoding='utf-8') as file:
        for inmueble in inmuebles:
            # nombre_comuna = Comuna.objects.get(id = inmueble.comuna).nombre_comuna
            nombre_comuna = inmueble.comuna.nombre_comuna
            if old_comuna != nombre_comuna:
                old_comuna = nombre_comuna
                file.write(f'{nombre_comuna}:\n')
            file.write(f'Inmueble en {inmueble.comuna}: {inmueble}\n')
    return inmuebles

#from web.services import test
#test()
#from web.services import get_fixtures
#get_fixtures()
#from web.services import get_inmuebles
#get_inmuebles('nombre 3', 'Descripcion 3')