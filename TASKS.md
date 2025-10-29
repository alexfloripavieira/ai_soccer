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

- [x] **Tarefa 0.7: Configuração do Git**
  - [x] 0.7.1: Inicializar repositório Git
  - [x] 0.7.2: Criar arquivo `.gitignore`
  - [x] 0.7.3: Adicionar padrões ao `.gitignore`
  - [x] 0.7.4: Fazer commit inicial

---

### Sprint 1: Sistema de Autenticação e Landing Page
**Duração**: 2 semanas

- [X] **Tarefa 1.1: Configuração do Modelo de Usuário Customizado**
  - [X] 1.1.1: Criar modelo `CustomUser` em `accounts/models.py`
  - [X] 1.1.2: Configurar `USERNAME_FIELD = 'email'`
  - [X] 1.1.3: Adicionar campos `created_at` e `updated_at`
  - [X] 1.1.4: Tornar campo `email` obrigatório e único
  - [X] 1.1.5: Configurar `AUTH_USER_MODEL` em `settings.py`
  - [X] 1.1.6: Criar migração inicial
  - [X] 1.1.7: Executar migração

- [X] **Tarefa 1.2: Criação do Template Base**
  - [X] 1.2.1: Criar arquivo `templates/base.html`
  - [X] 1.2.2: Adicionar carregamento do TailwindCSS
  - [X] 1.2.3: Configurar blocos Django
  - [X] 1.2.4: Adicionar meta tags responsivas
  - [X] 1.2.5: Configurar classes para fundo escuro
  - [X] 1.2.6: Adicionar fonte Inter via Google Fonts

- [X] **Tarefa 1.3: Desenvolvimento da Landing Page**
  - [X] 1.3.1: Criar view `HomeView` em `accounts/views.py`
  - [X] 1.3.2: Criar template `templates/home.html`
  - [X] 1.3.3: Implementar seção hero
  - [X] 1.3.4: Adicionar logo "AI Soccer" com gradiente
  - [X] 1.3.5: Criar seção de funcionalidades
  - [X] 1.3.6: Adicionar ícones ou ilustrações
  - [X] 1.3.7: Implementar seção de CTA
  - [X] 1.3.8: Garantir responsividade
  - [X] 1.3.9: Configurar URL raiz
  - [X] 1.3.10: Testar em diferentes telas

- [X] **Tarefa 1.4: Formulário de Cadastro de Usuário**
  - [X] 1.4.1: Criar `CustomUserCreationForm`
  - [X] 1.4.2: Configurar campos do formulário
  - [X] 1.4.3: Adicionar validação de senha
  - [X] 1.4.4: Adicionar classes CSS aos widgets
  - [X] 1.4.5: Criar view `SignUpView`
  - [X] 1.4.6: Criar template `signup.html`
  - [X] 1.4.7: Implementar layout do formulário
  - [X] 1.4.8: Adicionar mensagens de erro
  - [X] 1.4.9: Configurar redirecionamento
  - [X] 1.4.10: Adicionar URL `/signup/`
  - [X] 1.4.11: Incluir URLs em `core/urls.py`
  - [X] 1.4.12: Testar cadastro

- [X] **Tarefa 1.5: Formulário de Login**
  - [X] 1.5.1: Criar `CustomAuthenticationForm`
  - [X] 1.5.2: Configurar campo para aceitar email
  - [X] 1.5.3: Adicionar classes CSS
  - [X] 1.5.4: Criar view `LoginView`
  - [X] 1.5.5: Criar template `login.html`
  - [X] 1.5.6: Implementar layout
  - [X] 1.5.7: Adicionar link "Esqueci minha senha"
  - [X] 1.5.8: Adicionar link "Cadastre-se"
  - [X] 1.5.9: Configurar redirecionamento
  - [X] 1.5.10: Adicionar URL `/login/`
  - [X] 1.5.11: Configurar `LOGIN_URL`
  - [X] 1.5.12: Configurar `LOGIN_REDIRECT_URL`
  - [X] 1.5.13: Testar login

- [X] **Tarefa 1.6: Funcionalidade de Logout**
  - [X] 1.6.1: Criar view `LogoutView`
  - [X] 1.6.2: Configurar redirecionamento
  - [X] 1.6.3: Adicionar URL `/logout/`
  - [X] 1.6.4: Configurar `LOGOUT_REDIRECT_URL`
  - [X] 1.6.5: Testar logout

- [X] **Tarefa 1.7: Backend de Autenticação por Email**
  - [X] 1.7.1: Criar `EmailBackend` em `accounts/backends.py`
  - [X] 1.7.2: Implementar método `authenticate`
  - [X] 1.7.3: Configurar `AUTHENTICATION_BACKENDS`
  - [X] 1.7.4: Testar autenticação por email

- [X] **Tarefa 1.8: Testes de Integração**
  - [X] 1.8.1: Testar fluxo completo
  - [X] 1.8.2: Testar acesso a páginas protegidas
  - [X] 1.8.3: Testar logout e redirecionamento
  - [X] 1.8.4: Validar mensagens
  - [X] 1.8.5: Validar responsividade

---

### Sprint 2: Dashboard Principal e Navegação
**Duração**: 1 semana

- [X] **Tarefa 2.1: Criação do Template Base do Dashboard**
  - [X] 2.1.1: Criar `templates/dashboard/base_dashboard.html`
  - [X] 2.1.2: Implementar sidebar fixa
  - [X] 2.1.3: Adicionar logo no topo da sidebar
  - [X] 2.1.4: Implementar área de conteúdo principal
  - [X] 2.1.5: Adicionar navbar superior
  - [X] 2.1.6: Adicionar botão de logout
  - [X] 2.1.7: Implementar menu mobile
  - [X] 2.1.8: Adicionar classes responsivas
  - [X] 2.1.9: Testar navegação

- [X] **Tarefa 2.2: Dashboard Principal (Home)**
  - [X] 2.2.1: Criar view `DashboardView`
  - [X] 2.2.2: Criar template `dashboard/home.html`
  - [X] 2.2.3: Implementar seção de boas-vindas
  - [X] 2.2.4: Adicionar cards para módulos
  - [X] 2.2.5: Criar seção de resumo geral
  - [X] 2.2.6: Adicionar grid responsivo
  - [X] 2.2.7: Implementar hover effects
  - [X] 2.2.8: Adicionar URL `/dashboard/`
  - [X] 2.2.9: Testar acesso ao dashboard
  - [X] 2.2.10: Validar redirecionamento

