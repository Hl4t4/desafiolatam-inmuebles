python manage.py migrate
python manage.py loaddata web/fixtures/regiones.json
python manage.py loaddata web/fixtures/comunas.json
python manage.py loaddata web/fixtures/tipos_usuarios.json
python manage.py loaddata web/fixtures/tipos_inmuebles.json
python manage.py loaddata web/fixtures/usuarios.json
python manage.py loaddata web/fixtures/inmuebles.json 
python manage.py loaddata web/fixtures/solicitudes_arriendo.json

python manage.py collectstatic --noinput

gunicorn inmuebles.wsgi --bind=0.0.0.0:80 