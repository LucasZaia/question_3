# RAG: O Guia Completo das Técnicas Avançadas de Retrieval-Augmented Generation Para 2025

> Conteúdo convertido a partir do HTML local fornecido pelo usuário.
>
> Fonte: 

O Retrieval-Augmented Generation (RAG) representa uma das maiores inovações em processamento de linguagem natural e inteligência artificial generativa. Esta tecnologia combina a capacidade de recuperação de informações com a geração de texto por modelos de linguagem, criando sistemas mais precisos, atualizados e confiáveis.

## Get Gustavo Tavares’s stories in your inbox

Neste artigo completo, exploraremos as técnicas avançadas de RAG que estão moldando o futuro da IA conversacional, chatbots inteligentes e sistemas de busca semântica. Abordaremos implementações práticas de CRAG, CAG, Graph RAG, Agentic RAG, Adaptive RAG, Multi Modal RAG e W-RAG.

### O que é RAG? Fundamentos e Arquitetura

RAG (Retrieval-Augmented Generation) é uma arquitetura de machine learning que combina:

- Sistema de Recuperação: Busca informações relevantes em bases de conhecimento.

- Modelo Generativo: Produz respostas baseadas nas informações recuperadas.

- Mecanismo de Fusão: Integra conhecimento externo com capacidades generativas.

Arquitetura Básica do RAG

```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline

class BasicRAG:
    def __init__(self, documents, model_name="all-MiniLM-L6-v2"):
        self.documents = documents
        self.encoder = SentenceTransformer(model_name)
        self.generator = pipeline("text-generation",
                                model="microsoft/DialoGPT-medium")
        self.build_index()

    def build_index(self):
        """Constrói índice FAISS para busca semântica"""
        embeddings = self.encoder.encode(self.documents)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))

    def retrieve(self, query, k=3):
        """Recupera documentos relevantes"""
        query_embedding = self.encoder.encode([query])
        scores, indices = self.index.search(
            query_embedding.astype('float32'), k
        )
        return [self.documents[i] for i in indices[0]]

    def generate(self, query, context):
        """Gera resposta baseada no contexto"""
        prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
        response = self.generator(prompt, max_length=200)
        return response[0]['generated_text']
```

### 1. CRAG (Corrective Retrieval-Augmented Generation)

CRAG é uma evolução do RAG tradicional que incorpora mecanismos de correção para melhorar a qualidade da recuperação de informações. Esta técnica é essencial para sistemas de QA empresariais e assistentes virtuais que requerem alta precisão. A seguir, apresenta-se um exemplo de implementação do CRAG.

```python
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

class CRAG:
    def __init__(self, documents, confidence_threshold=0.7):
        self.documents = documents
        self.threshold = confidence_threshold
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        self.build_embeddings()

    def build_embeddings(self):
        """Constrói embeddings para documentos"""
        self.doc_embeddings = []
        for doc in self.documents:
            inputs = self.tokenizer(doc, return_tensors='pt',
                                  truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1)
                self.doc_embeddings.append(embedding.numpy())

    def corrective_retrieve(self, query, k=5):
        """Recuperação com correção baseada em confiança"""
        # Embedding da query
        query_inputs = self.tokenizer(query, return_tensors='pt',
                                    truncation=True, padding=True)
        with torch.no_grad():
            query_outputs = self.model(**query_inputs)
            query_embedding = query_outputs.last_hidden_state.mean(dim=1)

        # Cálculo de similaridade
        similarities = []
        for doc_emb in self.doc_embeddings:
            sim = cosine_similarity(query_embedding.numpy(), doc_emb)[0][0]
            similarities.append(sim)

        # Seleção corretiva
        top_indices = np.argsort(similarities)[-k:][::-1]
        corrected_docs = []

        for idx in top_indices:
            if similarities[idx] > self.threshold:
                corrected_docs.append({
                    'document': self.documents[idx],
                    'confidence': similarities[idx]
                })

        # Se não há documentos confiáveis, busca externa
        if not corrected_docs:
            return self.external_search(query)

        return corrected_docs

    def external_search(self, query):
        """Busca externa quando confiança é baixa"""
        # Implementação de busca web ou base externa
        return [{'document': f"External search result for: {query}",
                'confidence': 0.5}]
```

