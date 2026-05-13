# Paso 1: Conectar un agente al chat

## Contexto

La app ShopFast ya tiene un chat de soporte pero solo devuelve un placeholder. Vamos a conectar un agente de IA real usando Strands Agents.

## Prompt 0: Dale contexto a tu agente de código

Antes de pedirle que implemente algo, tu agente de código necesita entender el proyecto. Copia y pega esto primero:

---

```
Lee los archivos del proyecto para entender la estructura y el código existente:
- shopfast/app.py (la app FastAPI con las rutas)
- shopfast/database.py (las queries a SQLite)
- shopfast/seed_db.py (el esquema de la base de datos y datos mock)
- shopfast/templates/chat.html (la interfaz del chat)
- shopfast/requirements.txt (dependencias actuales)

Este es un panel de soporte al cliente para una tienda online llamada ShopFast.
Está construido con FastAPI + Jinja2 (server-side rendered) y usa SQLite como base de datos.
La base de datos tiene tablas de customers, orders y refunds.
El chat en /chat actualmente devuelve un placeholder. Vamos a conectar un agente de IA real.
```

---

## Prompt 1: Crea el agente

Ahora sí, pídele que implemente el agente. Usa el prompt que corresponda a tu provider:

### Si usas OpenAI

```
Crea un archivo shopfast/agent.py que configure un agente de Strands Agents.

Requisitos:
- Usa OpenAIModel de strands.models.openai (sin model_id, usa el default)
- Define un system prompt que diga: "Eres el agente de soporte al cliente de ShopFast, una tienda online. Ayudas a los clientes con sus preguntas sobre pedidos, envíos y devoluciones. Sé amable, profesional y conciso."
- Crea una instancia de Agent con el modelo y el system prompt
- Usa callback_handler=None para evitar que el agente imprima a stdout
- Exporta una función invoke_agent(user_message: str, conversation_history: list[dict]) -> str que:
  - Reciba el mensaje del usuario y el historial de conversación
  - Envíe el mensaje al agente y retorne la respuesta como string
  - Use el historial para mantener contexto entre mensajes
  - Extraiga el texto de result.message["content"]

Luego modifica shopfast/app.py:
- En el endpoint POST /chat, reemplaza la respuesta placeholder por una llamada a invoke_agent() con el mensaje del usuario y el historial
- La respuesta del agente debe mostrarse como el mensaje del assistant en el chat

Agrega strands-agents, strands-agents-tools y openai a requirements.txt

La API key se lee de la variable de entorno OPENAI_API_KEY.
```

### Si usas Anthropic

```
Crea un archivo shopfast/agent.py que configure un agente de Strands Agents.

Requisitos:
- Usa AnthropicModel de strands.models.anthropic (sin model_id, usa el default)
- Define un system prompt que diga: "Eres el agente de soporte al cliente de ShopFast, una tienda online. Ayudas a los clientes con sus preguntas sobre pedidos, envíos y devoluciones. Sé amable, profesional y conciso."
- Crea una instancia de Agent con el modelo y el system prompt
- Usa callback_handler=None para evitar que el agente imprima a stdout
- Exporta una función invoke_agent(user_message: str, conversation_history: list[dict]) -> str que:
  - Reciba el mensaje del usuario y el historial de conversación
  - Envíe el mensaje al agente y retorne la respuesta como string
  - Use el historial para mantener contexto entre mensajes
  - Extraiga el texto de result.message["content"]

Luego modifica shopfast/app.py:
- En el endpoint POST /chat, reemplaza la respuesta placeholder por una llamada a invoke_agent() con el mensaje del usuario y el historial
- La respuesta del agente debe mostrarse como el mensaje del assistant en el chat

Agrega strands-agents, strands-agents-tools y anthropic a requirements.txt

La API key se lee de la variable de entorno ANTHROPIC_API_KEY.
```

### Si usas Ollama (local, sin API key)

```
Crea un archivo shopfast/agent.py que configure un agente de Strands Agents.

Requisitos:
- Usa OllamaModel de strands.models.ollama con model_id="llama3.2:3b" y host="http://localhost:11434"
- Define un system prompt que diga: "Eres el agente de soporte al cliente de ShopFast, una tienda online. Ayudas a los clientes con sus preguntas sobre pedidos, envíos y devoluciones. Sé amable, profesional y conciso."
- Crea una instancia de Agent con el modelo y el system prompt
- Usa callback_handler=None para evitar que el agente imprima a stdout
- Exporta una función invoke_agent(user_message: str, conversation_history: list[dict]) -> str que:
  - Reciba el mensaje del usuario y el historial de conversación
  - Envíe el mensaje al agente y retorne la respuesta como string
  - Use el historial para mantener contexto entre mensajes
  - Extraiga el texto de result.message["content"]

Luego modifica shopfast/app.py:
- En el endpoint POST /chat, reemplaza la respuesta placeholder por una llamada a invoke_agent() con el mensaje del usuario y el historial
- La respuesta del agente debe mostrarse como el mensaje del assistant en el chat

Agrega strands-agents y strands-agents-tools a requirements.txt

Asegúrate de que Ollama esté corriendo (ollama serve) y que el modelo esté descargado (ollama pull llama3.2:3b).
```

---

## Pruébalo

Reinstala dependencias y reinicia el servidor:

```bash
pip install -r requirements.txt
python app.py
```

Ve a http://localhost:8000/chat y prueba:

### Lo que sí debería funcionar

```
Hola, ¿me puedes ayudar con un pedido?
```

```
¿Qué es ShopFast?
```

```
¿Cuál es su política de devoluciones?
```

### Lo que no debería poder hacer

```
¿Cuál es el estado de mi pedido ORD-001?
```

```
Soy maria.garcia@email.com, ¿qué pedidos tengo?
```

```
Quiero devolver mi pedido ORD-005
```

### Punto clave

El agente es amable pero inútil. No puede hacer nada real por el usuario porque no tiene acceso a los datos del producto.

## ¿Qué aprendimos?

Sin herramientas, el agente solo puede conversar. No puede acceder a los datos de tu producto. Es un chatbot genérico.

## ¿Te perdiste?

```bash
git checkout step/01-basic-agent
```