- [X] **Tarefa 2.3: Componente de Navegação Reutilizável**
  - [X] 2.3.1: Criar `templates/components/sidebar.html`
  - [X] 2.3.2: Implementar lógica de item ativo
  - [X] 2.3.3: Adicionar ícones aos itens
  - [X] 2.3.4: Criar `templates/components/navbar.html`
  - [X] 2.3.5: Implementar dropdown de usuário
  - [X] 2.3.6: Integrar componentes
  - [X] 2.3.7: Testar navegação

- [X] **Tarefa 2.4: Página de Perfil do Usuário**
  - [X] 2.4.1: Criar view `ProfileView`
  - [X] 2.4.2: Criar template `accounts/profile.html`
  - [X] 2.4.3: Exibir informações do usuário
  - [X] 2.4.4: Adicionar botão "Editar Perfil"
  - [X] 2.4.5: Adicionar URL `/profile/`
  - [X] 2.4.6: Adicionar link no navbar
  - [X] 2.4.7: Testar visualização

---

### Sprint 3: Módulo de Performance - Gestão de Atletas
**Duração**: 2 semanas

- [X] **Tarefa 3.1: Modelo de Atleta**
  - [X] 3.1.1: Criar modelo `Athlete` em `performance/models.py`
  - [X] 3.1.2: Adicionar campos básicos
  - [X] 3.1.3: Adicionar campos físicos
  - [X] 3.1.4: Adicionar campos de auditoria
  - [X] 3.1.5: Adicionar campo `created_by`
  - [X] 3.1.6: Criar método `__str__`
  - [X] 3.1.7: Criar método `age`
  - [X] 3.1.8: Criar e aplicar migrações
  - [X] 3.1.9: Registrar no admin

- [X] **Tarefa 3.2: Listagem de Atletas**
  - [X] 3.2.1: Criar view `AthleteListView`
  - [X] 3.2.2: Criar template `athlete_list.html`
  - [X] 3.2.3: Implementar tabela responsiva
  - [X] 3.2.4: Adicionar botão "Adicionar Atleta"
  - [X] 3.2.5: Implementar links de ação
  - [X] 3.2.6: Adicionar paginação
  - [X] 3.2.7: Adicionar busca por nome
  - [X] 3.2.8: Adicionar filtro por posição
  - [X] 3.2.9: Implementar estado vazio
  - [X] 3.2.10: Adicionar URL
  - [X] 3.2.11: Incluir URLs em `core/urls.py`
  - [X] 3.2.12: Testar listagem

- [X] **Tarefa 3.3: Formulário de Cadastro**
  - [X] 3.3.1: Criar `AthleteForm`
  - [X] 3.3.2: Configurar campos
  - [X] 3.3.3: Adicionar validação de data
  - [X] 3.3.4: Adicionar validação de valores
  - [X] 3.3.5: Adicionar classes CSS
  - [X] 3.3.6: Criar view `AthleteCreateView`
  - [X] 3.3.7: Configurar `created_by`
  - [X] 3.3.8: Criar template de formulário
  - [X] 3.3.9: Implementar layout
  - [X] 3.3.10: Adicionar botões
  - [X] 3.3.11: Configurar redirecionamento
  - [X] 3.3.12: Adicionar URL
  - [X] 3.3.13: Testar cadastro

- [X] **Tarefa 3.4: Página de Detalhes**
  - [X] 3.4.1: Criar view `AthleteDetailView`
  - [X] 3.4.2: Criar template de detalhes
  - [X] 3.4.3: Exibir informações em cards
  - [X] 3.4.4: Criar seção "Dados Pessoais"
  - [X] 3.4.5: Criar seção "Dados Físicos"
  - [X] 3.4.6: Adicionar placeholders
  - [X] 3.4.7: Adicionar botões de ação
  - [X] 3.4.8: Adicionar URL
  - [X] 3.4.9: Testar visualização

- [X] **Tarefa 3.5: Edição de Atleta**
  - [X] 3.5.1: Criar view `AthleteUpdateView`
  - [X] 3.5.2: Reutilizar template
  - [X] 3.5.3: Adicionar título de edição
  - [X] 3.5.4: Configurar redirecionamento
  - [X] 3.5.5: Adicionar URL
  - [X] 3.5.6: Testar edição

- [X] **Tarefa 3.6: Exclusão de Atleta**
  - [X] 3.6.1: Criar view `AthleteDeleteView`
  - [X] 3.6.2: Criar template de confirmação
  - [X] 3.6.3: Implementar modal
  - [X] 3.6.4: Adicionar botões
  - [X] 3.6.5: Configurar redirecionamento
  - [X] 3.6.6: Adicionar URL
  - [X] 3.6.7: Testar exclusão

- [X] **Tarefa 3.7: Integração com Menu**
  - [X] 3.7.1: Adicionar item "Performance"
  - [X] 3.7.2: Criar submenu
  - [X] 3.7.3: Atualizar lógica de highlight
  - [X] 3.7.4: Testar navegação

---

### Sprint 4: Módulo de Performance - Treinos e Cargas
**Duração**: 2 semanas

- [X] **Tarefa 4.1: Modelo de Carga de Treinamento**
  - [X] 4.1.1: Criar modelo `TrainingLoad` em `performance/models.py`
  - [X] 4.1.2: Adicionar ForeignKey para `Athlete`
  - [X] 4.1.3: Adicionar campo `training_date` (DateField)
  - [X] 4.1.4: Adicionar campo `duration_minutes` (PositiveIntegerField)
  - [X] 4.1.5: Adicionar campo `distance_km` (DecimalField)
  - [X] 4.1.6: Adicionar campo `heart_rate_avg` (PositiveIntegerField, opcional)
  - [X] 4.1.7: Adicionar campo `heart_rate_max` (PositiveIntegerField, opcional)
  - [X] 4.1.8: Adicionar choices para `intensity_level` (BAIXA, MEDIA, ALTA, MAXIMA)
  - [X] 4.1.9: Adicionar campos `created_at` e `updated_at`
  - [X] 4.1.10: Adicionar campo `created_by`
  - [X] 4.1.11: Criar método `__str__`
  - [X] 4.1.12: Criar método `fatigue_index()` para cálculo de fadiga
  - [X] 4.1.13: Configurar Meta (verbose_name, ordering)
  - [X] 4.1.14: Criar e aplicar migrações
  - [X] 4.1.15: Registrar no admin

- [X] **Tarefa 4.2: Formulário de Carga de Treinamento**
  - [X] 4.2.1: Criar `TrainingLoadForm` em `performance/forms.py`
  - [X] 4.2.2: Configurar campos do formulário
  - [X] 4.2.3: Adicionar widget DateInput com type='date'
  - [X] 4.2.4: Adicionar validação: data não pode ser futura
  - [X] 4.2.5: Adicionar validação: duration_minutes > 0
  - [X] 4.2.6: Adicionar validação: distance_km >= 0
  - [X] 4.2.7: Adicionar validação: heart_rate_avg <= heart_rate_max
  - [X] 4.2.8: Adicionar classes CSS aos widgets
  - [X] 4.2.9: Configurar help_text para campos
  - [X] 4.2.10: Testar validações