Aplicações Práticas do CRAG

- Sistemas de Suporte Técnico: Correção automática de respostas imprecisas.

- Chatbots Médicos: Validação de informações críticas.

- Assistentes Jurídicos: Verificação de precedentes legais.

### 2. CAG (Chain-of-Thought Augmented Generation)

CAG integra raciocínio em cadeia com recuperação de informações, permitindo reasoning complexo e resolução de problemas multi-etapas. É fundamental para IA explicável e sistemas de tutoria inteligente. A seguir, será apresentado um exemplo de implementação do CAG.

```python
class ChainOfThoughtRAG:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.reasoning_steps = []

    def decompose_query(self, complex_query):
        """Decompõe query complexa em sub-problemas"""
        decomposition_prompt = f"""
        Decomponha a seguinte pergunta complexa em etapas menores:
        Pergunta: {complex_query}

        Etapas:
        1.
        2.
        3.
        """
        # Usar LLM para decomposição
        steps = self.llm_decompose(decomposition_prompt)
        return steps

    def chain_retrieve_and_reason(self, query):
        """Executa raciocínio em cadeia com recuperação"""
        steps = self.decompose_query(query)
        reasoning_chain = []

        for i, step in enumerate(steps):
            # Recupera informações para cada etapa
            relevant_docs = self.retrieve_for_step(step)

            # Raciocina sobre a etapa atual
            step_reasoning = self.reason_step(step, relevant_docs,
                                            reasoning_chain)

            reasoning_chain.append({
                'step': i + 1,
                'question': step,
                'evidence': relevant_docs,
                'reasoning': step_reasoning
            })

        # Síntese final
        final_answer = self.synthesize_chain(reasoning_chain, query)
        return final_answer, reasoning_chain

    def reason_step(self, step, evidence, previous_reasoning):
        """Executa raciocínio para uma etapa específica"""
        context = "\n".join([doc['content'] for doc in evidence])
        previous_context = "\n".join([r['reasoning'] for r in previous_reasoning])

        reasoning_prompt = f"""
        Contexto anterior: {previous_context}
        Evidências: {context}
        Pergunta atual: {step}

        Raciocínio passo a passo:
        """

        return self.generate_reasoning(reasoning_prompt)

    def synthesize_chain(self, reasoning_chain, original_query):
        """Sintetiza resposta final da cadeia de raciocínio"""
        chain_summary = "\n".join([
            f"Etapa {r['step']}: {r['reasoning']}"
            for r in reasoning_chain
        ])

        synthesis_prompt = f"""
        Pergunta original: {original_query}
        Cadeia de raciocínio:
        {chain_summary}

        Resposta final integrada:
        """

        return self.generate_final_answer(synthesis_prompt)
```

Casos de Uso do CAG

- Educação: Tutores virtuais que explicam conceitos complexos.

- Pesquisa Científica: Análise de literatura com raciocínio estruturado.

- Consultoria: Resolução de problemas empresariais multi-facetados.

### 3. Graph RAG: Navegação Inteligente em Grafos de Conhecimento

Graph RAG utiliza grafos de conhecimento para capturar relações complexas entre entidades, proporcionando recuperação contextual mais rica e navegação semântica avançada. Será apresentado, a seguir, um exemplo de como o Graph-RAG pode ser implementado.

