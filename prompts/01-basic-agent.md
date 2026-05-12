# Paso 1: Conectar un agente al chat

## Contexto

La app ShopFast ya tiene un chat de soporte pero solo devuelve un placeholder. Vamos a conectar un agente de IA real usando Strands Agents.

## Prompt para tu agente de código

Copia y pega esto en tu agente de código (Cursor, Claude Code, Kiro, etc.):

---

```
Crea un archivo shopfast/agent.py que configure un agente de Strands Agents.

Requisitos:
- Usa OpenAIModel de strands.models.openai con model_id="gpt-4o-mini"
- Define un system prompt que diga: "Eres el agente de soporte al cliente de ShopFast, una tienda online. Ayudas a los clientes con sus preguntas sobre pedidos, envíos y devoluciones. Sé amable, profesional y conciso."
- Crea una instancia de Agent con el modelo y el system prompt
- Exporta una función invoke_agent(user_message: str, conversation_history: list[dict]) -> str que:
  - Reciba el mensaje del usuario y el historial de conversación
  - Envíe el mensaje al agente y retorne la respuesta como string
  - Use el historial para mantener contexto entre mensajes

Luego modifica shopfast/app.py:
- En el endpoint POST /chat, reemplaza la respuesta placeholder por una llamada a invoke_agent() con el mensaje del usuario y el historial
- La respuesta del agente debe mostrarse como el mensaje del assistant en el chat

Agrega strands-agents y strands-agents-tools a requirements.txt
```

---

## Pruébalo

Reinstala dependencias y reinicia el servidor:

```bash
pip install -r requirements.txt
python app.py
```

Ve a http://localhost:8000/chat y prueba:

```
> Hola, ¿me puedes ayudar?
→ Respuesta amable del agente

> ¿Dónde está mi pedido ORD-001?
→ El agente inventa o dice que no tiene acceso a esa información
```

## ¿Qué aprendimos?

Sin herramientas, el agente solo puede conversar. No puede acceder a los datos de tu producto. Es un chatbot genérico.

## ¿Te perdiste?

```bash
git checkout step/01-basic-agent
```
