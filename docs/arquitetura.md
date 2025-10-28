# Arquitetura do Projeto

## Visão Geral

O **AI Soccer** é uma aplicação web Django full-stack organizada de forma modular, com separação clara de responsabilidades através de apps Django independentes.

## Arquitetura Modular

### Princípio de Organização

O projeto segue o padrão de **apps Django por domínio de negócio**, onde cada app representa uma área funcional específica do sistema.

```
ai_soccer_project/
├── core/              # Núcleo: configurações e URLs principais
├── accounts/          # Domínio: Autenticação e gestão de usuários
├── performance/       # Domínio: Performance de atletas
├── scouting/          # Domínio: Prospecção de jogadores
└── business/          # Domínio: Gestão financeira e comercial
```

### Apps do Projeto

#### Core
- **Responsabilidade**: Configurações centrais, URLs raiz, settings
- **Conteúdo**: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
- **Não possui models**: É apenas configuração

#### Accounts
- **Responsabilidade**: Autenticação, autorização, gestão de usuários
- **Funcionalidades**: Login, logout, cadastro, perfil de usuário
- **Autenticação**: Baseada em email (não username)

#### Performance
- **Responsabilidade**: Monitoramento e análise de performance de atletas
- **Funcionalidades** (planejadas):
  - Cadastro de atletas
  - Registro de treinos e cargas
  - Métricas de performance
  - Prevenção de lesões (IA)

#### Scouting
- **Responsabilidade**: Prospecção e análise de jogadores
- **Funcionalidades** (planejadas):
  - Cadastro de jogadores prospectados
  - Relatórios de scouting
  - Comparação de perfis
  - Detecção de talentos (IA)

#### Business
- **Responsabilidade**: Gestão financeira e comercial de clubes
- **Funcionalidades** (planejadas):
  - Cadastro de clubes
  - Controle financeiro
  - Valuation de atletas (IA)
  - Análise de receitas

## Estrutura de Diretórios

### Estrutura de uma App Django

Cada app segue a estrutura padrão do Django:

```
app_name/
├── __init__.py
├── admin.py          # Configuração do Django Admin
├── apps.py           # Configuração da app
├── models.py         # Modelos de dados (ORM)
├── views.py          # Lógica de apresentação
├── tests.py          # Testes automatizados
├── migrations/       # Migrações do banco de dados
│   └── __init__.py
├── urls.py          # URLs específicas da app (quando necessário)
├── forms.py         # Formulários Django (quando necessário)
└── signals.py       # Django signals (quando necessário)
```

### Diretórios Globais

```
ai_soccer_project/
├── static/           # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/        # Templates Django globais
│   ├── base.html
│   └── components/
└── media/           # Uploads de usuários (futuro)
```

## Camadas da Aplicação

### 1. Apresentação (Templates)
- Django Template Language (DTL)
- TailwindCSS para estilização
- Alpine.js para interatividade leve (quando necessário)

### 2. Lógica de Negócio (Views)
- Class-Based Views (CBV) sempre que possível
- Mixins do Django para reutilização
- LoginRequiredMixin para proteção de rotas

### 3. Acesso a Dados (Models)
- Django ORM
- SQLite para desenvolvimento
- PostgreSQL planejado para produção

### 4. Banco de Dados
- SQLite (inicial)
- Schema definido via migrations

## Padrões de Comunicação

### Entre Apps

**Princípio**: Apps devem ser o mais independentes possível.

**Relacionamentos Permitidos**:
- Todas as apps podem referenciar `accounts.User` (ForeignKey)
- `business` pode referenciar `performance.Athlete` para valuation
- Evitar dependências circulares

**Exemplo**:
```python
# performance/models.py
from django.conf import settings

class Athlete(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
```

### URLs

**Estrutura Hierárquica**:

```python
# core/urls.py (raiz)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),           # /, /login/, /signup/
    path('performance/', include('performance.urls')),
    path('scouting/', include('scouting.urls')),
    path('business/', include('business.urls')),
]
```

## Fluxo de Requisição

```
1. Requisição HTTP
   ↓
2. core/urls.py (routing)
   ↓
3. app/urls.py (routing específico)
   ↓
4. app/views.py (lógica de negócio)
   ↓
5. app/models.py (acesso a dados)
   ↓
6. Database (SQLite)
   ↓
7. app/views.py (processamento)
   ↓
8. templates/ (renderização)
   ↓
9. Resposta HTTP
```

## Autenticação e Autorização

### Fluxo de Autenticação

```
1. Usuário acessa /login/
2. Submete email + senha
3. Backend autentica via email (não username)
4. Django cria sessão
5. Redireciona para /dashboard/
6. LoginRequiredMixin protege rotas internas
```

### Proteção de Views

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    login_url = '/login/'
```

## Banco de Dados

### Estratégia de Migrations

- Migrations são versionadas no Git
- Sempre rodar `makemigrations` após alterações em models
- Nunca editar migrations existentes em produção
- Usar `squashmigrations` quando necessário

### Auditoria

Todos os models principais devem ter:
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

## Princípios de Design

### SOLID (adaptado para Django)

**Single Responsibility**: Cada app tem uma responsabilidade clara
**Open/Closed**: Extensível via signals e hooks do Django
**Liskov Substitution**: CBVs seguem contratos do Django
**Interface Segregation**: Forms e models específicos
**Dependency Inversion**: Uso de `settings.AUTH_USER_MODEL`

### DRY (Don't Repeat Yourself)

- Templates base reutilizáveis
- Componentes compartilhados
- Mixins para lógica comum
- Template tags customizados quando necessário

## Escalabilidade Futura

### Preparação para Crescimento

1. **Database**: Estrutura permite migração para PostgreSQL
2. **Cache**: Redis pode ser adicionado facilmente
3. **Storage**: S3 para arquivos estáticos em produção
4. **Queue**: Celery para tarefas assíncronas (IA)
5. **API**: Django REST Framework pode ser adicionado

### Containerização (Futura)

```
ai_soccer_project/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

## Segurança

### Práticas Implementadas

- CSRF protection (nativo do Django)
- Password hashing (nativo do Django)
- SQL injection protection (ORM)
- XSS protection (auto-escaping de templates)

### Configurações de Segurança

```python
# settings.py
DEBUG = False  # em produção
ALLOWED_HOSTS = ['seu-dominio.com']
SECRET_KEY = env('SECRET_KEY')  # via variável de ambiente
```

## Monitoramento e Logs

### Estrutura de Logs (Futura)

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## Considerações de Performance

### Otimizações Planejadas

- **Paginação**: Todas as listagens devem ser paginadas
- **Select Related**: Usar `select_related()` e `prefetch_related()`
- **Indexes**: Criar índices em campos frequentemente filtrados
- **Cache de Templates**: Ativar em produção
- **Static Files**: Usar CDN em produção

---

**Referências**:
- [Django Documentation](https://docs.djangoproject.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