```python
import networkx as nx
from neo4j import GraphDatabase
import torch
from torch_geometric.nn import GCNConv

class GraphRAG:
    def __init__(self, neo4j_uri, username, password):
        self.driver = GraphDatabase.driver(neo4j_uri,
                                         auth=(username, password))
        self.graph = nx.Graph()
        self.entity_embeddings = {}
        self.build_graph()

    def build_graph(self):
        """Constrói grafo de conhecimento"""
        with self.driver.session() as session:
            # Recupera nós e relacionamentos
            nodes_query = "MATCH (n) RETURN n.id as id, n.type as type, n.properties as props"
            edges_query = "MATCH (a)-[r]->(b) RETURN a.id as source, b.id as target, type(r) as relation"

            nodes = session.run(nodes_query)
            edges = session.run(edges_query)

            # Adiciona nós ao grafo
            for node in nodes:
                self.graph.add_node(node['id'],
                                  type=node['type'],
                                  **node['props'])

            # Adiciona arestas
            for edge in edges:
                self.graph.add_edge(edge['source'],
                                  edge['target'],
                                  relation=edge['relation'])

    def graph_walk_retrieve(self, query_entities, max_hops=3):
        """Recuperação baseada em caminhada no grafo"""
        relevant_subgraph = nx.Graph()
        visited = set()

        # BFS a partir das entidades da query
        queue = [(entity, 0) for entity in query_entities]

        while queue:
            current_entity, depth = queue.pop(0)

            if depth > max_hops or current_entity in visited:
                continue

            visited.add(current_entity)

            # Adiciona nó ao subgrafo
            if current_entity in self.graph:
                relevant_subgraph.add_node(
                    current_entity,
                    **self.graph.nodes[current_entity]
                )

                # Explora vizinhos
                for neighbor in self.graph.neighbors(current_entity):
                    edge_data = self.graph.edges[current_entity, neighbor]

                    # Filtra por relevância da relação
                    if self.is_relevant_relation(edge_data['relation']):
                        relevant_subgraph.add_edge(
                            current_entity, neighbor, **edge_data
                        )
                        queue.append((neighbor, depth + 1))

        return relevant_subgraph

    def gnn_enhanced_retrieval(self, subgraph, query_embedding):
        """Usa GNN para melhorar recuperação"""
        # Converte subgrafo para formato PyTorch Geometric
        node_features = self.extract_node_features(subgraph)
        edge_index = self.get_edge_index(subgraph)

        # Aplica GCN
        gcn = GCNConv(node_features.size(1), 128)
        enhanced_embeddings = gcn(node_features, edge_index)

        # Calcula similaridade com query
        similarities = torch.cosine_similarity(
            query_embedding.unsqueeze(0),
            enhanced_embeddings
        )

        # Retorna nós mais relevantes
        top_nodes = torch.topk(similarities, k=10)
        return top_nodes

    def multi_hop_reasoning(self, start_entities, target_concept):
        """Raciocínio multi-hop no grafo"""
        paths = []

        for start in start_entities:
            try:
                # Encontra caminhos mais curtos
                shortest_paths = nx.shortest_path(
                    self.graph, start, target_concept
                )

                # Extrai conhecimento do caminho
                path_knowledge = self.extract_path_knowledge(shortest_paths)
                paths.append(path_knowledge)

            except nx.NetworkXNoPath:
                continue

        return self.synthesize_multi_hop_answer(paths)
```

Aplicações do Graph RAG

- Descoberta de Medicamentos: Navegação em redes moleculares.

- Sistemas de Recomendação: Exploração de grafos de preferências.

- Análise de Redes Sociais: Compreensão de influências e conexões.

### 4. Agentic RAG: Autonomia e Tomada de Decisão

Agentic RAG incorpora agentes autônomos que podem tomar decisões sobre quando e como recuperar informações, executar planejamento dinâmico e adaptação contextual. A seguir, será demonstrado um exemplo prático da implementação do Agentic-RAG.

