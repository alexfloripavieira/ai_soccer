# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI Soccer** is a Django full-stack web application for sports management powered by artificial intelligence. The system integrates three core domains:
- **Performance**: Athlete monitoring, training load analysis, injury prevention
- **Scouting**: Player prospecting, talent detection, profile comparison
- **Business**: Financial management, athlete valuation, revenue analysis

**Current Status**: Initial setup phase. Apps structure created, implementation pending.

## Development Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## TailwindCSS Workflow

The project uses TailwindCSS for styling. CSS must be built before running the server:

```bash
# One-time build
npm run build:css

# Watch mode (auto-rebuild on template changes)
npm run watch:css
```

**Important**: Always run `npm run watch:css` in a separate terminal during development.

## Core Architecture

### Domain-Driven App Structure

The project uses **Django apps by business domain**, not by technical layer:

```
core/         → Settings and root configuration (NO models)
accounts/     → Authentication via EMAIL (not username)
performance/  → Athlete management, training loads, injuries
scouting/     → Player prospecting, scouting reports
business/     → Financial records, club management, valuations
```

### Key Architectural Principles

1. **App Independence**: Each app should be self-contained with minimal cross-dependencies
2. **No Circular Dependencies**: Avoid importing between domain apps
3. **User Reference**: Always use `settings.AUTH_USER_MODEL` for ForeignKeys to User
4. **Audit Fields**: ALL main models must have `created_at` and `updated_at` fields

### Cross-App Relationships

**Allowed**:
```python
# Any app can reference User
from django.conf import settings
created_by = models.ForeignKey(settings.AUTH_USER_MODEL, ...)

# Business can reference Performance (for athlete valuation)
from performance.models import Athlete
```

**Avoid**: Circular imports between performance ↔ scouting, scouting ↔ business, etc.

## Critical Coding Standards

### Language Convention (STRICTLY ENFORCED)

```python
# ✅ CORRECT: Code in English, UI in Portuguese
class Athlete(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'

# ❌ WRONG: Code in Portuguese
class Atleta(models.Model):
    nome = models.CharField(max_length=200)
```

### Quote Convention (STRICTLY ENFORCED)

```python
# ✅ ALWAYS use single quotes
name = 'João Silva'
position = 'Atacante'

# ✅ Double quotes ONLY when necessary
message = "He said: 'Hello'"

# ❌ WRONG: Unnecessary double quotes
name = "João Silva"
```

### Model Structure Pattern

```python
from django.db import models
from django.conf import settings

class ModelName(models.Model):
    """Docstring."""

    # 1. Choices constants
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
    ]

    # 2. Relational fields first
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, ...)

    # 3. Main fields
    name = models.CharField('Nome', max_length=200)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES)

    # 4. Audit fields LAST (mandatory)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nome do Modelo'
        verbose_name_plural = 'Nomes dos Modelos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

### View Pattern (Prefer Class-Based Views)

```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# ✅ CORRECT: CBV with LoginRequired
class AthleteListView(LoginRequiredMixin, ListView):
    model = Athlete
    template_name = 'performance/athlete_list.html'
    context_object_name = 'athletes'
    paginate_by = 20
    login_url = '/login/'

# ⚠️ Use function-based views ONLY when CBV doesn't fit
```

**Critical**: Mixins go FIRST, then the view class: `LoginRequiredMixin, ListView` (not reversed).

## Database Commands

```bash
# Create migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration SQL (useful for debugging)
python manage.py sqlmigrate app_name 0001

# Check for issues
python manage.py check

# Access Django shell
python manage.py shell
```

## Django Admin

```bash
# Access admin interface
python manage.py createsuperuser
# Navigate to: http://localhost:8000/admin
```

Register models in `admin.py`:
```python
from django.contrib import admin
from .models import Athlete

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'birth_date', 'created_at']
    list_filter = ['position', 'created_at']
    search_fields = ['name']
```

## Template Structure

```
templates/
├── base.html              # Base template (extends by all)
├── components/            # Reusable components
│   ├── sidebar.html
│   └── navbar.html
├── accounts/              # App-specific templates
│   ├── login.html
│   └── signup.html
├── performance/
└── ...
```

Template inheritance:
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    {# Content here #}
</div>
{% endblock %}
```

## Design System (TailwindCSS)

