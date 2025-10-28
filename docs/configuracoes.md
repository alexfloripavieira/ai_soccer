# Configurações do Projeto

## Arquivo settings.py

Localização: `core/settings.py`

## Configurações Atuais

### Configurações Básicas

```python
# Debug (NUNCA deixar True em produção)
DEBUG = True

# Hosts permitidos (configurar em produção)
ALLOWED_HOSTS = []

# Secret Key (TROCAR em produção!)
SECRET_KEY = 'django-insecure-...'
```

### Apps Instaladas

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Adicionar apps do projeto:
    # 'accounts',
    # 'performance',
    # 'scouting',
    # 'business',
]
```

### Banco de Dados

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Internacionalização

```python
LANGUAGE_CODE = 'en-us'  # Alterar para 'pt-br'
TIME_ZONE = 'UTC'         # Alterar para 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
```

### Arquivos Estáticos

```python
STATIC_URL = 'static/'
# Adicionar:
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para produção
```

## Configurações Recomendadas

### Para Desenvolvimento

```python
# core/settings.py

# Adicionar suporte ao modelo customizado de usuário
AUTH_USER_MODEL = 'accounts.CustomUser'

# URLs de autenticação
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Configurar templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Adicionar
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Arquivos de mídia (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Idioma e timezone
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
```

## Variáveis de Ambiente

### Usando django-environ (Recomendado)

#### 1. Instalar
```bash
pip install django-environ
```

#### 2. Criar .env
```bash
# .env (na raiz do projeto)
DEBUG=True
SECRET_KEY=sua-secret-key-super-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 3. Configurar settings.py
```python
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

# Ler .env
environ.Env.read_env(BASE_DIR / '.env')

# Usar variáveis
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
```

#### 4. Adicionar ao .gitignore
```bash
echo ".env" >> .gitignore
```

#### 5. Criar .env.example
```bash
# .env.example
DEBUG=True
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Configurações por Ambiente

### Estrutura Recomendada (Futuro)

```
core/
├── settings/
│   ├── __init__.py
│   ├── base.py        # Configurações comuns
│   ├── development.py # Desenvolvimento
│   ├── production.py  # Produção
│   └── testing.py     # Testes
```

### base.py (Configurações Comuns)
```python
# core/settings/base.py
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()

# Apps e middleware comuns
INSTALLED_APPS = [...]
MIDDLEWARE = [...]

# Templates, database, etc.
```

### development.py
```python
# core/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email console backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### production.py
```python
# core/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# PostgreSQL
DATABASES = {
    'default': env.db()
}

# Segurança
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Usar configuração específica
```bash
# Desenvolvimento (padrão)
python manage.py runserver

# Produção
python manage.py runserver --settings=core.settings.production
```

## Configurações de Segurança

### Produção

```python
# SECRET_KEY via variável de ambiente
SECRET_KEY = env('SECRET_KEY')

# Debug desligado
DEBUG = False

# Hosts permitidos
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Clickjacking
X_FRAME_OPTIONS = 'DENY'

# Content type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS
SECURE_BROWSER_XSS_FILTER = True
```

## Configurações de Email

### Console (Desenvolvimento)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### SMTP (Produção)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
```

## Configurações de Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Configurações de Cache (Futuro)

### Redis
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## Comandos Úteis

```bash
# Ver todas as configurações
python manage.py diffsettings

# Verificar configuração
python manage.py check

# Verificar deploy
python manage.py check --deploy

# Shell com configurações
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
```

## Checklist de Produção

Antes de fazer deploy:

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` via variável de ambiente
- [ ] `ALLOWED_HOSTS` configurado
- [ ] HTTPS configurado
- [ ] Configurações de segurança ativas
- [ ] Banco de dados de produção (PostgreSQL)
- [ ] Email configurado
- [ ] Logging configurado
- [ ] Arquivos estáticos coletados (`collectstatic`)
- [ ] `.env` não está no Git

---

**Última Atualização**: 2025-10-28
