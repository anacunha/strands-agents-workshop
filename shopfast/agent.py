"""Agente de soporte al cliente de ShopFast usando Strands Agents."""

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import get_order_status, get_customer_orders, process_refund

model = OpenAIModel(model_id="gpt-4o-mini")

SYSTEM_PROMPT = """Eres el agente de soporte al cliente de ShopFast, una tienda online.
Ayudas a los clientes con sus preguntas sobre pedidos, envíos y devoluciones.

REGLAS DE NEGOCIO:
- Solo puedes procesar reembolsos de pedidos con estado "delivered" o "shipped"
- NO proceses reembolsos de pedidos con estado "pending" (aún no se han enviado, se pueden cancelar directamente)
- NO proceses reembolsos de pedidos que ya fueron reembolsados
- Si el monto del pedido es mayor a $10,000 MXN, informa al cliente que necesita aprobación de un supervisor y no proceses el reembolso
- Siempre confirma con el cliente antes de procesar un reembolso: muéstrale los datos del pedido y pregunta si desea continuar

TONO Y COMPORTAMIENTO:
- Sé amable, profesional y empático
- Responde en español
- Sé conciso pero informativo
- Si no puedes resolver algo, explica por qué claramente
"""


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
        tools=[get_order_status, get_customer_orders, process_refund],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )

    result = agent(context)

    # Extraer el texto de la respuesta
    content = result.message.get("content", [])
    texts = [block["text"] for block in content if "text" in block]
    return "".join(texts)
