# Estrutura de Apps Django

## Visão Geral

Cada app Django no AI Soccer representa um domínio de negócio específico e segue uma estrutura padronizada.

## Apps do Projeto

### core/
**Responsabilidade**: Configurações centrais do Django

**Arquivos**:
- `settings.py` - Configurações do projeto
- `urls.py` - URLs raiz
- `wsgi.py` / `asgi.py` - Servidores de aplicação

**Não contém**: Models, views, templates

### accounts/
**Responsabilidade**: Autenticação e gestão de usuários

**Status**: ⚠️ Estrutura criada, implementação pendente

**Funcionalidades Planejadas**:
- Modelo customizado de User (email como username)
- Login, logout, cadastro
- Recuperação de senha
- Perfil de usuário

**Arquivos**:
```
accounts/
├── models.py      # CustomUser model
├── views.py       # Login, logout, signup views
├── forms.py       # CustomUserCreationForm, AuthenticationForm
├── backends.py    # EmailBackend para autenticação
└── urls.py        # /login/, /signup/, /logout/, /profile/
```

### performance/
**Responsabilidade**: Análise de performance de atletas

**Status**: ⚠️ Estrutura criada, implementação pendente

**Funcionalidades Planejadas**:
- Cadastro de atletas
- Registro de treinos e cargas
- Métricas de performance
- Registro de lesões
- Dashboards individuais e coletivos
- IA: Prevenção de lesões

**Models Planejados**:
- `Athlete` - Dados do atleta
- `TrainingLoad` - Cargas de treino
- `PerformanceMetric` - Métricas de desempenho
- `InjuryRecord` - Histórico de lesões

### scouting/
**Responsabilidade**: Prospecção e análise de jogadores

**Status**: ⚠️ Estrutura criada, implementação pendente

**Funcionalidades Planejadas**:
- Cadastro de jogadores prospectados
- Relatórios de scouting
- Comparação de perfis
- Busca avançada
- IA: Detecção de talentos

**Models Planejados**:
- `ScoutedPlayer` - Jogador prospectado
- `ScoutingReport` - Relatório de avaliação

### business/
**Responsabilidade**: Gestão financeira e comercial

**Status**: ⚠️ Estrutura criada, implementação pendente

**Funcionalidades Planejadas**:
- Cadastro de clubes
- Controle financeiro
- Gestão de receitas
- Valuation de atletas
- IA: Previsão de receitas

**Models Planejados**:
- `Club` - Dados do clube
- `FinancialRecord` - Transações financeiras
- `Revenue` - Receitas por categoria
- `AthleteValuation` - Valuation de atletas

## Estrutura Padrão de uma App

```
app_name/
├── __init__.py
├── admin.py          # Registro no Django Admin
├── apps.py           # Configuração da app
├── models.py         # Models (ORM)
├── views.py          # Views (CBV preferencial)
├── forms.py          # Formulários (quando necessário)
├── urls.py           # URLs da app (quando necessário)
├── signals.py        # Django signals (quando necessário)
├── utils.py          # Funções auxiliares (quando necessário)
├── tests.py          # Testes (futuro)
├── migrations/       # Migrações do banco
│   └── __init__.py
└── templates/        # Templates específicos (quando necessário)
    └── app_name/
        └── template.html
```

## Quando Criar um Novo Arquivo

### forms.py
Criar quando:
- Necessitar customização de formulários
- Adicionar validações específicas
- Customizar widgets

```python
# performance/forms.py
from django import forms
from .models import Athlete

class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = ['name', 'birth_date', 'position']
```

### urls.py
Criar quando:
- App tiver views próprias
- Necessitar URLs específicas

```python
# performance/urls.py
from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    path('athletes/', views.AthleteListView.as_view(), name='athlete-list'),
    path('athletes/<int:pk>/', views.AthleteDetailView.as_view(), name='athlete-detail'),
]
```

### signals.py
Criar quando:
- Necessitar lógica automática após salvar/deletar
- Integração entre models

```python
# performance/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Athlete

@receiver(post_save, sender=Athlete)
def athlete_post_save(sender, instance, created, **kwargs):
    if created:
        # Lógica após criar atleta
        pass
```

### utils.py
Criar quando:
- Funções auxiliares reutilizáveis
- Lógica de negócio complexa
- Cálculos e processamentos

```python
# performance/utils.py
from datetime import date

def calculate_age(birth_date):
    """Calculate age from birth date."""
    today = date.today()
    return today.year - birth_date.year
```

## Dependências Entre Apps

### Permitido

```python
# Qualquer app pode importar User
from django.conf import settings

class Athlete(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
```

### Com Cuidado

```python
# business pode referenciar performance (para valuation)
from performance.models import Athlete

class AthleteValuation(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2)
```

### Evitar

```python
# ❌ Dependências circulares
# performance importando business E business importando performance
```

## Registrando Apps

### settings.py
```python
INSTALLED_APPS = [
    # Apps Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do projeto
    'accounts.apps.AccountsConfig',
    'performance.apps.PerformanceConfig',
    'scouting.apps.ScoutingConfig',
    'business.apps.BusinessConfig',
]
```

## URLs Principais

### core/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),           # /, /login/, /signup/
    path('performance/', include('performance.urls')),
    path('scouting/', include('scouting.urls')),
    path('business/', include('business.urls')),
]
```

## Admin

Cada app deve registrar seus models no admin:

```python
# performance/admin.py
from django.contrib import admin
from .models import Athlete

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'birth_date', 'created_at']
    list_filter = ['position', 'created_at']
    search_fields = ['name']
    date_hierarchy = 'created_at'
```

## Templates

### Organização

```
templates/
├── base.html                    # Template base global
├── components/                  # Componentes reutilizáveis
│   ├── sidebar.html
│   └── navbar.html
├── accounts/                    # Templates de accounts
│   ├── login.html
│   └── signup.html
├── performance/                 # Templates de performance
│   ├── athlete_list.html
│   └── athlete_detail.html
├── scouting/                    # Templates de scouting
└── business/                    # Templates de business
```

## Boas Práticas

### 1. Isolamento
- Apps devem ser o mais independentes possível
- Evitar dependências circulares
- Comunicação via signals quando necessário

### 2. Nomenclatura
- Nomes de apps no plural (accounts, não account)
- Models no singular (Athlete, não Athletes)
- Views descritivas (AthleteListView, não ListView)

### 3. Organização
- Um model por conceito de negócio
- Views relacionadas juntas
- Forms no mesmo arquivo quando possível

### 4. Documentação
- Docstrings em models e views complexas
- Comentários explicando o "porquê", não o "o quê"

---

**Última Atualização**: 2025-10-28