```python
from enum import Enum
import asyncio
from typing import List, Dict, Any

class AgentAction(Enum):
    RETRIEVE = "retrieve"
    GENERATE = "generate"
    VERIFY = "verify"
    SEARCH_EXTERNAL = "search_external"
    DECOMPOSE = "decompose"

class RAGAgent:
    def __init__(self, tools, memory_size=1000):
        self.tools = tools
        self.memory = []
        self.memory_size = memory_size
        self.state = "idle"
        self.confidence_threshold = 0.8

    async def plan_and_execute(self, user_query):
        """Planejamento e execução autônoma"""
        # Análise inicial da query
        query_complexity = self.analyze_query_complexity(user_query)

        # Planejamento baseado na complexidade
        action_plan = self.create_action_plan(user_query, query_complexity)

        # Execução do plano
        results = []
        for action in action_plan:
            result = await self.execute_action(action, user_query, results)
            results.append(result)

            # Avaliação contínua
            if self.should_replan(result):
                new_plan = self.replan(user_query, results)
                action_plan.extend(new_plan)

        # Síntese final
        final_answer = self.synthesize_results(results, user_query)
        self.update_memory(user_query, final_answer, results)

        return final_answer

    def create_action_plan(self, query, complexity):
        """Cria plano de ações baseado na complexidade"""
        if complexity == "simple":
            return [
                {"action": AgentAction.RETRIEVE, "params": {"k": 3}},
                {"action": AgentAction.GENERATE, "params": {"style": "direct"}}
            ]
        elif complexity == "complex":
            return [
                {"action": AgentAction.DECOMPOSE, "params": {}},
                {"action": AgentAction.RETRIEVE, "params": {"k": 5}},
                {"action": AgentAction.VERIFY, "params": {"threshold": 0.7}},
                {"action": AgentAction.GENERATE, "params": {"style": "detailed"}}
            ]
        else:  # very_complex
            return [
                {"action": AgentAction.DECOMPOSE, "params": {}},
                {"action": AgentAction.RETRIEVE, "params": {"k": 10}},
                {"action": AgentAction.SEARCH_EXTERNAL, "params": {}},
                {"action": AgentAction.VERIFY, "params": {"threshold": 0.9}},
                {"action": AgentAction.GENERATE, "params": {"style": "comprehensive"}}
            ]

    async def execute_action(self, action_config, query, previous_results):
        """Executa ação específica"""
        action = action_config["action"]
        params = action_config["params"]

        if action == AgentAction.RETRIEVE:
            return await self.tools["retriever"].retrieve(query, **params)

        elif action == AgentAction.GENERATE:
            context = self.build_context(previous_results)
            return await self.tools["generator"].generate(query, context, **params)

        elif action == AgentAction.VERIFY:
            return await self.verify_information(previous_results, **params)

        elif action == AgentAction.SEARCH_EXTERNAL:
            return await self.tools["Web Search"].search(query, **params)

        elif action == AgentAction.DECOMPOSE:
            return await self.decompose_complex_query(query)

    def should_replan(self, result):
        """Decide se deve replanejar baseado no resultado"""
        if hasattr(result, 'confidence') and result.confidence < self.confidence_threshold:
            return True

        if hasattr(result, 'error') and result.error:
            return True

        return False

    def adaptive_learning(self, feedback):
        """Aprendizado adaptativo baseado em feedback"""
        # Atualiza thresholds e estratégias
        if feedback['success']:
            self.confidence_threshold *= 0.95  # Mais confiante
        else:
            self.confidence_threshold *= 1.05  # Mais cauteloso

        # Atualiza memória de estratégias bem-sucedidas
        self.update_strategy_memory(feedback)
```

Casos de Uso do Agentic RAG

- Assistentes Pessoais: Tomada de decisões autônomas.

- Automação de Pesquisa: Investigação científica automatizada.

- Sistemas de Trading: Análise e decisão em tempo real.

### 5. Adaptive RAG: Personalização e Aprendizado Contínuo

Adaptive RAG implementa aprendizado contínuo e personalização dinâmica, ajustando-se às preferências do usuário e contextos específicos. A seguir, um exemplo prático da implementação do Adaptive RAG.

