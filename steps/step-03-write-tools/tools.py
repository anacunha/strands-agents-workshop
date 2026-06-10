"""Ferramentas do agente de suporte da ShopFast."""

import sqlite3
from pathlib import Path
from strands import tool

DB_PATH = Path(__file__).parent / "data" / "shop.db"


@tool
def get_order_status(order_id: str) -> str:
    """Consulta o status atual de um pedido pelo seu ID.
    Use esta ferramenta quando precisar do status de um pedido específico.

    order_id: O identificador do pedido (exemplo: ORD-001)
    """
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT status, tracking_number, total, created_at FROM orders WHERE id = ?",
        (order_id,)
    ).fetchone()
    conn.close()

    if not row:
        return f"Não encontrei nenhum pedido com o ID {order_id}."

    status, tracking, total, created = row
    result = f"Pedido {order_id}: status={status}, total=R${total:.2f}, data={created[:10]}"
    if tracking:
        result += f", rastreio={tracking}"
    return result


@tool
def get_customer_orders(email: str) -> str:
    """Busca todos os pedidos de um cliente pelo email.
    Use esta ferramenta quando precisar ver os pedidos de um cliente ou quando o número do pedido não for informado.

    email: O email do cliente
    """
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT o.id, o.status, o.total, o.created_at
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE c.email = ?
        ORDER BY o.created_at DESC
    """, (email,)).fetchall()
    conn.close()

    if not rows:
        return f"Não encontrei pedidos associados ao email {email}."

    lines = [f"Pedidos de {email}:"]
    for order_id, status, total, created in rows:
        lines.append(f"  - {order_id}: {status}, R${total:.2f} ({created[:10]})")
    return "\n".join(lines)


@tool
def process_refund(order_id: str, reason: str) -> str:
    """Processa o reembolso de um pedido.
    Use esta ferramenta quando for preciso devolver um produto ou solicitar um reembolso.
    Antes de processar, verifique se o pedido existe usando get_order_status.

    order_id: O identificador do pedido a reembolsar
    reason: O motivo do reembolso informado pelo cliente
    """
    conn = sqlite3.connect(DB_PATH)

    # Verifica se o pedido existe e ainda não foi reembolsado
    order = conn.execute(
        "SELECT status, total FROM orders WHERE id = ?", (order_id,)
    ).fetchone()

    if not order:
        conn.close()
        return f"Não encontrei o pedido {order_id}."

    if order[0] == "refunded":
        conn.close()
        return f"O pedido {order_id} já foi reembolsado anteriormente."

    # Cria o reembolso
    refund_count = conn.execute("SELECT COUNT(*) FROM refunds").fetchone()[0]
    refund_id = f"REF-{refund_count + 1:03d}"

    conn.execute(
        "INSERT INTO refunds (id, order_id, reason, amount, status, created_at) VALUES (?, ?, ?, ?, 'approved', datetime('now'))",
        (refund_id, order_id, reason, order[1])
    )
    conn.execute(
        "UPDATE orders SET status = 'refunded', updated_at = datetime('now') WHERE id = ?",
        (order_id,)
    )
    conn.commit()
    conn.close()

    return f"Reembolso {refund_id} processado com sucesso. Valor: R${order[1]:.2f}. O pedido {order_id} foi marcado como reembolsado."
