# Agentes e RAG com LlamaIndex. Como ligar seu conteúdo a LLMs e…

> Conteúdo convertido a partir do HTML local fornecido pelo usuário.
>
> Fonte: 

## Como ligar seu conteúdo a LLMs e habilitar ferramentas de agente com Python e

## Introdução

LlamaIndex é um framework para construir apps de IA conectados aos seus dados (PDFs, pastas, bancos, S3…). Ele resolve o essencial do RAG (ingestão → indexação vetorial → recuperação → resposta com contexto) e também oferece agentes com ferramentas (query engines, planejadores, ReAct/Function Agents).

Tradução prática: em poucas linhas você lê arquivos, cria um índice vetorial e passa a perguntar para seus documentos — e, quando precisar, um agente escolhe ferramentas (retrievers, consultas específicas) para responder melhor.

## Por que LlamaIndex?

- RAG plug-and-play: leitores de dados, divisão em chunks, embeddings, índices e retrievers prontos.

- Agentes nativos: ReActAgent/FunctionAgent com QueryEngineTool para o agente usar seus índices como ferramentas.

- Ecosistema amplo: integrações via pacotes (LLMs, embeddings, vetores).

- Servir/escala: guias de deploy, async e serviços (LlamaCloud/LlamaParse) quando quiser subir o nível.

## Instalação

```python
# pacote "starter" (inclui core + integrações básicas)
pip install llama-index

# ou instalação modular:
# pip install llama-index-core
```

Configure sua chave (se usar OpenAI): export OPENAI_API_KEY="sua_chave" — caso contrário você verá erro de credencial. LlamaIndex+2GitHub+2

## Exemplos práticos

### Exemplo 1 — RAG básico sobre uma pasta (PDFs, DOCX, TXT)

Objetivo: carregar arquivos locais, indexar e fazer perguntas com contexto.

```python
# rag_basico.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI

# 1) Carregar documentos da pasta ./docs
docs = SimpleDirectoryReader("./docs").load_data()
# 2) Construir índice vetorial
index = VectorStoreIndex.from_documents(docs)
# 3) Criar um Query Engine (camada de perguntas)
engine = index.as_query_engine(llm=OpenAI(model="gpt-4o"))
# 4) Perguntar
print(engine.query("Quais são as políticas de segurança descritas nos documentos?"))
```

Como funciona: o SimpleDirectoryReader decide o melhor leitor por extensão; o VectorStoreIndex cria o índice vetorial; o query_engine faz a recuperação + chamada ao LLM.

Dica: rode em async para maior throughput quando usar LLMs/IO.

### Exemplo 2 — Agente com ferramentas de consulta (ReAct/Function)

Objetivo: dar ao agente “ferramentas” (query engines) para ele decidir onde buscar a resposta.

```python
# agente_query_tools.py
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.react import ReActAgent
from llama_index.llms.openai import OpenAI

# Índices especializados (ex.: relatórios de 2024 e 2025)
idx_2024 = VectorStoreIndex.from_documents(SimpleDirectoryReader("./docs/2024").load_data())
idx_2025 = VectorStoreIndex.from_documents(SimpleDirectoryReader("./docs/2025").load_data())
# Cada índice vira uma "tool" consultável
tool_2024 = QueryEngineTool.from_defaults(
    query_engine=idx_2024.as_query_engine(llm=OpenAI(model="gpt-4o")),
    name="docs_2024",
    description="Consultas a documentos do ano de 2024"
)
tool_2025 = QueryEngineTool.from_defaults(
    query_engine=idx_2025.as_query_engine(llm=OpenAI(model="gpt-4o")),
    name="docs_2025",
    description="Consultas a documentos do ano de 2025"
)
# Agente com loop ReAct e ferramentas
agent = ReActAgent.from_tools([tool_2024, tool_2025], llm=OpenAI(model="gpt-4o"))
# O agente escolhe a ferramenta e responde
resp = agent.chat("Comparar políticas de segurança 2024 vs 2025 e resumir diferenças.")
print(resp)
```

Se usar function calling (OpenAI), prefira FunctionAgent com tools=[...]. Exemplo ReAct com 10-K de Lyft/Uber na doc: ótimo para entender o padrão “ferramenta = query engine”.

## Variantes úteis (quando subir a complexidade)

- Parsing avançado (OCR/estruturas complicadas): (serviço).

- Vector stores externos: plugar Milvus, Qdrant, Chroma, Pinecone (via integrações).

- Planejamento/Agentes: Query Planning + Agents para compor consultas complexas.

- Cloud & Workflows duráveis: LlamaAgents/LlamaCloud para servir workflows com espera por sinais externos/UI.

## Troubleshooting rápido

- ValueError: No API key found for OpenAI → exporte OPENAI_API_KEY.

- PDFs sem texto → faça OCR antes (ou use LlamaParse).

- Custo/latência → troque para gpt-4o-mini, limite tokens e tamanho de chunk, use async.

## Conclusão

O encurta o caminho entre seus dados e respostas úteis: do RAG básico (leitor + índice + pergunta) até agentes capazes de escolher qual índice/ferramenta usar a cada pergunta. Comece com o Exemplo 1 (pasta → índice → pergunta). Em seguida, evolua para o Exemplo 2 (agente + ferramentas). Se precisar de parsing pesado, conecte LlamaParse; para produção, sirva com FastAPI + Docker e um vector store dedicado.

Até a próxima!
