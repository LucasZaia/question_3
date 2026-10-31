# O que Anthropic, OpenAI e Google concordam sobre contexto (e por que você deveria prestar atenção)

> Conteúdo convertido a partir do HTML local fornecido pelo usuário.
>
> Fonte: 

Tem um tipo de conversa que tem se repetido com frequência: alguém próximo me dizendo que o Claude Code piorou, que o modelo “foi nerfado”, que tá tendo que refazer tudo na mão. No mesmo dia, outro alguém me dizendo que nunca produziu tanto na vida. Mesma ferramenta. Mesmo modelo.

Eu fiquei curioso. Não pelo resultado em si — isso eu já sabia, já escrevi sobre spec-driven, sobre context window, sobre code review com agente. O que pegou foi outra coisa: por que as pessoas tratam cada uma dessas práticas como dica isolada, quando na real elas são peças de uma mesma engenharia?

Fui puxar o fio. E descobri que essa engenharia tem nome: harness.

## O que é harness

A primeira vez que eu ouvi “harness” nesse contexto foi numa discussão sobre ferramentas de agentic coding. Alguém perguntou se uma ferramenta nova valia os $200/mês, e a resposta foi: “o modelo por baixo é o mesmo Sonnet que o Cursor usa. O que eles vendem é o harness.”

Eu não entendi na hora. Depois caiu a ficha.

Traduzir harness pro português é ingrato. Literalmente é “arnês” — aquela coisa que você veste num cavalo pra prender na carroça. Forçando a barra, dá pra dizer “arcabouço” ou “estrutura de apoio”. Mas nenhum termo em pt-BR captura direito o que a palavra carrega em contexto técnico, então vou usar harness mesmo ao longo do texto.

Pensa num motor de carro. Um V8 biturbo, 600cv, lindão. Agora imagina esse motor no chão da garagem, sem carro ao redor. Ele faz barulho, esquenta, gira — mas não te leva a lugar nenhum. Pra ele ser útil, precisa de chassi, direção, câmbio, freio, suspensão, painel. Precisa de um carro.

O modelo de IA é o motor. Potente, impressionante, capaz de coisas absurdas. Mas sozinho, é uma API que recebe texto e devolve texto.

O harness é o carro. É toda a engenharia ao redor do modelo que transforma potência bruta em resultado: as instruções persistentes do projeto, como o agente decide quais arquivos ler, como ele quebra uma tarefa grande em passos, como ele valida o próprio output antes de te devolver, como ele aplica o diff no arquivo certo. O harness é direção, câmbio, freio e GPS — tudo junto.

Quando a gente configura um CLAUDE.md (ou AGENTS.md, ou GEMINI.md — já chego lá), escreve uma spec, define critério de aceite, separa skills por workflow — a gente tá montando o carro ao redor do motor.

E aqui vem a parte que eu acho mais interessante: a Anthropic, a OpenAI e o Google chegaram na mesma conclusão sobre como montar esse carro. Sem combinar.

## Antes: o que eu aprendi quebrando a cara

Mas antes de falar das três empresas, deixa eu contar o que aconteceu quando eu achei que “mais contexto = melhor resultado.”

Eu tava montando um projeto pro curso que eu tô desenvolvendo na Alura e resolvi ser caprichoso. Criei um CLAUDE.md com umas 300 linhas. Padrões de API, convenções de teste, checklist de review, guia de commit, padrões de naming, decisões arquiteturais, referências de libs. Um documento bonito, completo, detalhado.

E o agent ficou pior.

Nas primeiras interações, lindo. Seguia tudo à risca. Aí a conversa crescia — eu lia arquivos, rodava comandos, fazia edições — e lá pela interação 15, o agent gerava um endpoint que ignorava metade das regras. Não porque ele “esqueceu”. Por outro motivo.

Existe um fenômeno chamado “lost in the middle”. LLMs dão mais peso pra informação que tá no começo e no final da context window. O miolo perde relevância relativa. E adivinha onde as suas 300 linhas de instrução ficam conforme a conversa cresce? No miolo.

Pensa assim: é como um dev que leu o onboarding doc no primeiro dia. Depois de 8 horas debugando um problema específico, as convenções ficam no fundo da cabeça. Ele não esqueceu que existem — a atenção tá em outro lugar.

