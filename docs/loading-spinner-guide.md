# Guia de Loading Spinners - AI Soccer

Este guia documenta o sistema completo de loading spinners implementado no projeto AI Soccer, incluindo componentes, API JavaScript e exemplos de uso.

---

## Visão Geral

O sistema de loading spinners fornece:
- **Componente reutilizável** de loading em `/templates/components/loading.html`
- **API JavaScript** em `/static/js/loading.js` para controle programático
- **Auto-inicialização** via atributos `data-loading`
- **Consistência visual** com o design system do projeto (tema escuro, gradiente verde-azul)
- **Acessibilidade** com atributos ARIA apropriados

---

## Componente Base

### Template: `templates/components/loading.html`

O componente suporta dois modos:

#### 1. Full Page Overlay (padrão)

```django
{% include 'components/loading.html' with
   loading_id='page-loading'
   loading_text='Carregando...'
   loading_subtitle='Por favor, aguarde'
   show_progress=True
%}
```

**Parâmetros:**
- `loading_id`: ID único do elemento (padrão: `page-loading`)
- `loading_text`: Texto principal (padrão: `Carregando...`)
- `loading_subtitle`: Texto secundário (padrão: `Por favor, aguarde`)
- `show_progress`: Mostrar barra de progresso animada (opcional)

#### 2. Inline Spinner

```django
{% include 'components/loading.html' with
   loading_id='inline-loading'
   loading_text='Processando'
   inline=True
   extra_classes='text-green-400'
%}
```

**Parâmetros:**
- `inline=True`: Ativa modo inline
- `extra_classes`: Classes Tailwind adicionais

---

## API JavaScript

### Métodos Disponíveis

#### `Loading.show(loadingId, options)`

Mostra um spinner específico com fade-in.

```javascript
Loading.show('my-spinner', {
  text: 'Processando dados...',
  subtitle: 'Isso pode levar alguns segundos'
});
```

#### `Loading.hide(loadingId, callback)`

Esconde um spinner com fade-out.

```javascript
Loading.hide('my-spinner', () => {
  console.log('Loading escondido!');
});
```

#### `Loading.showPage(text, subtitle)`

Mostra o overlay de loading global.

```javascript
Loading.showPage('Carregando dashboard...', 'Buscando dados');
```

#### `Loading.hidePage(callback)`

Esconde o overlay global.

```javascript
Loading.hidePage(() => {
  console.log('Página carregada!');
});
```

#### `Loading.button(button, loading, loadingText)`

Controla estado de loading em botões.

```javascript
const btn = document.getElementById('submit-btn');

// Ativar loading
Loading.button(btn, true, 'Enviando...');

// Desativar loading
Loading.button(btn, false);
```

**O que faz:**
- Desabilita o botão
- Substitui conteúdo por spinner + texto
- Adiciona classes de opacidade
- Restaura estado original ao desativar

#### `Loading.form(form, options)`

Gerencia loading automático em formulários.

```javascript
const form = document.getElementById('my-form');

Loading.form(form, {
  buttonText: 'Enviando...',
  text: 'Processando formulário...',
  subtitle: 'Por favor, aguarde',
  showPageLoading: true // ou false
});
```

#### `Loading.wrap(loadingId, promise, options)`

Envolve uma Promise com loading automático.

```javascript
const result = await Loading.wrap('my-spinner',
  fetch('/api/data').then(r => r.json()),
  { text: 'Buscando dados...' }
);
```

#### `Loading.skeleton(container, count)`

Cria skeleton screens para loading de listas.

```javascript
const container = document.getElementById('results');
Loading.skeleton(container, 5); // 5 items de skeleton
```

---

## Auto-Inicialização com Atributos Data

### Formulários

Adicione `data-loading` ao formulário:

```html
<form method="post"
      data-loading
      data-loading-text="Salvando dados..."
      data-loading-subtitle="Processando"
      data-loading-button="Salvando..."
      data-loading-page="true">
  <!-- campos do formulário -->
  <button type="submit">Salvar</button>
</form>
```

### Links

Adicione `data-loading` aos links:

```html
<a href="/dashboard"
   data-loading
   data-loading-text="Carregando dashboard..."
   data-loading-subtitle="Preparando dados">
  Ir para Dashboard
</a>
```

---

## Exemplos de Implementação

### Exemplo 1: Lista de Atletas (Export + Search)