- [X] **Tarefa 4.3: Listagem de Cargas de Treinamento**
  - [X] 4.3.1: Criar view `TrainingLoadListView`
  - [X] 4.3.2: Configurar filtro por atleta
  - [X] 4.3.3: Adicionar ordenação por data (mais recente primeiro)
  - [X] 4.3.4: Criar template `training_load_list.html`
  - [X] 4.3.5: Implementar tabela responsiva
  - [X] 4.3.6: Exibir nome do atleta com link
  - [X] 4.3.7: Exibir data, duração e distância
  - [X] 4.3.8: Exibir nível de intensidade com badge colorido
  - [X] 4.3.9: Adicionar botão "Adicionar Carga"
  - [X] 4.3.10: Implementar filtro por período (última semana, mês, etc)
  - [X] 4.3.11: Adicionar paginação
  - [X] 4.3.12: Adicionar URL `/performance/training-loads/`
  - [X] 4.3.13: Testar listagem

- [X] **Tarefa 4.4: Cadastro de Carga de Treinamento**
  - [X] 4.4.1: Criar view `TrainingLoadCreateView`
  - [X] 4.4.2: Configurar formulário
  - [X] 4.4.3: Configurar `created_by` automaticamente
  - [X] 4.4.4: Criar template `training_load_form.html`
  - [X] 4.4.5: Implementar layout do formulário
  - [X] 4.4.6: Adicionar seletor de atleta
  - [X] 4.4.7: Adicionar campos de frequência cardíaca
  - [X] 4.4.8: Implementar mensagens de sucesso
  - [X] 4.4.9: Configurar redirecionamento
  - [X] 4.4.10: Adicionar URL `/performance/training-loads/add/`
  - [X] 4.4.11: Testar cadastro

- [X] **Tarefa 4.5: Edição e Exclusão de Cargas**
  - [X] 4.5.1: Criar view `TrainingLoadUpdateView`
  - [X] 4.5.2: Reutilizar template de formulário
  - [X] 4.5.3: Adicionar URL de edição
  - [X] 4.5.4: Criar view `TrainingLoadDeleteView`
  - [X] 4.5.5: Criar template de confirmação
  - [X] 4.5.6: Adicionar URL de exclusão
  - [X] 4.5.7: Testar edição e exclusão

- [X] **Tarefa 4.6: Visualização de Cargas por Atleta**
  - [X] 4.6.1: Adicionar aba "Cargas de Treino" na página de detalhes do atleta
  - [X] 4.6.2: Listar últimas 10 cargas
  - [X] 4.6.3: Exibir gráfico de barras de intensidade (opcional)
  - [X] 4.6.4: Calcular e exibir média de duração
  - [X] 4.6.5: Calcular e exibir distância total
  - [X] 4.6.6: Adicionar botão "Ver todas as cargas"
  - [X] 4.6.7: Testar visualização

---

### Sprint 5: Módulo de Performance - Lesões e Dashboard
**Duração**: 2 semanas

- [X] **Tarefa 5.1: Modelo de Registro de Lesão**
  - [X] 5.1.1: Criar modelo `InjuryRecord` em `performance/models.py`
  - [X] 5.1.2: Adicionar ForeignKey para `Athlete`
  - [X] 5.1.3: Adicionar campo `injury_date` (DateField)
  - [X] 5.1.4: Adicionar choices para `injury_type` (MUSCULAR, ARTICULAR, OSSEA, etc)
  - [X] 5.1.5: Adicionar choices para `body_part` (JOELHO, TORNOZELO, COXA, etc)
  - [X] 5.1.6: Adicionar choices para `severity_level` (LEVE, MODERADA, GRAVE)
  - [X] 5.1.7: Adicionar campo `description` (TextField, opcional)
  - [X] 5.1.8: Adicionar campo `expected_return` (DateField, opcional)
  - [X] 5.1.9: Adicionar campo `actual_return` (DateField, opcional)
  - [X] 5.1.10: Adicionar campos de auditoria
  - [X] 5.1.11: Adicionar campo `created_by`
  - [X] 5.1.12: Criar método `__str__`
  - [X] 5.1.13: Criar método `days_out()` para calcular tempo afastado
  - [X] 5.1.14: Configurar Meta
  - [X] 5.1.15: Criar e aplicar migrações
  - [X] 5.1.16: Registrar no admin

- [X] **Tarefa 5.2: CRUD de Lesões**
  - [X] 5.2.1: Criar `InjuryRecordForm`
  - [X] 5.2.2: Configurar validações de datas
  - [X] 5.2.3: Adicionar classes CSS
  - [X] 5.2.4: Criar view `InjuryRecordListView`
  - [X] 5.2.5: Criar template de listagem
  - [X] 5.2.6: Implementar filtro por atleta
  - [X] 5.2.7: Implementar filtro por gravidade
  - [X] 5.2.8: Criar view `InjuryRecordCreateView`
  - [X] 5.2.9: Criar template de formulário
  - [X] 5.2.10: Criar views de edição e exclusão
  - [X] 5.2.11: Adicionar URLs
  - [X] 5.2.12: Testar CRUD completo

- [X] **Tarefa 5.3: Dashboard de Performance**
  - [X] 5.3.1: Criar view `PerformanceDashboardView`
  - [X] 5.3.2: Calcular total de atletas
  - [X] 5.3.3: Calcular atletas ativos vs lesionados
  - [X] 5.3.4: Calcular média de idade
  - [X] 5.3.5: Buscar últimas cargas de treino
  - [X] 5.3.6: Buscar lesões recentes
  - [X] 5.3.7: Criar template `performance_dashboard.html`
  - [X] 5.3.8: Implementar cards de estatísticas
  - [X] 5.3.9: Criar seção "Alertas" (atletas com carga excessiva)
  - [X] 5.3.10: Criar tabela de últimas atividades
  - [X] 5.3.11: Adicionar URL `/performance/dashboard/`
  - [X] 5.3.12: Atualizar menu de navegação
  - [X] 5.3.13: Testar dashboard

- [X] **Tarefa 5.4: Integração de Lesões na Página do Atleta**
  - [X] 5.4.1: Adicionar aba "Histórico de Lesões"
  - [X] 5.4.2: Listar lesões do atleta
  - [X] 5.4.3: Exibir status (recuperado ou em recuperação)
  - [X] 5.4.4: Calcular total de dias afastado
  - [X] 5.4.5: Adicionar indicador visual de atleta lesionado
  - [X] 5.4.6: Testar visualização

