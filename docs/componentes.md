# Guia de Componentes

## Visão Geral

Este guia contém todos os componentes TailwindCSS reutilizáveis do AI Soccer. Copie e adapte conforme necessário.

## Botões

### Botão Primário (Gradient)

**Uso**: Ações principais, CTAs, submissão de formulários

```html
<button class="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
    Botão Primário
</button>

<!-- Com ícone -->
<button class="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
    </svg>
    <span>Adicionar</span>
</button>
```

### Botão Secundário

**Uso**: Ações secundárias, cancelar

```html
<button class="px-6 py-3 bg-slate-700 text-slate-100 font-semibold rounded-lg border border-slate-600 hover:bg-slate-600 transition-all duration-200">
    Botão Secundário
</button>
```

### Botão Ghost

**Uso**: Ações terciárias, links de ação

```html
<button class="px-6 py-3 text-slate-300 font-semibold rounded-lg hover:bg-slate-800 transition-all duration-200">
    Botão Ghost
</button>
```

### Botão Danger

**Uso**: Ações destrutivas (excluir, remover)

```html
<button class="px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-all duration-200">
    Excluir
</button>
```

### Botão Disabled

```html
<button class="px-6 py-3 bg-slate-700 text-slate-400 font-semibold rounded-lg opacity-50 cursor-not-allowed" disabled>
    Desabilitado
</button>
```

### Botões de Tamanho

```html
<!-- Pequeno -->
<button class="px-4 py-2 text-sm bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg">
    Pequeno
</button>

<!-- Médio (padrão) -->
<button class="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg">
    Médio
</button>

<!-- Grande -->
<button class="px-8 py-4 text-lg bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg">
    Grande
</button>
```

## Formulários

### Input Text

```html
<div class="mb-4">
    <label for="name" class="block text-sm font-medium text-slate-300 mb-2">
        Nome
    </label>
    <input
        type="text"
        id="name"
        name="name"
        class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
        placeholder="Digite o nome..."
    >
</div>
```

### Input com Ícone

```html
<div class="mb-4">
    <label for="email" class="block text-sm font-medium text-slate-300 mb-2">
        Email
    </label>
    <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
            </svg>
        </div>
        <input
            type="email"
            id="email"
            class="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
            placeholder="seu@email.com"
        >
    </div>
</div>
```

### Select

```html
<div class="mb-4">
    <label for="position" class="block text-sm font-medium text-slate-300 mb-2">
        Posição
    </label>
    <select
        id="position"
        name="position"
        class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
    >
        <option value="">Selecione...</option>
        <option value="GK">Goleiro</option>
        <option value="DF">Defensor</option>
        <option value="MF">Meio-campo</option>
        <option value="FW">Atacante</option>
    </select>
</div>
```

### Textarea

```html
<div class="mb-4">
    <label for="notes" class="block text-sm font-medium text-slate-300 mb-2">
        Observações
    </label>
    <textarea
        id="notes"
        name="notes"
        rows="4"
        class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
        placeholder="Digite suas observações..."
    ></textarea>
</div>
```

### Checkbox

```html
<div class="flex items-center mb-4">
    <input
        type="checkbox"
        id="active"
        name="active"
        class="w-4 h-4 text-green-500 bg-slate-800 border-slate-700 rounded focus:ring-green-500 focus:ring-2"
    >
    <label for="active" class="ml-2 text-sm text-slate-300">
        Ativo
    </label>
</div>
```

### Radio

```html
<div class="space-y-2">
    <div class="flex items-center">
        <input
            type="radio"
            id="male"
            name="gender"
            value="M"
            class="w-4 h-4 text-green-500 bg-slate-800 border-slate-700 focus:ring-green-500 focus:ring-2"
        >
        <label for="male" class="ml-2 text-sm text-slate-300">
            Masculino
        </label>
    </div>
    <div class="flex items-center">
        <input
            type="radio"
            id="female"
            name="gender"
            value="F"
            class="w-4 h-4 text-green-500 bg-slate-800 border-slate-700 focus:ring-green-500 focus:ring-2"
        >
        <label for="female" class="ml-2 text-sm text-slate-300">
            Feminino
        </label>
    </div>
</div>
```

### Mensagem de Erro

```html
<div class="mb-4">
    <input type="text" class="w-full px-4 py-3 bg-slate-800 border border-red-500 rounded-lg text-slate-100">
    <p class="mt-1 text-sm text-red-400">Este campo é obrigatório.</p>
</div>
```

## Cards

### Card Básico

```html
<div class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-xl font-bold text-slate-100 mb-2">Título do Card</h3>
    <p class="text-slate-400">Conteúdo do card...</p>
</div>
```

### Card com Hover

