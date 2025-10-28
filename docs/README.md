# Documentação AI Soccer

Bem-vindo à documentação do **AI Soccer** - Sistema de Gestão Esportiva com Inteligência Artificial.

## Índice da Documentação

### 📋 Visão Geral
- [Arquitetura do Projeto](arquitetura.md) - Estrutura geral e organização do código
- [Stack Tecnológica](stack.md) - Tecnologias e ferramentas utilizadas

### 🎨 Design e Frontend
- [Design System](design-system.md) - Padrões visuais, cores, tipografia e componentes
- [Guia de Componentes](componentes.md) - Componentes TailwindCSS reutilizáveis

### 💻 Desenvolvimento
- [Guia de Código](coding-guidelines.md) - Padrões de código e boas práticas
- [Estrutura de Apps](apps-structure.md) - Organização das apps Django
- [Modelos de Dados](models.md) - Estrutura do banco de dados

### 🚀 Setup e Configuração
- [Guia de Instalação](instalacao.md) - Como configurar o ambiente de desenvolvimento
- [Configurações](configuracoes.md) - Variáveis de ambiente e settings

### 📚 Referências
- [PRD - Product Requirements Document](../PRD.md) - Documento de requisitos do produto
- [Glossário](glossario.md) - Termos e conceitos do projeto

---

## Início Rápido

### Pré-requisitos
- Python 3.12+
- Node.js (para TailwindCSS)
- Git

### Instalação Básica

```bash
# Clone o repositório
cd ai_soccer_project

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

Acesse: http://localhost:8000

---

## Estrutura do Projeto

```
ai_soccer_project/
├── core/              # Configurações principais do Django
├── accounts/          # Autenticação e usuários
├── performance/       # Módulo de performance de atletas
├── scouting/          # Módulo de prospecção
├── business/          # Módulo de gestão financeira
├── docs/              # Documentação do projeto
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── templates/         # Templates Django
├── manage.py          # Script de gerenciamento Django
└── requirements.txt   # Dependências Python
```

---

## Princípios do Projeto

### Simplicidade
- Código simples e direto
- Sem over-engineering
- Funcionalidades apenas quando necessárias

### Modularidade
- Apps Django separadas por domínio
- Responsabilidades bem definidas
- Baixo acoplamento entre módulos

### Padrões
- PEP 8 para código Python
- Aspas simples sempre que possível
- Código em inglês, interface em português

### Design Consistente
- Design system unificado
- TailwindCSS para estilização
- Tema escuro moderno

---

## Contribuindo

Antes de contribuir, leia:
1. [Guia de Código](coding-guidelines.md)
2. [Design System](design-system.md)
3. [Estrutura de Apps](apps-structure.md)

---

## Suporte

Para dúvidas sobre o projeto:
- Consulte a documentação específica de cada módulo
- Revise o [PRD](../PRD.md) para entender os requisitos
- Verifique o [Glossário](glossario.md) para termos técnicos

---

**Versão da Documentação**: 1.0
**Última Atualização**: 2025-10-28
