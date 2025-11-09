1. Clonar el repositorio:
   
git clone https://github.com/C-1412/Tesis.git

Crear y activar entorno virtual:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Instalar requerimientos:
pip install -r requirements.txt

Ejecutar migraciones:
python manage.py migrate

Crear superusuario:
python manage.py createsuperuser


Levantar el servidor:
python manage.py runserver
