# Guia de Código

## Princípios Fundamentais

### 1. Simplicidade Acima de Tudo
- Código simples e direto
- Evitar over-engineering
- Se pode ser feito de forma simples, faça de forma simples
- Não adicionar funcionalidades "por precaução"

### 2. PEP 8
Seguir rigorosamente o [PEP 8](https://peps.python.org/pep-0008/) - Guia de Estilo Python.

### 3. Idioma
- **Código**: Sempre em inglês (variáveis, funções, classes, comentários)
- **Interface**: Sempre em português brasileiro (textos exibidos ao usuário)

```python
# ✅ CORRETO
class Athlete(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'

# ❌ ERRADO
class Atleta(models.Model):
    nome = models.CharField(max_length=200)
```

## Convenções de Nomenclatura

### Variáveis e Funções
```python
# snake_case para variáveis e funções
athlete_name = 'João Silva'
birth_date = date(1995, 5, 10)

def calculate_age(birth_date):
    pass
```

### Classes
```python
# PascalCase para classes
class Athlete(models.Model):
    pass

class TrainingLoad(models.Model):
    pass
```

### Constantes
```python
# UPPER_CASE para constantes
MAX_UPLOAD_SIZE = 5242880  # 5MB
DEFAULT_PAGINATION = 20
```

## Aspas

### Regra Principal: Aspas Simples
```python
# ✅ SEMPRE usar aspas simples
name = 'João Silva'
position = 'Atacante'

# ✅ Aspas duplas APENAS quando necessário (strings com aspas simples)
message = "O jogador disse: 'Vou marcar um gol'"

# ❌ EVITAR aspas duplas sem necessidade
name = "João Silva"  # Errado
```

### Docstrings
```python
# ✅ Docstrings usam aspas triplas (simples ou duplas, preferir duplas)
def calculate_age(birth_date):
    """
    Calculate age based on birth date.

    Args:
        birth_date (date): Birth date of the person

    Returns:
        int: Age in years
    """
    pass
```

## Organização de Imports

### Ordem de Imports (PEP 8)
```python
# 1. Biblioteca padrão Python
import os
import sys
from datetime import date, datetime

# 2. Bibliotecas de terceiros
from django.db import models
from django.contrib.auth import get_user_model

# 3. Imports locais do projeto
from accounts.models import User
from performance.utils import calculate_age
```

### Formatação
```python
# ✅ Um import por linha
from django.db import models
from django.contrib.auth import get_user_model

# ❌ Múltiplos imports em uma linha
from django.db import models; from django.contrib.auth import get_user_model

# ✅ Exceção: múltiplos itens do mesmo módulo
from datetime import date, datetime, timedelta
```

## Models (Django)

### Estrutura Padrão
```python
from django.db import models
from django.conf import settings

class Athlete(models.Model):
    """Model representing an athlete."""

    # Constantes
    POSITION_CHOICES = [
        ('GK', 'Goleiro'),
        ('DF', 'Defensor'),
        ('MF', 'Meio-campo'),
        ('FW', 'Atacante'),
    ]

    # Campos relacionais primeiro
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Criado por'
    )

    # Campos principais
    name = models.CharField('Nome', max_length=200)
    birth_date = models.DateField('Data de nascimento')
    position = models.CharField('Posição', max_length=2, choices=POSITION_CHOICES)

    # Campos numéricos
    height = models.FloatField('Altura (cm)')
    weight = models.FloatField('Peso (kg)')

    # Campos de auditoria (sempre no final)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def age(self):
        """Calculate current age."""
        today = date.today()
        return today.year - self.birth_date.year
```

### Campos de Auditoria Obrigatórios
```python
# SEMPRE incluir em todos os models principais
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### ForeignKey
```python
# ✅ SEMPRE usar settings.AUTH_USER_MODEL para User
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# ❌ NUNCA importar User diretamente
from accounts.models import User
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

## Views (Django)

### Preferir Class-Based Views
```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# ✅ CORRETO: CBV
class AthleteListView(LoginRequiredMixin, ListView):
    model = Athlete
    template_name = 'performance/athlete_list.html'
    context_object_name = 'athletes'
    paginate_by = 20
    login_url = '/login/'

# ⚠️ Function-Based Views apenas quando CBV não faz sentido
def custom_dashboard(request):
    # Lógica muito específica que não se encaixa em CBVs
    pass
```

### Mixins
```python
# Ordem dos mixins importa!
# Mixins primeiro, depois a view base
class AthleteCreateView(LoginRequiredMixin, CreateView):
    pass

# ❌ ERRADO
class AthleteCreateView(CreateView, LoginRequiredMixin):
    pass
```

## Forms (Django)

### ModelForm Preferencial
```python
from django import forms
from performance.models import Athlete

class AthleteForm(forms.ModelForm):
    """Form for creating and updating athletes."""

    class Meta:
        model = Athlete
        fields = ['name', 'birth_date', 'position', 'height', 'weight']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg'
            }),
        }

    def clean_birth_date(self):
        """Validate that birth_date is not in the future."""
        birth_date = self.cleaned_data['birth_date']
        if birth_date > date.today():
            raise forms.ValidationError('Data de nascimento não pode ser no futuro.')
        return birth_date
```

## Templates (Django)

### Estrutura de Template
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Lista de Atletas{% endblock %}

{% block extra_css %}
<style>
    /* Estilos específicos da página */
</style>
{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-slate-100 mb-6">Atletas</h1>

    {% for athlete in athletes %}
        <div class="bg-slate-800 rounded-lg p-4">
            <h2>{{ athlete.name }}</h2>
            <p>{{ athlete.position }}</p>
        </div>
    {% empty %}
        <p class="text-slate-400">Nenhum atleta cadastrado.</p>
    {% endfor %}
</div>
{% endblock %}

{% block extra_js %}
<script>
    // JavaScript específico da página
</script>
{% endblock %}
```

### Boas Práticas de Templates
```django
{# ✅ Sempre usar empty em loops #}
{% for item in items %}
    {{ item }}
{% empty %}
    <p>Nenhum item encontrado.</p>
{% endfor %}

{# ✅ Comentários Django (não HTML) para lógica #}
{# TODO: Adicionar paginação aqui #}

{# ✅ Usar include para componentes reutilizáveis #}
{% include 'components/sidebar.html' %}

{# ✅ Espaçamento consistente #}
<div class="container">
    <h1>Título</h1>
    <p>Parágrafo</p>
</div>
```

## Comentários

### Quando Comentar
```python
# ✅ Comentar o PORQUÊ, não o QUÊ
# Calculate age considering leap years
age = calculate_complex_age(birth_date)

# ❌ Não comentar o óbvio
# Increment counter by 1
counter += 1
```

### Docstrings
```python
def calculate_injury_risk(athlete_id, training_load):
    """
    Calculate injury risk for an athlete based on training load.

    Uses machine learning model to predict injury probability
    based on historical data and current training load.

    Args:
        athlete_id (int): Primary key of the athlete
        training_load (float): Current training load value

    Returns:
        float: Risk score between 0-100 (0 = low risk, 100 = high risk)

    Raises:
        Athlete.DoesNotExist: If athlete_id is invalid
        ValueError: If training_load is negative

    Example:
        >>> risk = calculate_injury_risk(123, 85.5)
        >>> print(f'Risk: {risk}%')
        Risk: 42.3%
    """
    pass
```

## Indentação e Espaçamento

### Indentação
```python
# 4 espaços (nunca tabs)
def my_function():
    if condition:
        do_something()
        do_another_thing()
```

### Linhas em Branco
```python
# 2 linhas em branco entre classes e funções de nível superior
class FirstClass:
    pass


class SecondClass:
    pass


def top_level_function():
    pass


# 1 linha em branco entre métodos de uma classe
class MyClass:
    def first_method(self):
        pass

    def second_method(self):
        pass
```

### Limite de Caracteres
```python
# ✅ Máximo 79 caracteres por linha (PEP 8)
athlete = Athlete.objects.filter(
    birth_date__year__gte=1995,
    position='FW'
).first()

# ✅ Quebra de linha em listas longas
positions = [
    'Goleiro',
    'Zagueiro',
    'Lateral',
    'Volante',
]
```

## Tratamento de Erros

### Try-Except Específico
```python
# ✅ CORRETO: Catch específico
try:
    athlete = Athlete.objects.get(pk=athlete_id)
except Athlete.DoesNotExist:
    return None

# ❌ ERRADO: Catch genérico
try:
    athlete = Athlete.objects.get(pk=athlete_id)
except:
    return None
```

### Logging de Erros
```python
import logging

logger = logging.getLogger(__name__)

try:
    process_data()
except Exception as e:
    logger.error(f'Error processing data: {e}')
    raise
```

## Type Hints (Recomendado)

```python
from typing import List, Optional, Dict
from datetime import date

def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date."""
    today = date.today()
    return today.year - birth_date.year

def get_athletes_by_position(position: str) -> List[Athlete]:
    """Get all athletes for a given position."""
    return Athlete.objects.filter(position=position)

def find_athlete(athlete_id: int) -> Optional[Athlete]:
    """Find athlete by ID, return None if not found."""
    try:
        return Athlete.objects.get(pk=athlete_id)
    except Athlete.DoesNotExist:
        return None
```

## Testes (Futuro)

### Estrutura de Teste
```python
from django.test import TestCase
from performance.models import Athlete

class AthleteModelTest(TestCase):
    """Test cases for Athlete model."""

    def setUp(self):
        """Set up test data."""
        self.athlete = Athlete.objects.create(
            name='Test Athlete',
            birth_date=date(1995, 5, 10)
        )

    def test_age_calculation(self):
        """Test that age is calculated correctly."""
        expected_age = date.today().year - 1995
        self.assertEqual(self.athlete.age(), expected_age)

    def test_str_representation(self):
        """Test string representation of athlete."""
        self.assertEqual(str(self.athlete), 'Test Athlete')
```

## Git Commits

### Mensagens de Commit
```bash
# Formato: tipo(escopo): mensagem curta
# Tipos: feat, fix, docs, style, refactor, test, chore

# ✅ CORRETO
git commit -m "feat(performance): add athlete model"
git commit -m "fix(accounts): correct email validation"
git commit -m "docs: update coding guidelines"

# ❌ ERRADO
git commit -m "updates"
git commit -m "fix bug"
```

## Checklist de Code Review

Antes de fazer commit, verificar:

- [ ] Código segue PEP 8
- [ ] Variáveis e funções em inglês
- [ ] Textos de interface em português
- [ ] Aspas simples usadas corretamente
- [ ] Models têm `created_at` e `updated_at`
- [ ] Views protegidas com `LoginRequiredMixin` quando necessário
- [ ] Imports organizados corretamente
- [ ] Sem código comentado (deletar ao invés de comentar)
- [ ] Docstrings em funções complexas
- [ ] Sem warnings do linter

## Ferramentas Recomendadas

### Linters
```bash
# flake8 para verificar PEP 8
pip install flake8
flake8 .

# black para auto-formatação
pip install black
black .
```

### Configuração do VS Code
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```

---

**Última Atualização**: 2025-10-28
