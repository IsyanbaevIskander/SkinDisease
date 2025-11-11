from project.env import env
from project.settings.base import BASE_DIR, DEBUG

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env.str('POSTGRES_DB', 'postgres'),
            'USER': env.str('POSTGRES_USER', 'postgres'),
            'PASSWORD': env.str('POSTGRES_PASSWORD', ''),
            'HOST': env.str('POSTGRES_HOST', 'localhost'),
            'PORT': env.int('POSTGRES_PORT', 5432),
        }
    }
