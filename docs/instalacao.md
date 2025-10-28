# Guia de Instalação

## Pré-requisitos

### Software Necessário

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Node.js** (LTS): [Download Node.js](https://nodejs.org/) - Necessário para TailwindCSS

### Verificar Instalações

```bash
# Python
python --version
# ou
python3 --version

# pip
pip --version

# Git
git --version

# Node.js
node --version

# npm
npm --version
```

## Instalação Passo a Passo

### 1. Clonar o Repositório (se aplicável)

```bash
git clone <url-do-repositorio>
cd ai_soccer_project
```

Ou navegue até o diretório do projeto:
```bash
cd /caminho/para/ai_soccer_project
```

### 2. Criar Ambiente Virtual Python

```bash
# Linux/Mac
python3 -m venv venv

# Windows
python -m venv venv
```

### 3. Ativar Ambiente Virtual

```bash
# Linux/Mac
source venv/bin/activate

# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

**Importante**: Sempre ative o ambiente virtual antes de trabalhar no projeto!

### 4. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` estiver vazio ou não existir, instale o Django manualmente:

```bash
pip install Django>=5.0
```

### 5. Instalar Dependências Node.js (TailwindCSS)

```bash
# Inicializar npm (se package.json não existir)
npm init -y

# Instalar TailwindCSS
npm install -D tailwindcss
```

### 6. Configurar TailwindCSS

Criar arquivo de configuração:
```bash
npx tailwindcss init
```

Editar `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Criar `static/css/input.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Adicionar script de build no `package.json`:
```json
{
  "scripts": {
    "build:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css",
    "watch:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
  }
}
```

Build inicial do CSS:
```bash
npm run build:css
```

### 7. Configurar Django

#### 7.1. Registrar Apps no settings.py

Editar `core/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps do projeto
    'accounts',
    'performance',
    'scouting',
    'business',
]
```

#### 7.2. Configurar Idioma e Timezone

```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
```

#### 7.3. Configurar Templates

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Adicionar esta linha
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
```

#### 7.4. Configurar Arquivos Estáticos

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### 8. Criar Diretórios Necessários

```bash
# Linux/Mac
mkdir -p templates static/css static/js static/images

# Windows (CMD)
mkdir templates
mkdir static\css
mkdir static\js
mkdir static\images
```

### 9. Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 10. Criar Superusuário (Admin)

```bash
python manage.py createsuperuser
```

Preencha:
- **Email**: seu@email.com
- **Password**: (senha segura)
- **Password (again)**: (confirme a senha)

### 11. Iniciar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

Admin: http://localhost:8000/admin

## Desenvolvimento com TailwindCSS

### Watch Mode (Recomendado)

Em um terminal separado (com venv ativado):
```bash
npm run watch:css
```

Isso irá regenerar o CSS automaticamente quando você editar os templates.

## Verificar Instalação

### Checklist

- [ ] Python 3.12+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências Python instaladas
- [ ] TailwindCSS instalado
- [ ] Diretórios criados (templates, static)
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Servidor rodando sem erros

### Testar Funcionalidades

```bash
# Ver versão do Django
python -m django --version

# Listar apps instaladas
python manage.py showmigrations

# Verificar configuração
python manage.py check
```

## Troubleshooting

### Erro: "No module named 'django'"

**Solução**: Ativar ambiente virtual e instalar Django
```bash
source venv/bin/activate  # ou venv\Scripts\activate (Windows)
pip install Django
```

### Erro: "npm: command not found"

**Solução**: Instalar Node.js

### Erro: "Port 8000 is already in use"

**Solução**: Usar porta diferente ou matar processo
```bash
# Usar outra porta
python manage.py runserver 8001

# Linux/Mac - matar processo
lsof -ti:8000 | xargs kill

# Windows - matar processo
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erro: "OperationalError: no such table"

**Solução**: Executar migrações
```bash
python manage.py migrate
```

### CSS não está carregando

**Solução**: Build do TailwindCSS
```bash
npm run build:css
```

## Próximos Passos

Após instalação bem-sucedida:

1. ✅ Leia [Guia de Código](coding-guidelines.md)
2. ✅ Explore [Design System](design-system.md)
3. ✅ Entenda [Arquitetura](arquitetura.md)
4. ✅ Consulte [PRD](../PRD.md) para funcionalidades

---

**Última Atualização**: 2025-10-28
