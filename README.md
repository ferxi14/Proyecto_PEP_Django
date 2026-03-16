# GameVault — Catálogo Personal de Videojuegos

Aplicación web desarrollada con **Django 6.0.3** que permite a los usuarios registrados gestionar su catálogo personal de videojuegos. Incluye autenticación completa, CRUD, y control de permisos por propietario.

---

## Estructura del Proyecto

```
gamevault/
├── manage.py
├── requirements.txt
├── pythonanywhere_wsgi.py       # Config despliegue
├── gamevault/                  # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalog/                     # Aplicación principal
│   ├── models.py                # Modelo Game
│   ├── views.py                 # Vistas basadas en clases
│   ├── forms.py                 # Formularios
│   ├── urls.py                  # URLs con name=
│   ├── admin.py
│   └── templates/catalog/       # Plantillas de la app
│       ├── game_list.html
│       ├── game_detail.html
│       ├── game_form.html
│       ├── game_confirm_delete.html
│       └── my_games.html
├── templates/                   # Plantillas globales
│   ├── base.html                # Plantilla base con herencia
│   └── registration/
│       ├── login.html
│       └── signup.html
└── static/                      # Archivos estáticos
    ├── css/style.css            # CSS propio
    └── js/main.js
```

---

## Instalación Local

### 1. Clonar / descargar el proyecto

```bash
cd ~/proyectos
# Si usas git:
git clone <url-repo> gamevault
cd gamevault
```

### 2. Crear y activar el entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar (Linux/macOS)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario (administrador)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver 8020
```

Abre **http://127.0.0.1:8020** en tu navegador.

---

##  Dependencias (`requirements.txt`)

| Paquete | Versión | Uso |
|---|---|---|
| Django | 6.0.3 | Framework web principal |
| Pillow | 12.1.1 | Procesamiento de imágenes (pósters) |
| whitenoise | 6.6.0 | Servir estáticos en producción |
| gunicorn | 21.2.0 | Servidor WSGI para producción |

---

## Modelo de Datos

### `Game` (catalog/models.py)

| Campo | Tipo | Descripción |
|---|---|---|
| `title` | CharField(200) | **Texto corto** — Título de la videojuego |
| `director` | CharField(150) | **Texto corto** — Director/a |
| `synopsis` | TextField | **Texto largo** — Sinopsis o reseña personal |
| `year` | PositiveIntegerField | Año de estreno |
| `genre` | CharField (choices) | Género videojuegosmatográfico |
| `rating` | IntegerField (choices) | Puntuación del usuario (1-5 estrellas) |
| `poster` | ImageField | Imagen del póster (opcional) |
| `is_favorite` | BooleanField | Marcada como favorita |
| `created_at` | DateTimeField(`auto_now_add=True`) | **Fecha automática de creación** |
| `updated_at` | DateTimeField(`auto_now=True`) | Última modificación |
| `author` | **ForeignKey(User)** | **Propietario** del registro |

---

##  URLs con nombres (URL dispatcher)

| URL | Nombre (`name=`) | Vista |
|---|---|---|
| `/` | `catalog:game_list` | Catálogo completo |
| `/mis-peliculas/` | `catalog:my_games` | Mis videojuegos |
| `/pelicula/<pk>/` | `catalog:game_detail` | Detalle |
| `/pelicula/nueva/` | `catalog:game_create` | Crear |
| `/pelicula/<pk>/editar/` | `catalog:game_update` | Editar |
| `/pelicula/<pk>/eliminar/` | `catalog:game_delete` | Eliminar |
| `/login/` | `login` | Iniciar sesión |
| `/logout/` | `logout` | Cerrar sesión |
| `/signup/` | `signup` | Registro |

---

## Sistema de Usuarios y Seguridad

- **Registro**: formulario con `CustomUserCreationForm` que incluye email.
- **Login/Logout**: vistas de Django (`LoginView`, `LogoutView`).
- **Protección de vistas**: `LoginRequiredMixin` en Crear, Editar y Borrar.
- **Control de propiedad**: en `dispatch()` se verifica que `request.user == game.author`.
- **Excepción staff/superusuario**: `is_staff` o `is_superuser` pueden gestionar cualquier videojuego.
- **Mensajes de error**: usando `django.contrib.messages` con `messages.error()`.

---

## Vistas Basadas en Clases (CBV)

| Clase | Herencia | Descripción |
|---|---|---|
| `GameListView` | `ListView` | Catálogo con filtros y búsqueda |
| `MyGamesView` | `LoginRequiredMixin, ListView` | Videojuegos propias |
| `GameDetailView` | `DetailView` | Detalle expandido |
| `GameCreateView` | `LoginRequiredMixin, CreateView` | Crear videojuego |
| `GameUpdateView` | `LoginRequiredMixin, UpdateView` | Editar (con control de autor) |
| `GameDeleteView` | `LoginRequiredMixin, DeleteView` | Eliminar (con control de autor) |
| `SignUpView` | `FormView` | Registro de usuario |

---

## Despliegue en PythonAnywhere

### 1. Crear cuenta gratuita
Regístrate en [pythonanywhere.com](https://www.pythonanywhere.com/)

### 2. Abrir una consola Bash (desde el Dashboard)

```bash
# Crear entorno virtual
mkvirtualenv --python=/usr/bin/python3.10 gamevault-env

# Instalar dependencias
pip install django pillow whitenoise gunicorn
```

### 3. Subir el código

**Opción A — Git (recomendado):**
```bash
git clone <url-de-tu-repo> ~/gamevault
```

**Opción B — Subir ZIP por Files:**
Sube el ZIP del proyecto y descomprímelo:
```bash
cd ~
unzip gamevault.zip
```

### 4. Configurar la web app

En el Dashboard → **Web** → **Add a new web app**:
- Framework: **Manual configuration**
- Python: **3.10**

### 5. Configurar el archivo WSGI

En **Web** → **WSGI configuration file**, reemplaza todo el contenido con:

```python
import sys, os
path = '/home/ferxi14/gamevault'
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'gamevault.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6. Configurar archivos estáticos

En **Web** → **Static files**:

| URL | Directory |
|---|---|
| `/static/` | `/home/ferxi14/gamevault/staticfiles` |
| `/media/` | `/home/ferxi14/gamevault/media` |

Ejecuta en la consola Bash:
```bash
cd ~/gamevault
python manage.py collectstatic --noinput
```

### 7. Configurar el entorno virtual

En **Web** → **Virtualenv**: introduce la ruta:
```
/home/ferxi14/.virtualenvs/gamevault-env
```

### 8. Ajustar settings.py para producción

En la consola Bash, edita `settings.py`:
```bash
nano ~/gamevault/gamevault/settings.py
```

Cambia:
```python
DEBUG = False
ALLOWED_HOSTS = ['ferxi14.pythonanywhere.com']
SECRET_KEY = 'pon-aqui-una-clave-secreta-larga-y-aleatoria'
```

### 9. Aplicar migraciones y crear admin

```bash
cd ~/gamevault
python manage.py migrate
python manage.py createsuperuser
```

### 10. Recargar la web app

En el Dashboard → **Web** → botón **Reload**. Ya está en línea