# Busca Semântica

Sistema de busca semântica usando LangChain, embeddings da OpenAI e Pinecone como banco vetorial (vector store).

## Configuração

Instale as dependências:

```bash
uv sync --extra dev
```

Copie o arquivo de ambiente e informe as chaves da OpenAI e do Pinecone:

```bash
cp .env.example .env
```

Preencha `OPENAI_API_KEY` e `PINECONE_API_KEY` no arquivo `.env`.

## Comandos

Indexar os documentos:

```bash
./scripts/ingest_documents.sh
```

Faça uma busca semântica:

```bash
./scripts/search_documents.sh "Como consultar o uso de memória no Linux?"
```

Ou execute sem parâmetros para digitar a consulta no terminal:

```bash
./scripts/search_documents.sh
Digite o que deseja buscar: Como consultar o uso de memória no Linux?
```

Exemplos de consultas para os cinco documentos:

```bash
# LlamaIndex
./scripts/search_documents.sh "Como conectar documentos a LLMs usando LlamaIndex?"

# Arquitetura da informação
./scripts/search_documents.sh "Como organizar o conteúdo de uma interface?"

# Contexto em modelos de linguagem
./scripts/search_documents.sh "Por que o contexto é importante para os modelos de linguagem?"

# RAG
./scripts/search_documents.sh "Quais são as principais técnicas de RAG?"

# Claude Code
./scripts/search_documents.sh "Quais skills do Claude Code podem melhorar o desenvolvimento?"
```

Espera-se que cada consulta retorne, entre os primeiros resultados, o documento relacionado ao tema pesquisado.

## Avaliação de relevância

Execute:

```bash
./scripts/evaluate_search.sh --limit 5
```

## Limpar o índice

```bash
./scripts/clear_pinecone.sh
```

O script exige que você digite `DELETE` para confirmar. Para execução automatizada:

```bash
./scripts/clear_pinecone.sh --yes
```

## Testes

```bash
uv run python -m pytest -q
```

## Converter HTML para Markdown

Se os documentos ainda estiverem em HTML, converta-os de `docs_extractor/` para Markdown em `data/documents/`:

```bash
./scripts/convert_article_html.sh
```

## Como o sistema funciona

### 1. Processamento dos documentos

Os arquivos HTML são convertidos para Markdown pelo script acima. Em seguida, cada documento é dividido em chunks de até 800 caracteres, com sobreposição de 120 caracteres entre chunks consecutivos. A sobreposição reduz a perda de contexto nas divisões do texto.

### 2. Ingestão dos documentos

Na ingestão, cada chunk é convertido em um vetor pela API de embeddings da OpenAI. Os vetores, o conteúdo e os metadados dos chunks são então indexados no Pinecone.

### 3. Busca semântica

Quando o usuário realiza uma consulta, o texto é convertido em um embedding pelo mesmo modelo utilizado na ingestão. Assim, a consulta e os documentos ficam representados no mesmo espaço vetorial.

O Pinecone compara o vetor da consulta com os vetores dos chunks armazenados e retorna os trechos mais próximos, acompanhados dos respectivos scores de similaridade. O `SearchService` transforma esses dados em resultados com posição no ranking, score, fonte e conteúdo do chunk. Na busca vetorial, as primeiras posições representam maior proximidade semântica. O score exibido é o score original do Pinecone e não uma porcentagem.

### 4. Reranking

A busca vetorial pode retornar um trecho relevante em uma posição inferior do ranking. Para melhorar essa ordenação, os candidatos são enviados a um modelo da OpenAI com instruções específicas para avaliar a relação entre a consulta e cada trecho. O modelo pode reordenar os resultados, colocando os conteúdos mais relevantes nas primeiras posições. Nesse caso, a posição exibida é a posição final do reranking, enquanto o score continua sendo o score original do Pinecone.

### Fluxo completo

```text
                         INDEXAÇÃO

┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ HTML        │ → │ Markdown    │ → │ Chunks      │
│ docs_extractor│  │ documentos  │   │ 800 / 120   │
└─────────────┘   └─────────────┘   └──────┬──────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ Embeddings     │
                                  │ OpenAI         │
                                  └──────┬─────────┘
                                         │
                                         ▼
                                  ┌────────────────┐
                                  │ Ingestão       │
                                  │ IDs + metadados│
                                  └──────┬─────────┘
                                         │
                                         ▼
                                  ┌────────────────┐
                                  │ Pinecone       │
                                  │ vector store   │
                                  └──────┬─────────┘
                                         │
                         CONSULTA       │

┌─────────────┐   ┌─────────────┐   ┌───▼─────────┐   ┌─────────────┐
│ Pergunta    │ → │ Embedding   │ → │ Busca       │ → │ Candidatos  │
│ do usuário  │   │ da consulta │   │ vetorial    │   │ + scores    │
└─────────────┘   └─────────────┘   └─────────────┘   └──────┬──────┘
                                                            │
                                                            ▼
                                                   ┌────────────────┐
                                                   │ Reranking       │
                                                   │ opcional/OpenAI │
                                                   └──────┬─────────┘
                                                          │
                                                          ▼
                                                   ┌────────────────┐
                                                   │ Resultados      │
                                                   │ rank + fonte    │
                                                   └────────────────┘
```
