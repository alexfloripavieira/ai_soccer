# Stack Tecnológica

## Visão Geral

O AI Soccer utiliza uma stack moderna e robusta, focada em produtividade e simplicidade.

## Backend

### Python 3.12+
- **Versão**: 3.12 ou superior
- **Por quê**: Performance melhorada, type hints avançados, segurança
- **Instalação**: https://www.python.org/downloads/

### Django 5.x
- **Versão**: 5.0+
- **Framework Web**: Full-stack framework Python
- **Por quê**:
  - Batteries included (admin, auth, ORM, templates)
  - Segurança por padrão
  - Comunidade ativa
  - Documentação excelente

**Principais módulos Django utilizados**:
```python
django.contrib.admin       # Interface administrativa
django.contrib.auth        # Sistema de autenticação
django.contrib.sessions    # Gerenciamento de sessões
django.contrib.messages    # Sistema de mensagens
django.contrib.staticfiles # Arquivos estáticos
```

### Django ORM
- **Banco de Dados**: SQLite (desenvolvimento)
- **ORM**: Object-Relational Mapping nativo do Django
- **Migrations**: Sistema de versionamento do schema

**Exemplo de uso**:
```python
from django.db import models

class Athlete(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
```

## Frontend

### Django Template Language (DTL)
- **Templating Engine**: Nativo do Django
- **Sintaxe**: `{% %}` para lógica, `{{ }}` para variáveis
- **Segurança**: Auto-escaping de HTML

**Exemplo**:
```django
{% extends 'base.html' %}

{% block content %}
  <h1>{{ athlete.name }}</h1>
  <p>Idade: {{ athlete.age }}</p>
{% endblock %}
```

### TailwindCSS 3.x
- **Framework CSS**: Utility-first CSS framework
- **Versão**: 3.x
- **Por quê**:
  - Design system consistente
  - Desenvolvimento rápido
  - Customização fácil
  - Produção otimizada

**Setup**:
```bash
npm install -D tailwindcss
npx tailwindcss init
```

**Configuração** (`tailwind.config.js`):
```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#10b981',
        'secondary': '#3b82f6',
      },
    },
  },
  plugins: [],
}
```

### Alpine.js (Opcional)
- **JavaScript Framework**: Para interatividade leve
- **Uso**: Quando necessário (dropdowns, modals, tabs)
- **Por quê**: Integração fácil com Django templates

### Chart.js / ApexCharts (Planejado)
- **Visualização de Dados**: Gráficos interativos
- **Uso**: Dashboards de performance, scouting e business
- **Integração**: Via CDN ou npm

## Banco de Dados

### SQLite (Desenvolvimento)
- **Engine**: `django.db.backends.sqlite3`
- **Arquivo**: `db.sqlite3` na raiz do projeto
- **Por quê**:
  - Zero configuração
  - Perfeito para desenvolvimento
  - Fácil backup (copiar arquivo)

**Configuração** (`settings.py`):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL (Produção - Futuro)
- **Engine**: `django.db.backends.postgresql`
- **Por quê**:
  - Performance superior
  - Recursos avançados
  - Escalabilidade
  - Transações robustas

## Ferramentas de Desenvolvimento

### Python Virtual Environment
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

### pip (Gerenciador de Pacotes Python)
- **Arquivo**: `requirements.txt`
- **Instalação**: `pip install -r requirements.txt`

### Node.js e npm
- **Versão**: LTS (Long Term Support)
- **Uso**: Build do TailwindCSS
- **Instalação**: https://nodejs.org/

**Scripts npm** (`package.json`):
```json
{
  "scripts": {
    "build:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css",
    "watch:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
  }
}
```

### Git (Controle de Versão)
- **Repositório**: Local ou remoto (GitHub, GitLab)
- **Branches**: main, develop, feature branches
- **Commits**: Mensagens claras e descritivas

## Machine Learning (Planejado)

### scikit-learn
- **Uso**: Modelos preditivos básicos
- **Casos**:
  - Prevenção de lesões (Performance)
  - Potencial de jogadores (Scouting)
  - Previsão de receitas (Business)

### pandas
- **Uso**: Manipulação e análise de dados
- **Casos**: ETL, feature engineering, estatísticas

### numpy
- **Uso**: Operações numéricas
- **Casos**: Cálculos matemáticos, arrays

**Exemplo de requirements.txt**:
```
Django>=5.0
scikit-learn>=1.3
pandas>=2.0
numpy>=1.24
```

## Infraestrutura

### Desenvolvimento

#### Django Development Server
```bash
python manage.py runserver
```
- **Porta**: 8000
- **URL**: http://localhost:8000
- **Auto-reload**: Sim

### Produção (Futuro)

#### Gunicorn
- **WSGI Server**: Para servir aplicação Django

#### Nginx
- **Reverse Proxy**: Para servir arquivos estáticos e proxy reverso

#### Docker
- **Containerização**: Dockerfile + docker-compose.yml

**Exemplo de deploy**:
```
Nginx → Gunicorn → Django
  ↓
PostgreSQL
  ↓
Redis (cache)
```

## Segurança

### Bibliotecas de Segurança

#### django-environ (Recomendado)
```bash
pip install django-environ
```
- **Uso**: Gerenciamento de variáveis de ambiente
- **Por quê**: Secret keys e configurações sensíveis

**Exemplo**:
```python
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
```

## Testing (Futuro)

### pytest + pytest-django
- **Framework de Testes**: Alternativa ao unittest do Django
- **Por quê**: Sintaxe mais limpa, fixtures poderosos

### coverage
- **Cobertura de Testes**: Medir % de código testado
- **Meta**: > 80% de cobertura

## Monitoramento (Futuro)

### Sentry
- **Error Tracking**: Monitoramento de erros em produção
- **Alertas**: Notificações de bugs

### Logging
- **Python logging**: Biblioteca nativa
- **Django logging**: Configuração em settings.py

## IDEs Recomendadas

### VS Code
- **Extensões Recomendadas**:
  - Python
  - Django
  - Pylance
  - Tailwind CSS IntelliSense
  - GitLens

### PyCharm
- **Versão**: Professional (suporte completo a Django)
- **Features**: Debugging, Django console, template hints

## Versionamento de Dependências

### requirements.txt
```
Django==5.0.0
# Fixar versões em produção
```

### requirements-dev.txt (Futuro)
```
-r requirements.txt
pytest-django==4.5.0
coverage==7.3.0
black==23.9.0
flake8==6.1.0
```

## Comandos Úteis

### Django
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Shell interativo
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

### TailwindCSS
```bash
# Build CSS (produção)
npm run build:css

# Watch CSS (desenvolvimento)
npm run watch:css
```

### Git
```bash
# Status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "feat: adiciona modelo de atleta"

# Push
git push origin main
```

## Recursos de Aprendizado

### Django
- [Django Official Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)

### TailwindCSS
- [Tailwind Docs](https://tailwindcss.com/docs)
- [Tailwind UI](https://tailwindui.com/)

### Python
- [Real Python](https://realpython.com/)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)

---

**Última Atualização**: 2025-10-28