**Template:** `templates/performance/athlete_list.html`

```django
{# Botão de exportação com loading #}
<button id="export-btn" onclick="handleExport()">
  Exportar Excel
</button>

{# Formulário de busca com loading automático #}
<form id="search-form" method="get">
  <input type="text" name="q" placeholder="Buscar...">
  <button type="submit" id="search-btn">Buscar</button>
</form>
```

```javascript
// Export com loading
function handleExport() {
  const exportBtn = document.getElementById('export-btn');
  Loading.button(exportBtn, true, 'Exportando...');

  window.location.href = '/export';

  setTimeout(() => {
    Loading.button(exportBtn, false);
  }, 3000);
}

// Search com loading
document.getElementById('search-form')?.addEventListener('submit', function(e) {
  const searchBtn = document.getElementById('search-btn');
  Loading.button(searchBtn, true, 'Buscando...');
});
```

### Exemplo 2: Busca Global com AJAX

**Template:** `templates/core/global_search.html`

```django
{# Spinner dedicado para busca #}
{% include 'components/loading.html' with
   loading_id='search-loading-overlay'
   loading_text='Buscando...'
   loading_subtitle='Pesquisando no sistema'
%}

<form>
  <input type="text" name="q" id="search-input">
  <button type="submit">Buscar</button>
</form>
```

```javascript
searchForm.addEventListener('submit', function(e) {
  const query = searchInput.value.trim();

  Loading.button(searchButton, true, 'Buscando...');

  Loading.show('search-loading-overlay', {
    text: 'Buscando...',
    subtitle: `Pesquisando por "${query}"`
  });
});
```

### Exemplo 3: Formulário de Criação/Edição

**Template:** `templates/performance/athlete_form.html`

```django
{# Formulário com auto-loading via data attributes #}
<form id="athlete-form"
      method="post"
      data-loading
      data-loading-text="Salvando atleta..."
      data-loading-subtitle="Por favor, aguarde">

  {% csrf_token %}

  {# Campos do formulário #}

  <button type="submit" id="submit-btn">
    Salvar Atleta
  </button>
</form>
```

```javascript
document.getElementById('athlete-form')?.addEventListener('submit', function(e) {
  const submitBtn = document.getElementById('submit-btn');

  // Validação client-side
  const hasErrors = validateForm();

  if (hasErrors) {
    e.preventDefault();
    Loading.button(submitBtn, false);
    Loading.hidePage();
    return;
  }

  // Loading será mostrado automaticamente via data-loading
  Loading.button(submitBtn, true, 'Salvando...');
});
```

---

## Padrões de Design

### Animações

O componente usa 3 animações principais:

1. **Spin Slow** (1.5s): Anel externo rotaciona horário
2. **Spin Reverse** (1s): Anel interno rotaciona anti-horário
3. **Progress** (1.5s): Barra de progresso vai e volta

### Cores e Gradientes

Seguindo o design system AI Soccer:

- **Spinner primário**: `border-slate-700` com `border-t-transparent`
- **Spinner secundário**: `border-r-green-500` + `border-b-blue-500`
- **Glow interno**: `bg-gradient-to-br from-green-500/20 to-blue-500/20`
- **Overlay**: `bg-slate-950/90` com `backdrop-blur-sm`

### Acessibilidade

Todos os spinners incluem:

```html
<div role="status"
     aria-live="polite"
     aria-label="Carregando conteúdo">
```

---

## Casos de Uso Recomendados

### ✅ Use Loading Spinners Para:

1. **Operações de rede**
   - Requisições AJAX
   - Download de arquivos
   - Upload de imagens

2. **Processamento pesado**
   - Cálculos complexos
   - Geração de relatórios
   - Exportação de dados

3. **Navegação entre páginas**
   - Transições de rota
   - Carregamento de dashboards
   - Abertura de formulários

4. **Submissão de formulários**
   - Criação de registros
   - Atualização de dados
   - Validação assíncrona

### ❌ Não Use Para:

1. Operações instantâneas (< 200ms)
2. Validações simples client-side
3. Toggles e switches
4. Hover states
5. Animações decorativas

---

## Troubleshooting

### Loading não aparece

**Problema:** `Loading.show()` não funciona

**Soluções:**
1. Verifique se o `loading_id` está correto
2. Confirme que o componente foi incluído no template
3. Verifique console para erros JavaScript
4. Certifique-se que `loading.js` foi carregado

