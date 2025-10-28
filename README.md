# AI Soccer

Sistema de Gestão Esportiva baseado em Inteligência Artificial para análise de Performance, Scouting e Business no futebol profissional.

## 🎯 Sobre o Projeto

O **AI Soccer** é uma plataforma web full-stack desenvolvida com Django que integra três pilares fundamentais:

- **⚡ Performance**: Monitoramento de atletas, análise tática e prevenção de lesões
- **🔍 Scouting**: Prospecção de talentos e análise de mercado
- **💼 Business**: Gestão financeira, valuation de atletas e análise comercial

## 🚀 Quick Start

```bash
# 1. Clonar/acessar o projeto
cd ai_soccer_project

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar migrações
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

Acesse: http://localhost:8000

## 📚 Documentação

A documentação completa está disponível em [`docs/`](docs/):

### Início Rápido
- [📖 README da Documentação](docs/README.md) - Índice completo
- [🛠️ Guia de Instalação](docs/instalacao.md) - Setup passo a passo

### Desenvolvimento
- [💻 Guia de Código](docs/coding-guidelines.md) - Padrões e convenções
- [🎨 Design System](docs/design-system.md) - Cores, tipografia, componentes
- [🧩 Componentes](docs/componentes.md) - Biblioteca de componentes TailwindCSS

### Arquitetura
- [🏗️ Arquitetura](docs/arquitetura.md) - Estrutura e organização
- [📦 Stack Tecnológica](docs/stack.md) - Tecnologias utilizadas
- [📂 Estrutura de Apps](docs/apps-structure.md) - Apps Django
- [🗄️ Models](docs/models.md) - Estrutura de dados

### Configuração
- [⚙️ Configurações](docs/configuracoes.md) - Settings e variáveis de ambiente
- [📝 Glossário](docs/glossario.md) - Termos técnicos e de futebol

### Planejamento
- [📋 PRD](PRD.md) - Product Requirements Document completo

## 🛠️ Stack Tecnológica

### Backend
- **Python 3.12+**
- **Django 5.x** - Framework web full-stack
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **Django Template Language** - Templates
- **TailwindCSS 3.x** - Framework CSS
- **Chart.js** - Visualização de dados (planejado)

### Machine Learning (Planejado)
- **scikit-learn** - Modelos preditivos
- **pandas** - Análise de dados
- **numpy** - Operações numéricas

## 📁 Estrutura do Projeto

```
ai_soccer_project/
├── core/              # Configurações principais
├── accounts/          # Autenticação e usuários
├── performance/       # Análise de performance de atletas
├── scouting/          # Prospecção de jogadores
├── business/          # Gestão financeira e comercial
├── docs/              # Documentação completa
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── templates/         # Templates Django
├── manage.py          # Script de gerenciamento Django
├── requirements.txt   # Dependências Python
└── README.md          # Este arquivo
```

## 📋 Status do Projeto

**Versão Atual**: 0.1.0 (Setup Inicial)

### ✅ Completo
- [x] Estrutura inicial do projeto Django
- [x] Apps Django criadas (accounts, performance, scouting, business)
- [x] Documentação completa
- [x] PRD detalhado
- [x] Design System definido

### 🚧 Em Desenvolvimento
- [ ] Configuração completa do Django (settings.py)
- [ ] Implementação do modelo de usuário customizado
- [ ] Templates base e design system
- [ ] Integração do TailwindCSS

### 📅 Planejado (Sprints)
- Sprint 0: Configuração inicial e setup ✅
- Sprint 1: Sistema de autenticação e landing page
- Sprint 2: Dashboard principal
- Sprint 3-7: Módulos Performance, Scouting e Business
- Sprint 13: Modelos de IA
- Sprint 16: Deploy

Ver [PRD.md](PRD.md) para roadmap completo.

## 🎨 Design

- **Tema**: Dark mode com gradientes vibrantes
- **Cores Primárias**: Verde (#10b981) → Azul (#3b82f6)
- **Fonte**: Inter (Google Fonts)
- **Framework CSS**: TailwindCSS 3.x

Ver [Design System](docs/design-system.md) para especificações completas.

## 📝 Convenções de Código

- **Idioma do código**: Inglês
- **Idioma da interface**: Português brasileiro
- **Estilo Python**: PEP 8
- **Aspas**: Simples sempre que possível
- **Views**: Class-Based Views (CBV) preferencial
- **Models**: Sempre incluir `created_at` e `updated_at`

Ver [Guia de Código](docs/coding-guidelines.md) para detalhes completos.

## 🤝 Contribuindo

1. Leia a [Documentação](docs/README.md)
2. Siga o [Guia de Código](docs/coding-guidelines.md)
3. Consulte o [PRD](PRD.md) para funcionalidades planejadas
4. Mantenha o código simples e direto

## 📄 Licença

Este projeto está em desenvolvimento para fins educacionais e de portfólio.

## 👥 Autores

- **AI Soccer Team**

## 🔗 Links Úteis

- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Python PEP 8](https://peps.python.org/pep-0008/)

---

**Última Atualização**: 2025-10-28
