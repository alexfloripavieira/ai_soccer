# Design System

## Visão Geral

O AI Soccer utiliza um design system consistente baseado em TailwindCSS, com tema escuro moderno e gradientes vibrantes.

## Princípios de Design

### 1. Consistência
- Todos os componentes seguem o mesmo padrão visual
- Espaçamentos uniformes
- Transições suaves

### 2. Dark Mode First
- Interface otimizada para tema escuro
- Alto contraste para legibilidade
- Cores vibrantes sobre fundo escuro

### 3. Responsividade
- Mobile-first approach
- Breakpoints do TailwindCSS
- Grid system flexível

### 4. Acessibilidade
- Contraste adequado (WCAG AA mínimo)
- Estados de foco visíveis
- Textos alternativos

## Paleta de Cores

### Cores Primárias

#### Gradiente Principal
```css
/* Usado em: Botões principais, logo, destaques */
from-green-500 to-blue-500

Hex:
  --primary-from: #10b981  /* Green-500 */
  --primary-to: #3b82f6    /* Blue-500 */
```

**Aplicação**:
```html
<div class="bg-gradient-to-r from-green-500 to-blue-500">
    AI Soccer
</div>
```

#### Cores de Acento
```css
/* Purple - Para destaques secundários */
--accent: #8b5cf6          /* Purple-500 */

/* Pink - Para alertas e destaques */
--accent-secondary: #ec4899 /* Pink-500 */
```

### Cores de Fundo (Dark Mode)

```css
/* Fundo principal da aplicação */
--bg-primary: #0f172a      /* Slate-900 */

/* Cards, painéis, seções */
--bg-secondary: #1e293b    /* Slate-800 */

/* Elementos elevados, dropdowns */
--bg-tertiary: #334155     /* Slate-700 */

/* Overlays, modals */
--bg-overlay: #475569      /* Slate-600 */
```

**Aplicação**:
```html
<!-- Body -->
<body class="bg-slate-900">

<!-- Card -->
<div class="bg-slate-800 rounded-lg">
    Conteúdo
</div>

<!-- Button secundário -->
<button class="bg-slate-700 hover:bg-slate-600">
    Ação
</button>
```

### Cores de Texto

```css
/* Texto principal */
--text-primary: #f1f5f9    /* Slate-100 */

/* Texto secundário */
--text-secondary: #cbd5e1  /* Slate-300 */

/* Texto auxiliar, placeholders */
--text-muted: #94a3b8      /* Slate-400 */
```

**Hierarquia de Texto**:
```html
<h1 class="text-slate-100">Título Principal</h1>
<p class="text-slate-300">Texto normal</p>
<span class="text-slate-400">Informação auxiliar</span>
```

### Cores de Status

```css
/* Sucesso, confirmação */
--success: #10b981         /* Green-500 */

/* Aviso, atenção */
--warning: #f59e0b         /* Amber-500 */

/* Erro, perigo */
--error: #ef4444           /* Red-500 */

/* Informação */
--info: #3b82f6            /* Blue-500 */
```

**Aplicação**:
```html
<!-- Badge de sucesso -->
<span class="bg-green-900 text-green-300 px-3 py-1 rounded-full">
    Ativo
</span>

<!-- Alerta de erro -->
<div class="bg-red-900 text-red-300 p-4 rounded-lg">
    Erro ao processar dados
</div>
```

## Tipografia

### Fonte

**Família**: Inter (via Google Fonts)
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**CSS**:
```css
font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Escala de Tamanhos

```css
/* Extra pequeno */
--text-xs: 0.75rem;    /* 12px */
text-xs

/* Pequeno */
--text-sm: 0.875rem;   /* 14px */
text-sm

/* Base */
--text-base: 1rem;     /* 16px */
text-base

/* Grande */
--text-lg: 1.125rem;   /* 18px */
text-lg

/* Extra grande */
--text-xl: 1.25rem;    /* 20px */
text-xl