```python
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
import pickle

class AdaptiveRAG:
    def __init__(self, base_retriever, user_profile_path=None):
        self.base_retriever = base_retriever
        self.user_profiles = defaultdict(dict)
        self.adaptation_history = []
        self.context_clusters = None
        self.load_user_profiles(user_profile_path)

    def adapt_to_user(self, user_id, query, feedback_history):
        """Adapta sistema para usuário específico"""
        # Carrega ou cria perfil do usuário
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = self.create_user_profile()

        profile = self.user_profiles[user_id]

        # Atualiza preferências baseado no histórico
        self.update_preferences(profile, feedback_history)

        # Adapta estratégia de recuperação
        adapted_strategy = self.adapt_retrieval_strategy(profile, query)

        return adapted_strategy

    def create_user_profile(self):
        """Cria perfil inicial do usuário"""
        return {
            'domain_preferences': {},
            'complexity_preference': 'medium',
            'response_style': 'balanced',
            'topic_interests': [],
            'feedback_patterns': [],
            'success_metrics': {
                'accuracy': 0.5,
                'relevance': 0.5,
                'completeness': 0.5
            }
        }

    def update_preferences(self, profile, feedback_history):
        """Atualiza preferências baseado no feedback"""
        for feedback in feedback_history[-10:]:  # Últimos 10 feedbacks
            # Atualiza métricas de sucesso
            for metric, value in feedback['metrics'].items():
                current = profile['success_metrics'][metric]
                profile['success_metrics'][metric] = 0.9 * current + 0.1 * value

            # Atualiza preferências de domínio
            domain = feedback.get('domain')
            if domain:
                if domain not in profile['domain_preferences']:
                    profile['domain_preferences'][domain] = 0.5

                # Aumenta preferência se feedback positivo
                if feedback['rating'] > 3:
                    profile['domain_preferences'][domain] *= 1.1
                else:
                    profile['domain_preferences'][domain] *= 0.9

    def adapt_retrieval_strategy(self, profile, query):
        """Adapta estratégia de recuperação"""
        # Detecta domínio da query
        query_domain = self.detect_domain(query)

        # Ajusta parâmetros baseado no perfil
        k = self.calculate_adaptive_k(profile, query_domain)
        similarity_threshold = self.calculate_threshold(profile)

        # Seleciona fontes preferenciais
        preferred_sources = self.select_sources(profile, query_domain)

        return {
            'k': k,
            'threshold': similarity_threshold,
            'sources': preferred_sources,
            'reranking_weights': self.get_reranking_weights(profile)
        }

    def contextual_adaptation(self, context_type, session_history):
        """Adaptação baseada no contexto da sessão"""
        # Clusteriza contextos similares
        if self.context_clusters is None:
            self.build_context_clusters()

        # Identifica cluster do contexto atual
        current_cluster = self.identify_context_cluster(context_type)

        # Adapta baseado em sessões similares
        similar_sessions = self.find_similar_sessions(current_cluster)
        adaptation_params = self.learn_from_similar_sessions(similar_sessions)

        return adaptation_params

    def meta_learning_update(self, task_performance):
        """Meta-aprendizado para melhorar adaptação"""
        # Analisa padrões de performance
        performance_patterns = self.analyze_performance_patterns(task_performance)

        # Atualiza estratégias de adaptação
        for pattern in performance_patterns:
            if pattern['success_rate'] > 0.8:
                self.promote_strategy(pattern['strategy'])
            elif pattern['success_rate'] < 0.4:
                self.demote_strategy(pattern['strategy'])

        # Salva aprendizado
        self.save_adaptation_knowledge()

    def real_time_adaptation(self, query, initial_results, user_interaction):
        """Adaptação em tempo real baseada na interação"""
        # Monitora interação do usuário
        interaction_signals = self.extract_interaction_signals(user_interaction)

        # Ajusta resultados dinamicamente
        if interaction_signals['needs_more_detail']:
            enhanced_results = self.enhance_detail(initial_results)
            return enhanced_results

        elif interaction_signals['needs_simplification']:
            simplified_results = self.simplify_results(initial_results)
            return simplified_results

        elif interaction_signals['needs_different_perspective']:
            alternative_results = self.find_alternative_perspective(query)
            return alternative_results

        return initial_results
```

Aplicações do Adaptive RAG

- E-learning Personalizado: Adaptação ao estilo de aprendizado.

- Assistentes de Saúde: Personalização para condições específicas.

- Sistemas de Recomendação: Evolução contínua das preferências.

### 6. Multi Modal RAG: Integração de Múltiplas Modalidades

Multi Modal RAG processa e integra texto, imagens, áudio e vídeo, proporcionando compreensão holística e recuperação cross-modal. Será demonstrado, a seguir, um exemplo prático de implementação do Multi Modal RAG.