```html
<div class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg p-6 hover:shadow-xl hover:border-slate-600 transition-all duration-200 cursor-pointer">
    <h3 class="text-xl font-bold text-slate-100 mb-2">Card Interativo</h3>
    <p class="text-slate-400">Clique para mais detalhes</p>
</div>
```

### Card com Header e Footer

```html
<div class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-700 px-6 py-4 border-b border-slate-600">
        <h3 class="text-xl font-bold text-slate-100">Header</h3>
    </div>

    <!-- Body -->
    <div class="p-6">
        <p class="text-slate-300">Conteúdo principal do card</p>
    </div>

    <!-- Footer -->
    <div class="bg-slate-700 px-6 py-4 border-t border-slate-600 flex justify-end space-x-3">
        <button class="px-4 py-2 text-slate-300 rounded-lg hover:bg-slate-600">
            Cancelar
        </button>
        <button class="px-4 py-2 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-lg">
            Confirmar
        </button>
    </div>
</div>
```

### Card de Estatística

```html
<div class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg p-6">
    <div class="flex items-center justify-between">
        <div>
            <p class="text-sm text-slate-400 mb-1">Total de Atletas</p>
            <p class="text-3xl font-bold text-slate-100">125</p>
        </div>
        <div class="p-3 bg-green-900 rounded-lg">
            <svg class="w-8 h-8 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
        </div>
    </div>
    <div class="mt-4 flex items-center text-sm">
        <span class="text-green-400 flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
            </svg>
            12%
        </span>
        <span class="text-slate-400 ml-2">vs. mês anterior</span>
    </div>
</div>
```

## Badges/Tags

### Badge de Status

```html
<!-- Sucesso -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-900 text-green-300">
    Ativo
</span>

<!-- Aviso -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-900 text-yellow-300">
    Pendente
</span>

<!-- Erro -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-900 text-red-300">
    Inativo
</span>

<!-- Info -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-900 text-blue-300">
    Novo
</span>
```

### Badge com Ícone

```html
<span class="inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium bg-green-900 text-green-300">
    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
    </svg>
    <span>Aprovado</span>
</span>
```

## Tabelas

### Tabela Básica

```html
<div class="overflow-x-auto">
    <table class="w-full">
        <thead class="bg-slate-800 border-b border-slate-700">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    Nome
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    Posição
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    Idade
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-slate-300 uppercase tracking-wider">
                    Ações
                </th>
            </tr>
        </thead>
        <tbody class="bg-slate-900 divide-y divide-slate-800">
            <tr class="hover:bg-slate-800 transition-all">
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-slate-100">João Silva</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-slate-300">Atacante</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-slate-300">25</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <a href="#" class="text-green-400 hover:text-green-300 mr-3">Editar</a>
                    <a href="#" class="text-red-400 hover:text-red-300">Excluir</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

## Navegação

### Navbar

```html
<nav class="bg-slate-900 border-b border-slate-800">
    <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
            <!-- Logo -->
            <div class="flex items-center space-x-8">
                <a href="/" class="text-2xl font-bold bg-gradient-to-r from-green-500 to-blue-500 bg-clip-text text-transparent">
                    AI Soccer
                </a>

                <!-- Links (desktop) -->
                <div class="hidden md:flex space-x-4">
                    <a href="#" class="text-slate-300 hover:text-white px-3 py-2 rounded-lg hover:bg-slate-800 transition-all">
                        Performance
                    </a>
                    <a href="#" class="text-slate-300 hover:text-white px-3 py-2 rounded-lg hover:bg-slate-800 transition-all">
                        Scouting
                    </a>
                    <a href="#" class="text-slate-300 hover:text-white px-3 py-2 rounded-lg hover:bg-slate-800 transition-all">
                        Business
                    </a>
                </div>
            </div>

            <!-- Ações -->
            <div>
                <a href="#" class="px-4 py-2 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg">
                    Entrar
                </a>
            </div>
        </div>
    </div>
</nav>
```

### Sidebar

```html
<aside class="w-64 bg-slate-900 border-r border-slate-800 h-screen fixed left-0 top-0">
    <div class="p-6">
        <!-- Logo -->
        <h2 class="text-2xl font-bold bg-gradient-to-r from-green-500 to-blue-500 bg-clip-text text-transparent mb-8">
            AI Soccer
        </h2>

        <!-- Menu -->
        <nav class="space-y-2">
            <a href="#" class="flex items-center space-x-3 px-4 py-3 text-slate-100 bg-slate-800 rounded-lg">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                </svg>
                <span>Dashboard</span>
            </a>

            <a href="#" class="flex items-center space-x-3 px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                <span>Performance</span>
            </a>

            <a href="#" class="flex items-center space-x-3 px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                <span>Scouting</span>
            </a>

            <a href="#" class="flex items-center space-x-3 px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>Business</span>
            </a>
        </nav>
    </div>
