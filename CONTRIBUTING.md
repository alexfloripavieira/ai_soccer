# Guia de Contribuição

## Antes de Começar

1. ✅ Leia a [Documentação](docs/README.md)
2. ✅ Configure o [ambiente de desenvolvimento](docs/instalacao.md)
3. ✅ Familiarize-se com o [PRD](PRD.md)

## Padrões de Código

### Leitura Obrigatória
- [Guia de Código](docs/coding-guidelines.md) - **LEIA PRIMEIRO!**
- [Design System](docs/design-system.md) - Para mudanças visuais
- [Arquitetura](docs/arquitetura.md) - Para entender a estrutura

### Princípios

1. **Simplicidade**: Código simples e direto, sem over-engineering
2. **PEP 8**: Seguir estritamente o guia de estilo Python
3. **Aspas Simples**: Usar sempre que possível
4. **Código em Inglês**: Variáveis, funções, classes
5. **Interface em Português**: Textos exibidos ao usuário

## Workflow de Contribuição

### 1. Criar Branch

```bash
# Feature
git checkout -b feat/nome-da-feature

# Bugfix
git checkout -b fix/nome-do-bug

# Documentação
git checkout -b docs/nome-da-doc
```

### 2. Desenvolver

- Siga o [Guia de Código](docs/coding-guidelines.md)
- Teste suas mudanças
- Mantenha commits pequenos e focados

### 3. Commit

Formato: `tipo(escopo): mensagem`

**Tipos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

**Exemplos**:
```bash
git commit -m "feat(performance): add athlete model"
git commit -m "fix(accounts): correct email validation"
git commit -m "docs: update coding guidelines"
```

### 4. Push e Pull Request

```bash
git push origin feat/nome-da-feature
```

## Checklist Antes de Commit

- [ ] Código segue PEP 8
- [ ] Variáveis e funções em inglês
- [ ] Textos de interface em português
- [ ] Aspas simples usadas
- [ ] Models têm `created_at` e `updated_at`
- [ ] Views protegidas com `LoginRequiredMixin`
- [ ] Imports organizados
- [ ] Sem código comentado
- [ ] Sem warnings

## O Que NÃO Fazer

❌ Não adicionar funcionalidades não solicitadas
❌ Não fazer over-engineering
❌ Não misturar idiomas (código em português)
❌ Não usar aspas duplas desnecessariamente
❌ Não fazer commits grandes demais
❌ Não deixar código comentado
❌ Não ignorar o guia de estilo

## Dúvidas?

Consulte a documentação:
- [README da Documentação](docs/README.md)
- [Glossário](docs/glossario.md)
- [PRD](PRD.md)

---

**Obrigado por contribuir!** 🚀