```python
import torch
import torchvision.transforms as transforms
from transformers import CLIPModel, CLIPProcessor
import librosa
import cv2
from PIL import Image

class MultiModalRAG:
    def __init__(self):
        # Modelos para diferentes modalidades
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # Índices para cada modalidade
        self.text_index = None
        self.image_index = None
        self.audio_index = None
        self.video_index = None

        # Embeddings multimodais
        self.multimodal_embeddings = {}

    def process_multimodal_document(self, document):
        """Processa documento multimodal"""
        processed_doc = {
            'id': document['id'],
            'embeddings': {},
            'content': {}
        }

        # Processa texto
        if 'text' in document:
            text_embedding = self.encode_text(document['text'])
            processed_doc['embeddings']['text'] = text_embedding
            processed_doc['content']['text'] = document['text']

        # Processa imagens
        if 'images' in document:
            image_embeddings = []
            for img_path in document['images']:
                img_embedding = self.encode_image(img_path)
                image_embeddings.append(img_embedding)
            processed_doc['embeddings']['images'] = image_embeddings
            processed_doc['content']['images'] = document['images']

        # Processa áudio
        if 'audio' in document:
            audio_embedding = self.encode_audio(document['audio'])
            processed_doc['embeddings']['audio'] = audio_embedding
            processed_doc['content']['audio'] = document['audio']

        # Processa vídeo
        if 'video' in document:
            video_embedding = self.encode_video(document['video'])
            processed_doc['embeddings']['video'] = video_embedding
            processed_doc['content']['video'] = document['video']

        return processed_doc

    def encode_text(self, text):
        """Codifica texto usando CLIP"""
        inputs = self.clip_processor(text=text, return_tensors="pt")
        with torch.no_grad():
            text_features = self.clip_model.get_text_features(**inputs)
        return text_features.numpy()

    def encode_image(self, image_path):
        """Codifica imagem usando CLIP"""
        image = Image.open(image_path)
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
        return image_features.numpy()

    def encode_audio(self, audio_path):
        """Codifica áudio usando features espectrais"""
        # Carrega áudio
        y, sr = librosa.load(audio_path)

        # Extrai features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        # Combina features
        audio_features = np.concatenate([
            np.mean(mfccs, axis=1),
            np.mean(spectral_centroids, axis=1),
            np.mean(chroma, axis=1)
        ])

        return audio_features

    def encode_video(self, video_path):
        """Codifica vídeo extraindo frames-chave"""
        cap = cv2.VideoCapture(video_path)
        frame_embeddings = []

        # Extrai frames em intervalos regulares
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(1, frame_count // 10)  # 10 frames representativos

        for i in range(0, frame_count, interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()

            if ret:
                # Converte para PIL Image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)

                # Codifica frame
                frame_embedding = self.encode_image_direct(pil_image)
                frame_embeddings.append(frame_embedding)

        cap.release()

        # Média dos embeddings dos frames
        if frame_embeddings:
            return np.mean(frame_embeddings, axis=0)
        else:
            return np.zeros(512)  # Embedding vazio

    def cross_modal_retrieve(self, query, modalities=['text', 'image'], k=5):
        """Recuperação cross-modal"""
        query_embeddings = {}

        # Codifica query em diferentes modalidades
        if 'text' in modalities and isinstance(query, str):
            query_embeddings['text'] = self.encode_text(query)

        if 'image' in modalities and hasattr(query, 'image_path'):
            query_embeddings['image'] = self.encode_image(query.image_path)

        # Busca em cada modalidade
        all_results = []

        for modality, query_emb in query_embeddings.items():
            modal_results = self.search_modality(modality, query_emb, k)
            all_results.extend(modal_results)

        # Fusão e re-ranking multimodal
        fused_results = self.multimodal_fusion(all_results, query_embeddings)

        return fused_results[:k]

    def multimodal_fusion(self, results, query_embeddings):
        """Fusão de resultados multimodais"""
        scored_results = []

        for result in results:
            total_score = 0
            modality_count = 0

            # Calcula score para cada modalidade disponível
            for modality, query_emb in query_embeddings.items():
                if modality in result['embeddings']:
                    similarity = self.calculate_similarity(
                        query_emb, result['embeddings'][modality]
                    )
                    total_score += similarity
                    modality_count += 1

            # Score médio ponderado
            if modality_count > 0:
                avg_score = total_score / modality_count
                # Bonus para documentos com múltiplas modalidades
                multimodal_bonus = 1 + (modality_count - 1) * 0.1
                final_score = avg_score * multimodal_bonus

                scored_results.append({
                    'document': result,
                    'score': final_score
                })

        # Ordena por score
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        return [r['document'] for r in scored_results]

    def generate_multimodal_response(self, query, retrieved_docs):
        """Gera resposta considerando múltiplas modalidades"""
        response = {
            'text': '',
            'images': [],
            'audio': None,
            'video': None
        }

        # Agrega conteúdo textual
        text_content = []
        for doc in retrieved_docs:
            if 'text' in doc['content']:
                text_content.append(doc['content']['text'])

        # Gera resposta textual
        if text_content:
            response['text'] = self.generate_text_response(query, text_content)

        # Seleciona imagens relevantes
        relevant_images = []
        for doc in retrieved_docs:
            if 'images' in doc['content']:
                relevant_images.extend(doc['content']['images'])

        response['images'] = relevant_images[:3]  # Top 3 imagens

        return response
```