---

### Sprint 6: Módulo de Scouting - Jogadores Observados
**Duração**: 2 semanas

- [X] Sprint 6 concluída

- [X] **Tarefa 6.1: Modelo de Jogador Observado**
  - [X] 6.1.1: Criar modelo `ScoutedPlayer` em `scouting/models.py`
  - [X] 6.1.2: Adicionar campo `name` (CharField)
  - [X] 6.1.3: Adicionar campo `birth_date` (DateField)
  - [X] 6.1.4: Adicionar campo `nationality` (CharField)
  - [X] 6.1.5: Adicionar choices para `position`
  - [X] 6.1.6: Adicionar campo `current_club` (CharField)
  - [X] 6.1.7: Adicionar campo `market_value` (DecimalField, opcional)
  - [X] 6.1.8: Adicionar campo `notes` (TextField)
  - [X] 6.1.9: Adicionar choices para `status` (MONITORANDO, INTERESSADO, NEGOCIANDO)
  - [X] 6.1.10: Adicionar campo `photo` (ImageField, opcional)
  - [X] 6.1.11: Adicionar campos de auditoria
  - [X] 6.1.12: Adicionar campo `created_by`
  - [X] 6.1.13: Criar método `age()`
  - [X] 6.1.14: Criar método `__str__`
  - [X] 6.1.15: Configurar Meta
  - [X] 6.1.16: Criar e aplicar migrações
  - [X] 6.1.17: Registrar no admin

- [X] **Tarefa 6.2: CRUD de Jogadores Observados**
  - [X] 6.2.1: Criar `ScoutedPlayerForm`
  - [X] 6.2.2: Configurar campos e validações
  - [X] 6.2.3: Adicionar classes CSS
  - [X] 6.2.4: Criar view `ScoutedPlayerListView`
  - [X] 6.2.5: Criar template de listagem
  - [X] 6.2.6: Implementar busca por nome e clube
  - [X] 6.2.7: Implementar filtro por posição
  - [X] 6.2.8: Implementar filtro por status
  - [X] 6.2.9: Adicionar ordenação por valor de mercado
  - [X] 6.2.10: Criar view `ScoutedPlayerCreateView`
  - [X] 6.2.11: Criar template de formulário
  - [X] 6.2.12: Implementar upload de foto
  - [X] 6.2.13: Criar view `ScoutedPlayerDetailView`
  - [X] 6.2.14: Criar template de detalhes
  - [X] 6.2.15: Criar views de edição e exclusão
  - [X] 6.2.16: Adicionar URLs em `scouting/urls.py`
  - [X] 6.2.17: Incluir URLs em `core/urls.py`
  - [X] 6.2.18: Testar CRUD completo

- [X] **Tarefa 6.3: Integração com Menu**
  - [X] 6.3.1: Adicionar item "Scouting" no menu
  - [X] 6.3.2: Criar submenu "Jogadores Observados"
  - [X] 6.3.3: Atualizar lógica de highlight
  - [X] 6.3.4: Testar navegação

---

### Sprint 7: Módulo de Scouting - Relatórios de Observação
**Duração**: 2 semanas

- [X] **Tarefa 7.1: Modelo de Relatório de Scouting**
  - [X] 7.1.1: Criar modelo `ScoutingReport` em `scouting/models.py`
  - [X] 7.1.2: Adicionar ForeignKey para `ScoutedPlayer`
  - [X] 7.1.3: Adicionar ForeignKey para `User` (scout que criou)
  - [X] 7.1.4: Adicionar campo `report_date` (DateField)
  - [X] 7.1.5: Adicionar campo `match_or_event` (CharField)
  - [X] 7.1.6: Adicionar campo `technical_score` (IntegerField, 0-10)
  - [X] 7.1.7: Adicionar campo `physical_score` (IntegerField, 0-10)
  - [X] 7.1.8: Adicionar campo `tactical_score` (IntegerField, 0-10)
  - [X] 7.1.9: Adicionar campo `mental_score` (IntegerField, 0-10)
  - [X] 7.1.10: Adicionar campo `potential_score` (IntegerField, 0-10)
  - [X] 7.1.11: Adicionar campo `strengths` (TextField)
  - [X] 7.1.12: Adicionar campo `weaknesses` (TextField)
  - [X] 7.1.13: Adicionar campo `recommendation` (TextField)
  - [X] 7.1.14: Adicionar campos de auditoria
  - [X] 7.1.15: Criar método `overall_score()` (média dos scores)
  - [X] 7.1.16: Criar método `__str__`
  - [X] 7.1.17: Configurar Meta
  - [X] 7.1.18: Criar e aplicar migrações
  - [X] 7.1.19: Registrar no admin

- [X] **Tarefa 7.2: CRUD de Relatórios**
  - [X] 7.2.1: Criar `ScoutingReportForm`
  - [X] 7.2.2: Adicionar validação: scores entre 0 e 10
  - [X] 7.2.3: Adicionar classes CSS
  - [X] 7.2.4: Criar view `ScoutingReportListView`
  - [X] 7.2.5: Criar template de listagem
  - [X] 7.2.6: Implementar filtro por jogador
  - [X] 7.2.7: Implementar filtro por scout
  - [X] 7.2.8: Criar view `ScoutingReportCreateView`
  - [X] 7.2.9: Criar template de formulário
  - [X] 7.2.10: Implementar seção de scores com sliders
  - [X] 7.2.11: Criar view `ScoutingReportDetailView`
  - [X] 7.2.12: Criar template de detalhes
  - [X] 7.2.13: Exibir gráfico radar dos scores
  - [X] 7.2.14: Criar views de edição e exclusão
  - [X] 7.2.15: Adicionar URLs
  - [X] 7.2.16: Testar CRUD completo

- [X] **Tarefa 7.3: Integração de Relatórios na Página do Jogador**
  - [X] 7.3.1: Adicionar aba "Relatórios" na página de detalhes
  - [X] 7.3.2: Listar relatórios do jogador
  - [X] 7.3.3: Calcular média geral dos scores
  - [X] 7.3.4: Exibir evolução dos scores (se múltiplos relatórios)
  - [X] 7.3.5: Adicionar botão "Novo Relatório"
  - [X] 7.3.6: Testar visualização