E piora. Quando a context window chega em uns 83% de uso, o Claude Code compacta automaticamente — cria um resumo de tudo que rolou até ali pra liberar espaço. E nessa compactação, detalhes finos das instruções viram poeira. O agent “sabe” que tem padrão de commit — mas o formato exato? Diluiu no resumo.

Quando eu cortei o CLAUDE.md pra 47 linhas e movi o resto pra skills (já explico), a diferença foi imediata. O agent voltou a seguir as convenções até em sessões longas.

A partir daí eu passei a tratar o CLAUDE.md como constituição: poucas regras universais, cirurgicamente editadas. Pra cada linha, um teste simples: “o agent erraria sem isso?” Se a resposta é não, a linha é ruído. Deletei.

## O que a Anthropic diz (e por que eu concordo)

A Anthropic publicou um post chamado “Effective context engineering for AI agents” que virou referência. A tese central: construir com LLMs não é mais sobre encontrar as palavras certas pro prompt. É sobre responder outra pergunta — “que configuração de contexto tem maior probabilidade de gerar o comportamento desejado?”

Os pontos que mais marcaram:

Eles falam de uma “Goldilocks zone” pra instruções — nem genérico demais (o agente não sabe o que fazer), nem específico demais (lógica hardcoded que quebra no primeiro caso diferente). Eu vivi os dois extremos. “Cria um endpoint” é genérico demais. “Cria um endpoint POST /api/v1/auth/login que recebe email e password no body como JSON, valida com class-validator, busca o usuário no banco usando TypeORM…” é específico demais — você tá escrevendo o código em português em vez de deixar o agente trabalhar.

O sweet spot, na minha experiência, é descrever o comportamento que você espera. “O endpoint de login deve receber credenciais, validar contra o banco, retornar um JWT com refresh token, e seguir o padrão de response dos outros endpoints do projeto.” O agente olha os outros endpoints, infere o padrão, e produz algo consistente.

Eles também falam de “context rot” — conforme o número de tokens cresce, a atenção do modelo se espalha e a qualidade cai. Não é bug, é limitação arquitetural. Cada token compete com todos os outros por um orçamento finito de atenção. A janela de contexto pode ser enorme — 200k tokens — mas isso não quer dizer que ele presta atenção igual em todos os 200k. É como uma sala de aula com 200 alunos: o professor não consegue dar atenção individual pra cada um, mesmo que todos caibam na sala.

O mecanismo prático disso no Claude Code é o CLAUDE.md — um arquivo markdown na raiz do projeto que o agente lê no início de cada sessão. Aqui tá o meu, simplificado:

```python
# Claude.md
## Stack
- frontend: react 19 + vite + typescript
- backend: nestjs + typeorm + postgresql
- monorepo: pnpm workspaces
- containers: docker compose
## Comandos
- build: `pnpm -r build`
- test backend: `pnpm --filter backend test`
- test frontend: `pnpm --filter frontend test`
- lint: `pnpm -r lint`
## Convenções
- módulos nestjs: um module por domínio, nunca misturar
- responses: sempre { data, meta, error } - sem exceção
- nomes de variável e função em inglês, comentários em pt-BR
- commits: conventional commits, scope obrigatório
## Não faça
- não crie barrel files (index.ts reexportando)
- não use any - se não sabe o tipo, pergunte
- não instale lib nova sem perguntar antes
```

Poucas linhas. Cabe numa tela, sem scroll. E a regra é: se eu não consigo explicar por que uma linha tá ali, ela não deveria estar ali.

## O que a OpenAI diz (e o que muda)

A OpenAI lançou o Codex e publicou um guia de boas práticas que poderia ter sido escrito pelo time da Anthropic de tão parecido.

## Get Vinicios Neves’s stories in your inbox

A primeira recomendação? Cria um AGENTS.md no repositório. Literalmente o mesmo conceito do CLAUDE.md, com outro nome. Mesma hierarquia: global (no home do usuário), projeto (na raiz do repo), e por diretório (overrides mais específicos). O agente concatena tudo e lê antes de começar qualquer tarefa.

```python
# AGENTS.md (exemplo da doc da OpenAI)
## Working agreements
- always run `npm test` after modifying javascript files
- prefer `pnpm` when installing dependencies
- ask for confirmation before adding new production dependencies
```

Parece familiar, né?

Mas tem um ponto onde a OpenAI bate mais forte que a Anthropic: verificação.