### Color Palette (Dark Theme)

```css
/* Primary gradient */
from-green-500 to-blue-500  /* #10b981 → #3b82f6 */

/* Backgrounds */
bg-slate-900  /* Primary background #0f172a */
bg-slate-800  /* Cards, panels #1e293b */
bg-slate-700  /* Elevated elements #334155 */

/* Text */
text-slate-100  /* Primary text #f1f5f9 */
text-slate-300  /* Secondary text #cbd5e1 */
text-slate-400  /* Muted text #94a3b8 */

/* Status colors */
bg-green-900 text-green-300  /* Success */
bg-red-900 text-red-300      /* Error */
bg-yellow-900 text-yellow-300 /* Warning */
```

### Component Patterns

**Primary Button**:
```html
<button class="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
    Action
</button>
```

**Input Field**:
```html
<input type="text" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200">
```

**Card**:
```html
<div class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-200">
    Content
</div>
```

Full component library available in `docs/componentes.md`.

## Import Organization (PEP 8)

```python
# 1. Standard library
import os
from datetime import date, datetime

# 2. Third-party
from django.db import models
from django.contrib.auth import get_user_model

# 3. Local imports
from accounts.models import User
from performance.utils import calculate_age
```

## Planned Models (Not Yet Implemented)

### accounts.CustomUser
- Email-based authentication (USERNAME_FIELD = 'email')
- No username field

### performance.Athlete
- Fields: name, birth_date, position, nationality, height, weight
- ForeignKey to User (created_by)
- Method: age() to calculate current age

### performance.TrainingLoad
- ForeignKey to Athlete
- Fields: training_date, duration_minutes, distance_km, heart_rate_avg, heart_rate_max, intensity_level
- Method: fatigue_index()

### performance.InjuryRecord
- ForeignKey to Athlete
- Fields: injury_date, injury_type, body_part, severity_level, expected_return

### scouting.ScoutedPlayer
- Similar to Athlete but for prospecting
- Fields: name, birth_date, position, current_club, nationality, market_value

### scouting.ScoutingReport
- ForeignKey to ScoutedPlayer and User (scout)
- Fields: technical_score, physical_score, tactical_score, mental_score, potential_score (all 0-10)
- Method: overall_score() calculates average

### business.Club
- Fields: name, country, division

### business.FinancialRecord
- ForeignKey to Club
- Fields: record_date, category, amount, transaction_type, description

### business.Revenue
- ForeignKey to Club
- Fields: year, month, ticketing, sponsorship, broadcasting, merchandising
- Method: total_revenue()

Full models specification in `docs/models.md`.

## What NOT to Do

- ❌ Do NOT add features "just in case" (violates simplicity principle)
- ❌ Do NOT use double quotes without necessity
- ❌ Do NOT write code in Portuguese (variable names, functions, classes)
- ❌ Do NOT use username-based auth (must be email-based)
- ❌ Do NOT create models without created_at/updated_at fields
- ❌ Do NOT import User model directly (use settings.AUTH_USER_MODEL)
- ❌ Do NOT create circular dependencies between apps
- ❌ Do NOT use function-based views when CBV is appropriate

## Project Philosophy

1. **Simplicity First**: If it can be simple, keep it simple
2. **No Over-Engineering**: Add complexity only when needed
3. **Code in English, UI in Portuguese**: Strict separation
4. **PEP 8 Compliance**: Follow rigorously
5. **Modular Architecture**: Apps by business domain, not technical layer

## Documentation

Comprehensive documentation available in `docs/`:
- `docs/coding-guidelines.md` - Complete coding standards
- `docs/design-system.md` - Full design system specification
- `docs/componentes.md` - Copy-paste ready components
- `docs/arquitetura.md` - Architecture deep dive
- `docs/models.md` - Complete data model specification
- `PRD.md` - Product requirements and roadmap

## Configuration Notes

### settings.py Requirements

When implementing features, ensure:
```python
# Must be configured for custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Authentication URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

# Templates directory
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Static files
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## Machine Learning Integration (Future)

Planned ML models using scikit-learn:
- **Performance**: Injury risk prediction based on training load
- **Scouting**: Player potential assessment from scouting scores
- **Business**: Revenue forecasting using historical data

Store ML code in: `ml_models/` directory (to be created).
