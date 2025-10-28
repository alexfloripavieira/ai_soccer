# Glossário

## Termos do Projeto

### A

**AbstractUser**
- Classe base do Django para criar modelos customizados de usuário
- Herda funcionalidades de autenticação e autorização

**App Django**
- Módulo independente que representa um domínio de negócio
- Contém models, views, templates e lógica específica

**AUTH_USER_MODEL**
- Configuração Django que referencia o modelo de usuário
- Usado para criar ForeignKeys para o usuário customizado

### B

**Backend de Autenticação**
- Classe que define como o Django autentica usuários
- No AI Soccer: autenticação por email ao invés de username

**Base Template**
- Template principal que outros templates estendem
- Define estrutura HTML comum (header, footer, etc.)

### C

**CBV (Class-Based View)**
- View baseada em classe
- Reutilizável e extensível através de herança

**CSRF (Cross-Site Request Forgery)**
- Ataque de segurança web
- Django protege automaticamente com tokens CSRF

**Context Processor**
- Função que adiciona variáveis a todos os templates
- Exemplo: dados do usuário logado

### D

**DTL (Django Template Language)**
- Linguagem de templates do Django
- Sintaxe: `{% %}` para lógica, `{{ }}` para variáveis

**Dashboard**
- Painel principal do sistema após login
- Exibe resumo e acesso rápido às funcionalidades

### F

**ForeignKey**
- Relacionamento um-para-muitos entre models
- Exemplo: Um usuário pode ter vários atletas

**FBV (Function-Based View)**
- View baseada em função
- Mais simples, menos reutilizável que CBV

### G

**Gradient**
- Transição suave entre cores
- Usado no AI Soccer: verde (#10b981) para azul (#3b82f6)

### I

**IA / ML (Inteligência Artificial / Machine Learning)**
- Modelos preditivos planejados para:
  - Prevenção de lesões (Performance)
  - Detecção de talentos (Scouting)
  - Previsão de receitas (Business)

### L

**LoginRequiredMixin**
- Mixin Django que protege views
- Redireciona usuários não autenticados para login

### M

**Migration**
- Arquivo Python que altera o schema do banco
- Versionamento de mudanças em models

**Model**
- Classe Python que representa tabela do banco
- Define campos e comportamentos

**Mixin**
- Classe que adiciona funcionalidade a outras classes
- Usado em CBVs para adicionar comportamentos

### O

**ORM (Object-Relational Mapping)**
- Sistema que mapeia objetos Python para banco de dados
- Django ORM permite queries sem SQL direto

### P

**PEP 8**
- Guia de estilo Python oficial
- Define convenções de nomenclatura e formatação

**Payload**
- Dados enviados em uma requisição HTTP
- Exemplo: dados de um formulário

### Q

**QuerySet**
- Conjunto de objetos retornados por uma query
- Lazy: só executa quando necessário

### R

**Related Name**
- Nome usado para relacionamento reverso
- Exemplo: `athlete.training_loads.all()`

### S

**Serializer**
- Converte objetos Python em JSON (e vice-versa)
- Usado em APIs REST (futuro)

**Signal**
- Notificação automática quando eventos ocorrem
- Exemplo: após salvar um model (`post_save`)

**Slug**
- Versão URL-friendly de um texto
- Exemplo: "João Silva" → "joao-silva"

**Static Files**
- Arquivos que não mudam (CSS, JS, imagens)
- Servidos de `static/` em desenvolvimento

### T

**Template Tag**
- Comando Django em templates
- Exemplo: `{% for %}`, `{% if %}`

**TailwindCSS**
- Framework CSS utility-first
- Classes prontas para estilização

### U

**URL Pattern**
- Rota que mapeia URL para view
- Definido em `urls.py`

**User Story**
- Descrição de funcionalidade do ponto de vista do usuário
- Formato: "Como [usuário], quero [ação], para [objetivo]"

### V

**Valuation**
- Avaliação do valor de mercado de um atleta
- Calculado por algoritmo de IA

**View**
- Função ou classe que processa requisição e retorna resposta
- Contém lógica de negócio

**Virtual Environment (venv)**
- Ambiente Python isolado
- Cada projeto tem suas próprias dependências

### W

**Widget**
- Representação HTML de um campo de formulário
- Exemplo: TextInput, Select, DatePicker

**WSGI (Web Server Gateway Interface)**
- Interface entre servidor web e aplicação Python
- Usado em produção (Gunicorn, uWSGI)

## Termos de Futebol

### A

**Atleta**
- Jogador de futebol cadastrado no sistema
- Possui dados pessoais, físicos e de performance

### C

**Carga de Treino**
- Registro de treino de um atleta
- Inclui: duração, distância, frequência cardíaca, intensidade

### D

**Dashboard de Performance**
- Painel visual com métricas de um atleta
- Gráficos de evolução, alertas, estatísticas

### F

**FC (Frequência Cardíaca)**
- Batimentos por minuto durante treino
- Indicador de intensidade de esforço

### I

**Índice de Fadiga**
- Métrica calculada baseada em carga de treino
- Indica nível de cansaço/recuperação

**Intensidade**
- Nível de esforço do treino
- Categorias: Baixa, Média, Alta, Muito Alta

### L

**Lesão**
- Machucado que afasta atleta de treinos/jogos
- Registrado com: tipo, gravidade, previsão de retorno

### M

**Métrica de Performance**
- Medida de desempenho físico
- Exemplos: velocidade máxima, aceleração, sprints

### P

**Posição**
- Função do atleta em campo
- Categorias: Goleiro, Defensor, Meio-campo, Atacante

**Prospecção**
- Processo de identificar novos talentos
- Análise de jogadores para possível contratação

### R

**Relatório de Scouting**
- Avaliação detalhada de jogador prospectado
- Inclui notas: técnica, físico, tático, mental, potencial

### S

**Scout**
- Profissional que avalia jogadores
- Produz relatórios de prospecção

### V

**Valor de Mercado**
- Preço estimado de um atleta
- Usado em negociações de transferência

## Siglas Técnicas

- **API**: Application Programming Interface
- **CBV**: Class-Based View
- **CRUD**: Create, Read, Update, Delete
- **CSS**: Cascading Style Sheets
- **DTL**: Django Template Language
- **ER**: Entity-Relationship (diagrama)
- **FBV**: Function-Based View
- **FK**: Foreign Key
- **HTML**: HyperText Markup Language
- **HTTP**: HyperText Transfer Protocol
- **JS**: JavaScript
- **JSON**: JavaScript Object Notation
- **KPI**: Key Performance Indicator
- **ML**: Machine Learning
- **MVP**: Minimum Viable Product
- **ORM**: Object-Relational Mapping
- **PK**: Primary Key
- **PRD**: Product Requirements Document
- **REST**: Representational State Transfer
- **SQL**: Structured Query Language
- **UI**: User Interface
- **URL**: Uniform Resource Locator
- **UX**: User Experience
- **WSGI**: Web Server Gateway Interface

## Referências

Para mais informações, consulte:

- [Django Glossary](https://docs.djangoproject.com/en/stable/glossary/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

---

**Última Atualização**: 2025-10-28
