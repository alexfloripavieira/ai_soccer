# AI Soccer - Agentes de Desenvolvimento

Esta pasta contém agentes especializados de IA para desenvolvimento do projeto AI Soccer. Cada agente é especialista em uma área específica da stack tecnológica do projeto.

## 📋 Índice de Agentes

### 🐍 Backend e Arquitetura

#### [Django Backend Specialist](django-backend.md)
**Especialidade**: Django 5.x, Python 3.12+, Django ORM, Models, Views (CBV)

**Quando Usar**:
- Criar ou modificar models Django
- Implementar views (Class-Based Views)
- Configurar URLs e routing
- Implementar lógica de negócio
- Criar forms e validações
- Configurar Django Admin
- Trabalhar com migrations

**Stack**:
- Python 3.12+
- Django 5.x
- Django ORM
- SQLite/PostgreSQL

---

### 🎨 Frontend e UI

#### [Frontend Specialist](frontend-specialist.md)
**Especialidade**: Django Template Language, TailwindCSS 3.x, Alpine.js

**Quando Usar**:
- Criar ou modificar templates Django
- Implementar design system com TailwindCSS
- Criar componentes visuais
- Implementar layouts responsivos
- Adicionar interatividade com Alpine.js
- Trabalhar com static files

**Stack**:
- Django Template Language (DTL)
- TailwindCSS 3.x
- Alpine.js (opcional)
- HTML5/CSS3

---

### 🧪 Quality Assurance

#### [QA Tester](qa-tester.md)
**Especialidade**: Testes de UI/UX, Testes de integração, Validação de design

**Quando Usar**:
- Validar funcionalidades implementadas
- Testar fluxos de usuário
- Verificar responsividade
- Validar design system
- Testar autenticação e segurança
- Verificar acessibilidade básica

**Ferramentas**:
- MCP Playwright (testes automatizados de UI)
- Django Test Framework (futuro)

---

## 🎯 Fluxo de Trabalho Recomendado

### 1. Nova Funcionalidade Backend
```
1. Django Backend Specialist → Implementa models, views, forms
2. Frontend Specialist → Cria templates e componentes visuais
3. QA Tester → Valida funcionalidade e design
```

### 2. Nova Tela/Interface
```
1. Frontend Specialist → Cria templates e estilização
2. Django Backend Specialist → Conecta views e lógica
3. QA Tester → Testa responsividade e fluxo
```

### 3. Correção de Bug
```
1. Identificar camada (Backend/Frontend)
2. Django Backend Specialist OU Frontend Specialist → Corrige
3. QA Tester → Valida correção e testa regressão
```

## 📚 Recursos Compartilhados

Todos os agentes têm acesso a:
- [Documentação completa](../docs/README.md)
- [PRD - Product Requirements Document](../PRD.md)
- [CLAUDE.md](../CLAUDE.md) - Guia técnico do projeto
- [Guia de Código](../docs/coding-guidelines.md)
- [Design System](../docs/design-system.md)

## 🔧 MCP Servers Utilizados

### Context7 (Documentação)
**Usado por**: Django Backend Specialist, Frontend Specialist

Fornece documentação atualizada de:
- Django
- TailwindCSS
- Python
- Alpine.js

**Como usar**:
```
Ao escrever código, consultar documentação oficial via Context7
para garantir uso correto de APIs e melhores práticas.
```

### Playwright (Testes)
**Usado por**: QA Tester

Automatiza testes de interface:
- Navegação e interação
- Validação de elementos
- Testes de formulários
- Verificação de design

## 🎨 Padrões do Projeto

### Convenções Críticas

**TODOS os agentes DEVEM seguir**:

1. **Idioma**:
   - Código: Inglês
   - Interface/UI: Português brasileiro

2. **Aspas**:
   - Python: Aspas simples sempre que possível
   - Templates: Aspas duplas nos atributos HTML

3. **PEP 8**:
   - Seguir rigorosamente
   - 4 espaços de indentação
   - Máximo 79 caracteres por linha

4. **Models**:
   - Sempre incluir `created_at` e `updated_at`
   - ForeignKey para User: usar `settings.AUTH_USER_MODEL`

5. **Views**:
   - Preferir Class-Based Views (CBV)
   - Usar `LoginRequiredMixin` para proteção

6. **Design**:
   - Dark mode first
   - Gradiente: verde (#10b981) → azul (#3b82f6)
   - Fonte: Inter
   - Framework: TailwindCSS

## 📝 Checklist Antes de Commit

- [ ] Código segue PEP 8
- [ ] Código em inglês, interface em português
- [ ] Aspas simples em Python
- [ ] Models têm `created_at` e `updated_at`
- [ ] Views protegidas com `LoginRequiredMixin`
- [ ] Templates seguem design system
- [ ] Testado manualmente ou com QA Tester
- [ ] Sem warnings ou erros

## 🚀 Como Invocar um Agente

No Claude Code, use a ferramenta Task para invocar agentes especializados:

```
Invoke Django Backend Specialist para criar o modelo de Atleta
```

```
Invoke Frontend Specialist para criar a landing page
```

```
Invoke QA Tester para validar o fluxo de autenticação
```

---

**Última Atualização**: 2025-10-28
