"""Agente de soporte al cliente de ShopFast usando Strands Agents."""

from strands import Agent
from strands.models.openai import OpenAIModel

model = OpenAIModel(model_id="gpt-4o-mini")

SYSTEM_PROMPT = """Eres el agente de soporte al cliente de ShopFast, una tienda online.
Ayudas a los clientes con sus preguntas sobre pedidos, envíos y devoluciones.
Sé amable, profesional y conciso."""


def invoke_agent(user_message: str, conversation_history: list[dict]) -> str:
    """Envía un mensaje al agente y retorna la respuesta."""
    # Construir el contexto completo con el historial
    if conversation_history:
        context = "Historial de la conversación:\n"
        for msg in conversation_history:
            role = "Cliente" if msg["role"] == "user" else "Agente"
            context += f"{role}: {msg['content']}\n"
        context += f"\nCliente: {user_message}"
    else:
        context = user_message

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )

    result = agent(context)
    return str(result)