/* 2x extra grande */
--text-2xl: 1.5rem;    /* 24px */
text-2xl

/* 3x extra grande */
--text-3xl: 1.875rem;  /* 30px */
text-3xl

/* 4x extra grande */
--text-4xl: 2.25rem;   /* 36px */
text-4xl
```

### Pesos de Fonte

```css
font-normal     /* 400 - Texto normal */
font-medium     /* 500 - Ênfase leve */
font-semibold   /* 600 - Subtítulos */
font-bold       /* 700 - Títulos */
```

### Hierarquia de Títulos

```html
<!-- H1 - Título principal da página -->
<h1 class="text-4xl font-bold text-slate-100 mb-6">
    Atletas
</h1>

<!-- H2 - Seções principais -->
<h2 class="text-3xl font-bold text-slate-100 mb-4">
    Informações Pessoais
</h2>

<!-- H3 - Subseções -->
<h3 class="text-2xl font-semibold text-slate-100 mb-3">
    Dados Físicos
</h3>

<!-- H4 - Elementos de card -->
<h4 class="text-xl font-semibold text-slate-100 mb-2">
    João Silva
</h4>

<!-- Parágrafo -->
<p class="text-base text-slate-300">
    Texto normal de conteúdo.
</p>

<!-- Texto auxiliar -->
<span class="text-sm text-slate-400">
    Informação adicional
</span>
```

## Espaçamento

### Sistema de Espaçamento (Tailwind)

```css
0   = 0px
1   = 0.25rem  (4px)
2   = 0.5rem   (8px)
3   = 0.75rem  (12px)
4   = 1rem     (16px)
6   = 1.5rem   (24px)
8   = 2rem     (32px)
12  = 3rem     (48px)
16  = 4rem     (64px)
```

### Padrões de Espaçamento

```html
<!-- Padding interno de cards -->
<div class="p-6">Card padrão</div>

<!-- Margens entre seções -->
<section class="mb-8">Seção</section>

<!-- Espaçamento entre elementos -->
<div class="space-y-4">
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<!-- Container com padding responsivo -->
<div class="container mx-auto px-4 py-8">
    Conteúdo
</div>
```

## Bordas e Sombras

### Border Radius

```css
rounded-none    /* 0 */
rounded-sm      /* 0.125rem */
rounded         /* 0.25rem */
rounded-md      /* 0.375rem */
rounded-lg      /* 0.5rem - PADRÃO */
rounded-xl      /* 0.75rem - Cards */
rounded-2xl     /* 1rem */
rounded-full    /* 9999px - Badges circulares */
```

### Borders

```css
/* Border padrão */
border border-slate-700

/* Border bottom (separadores) */
border-b border-slate-800
```

### Sombras

```css
/* Sombra leve - Cards */
shadow-lg

/* Sombra média - Cards elevados */
shadow-xl

/* Sombra em hover */
hover:shadow-2xl
```

**Exemplo**:
```html
<div class="bg-slate-800 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-200">
    Card com sombra
</div>
```

## Transições e Animações

### Transições Padrão

```css
/* Transição suave em hover */
transition-all duration-200

/* Transição de cores */
transition-colors duration-200

/* Transição de transformação */
transition-transform duration-200
```

### Efeitos Comuns

```html
<!-- Hover scale -->
<button class="transform hover:scale-105 transition-all duration-200">
    Botão
</button>

<!-- Hover opacity -->
<div class="hover:opacity-80 transition-opacity duration-200">
    Card
</div>

<!-- Hover shadow -->
<div class="shadow-lg hover:shadow-xl transition-all duration-200">
    Card
</div>
```

## Layout

### Container

```html
<!-- Container centralizado com largura máxima -->
<div class="container mx-auto px-4">
    Conteúdo centralizado
</div>

<!-- Container com padding vertical -->
<div class="container mx-auto px-4 py-8">
    Conteúdo com espaçamento
