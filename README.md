# Workshop: Agentes de IA como feature de tu producto

Construye un agente de soporte al cliente con herramientas reales usando Strands Agents y vibe coding.

## Requisitos previos

- Python 3.10+
- Una API key de OpenAI o Anthropic
- Tu agente de código favorito (Cursor, Claude Code, Kiro, GitHub Copilot...)
- Git

## Setup rápido

### 1. Clona el repositorio

```bash
git clone https://github.com/ramtoearth/strands-agents-workshop.git
cd strands-agents-workshop/
```

### 2. Ve a la carpeta del proyecto

```bash
cd shopfast/
```

### 3. Crea un entorno virtual e instala dependencias

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Inicializa la base de datos

```bash
python seed_db.py
```

### 5. Arranca la App

Abre http://localhost:8000

```bash
python app.py
```

## Configura tu API key

```bash
export OPENAI_API_KEY="tu-key-aquí"
# o
export ANTHROPIC_API_KEY="tu-key-aquí"
```

## Pasos del workshop

| Paso | Branch | Qué construyes |
|------|--------|----------------|
| 0 | `main` | App base (punto de partida) |
| 1 | [step/01-basic-agent](./prompts/01-basic-agent.md) | Agente conectado al chat, sin tools |
| 2 | [step/02-read-tools](./prompts/02-read-tools) | Tools de consulta (pedidos, clientes) |
| 3 | [step/03-write-tools](./prompts/03-write-tools) | Tool de acción (procesar reembolsos) |
| 4 | [step/04-guardrails](./prompts/04-guardrails) | Reglas de negocio en el system prompt |

## ¿Te perdiste en un paso?

```bash
git checkout step/02-read-tools  # Salta al paso 2 completo
```

## Los prompts

Cada paso tiene un prompt detallado en la carpeta `prompts/`. Copia el prompt, pégalo en tu agente de código, y deja que genere la implementación.

## ¿No quieres usar API keys?

Strands soporta Ollama para correr modelos localmente sin costo:

```bash
pip install ollama
ollama pull llama3.2:3b
```

Cambia `OpenAIModel` por `OllamaModel` en agent.py.

## Recursos

- [Strands Agents](https://strandsagents.com/)
- [Ollama](https://ollama.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