- [X] **Tarefa 7.4: Dashboard de Scouting**
  - [X] 7.4.1: Criar view `ScoutingDashboardView`
  - [X] 7.4.2: Calcular total de jogadores observados
  - [X] 7.4.3: Calcular jogadores por status
  - [X] 7.4.4: Buscar top 5 jogadores por overall_score
  - [X] 7.4.5: Criar template do dashboard
  - [X] 7.4.6: Implementar cards de estatísticas
  - [X] 7.4.7: Criar seção de recomendações prioritárias
  - [X] 7.4.8: Adicionar URL `/scouting/dashboard/`
  - [X] 7.4.9: Atualizar menu
  - [X] 7.4.10: Testar dashboard

---

### Sprint 8: Módulo de Scouting - Comparação de Jogadores
**Duração**: 1 semana

- [X] **Tarefa 8.1: Funcionalidade de Comparação**
  - [X] 8.1.1: Criar view `PlayerComparisonView`
  - [X] 8.1.2: Adicionar parâmetros para receber IDs de jogadores
  - [X] 8.1.3: Validar: máximo 3 jogadores para comparar
  - [X] 8.1.4: Buscar dados dos jogadores
  - [X] 8.1.5: Buscar última avaliação de cada jogador
  - [X] 8.1.6: Criar template `player_comparison.html`
  - [X] 8.1.7: Implementar tabela comparativa lado a lado
  - [X] 8.1.8: Exibir dados pessoais
  - [X] 8.1.9: Exibir scores técnicos
  - [X] 8.1.10: Criar gráfico radar comparativo
  - [X] 8.1.11: Destacar melhor jogador em cada métrica
  - [X] 8.1.12: Adicionar URL `/scouting/compare/`
  - [X] 8.1.13: Testar comparação

- [X] **Tarefa 8.2: Interface de Seleção**
  - [X] 8.2.1: Adicionar checkboxes na listagem de jogadores
  - [X] 8.2.2: Adicionar botão "Comparar Selecionados"
  - [X] 8.2.3: Implementar JavaScript para validação
  - [X] 8.2.4: Implementar envio via GET para página de comparação
  - [X] 8.2.5: Testar seleção e redirecionamento

- [X] Sprint 8 concluída

---

### Sprint 9: Módulo de Business - Gestão de Clubes
**Duração**: 1 semana

- [ ] **Tarefa 9.1: Modelo de Clube**
  - [ ] 9.1.1: Criar modelo `Club` em `business/models.py`
  - [ ] 9.1.2: Adicionar campo `name` (CharField, único)
  - [ ] 9.1.3: Adicionar campo `country` (CharField)
  - [ ] 9.1.4: Adicionar campo `city` (CharField)
  - [ ] 9.1.5: Adicionar choices para `division` (PRIMEIRA, SEGUNDA, etc)
  - [ ] 9.1.6: Adicionar campo `logo` (ImageField, opcional)
  - [ ] 9.1.7: Adicionar campos de auditoria
  - [ ] 9.1.8: Adicionar campo `created_by`
  - [ ] 9.1.9: Criar método `__str__`
  - [ ] 9.1.10: Configurar Meta
  - [ ] 9.1.11: Criar e aplicar migrações
  - [ ] 9.1.12: Registrar no admin

- [ ] **Tarefa 9.2: CRUD de Clubes**
  - [ ] 9.2.1: Criar `ClubForm`
  - [ ] 9.2.2: Configurar campos e validações
  - [ ] 9.2.3: Adicionar classes CSS
  - [ ] 9.2.4: Criar view `ClubListView`
  - [ ] 9.2.5: Criar template de listagem
  - [ ] 9.2.6: Implementar busca por nome e país
  - [ ] 9.2.7: Implementar filtro por divisão
  - [ ] 9.2.8: Criar view `ClubCreateView`
  - [ ] 9.2.9: Criar template de formulário
  - [ ] 9.2.10: Criar view `ClubDetailView`
  - [ ] 9.2.11: Criar template de detalhes
  - [ ] 9.2.12: Criar views de edição e exclusão
  - [ ] 9.2.13: Adicionar URLs em `business/urls.py`
  - [ ] 9.2.14: Incluir URLs em `core/urls.py`
  - [ ] 9.2.15: Testar CRUD completo

- [ ] **Tarefa 9.3: Integração com Menu**
  - [ ] 9.3.1: Adicionar item "Business" no menu
  - [ ] 9.3.2: Criar submenu "Clubes"
  - [ ] 9.3.3: Atualizar lógica de highlight
  - [ ] 9.3.4: Testar navegação

---

### Sprint 10: Módulo de Business - Registros Financeiros e Receitas
**Duração**: 2 semanas

- [ ] **Tarefa 10.1: Modelo de Registro Financeiro**
  - [ ] 10.1.1: Criar modelo `FinancialRecord` em `business/models.py`
  - [ ] 10.1.2: Adicionar ForeignKey para `Club`
  - [ ] 10.1.3: Adicionar campo `record_date` (DateField)
  - [ ] 10.1.4: Adicionar choices para `category` (SALARIOS, TRANSFERENCIAS, etc)
  - [ ] 10.1.5: Adicionar campo `amount` (DecimalField)
  - [ ] 10.1.6: Adicionar choices para `transaction_type` (RECEITA, DESPESA)
  - [ ] 10.1.7: Adicionar campo `description` (TextField)
  - [ ] 10.1.8: Adicionar campos de auditoria
  - [ ] 10.1.9: Adicionar campo `created_by`
  - [ ] 10.1.10: Criar método `__str__`
  - [ ] 10.1.11: Configurar Meta
  - [ ] 10.1.12: Criar e aplicar migrações
  - [ ] 10.1.13: Registrar no admin

- [ ] **Tarefa 10.2: CRUD de Registros Financeiros**
  - [ ] 10.2.1: Criar `FinancialRecordForm`
  - [ ] 10.2.2: Configurar validações
  - [ ] 10.2.3: Adicionar classes CSS
  - [ ] 10.2.4: Criar view `FinancialRecordListView`
  - [ ] 10.2.5: Criar template de listagem
  - [ ] 10.2.6: Implementar filtro por clube
  - [ ] 10.2.7: Implementar filtro por tipo de transação
  - [ ] 10.2.8: Implementar filtro por período
  - [ ] 10.2.9: Calcular totais de receitas e despesas
  - [ ] 10.2.10: Criar view `FinancialRecordCreateView`
  - [ ] 10.2.11: Criar template de formulário
  - [ ] 10.2.12: Criar views de edição e exclusão
  - [ ] 10.2.13: Adicionar URLs
  - [ ] 10.2.14: Testar CRUD completo