</div>
```

### Grid System

```html
<!-- 2 colunas responsivas -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
</div>

<!-- 3 colunas responsivas -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
    <div>Coluna 3</div>
</div>

<!-- 4 colunas responsivas -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
    <div>Coluna 3</div>
    <div>Coluna 4</div>
</div>
```

### Flexbox

```html
<!-- Flex row com espaçamento -->
<div class="flex items-center space-x-4">
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<!-- Flex com justify-between -->
<div class="flex items-center justify-between">
    <div>Esquerda</div>
    <div>Direita</div>
</div>

<!-- Flex column -->
<div class="flex flex-col space-y-4">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

## Breakpoints Responsivos

```css
/* Mobile first */
sm:   640px   /* Tablet pequeno */
md:   768px   /* Tablet */
lg:   1024px  /* Desktop */
xl:   1280px  /* Desktop grande */
2xl:  1536px  /* Desktop extra grande */
```

**Exemplo de uso**:
```html
<div class="
    text-base           /* Mobile */
    md:text-lg          /* Tablet+ */
    lg:text-xl          /* Desktop+ */
">
    Texto responsivo
</div>

<div class="
    grid grid-cols-1    /* Mobile: 1 coluna */
    md:grid-cols-2      /* Tablet: 2 colunas */
    lg:grid-cols-3      /* Desktop: 3 colunas */
    gap-6
">
    Cards responsivos
</div>
```

## Estados de Interação

### Hover
```html
<button class="bg-slate-700 hover:bg-slate-600 transition-colors duration-200">
    Hover me
</button>
```

### Focus
```html
<input class="
    border border-slate-700
    focus:outline-none
    focus:ring-2
    focus:ring-green-500
    focus:border-transparent
    transition-all duration-200
">
```

### Active
```html
<button class="
    bg-gradient-to-r from-green-500 to-blue-500
    active:opacity-80
    transition-opacity duration-200
">
    Click me
</button>
```

### Disabled
```html
<button class="
    bg-slate-700
    disabled:opacity-50
    disabled:cursor-not-allowed
" disabled>
    Disabled
</button>
```

## Utilitários Comuns

### Truncate Text
```html
<p class="truncate">
    Texto muito longo que será cortado com reticências...
</p>
```

### Line Clamp (múltiplas linhas)
```html
<p class="line-clamp-3">
    Texto que será limitado a 3 linhas com reticências no final...
</p>
```

### Scroll
```html
<div class="overflow-y-auto h-64">
    Conteúdo com scroll vertical
</div>

<div class="overflow-x-auto">
    <table>...</table>
</div>
```

### Visibility
```html
<!-- Ocultar em mobile, mostrar em desktop -->
<div class="hidden lg:block">
    Visível apenas em desktop
</div>

<!-- Mostrar em mobile, ocultar em desktop -->
<div class="block lg:hidden">
    Visível apenas em mobile
</div>
```

## Acessibilidade

### Contraste de Cores
- Texto primário em slate-100 sobre slate-900: ✅ Passa WCAG AA
- Texto secundário em slate-300 sobre slate-800: ✅ Passa WCAG AA
- Texto muted em slate-400 sobre slate-800: ⚠️ Usar apenas para informações não-críticas

### Focus Visível
```html
<!-- SEMPRE incluir ring em focus -->
<button class="focus:ring-2 focus:ring-green-500 focus:outline-none">
    Botão acessível
</button>
```

### Screen Readers
```html
<!-- Labels para inputs -->
<label for="name" class="block text-sm font-medium text-slate-300 mb-2">
    Nome
</label>
<input id="name" type="text" />

<!-- Textos alternativos -->
<img src="logo.png" alt="Logo AI Soccer" />

<!-- Botões apenas com ícone -->
<button aria-label="Fechar modal">
    <svg>...</svg>
</button>
```

---

**Última Atualização**: 2025-10-28
