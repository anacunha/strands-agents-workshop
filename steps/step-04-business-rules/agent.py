"""Agente de suporte da ShopFast usando Strands Agents."""

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import get_order_status, get_customer_orders, process_refund

model = OpenAIModel(model_id="gpt-4o-mini")

SYSTEM_PROMPT = """Você é o assistente do time de suporte da ShopFast, uma loja online.
Você ajuda os atendentes a responder dúvidas sobre pedidos, envios e devoluções.

REGRAS DE NEGÓCIO:
- Você só pode processar reembolsos de pedidos com status "delivered" ou "shipped"
- NÃO processe reembolsos de pedidos com status "pending" (ainda não foram enviados, podem ser cancelados diretamente)
- NÃO processe reembolsos de pedidos que já foram reembolsados
- Se o valor do pedido for maior que R$10.000, informe que é necessária a aprovação de um supervisor e não processe o reembolso
- Sempre confirme antes de processar um reembolso: mostre os dados do pedido e pergunte se deseja continuar

TOM E COMPORTAMENTO:
- Seja prestativo, profissional e empático
- Responda em português
- Seja conciso, mas informativo
- Se não puder resolver algo, explique o motivo com clareza
"""


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
        tools=[get_order_status, get_customer_orders, process_refund],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )

    result = agent(context)

    # Extrai o texto da resposta
    content = result.message.get("content", [])
    texts = [block["text"] for block in content if "text" in block]
    return "".join(texts)
