"""Agente de suporte da ShopFast usando Strands Agents."""

from strands import Agent
from strands.models.anthropic import AnthropicModel
from tools import get_order_status, get_customer_orders

# A key é lida da variável de ambiente ANTHROPIC_API_KEY (ou OPENAI_API_KEY).
model = AnthropicModel(model_id="claude-sonnet-4-6", max_tokens=1028)

# Trocar de provider é só trocar o model (e o import):
# from strands.models.openai import OpenAIModel
# model = OpenAIModel(model_id="gpt-4o-mini")

SYSTEM_PROMPT = """Você é o assistente do time de suporte da ShopFast, uma loja online.
Você ajuda os atendentes a responder dúvidas sobre pedidos, envios e devoluções.
Seja prestativo, profissional e conciso."""


def invoke_agent(user_message: str, conversation_history: list[dict]) -> str:
    """Envia uma mensagem ao agente e retorna a resposta."""
    # Monta o contexto completo com o histórico
    if conversation_history:
        context = "Histórico da conversa:\n"
        for msg in conversation_history:
            role = "Atendente" if msg["role"] == "user" else "Agente"
            context += f"{role}: {msg['content']}\n"
        context += f"\nAtendente: {user_message}"
    else:
        context = user_message

    agent = Agent(
        model=model,
        tools=[get_order_status, get_customer_orders],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )

    result = agent(context)

    # Extrai o texto da resposta
    content = result.message.get("content", [])
    texts = [block["text"] for block in content if "text" in block]
    return "".join(texts)