Aplicações do Multi Modal RAG

- Educação Visual: Integração de texto, imagens e vídeos educativos.

- Diagnóstico Médico: Análise de exames, relatórios e imagens.

- E-commerce: Busca por produtos usando texto e imagens.

### 7. W-RAG (Web-Enhanced RAG): Integração com a Web

W-RAG integra busca web em tempo real com recuperação local, proporcionando informações atualizadas e cobertura ampliada de conhecimento. A seguir, apresenta-se um exemplo prático da aplicação do W-RAG.

```python
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from datetime import datetime, timedelta

class WebEnhancedRAG:
    def __init__(self, local_retriever, web_apis):
        self.local_retriever = local_retriever
        self.web_apis = web_apis
        self.cache = {}
        self.cache_ttl = timedelta(hours=1)
        self.web_sources = {
            'news': ['reuters.com', 'bbc.com', 'cnn.com'],
            'academic': ['arxiv.org', 'scholar.google.com'],
            'technical': ['stackoverflow.com', 'github.com'],
            'general': ['wikipedia.org']
        }

    async def hybrid_retrieve(self, query, local_weight=0.6, web_weight=0.4):
        """Recuperação híbrida local + web"""
        # Recuperação local
        local_results = await self.local_retriever.retrieve(query)

        # Determina necessidade de busca web
        web_needed = self.assess_web_necessity(query, local_results)

        if web_needed:
            # Busca web assíncrona
            web_results = await self.Web Search_async(query)

            # Combina resultados
            combined_results = self.combine_local_web(
                local_results, web_results, local_weight, web_weight
            )
        else:
            combined_results = local_results

        return combined_results

    def assess_web_necessity(self, query, local_results):
        """Avalia necessidade de busca web"""
        # Verifica se query contém indicadores temporais
        temporal_indicators = ['latest', 'recent', 'current', 'today', 'news']
        has_temporal = any(indicator in query.lower() for indicator in temporal_indicators)

        # Verifica qualidade dos resultados locais
        local_confidence = self.calculate_local_confidence(local_results)

        # Verifica se é tópico que muda rapidamente
        dynamic_topics = ['stock', 'weather', 'news', 'covid', 'election']
        is_dynamic = any(topic in query.lower() for topic in dynamic_topics)

        return has_temporal or local_confidence < 0.7 or is_dynamic

    async def Web Search_async(self, query):
        """Busca web assíncrona em múltiplas fontes"""
        # Verifica cache primeiro
        cache_key = f"web_{hash(query)}"
        if cache_key in self.cache:
            cached_result, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                return cached_result

        # Determina tipo de busca baseado na query
        search_type = self.classify_query_type(query)

        # Busca em paralelo
        tasks = []

        # Google Search API
        if 'google' in self.web_apis:
            tasks.append(self.google_search(query))

        # Bing Search API
        if 'bing' in self.web_apis:
            tasks.append(self.bing_search(query))

        # Busca específica por tipo
        if search_type == 'news':
            tasks.append(self.news_search(query))
        elif search_type == 'academic':
            tasks.append(self.academic_search(query))
        elif search_type == 'technical':
            tasks.append(self.technical_search(query))

        # Executa buscas em paralelo
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filtra e processa resultados
        processed_results = self.process_web_results(results, query)

        # Cache resultado
        self.cache[cache_key] = (processed_results, datetime.now())

        return processed_results

    async def google_search(self, query):
        """Busca usando Google Custom Search API"""
        api_key = self.web_apis['google']['api_key']
        cx = self.web_apis['google']['cx']

        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cx,
            'q': query,
            'num': 10
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()

                results = []
                for item in data.get('items', []):
                    results.append({
                        'title': item['title'],
                        'url': item['link'],
                        'snippet': item['snippet'],
                        'source': 'google'
                    })

                return results

    async def news_search(self, query):
        """Busca específica em fontes de notícias"""
        news_results = []

        # NewsAPI
        if 'newsapi' in self.web_apis:
            api_key = self.web_apis['newsapi']['api_key']
            url = f"https://newsapi.org/v2/everything"
            params = {
                'apiKey': api_key,
                'q': query,
                'sortBy': 'publishedAt',
                'pageSize': 10
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    data = await response.json()

                    for article in data.get('articles', []):
                        news_results.append({
                            'title': article['title'],
                            'url': article['url'],
                            'snippet': article['description'],
                            'published': article['publishedAt'],
                            'source': 'news'
                        })

        return news_results

    def real_time_fact_checking(self, claim, sources):
        """Verificação de fatos em tempo real"""
        fact_check_results = []

        for source in sources:
            # Extrai informações da fonte
            source_info = self.extract_source_info(source)

            # Verifica credibilidade da fonte
            credibility_score = self.assess_source_credibility(source_info)

            # Compara com claim
            consistency_score = self.check_claim_consistency(claim, source['content'])

            fact_check_results.append({
                'source': source,
                'credibility': credibility_score,
                'consistency': consistency_score,
                'verdict': self.determine_verdict(credibility_score, consistency_score)
            })

        return self.aggregate_fact_check(fact_check_results)

    def temporal_aware_retrieval(self, query, time_sensitivity='medium'):
        """Recuperação consciente do tempo"""
        # Define janela temporal baseada na sensibilidade
        time_windows = {
            'high': timedelta(hours=1),
            'medium': timedelta(days=1),
            'low': timedelta(weeks=1)
        }

        cutoff_time = datetime.now() - time_windows[time_sensitivity]

        # Filtra resultados por timestamp
        recent_results = []
        for result in self.all_results:
            if result.get('timestamp', datetime.min) > cutoff_time:
                recent_results.append(result)

        # Se poucos resultados recentes, expande janela
        if len(recent_results) < 3:
            cutoff_time = datetime.now() - time_windows['low']
            recent_results = [
                r for r in self.all_results
                if r.get('timestamp', datetime.min) > cutoff_time
            ]

        return recent_results

    def web_content_extraction(self, url):
        """Extração inteligente de conteúdo web"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove elementos desnecessários
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()

            # Extrai conteúdo principal
            main_content = self.extract_main_content(soup)

            # Extrai metadados
            metadata = self.extract_metadata(soup)

            return {
                'content': main_content,
                'metadata': metadata,
                'url': url,
                'extracted_at': datetime.now()
            }

        except Exception as e:
            return {'error': str(e), 'url': url}
```