- [ ] **Tarefa 10.3: Modelo de Receita Mensal**
  - [ ] 10.3.1: Criar modelo `Revenue` em `business/models.py`
  - [ ] 10.3.2: Adicionar ForeignKey para `Club`
  - [ ] 10.3.3: Adicionar campo `year` (PositiveIntegerField)
  - [ ] 10.3.4: Adicionar campo `month` (PositiveIntegerField, 1-12)
  - [ ] 10.3.5: Adicionar campo `ticketing` (DecimalField)
  - [ ] 10.3.6: Adicionar campo `sponsorship` (DecimalField)
  - [ ] 10.3.7: Adicionar campo `broadcasting` (DecimalField)
  - [ ] 10.3.8: Adicionar campo `merchandising` (DecimalField)
  - [ ] 10.3.9: Adicionar campos de auditoria
  - [ ] 10.3.10: Criar método `total_revenue()`
  - [ ] 10.3.11: Criar método `__str__`
  - [ ] 10.3.12: Configurar Meta com unique_together (club, year, month)
  - [ ] 10.3.13: Criar e aplicar migrações
  - [ ] 10.3.14: Registrar no admin

- [ ] **Tarefa 10.4: CRUD de Receitas**
  - [ ] 10.4.1: Criar `RevenueForm`
  - [ ] 10.4.2: Configurar validações
  - [ ] 10.4.3: Criar view `RevenueListView`
  - [ ] 10.4.4: Criar template de listagem
  - [ ] 10.4.5: Implementar filtro por clube e ano
  - [ ] 10.4.6: Exibir total mensal
  - [ ] 10.4.7: Criar view `RevenueCreateView`
  - [ ] 10.4.8: Criar template de formulário
  - [ ] 10.4.9: Criar views de edição e exclusão
  - [ ] 10.4.10: Adicionar URLs
  - [ ] 10.4.11: Testar CRUD completo

- [ ] **Tarefa 10.5: Dashboard Financeiro**
  - [ ] 10.5.1: Criar view `FinancialDashboardView`
  - [ ] 10.5.2: Calcular receitas totais por clube
  - [ ] 10.5.3: Calcular despesas totais por clube
  - [ ] 10.5.4: Calcular saldo (receitas - despesas)
  - [ ] 10.5.5: Buscar receitas dos últimos 12 meses
  - [ ] 10.5.6: Criar template do dashboard
  - [ ] 10.5.7: Implementar gráfico de barras de receitas mensais
  - [ ] 10.5.8: Implementar gráfico de pizza por categoria
  - [ ] 10.5.9: Adicionar cards de resumo
  - [ ] 10.5.10: Adicionar URL `/business/dashboard/`
  - [ ] 10.5.11: Atualizar menu
  - [ ] 10.5.12: Testar dashboard

---

### Sprint 11: Integração entre Módulos
**Duração**: 1 semana

- [ ] **Tarefa 11.1: Integração Performance → Business**
  - [ ] 11.1.1: Adicionar campo `market_value` no modelo `Athlete`
  - [ ] 11.1.2: Criar migração para adicionar o campo
  - [ ] 11.1.3: Atualizar formulário de atleta
  - [ ] 11.1.4: Exibir valor de mercado na página de detalhes
  - [ ] 11.1.5: Criar view `AthleteValuationView`
  - [ ] 11.1.6: Calcular valor total do elenco
  - [ ] 11.1.7: Criar template de valorização
  - [ ] 11.1.8: Adicionar URL `/performance/valuation/`
  - [ ] 11.1.9: Adicionar item no menu
  - [ ] 11.1.10: Testar integração

- [ ] **Tarefa 11.2: Integração Scouting → Performance**
  - [ ] 11.2.1: Criar funcionalidade "Contratar Jogador"
  - [ ] 11.2.2: Adicionar botão na página de detalhes do jogador observado
  - [ ] 11.2.3: Criar view `ConvertToAthleteView`
  - [ ] 11.2.4: Copiar dados do ScoutedPlayer para Athlete
  - [ ] 11.2.5: Marcar ScoutedPlayer como "CONTRATADO"
  - [ ] 11.2.6: Adicionar URL
  - [ ] 11.2.7: Implementar mensagem de confirmação
  - [ ] 11.2.8: Testar conversão

- [ ] **Tarefa 11.3: Dashboard Principal Unificado**
  - [ ] 11.3.1: Atualizar `DashboardView`
  - [ ] 11.3.2: Adicionar widget de performance
  - [ ] 11.3.3: Adicionar widget de scouting
  - [ ] 11.3.4: Adicionar widget de business
  - [ ] 11.3.5: Criar seção "Atividades Recentes"
  - [ ] 11.3.6: Listar últimos atletas cadastrados
  - [ ] 11.3.7: Listar últimas lesões
  - [ ] 11.3.8: Listar últimos relatórios de scouting
  - [ ] 11.3.9: Implementar layout responsivo
  - [ ] 11.3.10: Testar dashboard unificado

---

### Sprint 12: Recursos Adicionais e Melhorias
**Duração**: 2 semanas

- [ ] **Tarefa 12.1: Sistema de Notificações**
  - [ ] 12.1.1: Instalar pacote `django-notifications-hq`
  - [ ] 12.1.2: Adicionar ao INSTALLED_APPS
  - [ ] 12.1.3: Executar migrações
  - [ ] 12.1.4: Criar notificação ao cadastrar lesão
  - [ ] 12.1.5: Criar notificação ao completar relatório de scouting
  - [ ] 12.1.6: Criar view `NotificationListView`
  - [ ] 12.1.7: Criar template de notificações
  - [ ] 12.1.8: Adicionar ícone de notificações no navbar
  - [ ] 12.1.9: Implementar badge com contador
  - [ ] 12.1.10: Adicionar URL `/notifications/`
  - [ ] 12.1.11: Testar notificações

- [ ] **Tarefa 12.2: Exportação de Dados**
  - [ ] 12.2.1: Instalar pacote `openpyxl` para Excel
  - [ ] 12.2.2: Criar view `ExportAthletesView`
  - [ ] 12.2.3: Gerar arquivo Excel com dados de atletas
  - [ ] 12.2.4: Adicionar botão "Exportar" na listagem
  - [ ] 12.2.5: Criar view `ExportTrainingLoadsView`
  - [ ] 12.2.6: Criar view `ExportScoutingReportsView`
  - [ ] 12.2.7: Adicionar URLs de exportação
  - [ ] 12.2.8: Testar downloads

- [ ] **Tarefa 12.3: Busca Global**
  - [ ] 12.3.1: Criar view `GlobalSearchView`
  - [ ] 12.3.2: Implementar busca em múltiplos modelos
  - [ ] 12.3.3: Criar template de resultados
  - [ ] 12.3.4: Adicionar campo de busca no navbar
  - [ ] 12.3.5: Implementar AJAX para busca dinâmica
  - [ ] 12.3.6: Adicionar URL `/search/`
  - [ ] 12.3.7: Testar busca

