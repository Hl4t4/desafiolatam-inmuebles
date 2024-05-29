import json
from unidecode import unidecode

def makeFixturesAndChoices (nombre_app:str) -> None:
    regiones = []
    choices_regiones = []
    choices_comunas = []

    with open('comunas-regiones.json', 'r', encoding = 'utf-8') as file:
        regiones = json.load(file)

    regiones = regiones['regiones']

    lista_regiones = []
    id_region = 1
    lista_comunas = []
    id_comuna = 1
    for region in regiones:
        new_region = {
            "model": f'{nombre_app}.Region',
            "pk": id_region,
            "fields": {
                "id": id_region,
                "nombre_region": region['region']
            }
        }
        id_region += 1
        choices_regiones.append(region['region'])
        lista_regiones.append(new_region)
        comunas = region['comunas']
        for comuna in comunas:
            new_comuna = {
                "model": f'{nombre_app}.Comuna',
                "pk": id_comuna,
                "fields": {
                    "id": id_comuna,
                    "nombre_comuna": comuna
                }
            }
            id_comuna += 1
            choices_comunas.append(comuna)
            lista_comunas.append(new_comuna)

    with open('RegionChoices.py', 'w', encoding = 'utf-8') as file:
        file.write(f'class RegionChoices (models.TextChoices):\n')
        for region in choices_regiones:
            file.write(f'    {unidecode(region).upper().strip().replace(" ", "_").replace(".", "").replace("\’", "").replace("'", "")} = "{region}", "{region}"\n')

    with open('ComunaChoices.py', 'w', encoding = 'utf-8') as file:
        file.write(f'class ComunaChoices (models.TextChoices):\n')
        for comuna in choices_comunas:
            file.write(f'    {unidecode(comuna).upper().strip().replace(".", "").replace("'", "").replace("\’", "").split('(')[0].replace(" ", "_")} = "{comuna}", "{comuna}"\n')

    with open ('comunas.json', 'w', encoding = 'utf-8') as file:
        json.dump(lista_comunas, file, indent=4, ensure_ascii=False)


    with open ('regiones.json', 'w', encoding = 'utf-8') as file:
        json.dump(lista_regiones, file, indent=4, ensure_ascii=False)


#### Funciona para cuando quieres tener comunas por region
def makeFixturesAndChoicesExpandedCommunes (nombre_app:str) -> None: 
    regiones = []
    choices_regiones = []
    choices_comunas = []

    with open('comunas-regiones.json', 'r', encoding = 'utf-8') as file:
        regiones = json.load(file)

    regiones = regiones['regiones']

    lista_regiones = []
    id_region = 1
    lista_comunas = []
    id_comuna = 1
    for region in regiones:
        new_region = {
            "model": f'{nombre_app}.Region',
            "pk": id_region,
            "fields": {
                "id": id_region,
                "nombre_region": region['region']
            }
        }
        choices_regiones.append(region['region'])
        lista_regiones.append(new_region)
        comunas = region['comunas']
        for comuna in comunas:
            new_comuna = {
                "model": f'{nombre_app}.Comuna',
                "pk": id_comuna,
                "fields": {
                    "id": id_comuna,
                    "nombre_comuna": comuna,
                    "region": id_region
                }
            }
            id_comuna += 1
            choices_comunas.append(comuna)
            lista_comunas.append(new_comuna)
        id_region += 1
        
    with open('RegionChoices.py', 'w', encoding = 'utf-8') as file:
        file.write(f'class RegionChoices (models.TextChoices):\n')
        for region in choices_regiones:
            file.write(f'    {unidecode(region).upper().strip().replace(" ", "_").replace(".", "").replace("\’", "").replace("'", "")} = "{region}", "{region}"\n')

    with open('ComunaChoices.py', 'w', encoding = 'utf-8') as file:
        file.write(f'class ComunaChoices (models.TextChoices):\n')
        for comuna in choices_comunas:
            file.write(f'    {unidecode(comuna).upper().strip().replace(".", "").replace("'", "").replace("\’", "").split('(')[0].replace(" ", "_")} = "{comuna}", "{comuna}"\n')

    with open ('comunas.json', 'w', encoding = 'utf-8') as file:
        json.dump(lista_comunas, file, indent=4, ensure_ascii=False)


    with open ('regiones.json', 'w', encoding = 'utf-8') as file:
        json.dump(lista_regiones, file, indent=4, ensure_ascii=False)


# makeFixturesAndChoices('web')
makeFixturesAndChoicesExpandedCommunes('web')