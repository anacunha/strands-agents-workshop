"""Herramientas del agente de soporte de ShopFast."""

import sqlite3
from pathlib import Path
from strands import tool

DB_PATH = Path(__file__).parent / "data" / "shop.db"


@tool
def get_order_status(order_id: str) -> str:
    """Consulta el estado actual de un pedido por su ID.
    Usa esta herramienta cuando el cliente pregunte por el estado de un pedido específico.

    order_id: El identificador del pedido (ejemplo: ORD-001)
    """
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT status, tracking_number, total, created_at FROM orders WHERE id = ?",
        (order_id,)
    ).fetchone()
    conn.close()

    if not row:
        return f"No encontré ningún pedido con ID {order_id}."

    status, tracking, total, created = row
    result = f"Pedido {order_id}: estado={status}, total=${total:.2f}, fecha={created[:10]}"
    if tracking:
        result += f", rastreo={tracking}"
    return result


@tool
def get_customer_orders(email: str) -> str:
    """Busca todos los pedidos de un cliente usando su email.
    Usa esta herramienta cuando el cliente quiera ver sus pedidos o no recuerde su número de pedido.

    email: El correo electrónico del cliente
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
        return f"No encontré pedidos asociados al email {email}."

    lines = [f"Pedidos de {email}:"]
    for order_id, status, total, created in rows:
        lines.append(f"  - {order_id}: {status}, ${total:.2f} ({created[:10]})")
    return "\n".join(lines)
