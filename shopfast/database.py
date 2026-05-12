import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "shop.db"


def get_db():
    """Obtiene una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_orders():
    """Retorna todos los pedidos con el nombre del cliente."""
    db = get_db()
    rows = db.execute("""
        SELECT o.*, c.name as customer_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.created_at DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_recent_orders(limit=5):
    """Retorna los pedidos más recientes."""
    db = get_db()
    rows = db.execute("""
        SELECT o.*, c.name as customer_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_order(order_id):
    """Retorna un pedido específico con info del cliente."""
    db = get_db()
    row = db.execute("""
        SELECT o.*, c.name as customer_name, c.email as customer_email,
               c.phone as customer_phone
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.id = ?
    """, (order_id,)).fetchone()
    db.close()
    if row:
        order = dict(row)
        order["items"] = json.loads(order["items"])
        return order
    return None


def get_all_customers():
    """Retorna todos los clientes."""
    db = get_db()
    rows = db.execute("""
        SELECT * FROM customers ORDER BY name
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_customer(customer_id):
    """Retorna un cliente específico."""
    db = get_db()
    row = db.execute("""
        SELECT * FROM customers WHERE id = ?
    """, (customer_id,)).fetchone()
    db.close()
    if row:
        return dict(row)
    return None


def get_orders_count():
    """Retorna el total de pedidos."""
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    db.close()
    return count


def get_pending_orders_count():
    """Retorna la cantidad de pedidos pendientes."""
    db = get_db()
    count = db.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'pending'"
    ).fetchone()[0]
    db.close()
    return count


def get_pending_refunds_count():
    """Retorna la cantidad de reembolsos pendientes."""
    db = get_db()
    count = db.execute(
        "SELECT COUNT(*) FROM refunds WHERE status = 'pending'"
    ).fetchone()[0]
    db.close()
    return count