O guia deles é direto: “não pare em pedir uma mudança. Peça pro agente confirmar que a mudança funciona.” Sem critério de aceite explícito, o agente produz código confiante que é sutilmente errado. Ele te devolve um endpoint lindo que compila, tem naming bonito — e retorna 200 quando deveria retornar 201. Porque você não disse o que “pronto” significava.

Dentro da OpenAI, o Codex roda code review em 100% dos PRs. E funciona porque os times escrevem testes primeiro e referenciam os comandos de teste no AGENTS.md. O agente sabe o que rodar pra verificar. Sem isso, é chute.

O AGENTS.md, aliás, virou padrão aberto — mantido pela Agentic AI Foundation dentro da Linux Foundation, com apoio do Google, Cursor, Sourcegraph e Factory. Não é mais coisa de uma empresa só. É o mais perto que a indústria chegou de um .editorconfig pra agentes de IA.

## O que o Google diz (e o que eles adicionaram)

O Google Gemini CLI usa GEMINI.md. Mesmo formato markdown, mesma hierarquia — global, projeto, diretório. Mas eles adicionaram duas coisas que eu acho particularmente elegantes.

A primeira: discovery sob demanda. Quando o agente do Gemini acessa um arquivo ou diretório, ele automaticamente escaneia por GEMINI.md naquele caminho e nos pais dele. Isso significa que você pode ter instruções super específicas pra um módulo — tipo “nessa pasta, todos os componentes são server components do Next.js, não use hooks de estado” — sem poluir o contexto global. O agente só descobre essas instruções quando precisa delas.

A segunda: o comando /memory show. Ele mostra o texto exato que o modelo tá recebendo como contexto persistente naquela sessão. É o debug que resolve a pergunta "por que o agente tá ignorando minha regra?" — na maioria das vezes, a regra simplesmente não tá no contexto. Não é que ele desobedeceu; é que ele nunca viu.

E um engenheiro do Google publicou um post no Medium contando exatamente o que eu vivi: criou um GEMINI.md gigantesco com todas as instruções possíveis pra todos os cenários. O agente ficou inconsistente, lento e errado. O diagnóstico dele: “context bloat” causando “context rot”. A solução: modularizar e entregar instruções sob demanda, no momento certo, pro cenário certo.

Ele chamou o padrão de “gated execution through delayed instructions” — basicamente, um if/else de contexto. Se a task é sobre API, carrega as instruções de API. Se é sobre teste, carrega as de teste. Se é sobre deploy, carrega as de deploy. Nunca tudo junto.

## O consenso

Quando você coloca as três empresas lado a lado, o alinhamento é quase perturbador:

Contexto persistente em markdown. CLAUDE.md, AGENTS.md, GEMINI.md — três nomes, mesma coisa. Um arquivo que o agente lê antes de trabalhar, com as regras do jogo. Versionado no repo, compartilhado com o time.

Hierarquia. Global → projeto → diretório → tarefa. Do mais genérico pro mais específico, com override. Instruções de diretório ganham de instruções globais.

Menos é mais. As três empresas falam de modularização, de carregar sob demanda, de manter o arquivo principal curto. O melhor contexto é o menor conjunto de tokens com o maior sinal possível.

Verificação é contexto. Dizer pro agente o que “pronto” significa — quais testes rodar, quais checks passar — é tão importante quanto dizer o que ele deve fazer. Sem isso, o agente chuta.

Skills > promptão. Instruções modulares que carregam quando relevante em vez de um documento monolítico que consome tokens o tempo todo.

## Na prática: como eu monto o harness de um projeto

Vou abrir o jogo do que eu uso no Hermex Locadora, o projeto integrador do curso que eu tô montando.

A primeira camada é o CLAUDE.md — aquele de 47 linhas que eu mostrei ali em cima. Onboarding permanente. O agente lê no início de cada sessão e sabe: qual a stack, como buildar, como testar, quais convenções seguir, o que não fazer.

A segunda camada são as skills, em .claude/skills/:

```python
.claude/skills/
├── api-conventions/
│   └── SKILL.md      # padrão de rotas, responses, error handling
├── testing/
│   └── SKILL.md      # o que testar, como nomear, quando mockar
└── review/
    └── SKILL.md      # checklist de review antes de abrir PR
```

