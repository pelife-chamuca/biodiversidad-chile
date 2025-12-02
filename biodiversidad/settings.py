import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "biodiversidad-chile-ps.onrender.com","biodiversidad-chile-ps.onrender.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "App",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "App.middleware.usuario_middleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "biodiversidad.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "biodiversidad.wsgi.application"

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_NAME"),
            "USER": os.getenv("MYSQL_USER"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD"),
            "HOST": os.getenv("MYSQL_HOST"),
            "PORT": os.getenv("MYSQL_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "chaparrita",
            "USER": "root",
            "PASSWORD": "admin",
            "HOST": "localhost",
            "PORT": "3306",
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ====== Configuración de seguridad ======
CSRF_COOKIE_SECURE = False  # Cambiar a True en despliegue HTTPS
SESSION_COOKIE_SECURE = False  # Cambiar a True en HTTPS
SESSION_COOKIE_AGE = 900  # 15 minutos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Redirección de login personalizada
LOGIN_URL = "/logearse/"
LOGIN_REDIRECT_URL = "/amenazas/"
LOGOUT_REDIRECT_URL = "/home/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
