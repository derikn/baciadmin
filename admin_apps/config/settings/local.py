# settings/local
from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2",
		"NAME": "adminapps",
		"USER": "admin",
		"PASSWORD": "admin",
		"HOST": "localhost",
		"PORT": "5432",

	}
}

INSTALLED_APPS += ("debug_toolbar",)