Cada skill tem umas 30–40 linhas. Focada num workflow. E a chave: o agente só carrega a skill quando detecta que a task é relevante. Pedir pra criar um endpoint? Carrega api-conventions. Pedir pra escrever teste? Carrega testing. Fazendo uma task de CSS? Não carrega nenhuma das duas. Mais espaço na context window pra focar na tarefa real.

A terceira camada é a spec. Antes de qualquer task, eu escrevo no Linear:

```python
## Contexto
O Hermex ainda não tem autenticação. Todos os endpoints são públicos.
## O que precisa ser feito
Endpoint de login que recebe email e senha, valida contra o banco,
retorna JWT + refresh token. Endpoint de refresh que renova o JWT
usando o refresh token.
## Restrições
- seguir o padrão de response do projeto ({ data, meta, error })
- refresh token com expiração de 7 dias, JWT com 15 minutos
- não criar migration nova - usar a tabela users que já existe
- não instalar lib de auth pronta - quero entender o fluxo
## Critério de aceite
- `pnpm --filter backend test` passa
- POST /auth/login retorna 200 com tokens válidos
- POST /auth/login com credencial inválida retorna 401
- POST /auth/refresh com token válido retorna novo JWT
- POST /auth/refresh com token expirado retorna 401
```

O agente sabe o que fazer (spec), como fazer (skill), e dentro de que regras (CLAUDE.md). Três camadas, cada uma no lugar certo, cada uma com o escopo certo.

Isso é um harness.

## Por que isso importa mais do que o modelo

O DHH falou recentemente que usar agente de IA parece menos “gerenciar projeto” e mais “vestir uma mech suit”. Eu gosto da metáfora, mas ela esconde uma coisa: a mech suit não vem pronta. Você monta ela. Peça por peça.

E é por isso que dois devs usando o mesmo modelo têm resultados radicalmente diferentes. O motor é idêntico. O carro ao redor é que muda tudo. Um tá numa Ferrari com direção precisa, suspensão calibrada, GPS atualizado. O outro tá num kart sem freio.

O cara que reclamava que o modelo “piorou”? Mandei ele ler o post da Anthropic sobre context engineering, montar um CLAUDE.md de 50 linhas, e escrever uma spec de uma página antes de abrir o terminal. Uma semana depois ele me mandou: “cara, parece outro modelo.”

Não era. Era o mesmo motor. Só que agora dentro de um carro.

Vinicios Neves

·

Dec 4, 2025

## A verdade que ninguém te conta sobre Vue vs React (e que vai doer)

### Salve o/

Vinicios Neves

·

Sep 7, 2023

## Entenda de Vez o hook useEffect e transforme seu código React

### Você já ouviu falar do useEffect no universo React? Se sim, bacana! Se não, vem comigo nessa viagem que vou te apresentar esse hook mágico…

Vinicios Neves

·

May 27, 2025

## Product Engineer: a nova cara da engenharia de software?

### Nos últimos tempos, tem pipocado por aí um termo que talvez você já tenha escutado: Product Engineer. Seja em vagas no LinkedIn, em…

Vinicios Neves

·

Jan 27

## O fim das especializações? Como a IA está transformando o que significa ser dev

### Eu lembro quando comecei a ouvir falar de programação. Existia uma figura quase mítica chamada “o programador” — alguém que dominava a…

In

The Daily Draft

by

Matt Lillywhite

·

Jul 7

## I’ll Instantly Know A Writer Used ChatGPT When I See This

### It’s pretty damn obvious now that I know what to look for.

Darius Foroux

·

May 8

## How to Do Hard Things When You Have Zero Motivation

### Tricks create novelty. These five strategies create consistency.

In

The Sunday Journal

by

Rafia Naseem

·

Jul 18

## 10 Websites Better Than Another Hour of Doomscrolling

### Here’s to the rabbit holes worth taking!

Tomas Pueyo

·

Jun 8

## How Did Islam Spread So Fast?

### In the 600s AD, Mecca was a village of a few hundred people, off the beaten path, a backwater uninteresting to distant empires. Then along…

Thomas Oppong

·

Jun 13

## This is Feynman’s Thinking Habit. It Made Him a Genius

### Think 10x clearer with this simple mental trick.

Mallick Speaks

·

Oct 3

## Sex for Rent in Germany: The Hidden Risk Behind the Housing Shortage

### A student arriving in Munich with €380 available for housing faces an awkward piece of arithmetic. The median room in a shared flat now…