</aside>
```

### Breadcrumbs

```html
<nav class="flex mb-6" aria-label="Breadcrumb">
    <ol class="inline-flex items-center space-x-1 md:space-x-3">
        <li class="inline-flex items-center">
            <a href="#" class="text-slate-400 hover:text-slate-300">
                Dashboard
            </a>
        </li>
        <li>
            <div class="flex items-center">
                <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
                <a href="#" class="ml-1 text-slate-400 hover:text-slate-300">
                    Performance
                </a>
            </div>
        </li>
        <li>
            <div class="flex items-center">
                <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
                <span class="ml-1 text-slate-100">
                    Atletas
                </span>
            </div>
        </li>
    </ol>
</nav>
```

## Alertas

### Alerta de Sucesso

```html
<div class="bg-green-900 border border-green-700 text-green-300 px-4 py-3 rounded-lg flex items-start" role="alert">
    <svg class="w-5 h-5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
    </svg>
    <div>
        <p class="font-medium">Sucesso!</p>
        <p class="text-sm">Atleta cadastrado com sucesso.</p>
    </div>
</div>
```

### Alerta de Erro

```html
<div class="bg-red-900 border border-red-700 text-red-300 px-4 py-3 rounded-lg flex items-start" role="alert">
    <svg class="w-5 h-5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
    </svg>
    <div>
        <p class="font-medium">Erro!</p>
        <p class="text-sm">Não foi possível processar a solicitação.</p>
    </div>
</div>
```

### Alerta de Aviso

```html
<div class="bg-yellow-900 border border-yellow-700 text-yellow-300 px-4 py-3 rounded-lg flex items-start" role="alert">
    <svg class="w-5 h-5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
    </svg>
    <div>
        <p class="font-medium">Atenção!</p>
        <p class="text-sm">Verifique os dados antes de continuar.</p>
    </div>
</div>
```

## Paginação

```html
<nav class="flex items-center justify-between border-t border-slate-800 px-4 py-3">
    <div class="flex-1 flex justify-between sm:hidden">
        <a href="#" class="relative inline-flex items-center px-4 py-2 border border-slate-700 text-sm font-medium rounded-lg text-slate-300 bg-slate-800 hover:bg-slate-700">
            Anterior
        </a>
        <a href="#" class="ml-3 relative inline-flex items-center px-4 py-2 border border-slate-700 text-sm font-medium rounded-lg text-slate-300 bg-slate-800 hover:bg-slate-700">
            Próxima
        </a>
    </div>
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
            <p class="text-sm text-slate-400">
                Mostrando <span class="font-medium">1</span> a <span class="font-medium">20</span> de{' '}
                <span class="font-medium">125</span> resultados
            </p>
        </div>
        <div>
            <nav class="relative z-0 inline-flex rounded-lg shadow-sm -space-x-px" aria-label="Pagination">
                <a href="#" class="relative inline-flex items-center px-3 py-2 rounded-l-lg border border-slate-700 bg-slate-800 text-sm font-medium text-slate-400 hover:bg-slate-700">
                    Anterior
                </a>
                <a href="#" class="relative inline-flex items-center px-4 py-2 border border-slate-700 bg-green-600 text-sm font-medium text-white">
                    1
                </a>
                <a href="#" class="relative inline-flex items-center px-4 py-2 border border-slate-700 bg-slate-800 text-sm font-medium text-slate-300 hover:bg-slate-700">
                    2
                </a>
                <a href="#" class="relative inline-flex items-center px-4 py-2 border border-slate-700 bg-slate-800 text-sm font-medium text-slate-300 hover:bg-slate-700">
                    3
                </a>
                <a href="#" class="relative inline-flex items-center px-3 py-2 rounded-r-lg border border-slate-700 bg-slate-800 text-sm font-medium text-slate-300 hover:bg-slate-700">
                    Próxima
                </a>
            </nav>
        </div>
    </div>
</nav>
```

## Loading Spinner

```html
<div class="flex justify-center items-center p-8">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
</div>

<!-- Com texto -->
<div class="flex flex-col items-center justify-center p-8">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mb-4"></div>
    <p class="text-slate-400">Carregando...</p>
</div>
```

## Empty State

```html
<div class="text-center py-12">
    <svg class="mx-auto h-12 w-12 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
    </svg>
    <h3 class="mt-4 text-lg font-medium text-slate-300">Nenhum atleta encontrado</h3>
    <p class="mt-2 text-sm text-slate-400">Comece cadastrando seu primeiro atleta.</p>
    <div class="mt-6">
        <button class="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg">
            Adicionar Atleta
        </button>
    </div>
</div>
```

---

**Última Atualização**: 2025-10-28
