## 13. Lista de Tarefas

### Sprint 0: Configuração Inicial do Projeto
**Duração**: 1 semana

- [X] **Tarefa 0.1: Configuração do Ambiente de Desenvolvimento**
  - [X] 0.1.1: Instalar Python 3.12+ no ambiente de desenvolvimento
  - [X] 0.1.2: Criar ambiente virtual Python (`python -m venv venv`)
  - [X] 0.1.3: Ativar ambiente virtual
  - [X] 0.1.4: Criar arquivo `requirements.txt` com dependências iniciais
  - [X] 0.1.5: Instalar dependências (`pip install -r requirements.txt`)

- [X] **Tarefa 0.2: Criação do Projeto Django**
  - [X] 0.2.1: Criar projeto Django com nome `core`
  - [X] 0.2.2: Verificar se `manage.py` foi criado corretamente
  - [X] 0.2.3: Testar servidor de desenvolvimento
  - [X] 0.2.4: Acessar http://localhost:8000 e confirmar página inicial

- [X] **Tarefa 0.3: Criação das Apps Django**
  - [X] 0.3.1: Criar app `accounts`
  - [X] 0.3.2: Criar app `performance`
  - [X] 0.3.3: Criar app `scouting`
  - [X] 0.3.4: Criar app `business`
  - [X] 0.3.5: Registrar todas as apps em `core/settings.py`

- [X] **Tarefa 0.4: Configuração Inicial do Django**
  - [X] 0.4.1: Configurar `LANGUAGE_CODE = 'pt-br'`
  - [X] 0.4.2: Configurar `TIME_ZONE = 'America/Sao_Paulo'`
  - [X] 0.4.3: Configurar `USE_I18N` e `USE_TZ`
  - [X] 0.4.4: Configurar diretório de templates
  - [X] 0.4.5: Configurar diretório de arquivos estáticos
  - [X] 0.4.6: Definir `STATIC_URL`

- [X] **Tarefa 0.5: Estrutura de Diretórios**
  - [X] 0.5.1: Criar diretório `templates/`
  - [X] 0.5.2: Criar diretório `static/`
  - [X] 0.5.3: Criar diretório `static/css/`
  - [X] 0.5.4: Criar diretório `static/js/`
  - [X] 0.5.5: Criar diretório `static/images/`

- [X] **Tarefa 0.6: Configuração do TailwindCSS**
  - [X] 0.6.1: Instalar Node.js
  - [X] 0.6.2: Inicializar npm no projeto
  - [X] 0.6.3: Instalar TailwindCSS via npm
  - [X] 0.6.4: Criar arquivo de configuração do Tailwind
  - [X] 0.6.5: Configurar `tailwind.config.js`
  - [X] 0.6.6: Criar arquivo `static/css/input.css`
  - [X] 0.6.7: Adicionar script de build no `package.json`
  - [X] 0.6.8: Executar build inicial do CSS
  - [X] 0.6.9: Verificar se `output.css` foi gerado

- [ ] **Tarefa 0.7: Configuração do Git**
  - [ ] 0.7.1: Inicializar repositório Git
  - [ ] 0.7.2: Criar arquivo `.gitignore`
  - [ ] 0.7.3: Adicionar padrões ao `.gitignore`
  - [ ] 0.7.4: Fazer commit inicial

---

### Sprint 1: Sistema de Autenticação e Landing Page
**Duração**: 2 semanas

- [ ] **Tarefa 1.1: Configuração do Modelo de Usuário Customizado**
  - [ ] 1.1.1: Criar modelo `CustomUser` em `accounts/models.py`
  - [ ] 1.1.2: Configurar `USERNAME_FIELD = 'email'`
  - [ ] 1.1.3: Adicionar campos `created_at` e `updated_at`
  - [ ] 1.1.4: Tornar campo `email` obrigatório e único
  - [ ] 1.1.5: Configurar `AUTH_USER_MODEL` em `settings.py`
  - [ ] 1.1.6: Criar migração inicial
  - [ ] 1.1.7: Executar migração

- [ ] **Tarefa 1.2: Criação do Template Base**
  - [ ] 1.2.1: Criar arquivo `templates/base.html`
  - [ ] 1.2.2: Adicionar carregamento do TailwindCSS
  - [ ] 1.2.3: Configurar blocos Django
  - [ ] 1.2.4: Adicionar meta tags responsivas
  - [ ] 1.2.5: Configurar classes para fundo escuro
  - [ ] 1.2.6: Adicionar fonte Inter via Google Fonts

- [ ] **Tarefa 1.3: Desenvolvimento da Landing Page**
  - [ ] 1.3.1: Criar view `HomeView` em `accounts/views.py`
  - [ ] 1.3.2: Criar template `templates/home.html`
  - [ ] 1.3.3: Implementar seção hero
  - [ ] 1.3.4: Adicionar logo "AI Soccer" com gradiente
  - [ ] 1.3.5: Criar seção de funcionalidades
  - [ ] 1.3.6: Adicionar ícones ou ilustrações
  - [ ] 1.3.7: Implementar seção de CTA
  - [ ] 1.3.8: Garantir responsividade
  - [ ] 1.3.9: Configurar URL raiz
  - [ ] 1.3.10: Testar em diferentes telas