- [ ] **Tarefa 12.4: Logs de Auditoria**
  - [ ] 12.4.1: Instalar pacote `django-auditlog`
  - [ ] 12.4.2: Adicionar ao INSTALLED_APPS
  - [ ] 12.4.3: Executar migrações
  - [ ] 12.4.4: Registrar modelos principais
  - [ ] 12.4.5: Criar view `AuditLogListView`
  - [ ] 12.4.6: Criar template de logs
  - [ ] 12.4.7: Implementar filtros
  - [ ] 12.4.8: Adicionar URL `/audit-logs/`
  - [ ] 12.4.9: Restringir acesso a administradores
  - [ ] 12.4.10: Testar logs

- [ ] **Tarefa 12.5: Melhorias de UX**
  - [ ] 12.5.1: Implementar loading spinners
  - [ ] 12.5.2: Adicionar animações de transição
  - [ ] 12.5.3: Implementar confirmações de exclusão com modal
  - [ ] 12.5.4: Adicionar tooltips em campos
  - [ ] 12.5.5: Implementar mensagens toast
  - [ ] 12.5.6: Melhorar feedback visual de formulários
  - [ ] 12.5.7: Adicionar dark mode toggle (opcional)
  - [ ] 12.5.8: Testar em múltiplos navegadores

---

### Sprint 13: Modelos Preditivos com IA
**Duração**: 2 semanas

- [X] **Tarefa 13.1: Configuração do Ambiente ML**
  - [X] 13.1.1: Adicionar scikit-learn ao requirements.txt
  - [X] 13.1.2: Adicionar pandas ao requirements.txt
  - [X] 13.1.3: Adicionar numpy ao requirements.txt
  - [X] 13.1.4: Instalar dependências
  - [X] 13.1.5: Criar diretório `ml_models/`
  - [X] 13.1.6: Criar arquivo `ml_models/__init__.py`

- [X] **Tarefa 13.2: Modelo de Predição de Lesões**
  - [X] 13.2.1: Criar script `ml_models/injury_predictor.py`
  - [X] 13.2.2: Importar bibliotecas necessárias
  - [X] 13.2.3: Criar função para buscar dados de treinamento
  - [X] 13.2.4: Preparar features (duração, distância, frequência)
  - [X] 13.2.5: Criar labels (lesionado ou não)
  - [X] 13.2.6: Implementar RandomForestClassifier
  - [X] 13.2.7: Treinar modelo com dados históricos
  - [X] 13.2.8: Criar função de predição
  - [X] 13.2.9: Calcular score de confiança
  - [X] 13.2.10: Salvar modelo treinado

- [X] **Tarefa 13.3: Integração da Predição de Lesões**
  - [X] 13.3.1: Criar management command para treinar modelo
  - [X] 13.3.2: Criar view `InjuryRiskView`
  - [X] 13.3.3: Calcular risco para cada atleta
  - [X] 13.3.4: Criar template de visualização
  - [X] 13.3.5: Exibir score de risco (0-100%)
  - [X] 13.3.6: Adicionar alertas para alto risco
  - [X] 13.3.7: Criar gráfico de fatores de risco
  - [X] 13.3.8: Adicionar URL `/performance/injury-risk/`
  - [X] 13.3.9: Adicionar item no menu
  - [X] 13.3.10: Testar predições

- [X] **Tarefa 13.4: Modelo de Avaliação de Potencial**
  - [X] 13.4.1: Criar script `ml_models/potential_evaluator.py`
  - [X] 13.4.2: Buscar dados de scouting reports
  - [X] 13.4.3: Preparar features (scores técnicos)
  - [X] 13.4.4: Implementar modelo de regressão
  - [X] 13.4.5: Treinar modelo
  - [X] 13.4.6: Criar função de predição de potencial
  - [X] 13.4.7: Integrar na página de jogador observado
  - [X] 13.4.8: Exibir "Potencial Estimado"
  - [X] 13.4.9: Testar avaliações

- [ ] **Tarefa 13.5: Modelo de Previsão de Receitas**
  - [ ] 13.5.1: Criar script `ml_models/revenue_forecaster.py`
  - [ ] 13.5.2: Buscar dados históricos de receitas
  - [ ] 13.5.3: Preparar série temporal
  - [ ] 13.5.4: Implementar LinearRegression
  - [ ] 13.5.5: Treinar modelo
  - [ ] 13.5.6: Criar função de previsão
  - [ ] 13.5.7: Criar view `RevenueForecastView`
  - [ ] 13.5.8: Criar template de visualização
  - [ ] 13.5.9: Exibir previsão para próximos 6 meses
  - [ ] 13.5.10: Criar gráfico de tendência
  - [ ] 13.5.11: Adicionar URL `/business/forecast/`
  - [ ] 13.5.12: Testar previsões

---

### Sprint 14: Testes e Garantia de Qualidade
**Duração**: 2 semanas

- [ ] **Tarefa 14.1: Testes Unitários - Accounts**
  - [ ] 14.1.1: Criar arquivo `accounts/tests/test_models.py`
  - [ ] 14.1.2: Testar criação de CustomUser
  - [ ] 14.1.3: Testar validação de email único
  - [ ] 14.1.4: Criar arquivo `accounts/tests/test_views.py`
  - [ ] 14.1.5: Testar view de signup
  - [ ] 14.1.6: Testar view de login
  - [ ] 14.1.7: Testar view de logout
  - [ ] 14.1.8: Criar arquivo `accounts/tests/test_forms.py`
  - [ ] 14.1.9: Testar validações de formulários
  - [ ] 14.1.10: Executar testes: `python manage.py test accounts`

- [ ] **Tarefa 14.2: Testes Unitários - Performance**
  - [ ] 14.2.1: Criar arquivo `performance/tests/test_models.py`
  - [ ] 14.2.2: Testar modelo Athlete
  - [ ] 14.2.3: Testar método age()
  - [ ] 14.2.4: Testar modelo TrainingLoad
  - [ ] 14.2.5: Testar método fatigue_index()
  - [ ] 14.2.6: Testar modelo InjuryRecord
  - [ ] 14.2.7: Testar método days_out()
  - [ ] 14.2.8: Criar arquivo `performance/tests/test_views.py`
  - [ ] 14.2.9: Testar CRUD de atletas
  - [ ] 14.2.10: Testar CRUD de cargas
  - [ ] 14.2.11: Testar CRUD de lesões
  - [ ] 14.2.12: Criar arquivo `performance/tests/test_forms.py`
  - [ ] 14.2.13: Testar validações
  - [ ] 14.2.14: Executar testes: `python manage.py test performance`

