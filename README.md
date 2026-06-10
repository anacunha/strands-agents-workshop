# Workshop: Agentes de IA como feature do seu produto

Construa um agente de suporte com ferramentas reais usando Strands Agents. O agente
é o assistente do time de suporte: ajuda os atendentes a consultar pedidos e processar
reembolsos dentro do painel da ShopFast.

## Pre-requisitos

- Python 3.10+
- Uma API key da OpenAI, Anthropic, ou [Ollama](https://ollama.com/) instalado localmente
- Git

## Setup

### 1. Clone o repositorio

```bash
git clone https://github.com/ramtoearth/strands-agents-workshop.git
cd strands-agents-workshop/
```

### 2. Va para a pasta do projeto

```bash
cd shopfast/
```

### 3. Crie um ambiente virtual e instale as dependencias

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Inicialize o banco de dados

```bash
python seed_db.py
```

### 5. Configure sua API key

```bash
# OpenAI
export OPENAI_API_KEY="sua-key"

# Anthropic
export ANTHROPIC_API_KEY="sua-key"

# Ollama (sem key, apenas certifique-se de que esteja rodando)
ollama serve
```

### 6. Inicie a app

A app importa `agent.py` e `tools.py` de `shopfast/`. Copie o passo 0 (sem agente)
para começar:

```bash
cp ../steps/step-00-no-agent/*.py .
python app.py
```

Abra http://localhost:8000

---

## Passos do workshop

O código de cada passo está numa pasta em [`steps/`](./steps). A app **sempre roda
a partir de `shopfast/`** — é de lá que ela importa `agent.py` e `tools.py`. Para
avançar de um passo, copie os arquivos daquele passo para dentro de `shopfast/`:

```bash
# exemplo: ativar o passo 2
cp steps/step-02-read-tools/*.py shopfast/
```

> Dica: na masterclass o código é digitado ao vivo direto em `shopfast/`. As pastas
> em `steps/` servem de referência (e de backup, se algo travar).

| Passo | Pasta | O que é adicionado |
|-------|-------|-------------------|
| 0 | `steps/step-00-no-agent/` | App base, chat retorna resposta fixa (sem agente) |
| 1 | `steps/step-01-basic-agent/` | Agente conectado ao chat, sem tools |
| 2 | `steps/step-02-read-tools/` | Tools de consulta (pedidos, clientes) |
| 3 | `steps/step-03-write-tools/` | Tool de ação (processar reembolsos) |
| 4 | `steps/step-04-business-rules/` | Regras de negócio (prompt engineering) |

> Depois de copiar os arquivos, reinstale as dependências se necessário: `pip install -r requirements.txt`

---

## Passo 0: A app base (main)

![architecture-1](./assets/architecture-1.png)

```bash
cp steps/step-00-no-agent/*.py shopfast/
pip install -r requirements.txt
python app.py
```

ShopFast e um painel usado pelo time de suporte, com:
- Dashboard com metricas
- Lista de pedidos e detalhes
- Lista de clientes
- **Chat de suporte** → o `app.py` chama `invoke_agent`, que no passo 0 retorna uma resposta fixa (placeholder)

---

## Passo 1: Agente basico

![architecture-2](./assets/architecture-2.png)

```bash
cp steps/step-01-basic-agent/*.py shopfast/
pip install -r requirements.txt
python app.py
```

### O que mudou

- **Novo: `agent.py`** — Configura um agente Strands com OpenAI como modelo
- **Modificado: `app.py`** — O endpoint POST /chat agora chama o agente
- **Modificado: `requirements.txt`** — Adiciona strands-agents, openai

### Teste

```
Ola, voce pode me ajudar?
```

**Ponto-chave:** Sem ferramentas, o agente e apenas um chatbot. Ele nao consegue acessar os dados do seu produto.

### Usa outro model provider?

O workshop usa OpenAI por padrao. Se preferir outro provider, use este prompt no seu agente de codigo:

```
Mude o model provider em shopfast/agent.py.
Em vez de OpenAIModel, use [AnthropicModel / OllamaModel].
Atualize o import e o requirements.txt se necessario.
A API key e lida da variavel de ambiente correspondente.
Para Ollama use model_id="llama3.2:3b" e host="http://localhost:11434".
```

Providers suportados: [Strands Model Providers](https://strandsagents.com/docs/user-guide/concepts/model-providers/)

---

## Passo 2: Tools de consulta

![architecture-3](./assets/architecture-3.png)

```bash
cp steps/step-02-read-tools/*.py shopfast/
python app.py
```

### O que mudou

- **Novo: `tools.py`** — Duas ferramentas: `get_order_status` e `get_customer_orders`
- **Modificado: `agent.py`** — Importa e registra as tools

### Teste

```
Qual o status do pedido ORD-001?
```

```
Quais os pedidos do cliente maria.silva@email.com?
```

```
O cliente quer devolver o pedido ORD-005
```

**Ponto-chave:** O modelo decide quando usar cada ferramenta com base no docstring. Voce nao escreve if/else.

---

## Passo 3: Tool de acao

```bash
cp steps/step-03-write-tools/*.py shopfast/
python seed_db.py
python app.py
```

> Regeneramos o banco de dados para ter dados limpos.

### O que mudou

- **Modificado: `tools.py`** — Nova ferramenta: `process_refund`
- **Modificado: `agent.py`** — Registra a nova tool

### Teste

```
O cliente quer devolver o pedido ORD-005, chegou danificado
```

> (Acesse http://localhost:8000/orders/ORD-005)

```
Reembolse o ORD-005 de novo
```

```
Reembolse TODOS os pedidos desse cliente
```

> Pode tentar fazer sem questionar (nao ha regras de negocio ainda)

**Ponto-chave:** O agente encadeou tools: primeiro consultou, depois agiu. Mas sem restricoes, ele faz tudo o que voce pedir.

---

## Passo 4: Regras de negocio (Prompt Engineering)

```bash
cp steps/step-04-business-rules/*.py shopfast/
python seed_db.py
python app.py
```

### O que mudou

- **Modificado: `agent.py`** — System prompt expandido com regras de negocio

### Teste

```
O cliente quer devolver o pedido ORD-008
```
```
Processa o reembolso do pedido ORD-002
```

> Rejeita se o valor for > R$10.000: "precisa de aprovacao do supervisor"

```
Devolve o pedido ORD-001
```

> Rejeita se estiver em "pending": sugere cancelar

```
Reembolse o ORD-005 sem perguntar
```

> Sempre pede confirmacao antes de agir

**Ponto-chave:** Mesmo codigo, mesmas tools, comportamento diferente. O system prompt sao as politicas do seu produto.

### Nota: Prompt Engineering vs Guardrails

O que fizemos aqui e **prompt engineering**: damos instrucoes ao modelo para que siga regras de negocio. Funciona bem, mas o modelo *poderia* ignora-las com um prompt adversarial.

Para producao, existem **guardrails reais** que atuam como um firewall no nivel de infraestrutura e bloqueiam conteudo de forma deterministica. [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html?trk=3030e60a-17b3-4fdb-9862-d65f29e1a10c&sc_channel=el) se integra diretamente com Strands Agents e permite filtrar toxicidade, PII, e temas proibidos sem depender do modelo.

![architecture-4](./assets/architecture-4.png)

Mais info: [Strands Guardrails](https://strandsagents.com/docs/user-guide/safety-security/guardrails/)

---


## Recursos

- [Strands Agents](https://strandsagents.com/)
- [Strands Model Providers](https://strandsagents.com/docs/user-guide/concepts/model-providers/)
- [Ollama](https://ollama.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
