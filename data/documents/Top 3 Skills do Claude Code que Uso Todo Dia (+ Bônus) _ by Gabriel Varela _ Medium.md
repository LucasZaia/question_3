# Top 3 Skills do Claude Code que Uso Todo Dia (+ Bônus)

> Conteúdo convertido a partir do HTML local fornecido pelo usuário.
>
> Fonte: 

## O Que São Skills do Claude Code?

Skills são instruções customizadas que você pode adicionar ao Claude Code para estender seu comportamento. Pense nelas como prompts reutilizáveis que ativam workflows específicos.

Você pode invocá-las com comandos como /review ou /grill-me, e o Claude segue as instruções definidas no arquivo da skill.

Algumas skills são built-in, outras vêm da comunidade. Aqui estão as que eu mais uso.

## 1. /review (Built-in)

Essa é uma skill built-in do Claude Code que faz code review de Pull Requests.

O que faz:

- Busca detalhes e diff do PR usando gh pr view e gh pr diff

- Analisa qualidade e estilo do código

- Identifica potenciais bugs, problemas de segurança e riscos

- Sugere melhorias específicas

- Verifica cobertura de testes e convenções do projeto

Quando eu uso: Antes de fazer merge de qualquer PR. Passo o número do PR e recebo uma revisão completa.

Exemplo:

```python
/review 42
```

Ou só /review pra listar PRs abertos primeiro, e depois escolher um pra revisar.

## 2. /grill-me

Essa skill vem da coleção de skills do Matt Pocock. É simples mas poderosa.

O que faz:

- Te entrevista implacavelmente sobre um plano ou design

- Percorre cada ramificação da sua árvore de decisões

- Te força a pensar em edge cases que você perdeu

- Se uma pergunta pode ser respondida explorando o codebase, ele explora ao invés de perguntar

A definição completa da skill:

```python
Interview me relentlessly about every aspect of this plan until we
reach a shared understanding. Walk down each branch of the design
tree, resolving dependencies between decisions one by one.

And finally, if a question can be answered by exploring the code
base, explore the code base instead.
```

Quando eu uso: Antes de implementar qualquer coisa complexa. Eu descrevo meu plano, digito /grill-me, e o Claude faz stress-test no meu raciocínio. É como ter um engenheiro sênior revisando sua arquitetura antes de escrever uma linha de código.

Exemplo:

```python
Estou pensando em implementar offline-first no nosso app React Native.
Usaríamos WatermelonDB para storage local e sync quando voltar online.

/grill-me
```

O Claude vai perguntar coisas como: “O que acontece quando o usuário edita o mesmo registro offline em dois dispositivos?”, “Como você lida com resolução de conflitos durante o sync?”, “Qual sua estratégia para datasets grandes que não cabem na memória?“

## 3. /caveman

Também do Matt Pocock. Essa economiza tokens e mantém as respostas enxutas.

O que faz:

- Modo de comunicação ultra-comprimido

- Remove palavras de preenchimento, artigos e gentilezas

- Mantém toda a substância técnica intacta

- Corta o uso de tokens em ~75%

O estilo:

## Get Gabriel Varela’s stories in your inbox

Não: “Claro! Ficarei feliz em ajudar você com isso. O problema que você está enfrentando provavelmente é causado por…”

Sim: “Bug in auth middleware. Token expiry check use < not <=. Fix:“

Regras que segue:

- Remove artigos (a/an/the)

- Remove preenchimento (just/really/basically/actually)

- Remove gentilezas (sure/certainly/of course)

- Abrevia termos comuns (DB/auth/config/req/res/fn/impl)

- Usa setas para causalidade (X -> Y)

Quando eu uso: Quando estou deep numa sessão de debug e não preciso de explicações. Só respostas.

Exemplo:

```python
/caveman

Why is my FlatList re-rendering all items when I update one?
```

Resposta: “keyExtractor return index -> all items re-render on data change. Use unique id. Wrap renderItem in memo.”

Para desligar: “stop caveman” ou “normal mode”.

## BÔNUS: /grill-with-docs

Essa é a versão evoluída do /grill-me. Mesmo questionamento implacável, mas com superpoderes de documentação.

O que adiciona:

- Desafia seu plano contra seu modelo de domínio existente

- Faz referência cruzada com seu código real (“Seu código faz X, mas você acabou de dizer Y. Qual está certo?“)

- Atualiza CONTEXT.md inline conforme termos são resolvidos

- Oferece criar ADRs (Architecture Decision Records) quando você toma decisões importantes

Comportamentos principais:

- Se você usa um termo que conflita com seu glossário, ele aponta imediatamente

- Se você usa termos vagos, ele propõe termos canônicos precisos

- Ele faz stress-test em relacionamentos com cenários concretos

Quando eu uso: Para decisões arquiteturais maiores onde eu quero que a conversa também produza documentação. As decisões que eu tomo ficam registradas, então o eu do futuro (ou colegas) entendem por que fizemos as coisas de determinada forma.

## Como Adicionar Essas Skills

- Crie uma pasta .claude/skills/ no seu projeto

- Adicione um arquivo SKILL.md para cada skill

- Use o formato de frontmatter:

```python
---
name: nome-da-skill
description: Quando usar essa skill
---
Suas instruções aqui...
```

Você pode encontrar a coleção completa de skills do Matt Pocock no GitHub: mattpocock/claude-code-skills

## Conclusão

Essas quatro skills cobrem a maior parte do meu workflow diário:

- /review para pegar problemas antes de PRs

- /grill-me para stress-test de planos

- /caveman para respostas rápidas e eficientes em tokens

- /grill-with-docs para decisões arquiteturais que precisam de documentação

A melhor parte? Você pode criar suas próprias skills para workflows repetitivos. Se você se pega dando as mesmas instruções pro Claude repetidamente, isso é uma skill esperando pra ser escrita.