- [ ] **Tarefa 1.4: Formulário de Cadastro de Usuário**
  - [ ] 1.4.1: Criar `CustomUserCreationForm`
  - [ ] 1.4.2: Configurar campos do formulário
  - [ ] 1.4.3: Adicionar validação de senha
  - [ ] 1.4.4: Adicionar classes CSS aos widgets
  - [ ] 1.4.5: Criar view `SignUpView`
  - [ ] 1.4.6: Criar template `signup.html`
  - [ ] 1.4.7: Implementar layout do formulário
  - [ ] 1.4.8: Adicionar mensagens de erro
  - [ ] 1.4.9: Configurar redirecionamento
  - [ ] 1.4.10: Adicionar URL `/signup/`
  - [ ] 1.4.11: Incluir URLs em `core/urls.py`
  - [ ] 1.4.12: Testar cadastro

- [ ] **Tarefa 1.5: Formulário de Login**
  - [ ] 1.5.1: Criar `CustomAuthenticationForm`
  - [ ] 1.5.2: Configurar campo para aceitar email
  - [ ] 1.5.3: Adicionar classes CSS
  - [ ] 1.5.4: Criar view `LoginView`
  - [ ] 1.5.5: Criar template `login.html`
  - [ ] 1.5.6: Implementar layout
  - [ ] 1.5.7: Adicionar link "Esqueci minha senha"
  - [ ] 1.5.8: Adicionar link "Cadastre-se"
  - [ ] 1.5.9: Configurar redirecionamento
  - [ ] 1.5.10: Adicionar URL `/login/`
  - [ ] 1.5.11: Configurar `LOGIN_URL`
  - [ ] 1.5.12: Configurar `LOGIN_REDIRECT_URL`
  - [ ] 1.5.13: Testar login

- [ ] **Tarefa 1.6: Funcionalidade de Logout**
  - [ ] 1.6.1: Criar view `LogoutView`
  - [ ] 1.6.2: Configurar redirecionamento
  - [ ] 1.6.3: Adicionar URL `/logout/`
  - [ ] 1.6.4: Configurar `LOGOUT_REDIRECT_URL`
  - [ ] 1.6.5: Testar logout

- [ ] **Tarefa 1.7: Backend de Autenticação por Email**
  - [ ] 1.7.1: Criar `EmailBackend` em `accounts/backends.py`
  - [ ] 1.7.2: Implementar método `authenticate`
  - [ ] 1.7.3: Configurar `AUTHENTICATION_BACKENDS`
  - [ ] 1.7.4: Testar autenticação por email

- [ ] **Tarefa 1.8: Testes de Integração**
  - [ ] 1.8.1: Testar fluxo completo
  - [ ] 1.8.2: Testar acesso a páginas protegidas
  - [ ] 1.8.3: Testar logout e redirecionamento
  - [ ] 1.8.4: Validar mensagens
  - [ ] 1.8.5: Validar responsividade

---

### Sprint 2: Dashboard Principal e Navegação
**Duração**: 1 semana

- [ ] **Tarefa 2.1: Criação do Template Base do Dashboard**
  - [ ] 2.1.1: Criar `templates/dashboard/base_dashboard.html`
  - [ ] 2.1.2: Implementar sidebar fixa
  - [ ] 2.1.3: Adicionar logo no topo da sidebar
  - [ ] 2.1.4: Implementar área de conteúdo principal
  - [ ] 2.1.5: Adicionar navbar superior
  - [ ] 2.1.6: Adicionar botão de logout
  - [ ] 2.1.7: Implementar menu mobile
  - [ ] 2.1.8: Adicionar classes responsivas
  - [ ] 2.1.9: Testar navegação

- [ ] **Tarefa 2.2: Dashboard Principal (Home)**
  - [ ] 2.2.1: Criar view `DashboardView`
  - [ ] 2.2.2: Criar template `dashboard/home.html`
  - [ ] 2.2.3: Implementar seção de boas-vindas
  - [ ] 2.2.4: Adicionar cards para módulos
  - [ ] 2.2.5: Criar seção de resumo geral
  - [ ] 2.2.6: Adicionar grid responsivo
  - [ ] 2.2.7: Implementar hover effects
  - [ ] 2.2.8: Adicionar URL `/dashboard/`
  - [ ] 2.2.9: Testar acesso ao dashboard
  - [ ] 2.2.10: Validar redirecionamento

- [ ] **Tarefa 2.3: Componente de Navegação Reutilizável**
  - [ ] 2.3.1: Criar `templates/components/sidebar.html`
  - [ ] 2.3.2: Implementar lógica de item ativo
  - [ ] 2.3.3: Adicionar ícones aos itens
  - [ ] 2.3.4: Criar `templates/components/navbar.html`
  - [ ] 2.3.5: Implementar dropdown de usuário
  - [ ] 2.3.6: Integrar componentes
  - [ ] 2.3.7: Testar navegação

