"""Passo 0: sem agente.

Retorna uma resposta fixa para validar a interface de chat antes de
conectar o Strands Agents nas próximas etapas.
"""


def invoke_agent(user_message: str, conversation_history: list[dict]) -> str:
    """Retorna uma resposta fixa (o agente ainda não está conectado)."""
    return "O agente ainda não está conectado. Aqui será integrado o Strands Agents."