- [ ] **Tarefa 14.3: Testes Unitários - Scouting**
  - [ ] 14.3.1: Criar arquivo `scouting/tests/test_models.py`
  - [ ] 14.3.2: Testar modelo ScoutedPlayer
  - [ ] 14.3.3: Testar modelo ScoutingReport
  - [ ] 14.3.4: Testar método overall_score()
  - [ ] 14.3.5: Criar arquivo `scouting/tests/test_views.py`
  - [ ] 14.3.6: Testar CRUD de jogadores
  - [ ] 14.3.7: Testar CRUD de relatórios
  - [ ] 14.3.8: Testar comparação de jogadores
  - [ ] 14.3.9: Executar testes: `python manage.py test scouting`

- [ ] **Tarefa 14.4: Testes Unitários - Business**
  - [ ] 14.4.1: Criar arquivo `business/tests/test_models.py`
  - [ ] 14.4.2: Testar modelo Club
  - [ ] 14.4.3: Testar modelo FinancialRecord
  - [ ] 14.4.4: Testar modelo Revenue
  - [ ] 14.4.5: Testar método total_revenue()
  - [ ] 14.4.6: Criar arquivo `business/tests/test_views.py`
  - [ ] 14.4.7: Testar CRUD de clubes
  - [ ] 14.4.8: Testar CRUD de registros financeiros
  - [ ] 14.4.9: Testar CRUD de receitas
  - [ ] 14.4.10: Executar testes: `python manage.py test business`

- [ ] **Tarefa 14.5: Testes de Integração**
  - [ ] 14.5.1: Criar arquivo `core/tests/test_integration.py`
  - [ ] 14.5.2: Testar fluxo completo de autenticação
  - [ ] 14.5.3: Testar fluxo de cadastro de atleta
  - [ ] 14.5.4: Testar fluxo de adição de carga de treino
  - [ ] 14.5.5: Testar fluxo de scouting completo
  - [ ] 14.5.6: Testar integração entre módulos
  - [ ] 14.5.7: Executar todos os testes: `python manage.py test`

- [ ] **Tarefa 14.6: Testes de Performance**
  - [ ] 14.6.1: Instalar django-debug-toolbar
  - [ ] 14.6.2: Configurar toolbar
  - [ ] 14.6.3: Analisar queries N+1
  - [ ] 14.6.4: Otimizar queries com select_related
  - [ ] 14.6.5: Otimizar queries com prefetch_related
  - [ ] 14.6.6: Adicionar índices no banco de dados
  - [ ] 14.6.7: Testar tempo de carregamento das páginas
  - [ ] 14.6.8: Meta: todas as páginas < 500ms

- [ ] **Tarefa 14.7: Cobertura de Testes**
  - [ ] 14.7.1: Instalar coverage
  - [ ] 14.7.2: Executar: `coverage run manage.py test`
  - [ ] 14.7.3: Gerar relatório: `coverage report`
  - [ ] 14.7.4: Gerar HTML: `coverage html`
  - [ ] 14.7.5: Analisar áreas não cobertas
  - [ ] 14.7.6: Adicionar testes faltantes
  - [ ] 14.7.7: Meta: cobertura > 80%

---

### Sprint 15: Polimento e Documentação
**Duração**: 1 semana

- [ ] **Tarefa 15.1: Revisão de Código**
  - [ ] 15.1.1: Executar flake8 para verificar PEP 8
  - [ ] 15.1.2: Corrigir warnings de estilo
  - [ ] 15.1.3: Executar pylint
  - [ ] 15.1.4: Corrigir problemas críticos
  - [ ] 15.1.5: Revisar imports não utilizados
  - [ ] 15.1.6: Revisar variáveis não utilizadas
  - [ ] 15.1.7: Verificar consistência de nomenclatura
  - [ ] 15.1.8: Verificar uso de single quotes

- [ ] **Tarefa 15.2: Segurança**
  - [ ] 15.2.1: Executar `python manage.py check --deploy`
  - [ ] 15.2.2: Revisar configurações de produção
  - [ ] 15.2.3: Configurar ALLOWED_HOSTS
  - [ ] 15.2.4: Configurar SECRET_KEY via variável de ambiente
  - [ ] 15.2.5: Configurar CSRF_TRUSTED_ORIGINS
  - [ ] 15.2.6: Configurar SECURE_SSL_REDIRECT
  - [ ] 15.2.7: Configurar SECURE_HSTS_SECONDS
  - [ ] 15.2.8: Revisar permissões de acesso
  - [ ] 15.2.9: Implementar rate limiting (opcional)

- [ ] **Tarefa 15.3: Documentação de Código**
  - [ ] 15.3.1: Adicionar docstrings a todos os modelos
  - [ ] 15.3.2: Adicionar docstrings a todas as views
  - [ ] 15.3.3: Adicionar docstrings a funções auxiliares
  - [ ] 15.3.4: Documentar métodos customizados
  - [ ] 15.3.5: Adicionar comentários em lógica complexa
  - [ ] 15.3.6: Verificar clareza do código

- [ ] **Tarefa 15.4: Documentação do Usuário**
  - [ ] 15.4.1: Criar arquivo `docs/INSTALLATION.md`
  - [ ] 15.4.2: Documentar pré-requisitos
  - [ ] 15.4.3: Documentar processo de instalação
  - [ ] 15.4.4: Criar arquivo `docs/USER_GUIDE.md`
  - [ ] 15.4.5: Documentar funcionalidades principais
  - [ ] 15.4.6: Adicionar screenshots
  - [ ] 15.4.7: Criar arquivo `docs/API.md` (se houver API)
  - [ ] 15.4.8: Atualizar README.md principal

- [ ] **Tarefa 15.5: Otimizações Finais**
  - [ ] 15.5.1: Minificar CSS e JS
  - [ ] 15.5.2: Otimizar imagens
  - [ ] 15.5.3: Configurar cache de templates
  - [ ] 15.5.4: Configurar compressão gzip
  - [ ] 15.5.5: Testar responsividade em todos os dispositivos
  - [ ] 15.5.6: Testar compatibilidade de navegadores
  - [ ] 15.5.7: Validar acessibilidade (WCAG)

- [ ] **Tarefa 15.6: Preparação para Deploy**
  - [ ] 15.6.1: Criar arquivo `.env.example`
  - [ ] 15.6.2: Documentar variáveis de ambiente
  - [ ] 15.6.3: Criar script de setup automatizado
  - [ ] 15.6.4: Testar em ambiente limpo
  - [ ] 15.6.5: Criar arquivo `requirements-production.txt`
  - [ ] 15.6.6: Preparar arquivos de configuração do servidor
  - [ ] 15.6.7: Documentar processo de deploy

---