### Loading não esconde

**Problema:** Spinner fica travado na tela

**Soluções:**
1. Sempre chame `Loading.hide()` ou `Loading.hidePage()`
2. Use `try/catch` em operações assíncronas:
   ```javascript
   try {
     Loading.showPage();
     await operation();
   } finally {
     Loading.hidePage();
   }
   ```
3. Configure timeout de segurança:
   ```javascript
   Loading.showPage();
   setTimeout(() => Loading.hidePage(), 10000); // 10s max
   ```

### Botão não restaura

**Problema:** `Loading.button()` não restaura conteúdo original

**Solução:** Sempre passe o mesmo elemento de botão:
```javascript
const btn = document.getElementById('my-btn'); // Guarde referência
Loading.button(btn, true);
// ...
Loading.button(btn, false); // Use mesma referência
```

---

## Performance

### Best Practices

1. **Evite múltiplos overlays**: Use apenas 1 overlay de página por vez
2. **Debounce para AJAX**: Use debounce em buscas auto-complete
3. **Skeleton para listas**: Prefira skeleton screens para carregamento de listas
4. **Lazy loading**: Carregue spinners inline apenas quando necessário

### Métricas

- **Tamanho do componente**: ~2KB (HTML + CSS)
- **Tamanho do script**: ~8KB (JavaScript não minificado)
- **Performance de animação**: 60 FPS constante
- **Tempo de fade in/out**: 200ms

---

## Integração com Backend

### Django Views

Para operações longas, use loading page:

```python
from django.views.generic import FormView

class AthleteCreateView(FormView):
    template_name = 'performance/athlete_form.html'

    def form_valid(self, form):
        # Operação pesada aqui
        # Loading será mostrado via data-loading
        athlete = form.save()
        messages.success(self.request, 'Atleta salvo com sucesso!')
        return redirect('performance:athlete_list')
```

### AJAX Views

Para operações AJAX, retorne JSON:

```python
from django.http import JsonResponse

def search_athletes(request):
    query = request.GET.get('q', '')
    # Busca no banco
    athletes = Athlete.objects.filter(name__icontains=query)

    return JsonResponse({
        'success': True,
        'count': athletes.count(),
        'results': list(athletes.values())
    })
```

Frontend:

```javascript
async function searchAthletes(query) {
  Loading.showPage('Buscando atletas...');

  try {
    const response = await fetch(`/api/search?q=${query}`);
    const data = await response.json();
    displayResults(data.results);
  } catch (error) {
    console.error('Erro na busca:', error);
  } finally {
    Loading.hidePage();
  }
}
```

---

## Customização

### Modificar Cores

Edite `templates/components/loading.html`:

```html
{# Trocar verde-azul por roxo-rosa #}
<div class="border-r-purple-500 border-b-pink-500"></div>
<div class="bg-gradient-to-br from-purple-500/20 to-pink-500/20"></div>
```

### Adicionar Novos Estilos

Crie variantes no componente:

```django
{% if variant == 'small' %}
  <div class="w-12 h-12">{# Spinner pequeno #}</div>
{% elif variant == 'large' %}
  <div class="w-32 h-32">{# Spinner grande #}</div>
{% endif %}
```

### Estender API JavaScript

Adicione novos métodos em `static/js/loading.js`:

```javascript
Loading.toast = function(message, duration = 3000) {
  // Implementar toast com loading
};
```

---

## Checklist de Implementação

Ao adicionar loading em nova página:

- [ ] Incluir `{% include 'components/loading.html' %}` se necessário
- [ ] Adicionar IDs únicos aos elementos interativos
- [ ] Implementar handlers de loading em JavaScript
- [ ] Testar em diferentes resoluções (mobile, tablet, desktop)
- [ ] Verificar acessibilidade (ARIA labels)
- [ ] Confirmar que loading esconde em caso de erro
- [ ] Adicionar timeouts de segurança para operações longas
- [ ] Testar em navegadores diferentes (Chrome, Firefox, Safari)
- [ ] Documentar casos especiais no código

---

## Recursos Adicionais

- **Tailwind Animations**: https://tailwindcss.com/docs/animation
- **MDN ARIA**: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA
- **Loading Best Practices**: https://web.dev/loading-best-practices/

---

**Última atualização:** 2025-10-30
**Versão:** 1.0.0
**Mantido por:** Equipe AI Soccer
