# Database Decision Protocol

> Escolha a ferramenta certa para o problema específico do dado, não o modismo do momento.

## Matriz de Armazenamento para Agentes de IA

| Tipo de Dado | Necessidade | Tecnologia | Exemplos no Framework |
|--------------|-------------|------------|----------------------|
| **A. Estado Crítico / Auditoria** | Consistência ACID, relações, transações | **Relacional (PostgreSQL, MySQL, SQLite)** | Estado do agente, execuções de workflows, usuários, permissões, histórico de ferramentas |
| **B. Sessão / Curto Prazo** | Latência ultra-baixa, expiração automática, chave-valor simples | **Key-Value (Redis)** | Contexto ativo de conversa, cache de prompts, variáveis temporárias de execução |
| **C. Conhecimento Semi-estruturado** | Flexibilidade de schema, documentos variados | **Document Store (MongoDB, DynamoDB)** | Perfis de agentes, tool definitions, configs customizadas, Chain of Thought logs |
| **D. Memória Longa / RAG** | Busca semântica/textual em volume, relevância | **Vetorial (pgvector, Pinecone, Weaviate) / Full-Text Search** | Documentos, manuais, histórico para recuperação de contexto |
| **E. Processamento Assíncrono** | Desacoplar, resiliência, idempotência, reprocessamento | **Filas (Kafka, RabbitMQ, Redis Streams)** | Geração de relatórios, chamadas APIs terceiros, webhooks, tarefas longas |

---

## Guidelines Práticos

### 1. Questione o Dado Antes de Escolher

Antes de persistir **qualquer** dado gerado pelo agente:

| Pergunta | Se SIM → Use |
|----------|--------------|
| Precisa durar para sempre e manter relações consistentes? | **Banco Relacional** |
| É dado temporário de sessão que expira rápido? | **Key-Value (Redis)** |
| Precisa ser buscado por relevância semântica/textual em grande escala? | **Base Vetorial / Full-Text Search** |
| Pode acontecer em segundo plano sem bloquear o usuário? | **Filas de Mensageria** |

### 2. Evite Acoplamento Excessivo (Anti-Patterns)

| Anti-Pattern | Por Que Falha | Correção |
|--------------|---------------|----------|
| Usar cache de sessão (Redis) como fonte oficial da verdade | Dados expiram, podem ser perdidos, sem ACID | Fonte da verdade = Relacional; Redis = cache apenas |
| Um único repositório para logs + vetores + estado transacional | Conflitos de consistência, performance, manutenção | Separe por responsabilidade (tabela por tipo) |
| Guardar Chain of Thought no banco relacional | Schema rígido, queries ineficientes para texto | Document Store ou Vetorial |
| Bloquear resposta do usuário esperando task pesada | Latência alta, timeout, má UX | Filas assíncronas + polling/webhook |

### 3. Comece Simples, Escale com Propósito

| Fase | Stack Mínima | Quando Adicionar |
|------|--------------|------------------|
| **Protótipo (Dia 0)** | Relacional (SQLite/Postgres) + Cache simples (Redis) | — |
| **Produção inicial** | + Document Store para tool definitions/configs | Quando ferramentas tornam-se dinâmicas |
| **Escala / RAG** | + Base Vetorial / Full-Text Search | Quando busca semântica vira gargalo |
| **Carga alta / Resiliência** | + Filas (Kafka/RabbitMQ) | Quando tasks longas travam requests |

---

## Checklist de Decisão (para PRD/SPEC)

Para cada entidade de dado do agente, registre no PRD:

```
Entidade: [nome]
Tipo: [A|B|C|D|E]
Justificativa: [ex: "Estado de workflow exige ACID e auditoria"]
Tecnologia: [ex: PostgreSQL]
Schema/Índices: [resumo]
TTL/Expiração: [se aplicável]
Idempotência: [chave de deduplicação se fila]
```

---

## Resumo

> Arquitetura madura = ferramenta certa para o problema do dado.

**Separe claramente:**
- Estado/Transações → Relacional
- Sessão/Cache → Key-Value
- Conhecimento/RAG → Vetorial/Full-Text
- Execução Assíncrona → Filas

Não centralize tudo no mesmo banco. Cada tipo de dado do agente tem necessidades diferentes.