Aplicações do W-RAG

- Jornalismo Automatizado: Verificação de fatos em tempo real.

- Análise de Mercado: Integração de dados financeiros atualizados.

- Monitoramento de Tendências: Acompanhamento de tópicos emergentes.

### Tendências Futuras

O futuro do RAG aponta para:

- Integração Multimodal Avançada: Processamento seamless de todas as modalidades.

- Raciocínio Causal: Compreensão de relações causa-efeito.

- Personalização Extrema: Adaptação individual em tempo real.

- Eficiência Computacional: Otimizações para deployment em larga escala.

- Explicabilidade Total: Transparência completa no processo de decisão.

### Implementação Prática

Para implementar essas técnicas em produção, considere:

- Arquitetura Modular: Permita combinação flexível de técnicas.

- Monitoramento Contínuo: Acompanhe performance e qualidade.

- Feedback Loop: Implemente aprendizado contínuo.

- Escalabilidade: Projete para crescimento de dados e usuários.

- Segurança: Proteja dados sensíveis e previna ataques.

### Conclusão

As técnicas avançadas de RAG apresentadas neste artigo representam o estado da arte em sistemas de recuperação e geração. Cada abordagem oferece vantagens específicas:

- CRAG: Melhora a precisão através de correção automática.

- CAG: Habilita raciocínio complexo e explicabilidade.

- Graph RAG: Explora relações semânticas profundas.

- Agentic RAG: Proporciona autonomia e adaptabilidade.

- Adaptive RAG: Personaliza experiências e aprende continuamente.

- Multi Modal RAG: Integra múltiplas modalidades de informação.

- W-RAG: Mantém informações sempre atualizadas.