- [ ] **Tarefa 2.4: Página de Perfil do Usuário**
  - [ ] 2.4.1: Criar view `ProfileView`
  - [ ] 2.4.2: Criar template `accounts/profile.html`
  - [ ] 2.4.3: Exibir informações do usuário
  - [ ] 2.4.4: Adicionar botão "Editar Perfil"
  - [ ] 2.4.5: Adicionar URL `/profile/`
  - [ ] 2.4.6: Adicionar link no navbar
  - [ ] 2.4.7: Testar visualização

---

### Sprint 3: Módulo de Performance - Gestão de Atletas
**Duração**: 2 semanas

- [ ] **Tarefa 3.1: Modelo de Atleta**
  - [ ] 3.1.1: Criar modelo `Athlete` em `performance/models.py`
  - [ ] 3.1.2: Adicionar campos básicos
  - [ ] 3.1.3: Adicionar campos físicos
  - [ ] 3.1.4: Adicionar campos de auditoria
  - [ ] 3.1.5: Adicionar campo `created_by`
  - [ ] 3.1.6: Criar método `__str__`
  - [ ] 3.1.7: Criar método `age`
  - [ ] 3.1.8: Criar e aplicar migrações
  - [ ] 3.1.9: Registrar no admin

- [ ] **Tarefa 3.2: Listagem de Atletas**
  - [ ] 3.2.1: Criar view `AthleteListView`
  - [ ] 3.2.2: Criar template `athlete_list.html`
  - [ ] 3.2.3: Implementar tabela responsiva
  - [ ] 3.2.4: Adicionar botão "Adicionar Atleta"
  - [ ] 3.2.5: Implementar links de ação
  - [ ] 3.2.6: Adicionar paginação
  - [ ] 3.2.7: Adicionar busca por nome
  - [ ] 3.2.8: Adicionar filtro por posição
  - [ ] 3.2.9: Implementar estado vazio
  - [ ] 3.2.10: Adicionar URL
  - [ ] 3.2.11: Incluir URLs em `core/urls.py`
  - [ ] 3.2.12: Testar listagem

- [ ] **Tarefa 3.3: Formulário de Cadastro**
  - [ ] 3.3.1: Criar `AthleteForm`
  - [ ] 3.3.2: Configurar campos
  - [ ] 3.3.3: Adicionar validação de data
  - [ ] 3.3.4: Adicionar validação de valores
  - [ ] 3.3.5: Adicionar classes CSS
  - [ ] 3.3.6: Criar view `AthleteCreateView`
  - [ ] 3.3.7: Configurar `created_by`
  - [ ] 3.3.8: Criar template de formulário
  - [ ] 3.3.9: Implementar layout
  - [ ] 3.3.10: Adicionar botões
  - [ ] 3.3.11: Configurar redirecionamento
  - [ ] 3.3.12: Adicionar URL
  - [ ] 3.3.13: Testar cadastro

- [ ] **Tarefa 3.4: Página de Detalhes**
  - [ ] 3.4.1: Criar view `AthleteDetailView`
  - [ ] 3.4.2: Criar template de detalhes
  - [ ] 3.4.3: Exibir informações em cards
  - [ ] 3.4.4: Criar seção "Dados Pessoais"
  - [ ] 3.4.5: Criar seção "Dados Físicos"
  - [ ] 3.4.6: Adicionar placeholders
  - [ ] 3.4.7: Adicionar botões de ação
  - [ ] 3.4.8: Adicionar URL
  - [ ] 3.4.9: Testar visualização

- [ ] **Tarefa 3.5: Edição de Atleta**
  - [ ] 3.5.1: Criar view `AthleteUpdateView`
  - [ ] 3.5.2: Reutilizar template
  - [ ] 3.5.3: Adicionar título de edição
  - [ ] 3.5.4: Configurar redirecionamento
  - [ ] 3.5.5: Adicionar URL
  - [ ] 3.5.6: Testar edição

- [ ] **Tarefa 3.6: Exclusão de Atleta**
  - [ ] 3.6.1: Criar view `AthleteDeleteView`
  - [ ] 3.6.2: Criar template de confirmação
  - [ ] 3.6.3: Implementar modal
  - [ ] 3.6.4: Adicionar botões
  - [ ] 3.6.5: Configurar redirecionamento
  - [ ] 3.6.6: Adicionar URL
  - [ ] 3.6.7: Testar exclusão

- [ ] **Tarefa 3.7: Integração com Menu**
  - [ ] 3.7.1: Adicionar item "Performance"
  - [ ] 3.7.2: Criar submenu
  - [ ] 3.7.3: Atualizar lógica de highlight
  - [ ] 3.7.4: Testar navegação

---

### Sprints 4-16: [Continuação conforme PRD original]

_As demais sprints seguem a mesma estrutura detalhada, cobrindo:_
- Sprint 4: Treinos e Cargas
- Sprint 5: Lesões e Dashboard de Performance
- Sprint 6-8: Módulo de Scouting
- Sprint 9-10: Módulo de Business
- Sprint 11: Integração entre Módulos
- Sprint 12: Recursos Adicionais
- Sprint 13: Modelos Preditivos (IA)
- Sprint 14: Testes
- Sprint 15: Polimento
- Sprint 16: Deploy

---
