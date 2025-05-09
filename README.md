proyecto básico en **Django** para desarrollar aplicación web. Dejo esta breve explicacion de como se realizo:

1. **Instale Python** : Me asegure de tener Python 3.x y pip instalados.
2. **Cree un Entorno Virtual** : Usando (.venv) esto me ayuda a mantener las dependencias aisladas y evitar problemas con otras versiones de bibliotecas.
3. **Instale Django** : Con el entorno virtual activado, instala Django con pip asi: (pip install django)
4. **Cree el Proyecto** : Ejecutando el comando para crear el proyecto (django-admin startproject mi_proyecto) Django generará todos los archivos y carpetas necesarios.
5. **Arranque el Servidor** : Inicie el servidor  (python manage.py runserver) y abri el navegador para ver que todo funciona bien.
6. **Crea una App** : Las apps en Django te permiten organizar funcionalidades. Cree una app y la añádi a la configuración del proyecto.
7. **Añade las Plantillas** : Creando archivos HTML en la carpeta de plantillas para personalizar la apariencia de el sitio.
8. **Estilos y Scripts** : Añadi archivos CSS y JavaScript en la carpeta de statics para dar estilo y agregar interactividad.

Estos son los paso que seguimos para realizar la pagino con django.

Despliegue en Railway.

**9. Cree una cuenta en Railway:**

* Inicie sesión en Railway y en  **"New Project"** .
* Seleccione la opción de **"Deploy from GitHub"** para conectar tu repositorio de GitHub al proyecto de Railway
* Railway detectará automáticamente el tipo de proyecto (Django) y procederá a instalar las dependencias definidas en el `requirements.txt` de tu proyecto.

10. Configurar variables de entorno:

En Railway en la pestaña **"Variables"** del proyecto y añade las siguientes variables de entorno:

* `DEBUG=False`
* `SECRET_KEY=<tu-secreto-django>`
* `DATABASE_URL=<url-de-conexion-a-postgresql>` (Ver más abajo).
* `ALLOWED_HOSTS=tu-dominio-railway.com`

**Configuración de PostgreSQL en Django**


**Instalae psycopg2:**

* para que Django pueda conectar con PostgreSQL (pip install psycopg2)

**Configuración de la base de datos en `settings.py`:**

* En el archivo `settings.py` de Django, modificamos la configuración de la base de datos para usar PostgreSQL. Usé las variables de entorno para la configuración.
* En Railway, la URL de conexión a PostgreSQL se genera automáticamente y la puedes encontrar en la sección de **"Variables"** como `DATABASE_URL`. Puedes configurar tu aplicación para que use esta URL.

**Migrar la base de datos a PostgreSQL:**

* En Railway, después de que la aplicación esté corriendo, debes correr las migraciones para crear las tablas de tu base de datos. Puedes hacerlo desde el terminal de Railway: (python manage.py migrate)

Att: Edgar Oviedo.
