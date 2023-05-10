#El nombre de la base de datos es lista_deseos_dojo

Se debe crear las tablas y db desde la carpeta db, alli se encuentran los script de las tablas y el diagrama de modelo

con el Archivo .env puede modificarse el user y password de la db mysql


#Esta version de Lista de Deseos Dojo hace uso de:

#Front End

HTML, CSS, JAVASRIPT Y BOOTSTRAP

#Back End

PYTHON, FLASK y MYSQL 

Hace uso del Modelo Vista Controlador (MVC)

#Archivos de Modelo:
base.py
usuarios.py

#Archivos de Vista (Templates, Static)

Templates:

base.html
main.html
form.html
detail.html
login.html
_menu.html

Static

miestilo.css
miscript.js
archios de bootstrap...
utilidad toaster.css y js para modificar a apariencia de los mensajes flash llamada toastr


#Archivo Controlador
Controller.py

Hace uso de archivo .env, pero no se incluye debido a la seguridad de Github
por lo que se debe crear un archivo .env para que funcione la app dentro de la carpeta y
el contenido del archivo .env es el que sigue a continuacion:

APP_SECRET_KEY="user_login"
BASEDATOS_HOST="localhost"
BASEDATOS_USER="root"
BASEDATOS_PASSWORD="root"
BASEDATOS_NOMBRE="lista_deseos_dojo"
NOMBRE_SISTEMA="Sistema de Lista de Deseos Dojo"


por ello se utiliza el archivo de git ignore