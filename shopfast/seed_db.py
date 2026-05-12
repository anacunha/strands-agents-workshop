"""Script para crear tablas y poblar la base de datos con datos mock."""

import sqlite3
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent / "data" / "shop.db"


def create_tables(conn):
    """Crea las tablas de la base de datos."""
    conn.executescript("""
        DROP TABLE IF EXISTS refunds;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            total_orders INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE orders (
            id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            status TEXT NOT NULL,
            tracking_number TEXT,
            total REAL NOT NULL,
            items TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE refunds (
            id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        );
    """)


def seed_customers(conn):
    """Inserta clientes con nombres en español."""
    customers = [
        ("CUST-001", "María García López", "maria.garcia@email.com", "+52 55 1234 5678"),
        ("CUST-002", "Carlos Hernández Ruiz", "carlos.hernandez@email.com", "+52 33 2345 6789"),
        ("CUST-003", "Ana Martínez Flores", "ana.martinez@email.com", "+52 81 3456 7890"),
        ("CUST-004", "José Rodríguez Sánchez", "jose.rodriguez@email.com", "+52 55 4567 8901"),
        ("CUST-005", "Laura Pérez Morales", "laura.perez@email.com", "+52 33 5678 9012"),
        ("CUST-006", "Miguel Ángel Torres", "miguel.torres@email.com", "+52 81 6789 0123"),
        ("CUST-007", "Carmen Díaz Vargas", "carmen.diaz@email.com", "+52 55 7890 1234"),
        ("CUST-008", "Roberto Jiménez Castro", "roberto.jimenez@email.com", "+52 33 8901 2345"),
        ("CUST-009", "Patricia Moreno Luna", "patricia.moreno@email.com", "+52 81 9012 3456"),
        ("CUST-010", "Fernando Ruiz Ortega", "fernando.ruiz@email.com", "+52 55 0123 4567"),
    ]

    now = datetime.now()
    for cust in customers:
        created = now - timedelta(days=random.randint(30, 180))
        conn.execute(
            "INSERT INTO customers (id, name, email, phone, total_orders, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (cust[0], cust[1], cust[2], cust[3], 0, created.isoformat()),
        )


def seed_orders(conn):
    """Inserta pedidos con datos variados."""
    items_catalog = [
        {"nombre": "iPhone 15 Pro", "cantidad": 1, "precio": 22999.00},
        {"nombre": "MacBook Air M3", "cantidad": 1, "precio": 28999.00},
        {"nombre": "AirPods Pro", "cantidad": 1, "precio": 4999.00},
        {"nombre": "Samsung Galaxy S24", "cantidad": 1, "precio": 18999.00},
        {"nombre": "Tablet Samsung A9", "cantidad": 1, "precio": 6499.00},
        {"nombre": "Camiseta Nike Dri-FIT", "cantidad": 2, "precio": 899.00},
        {"nombre": "Jeans Levi's 501", "cantidad": 1, "precio": 1599.00},
        {"nombre": "Sudadera Adidas", "cantidad": 1, "precio": 1299.00},
        {"nombre": "Tenis Nike Air Max", "cantidad": 1, "precio": 2899.00},
        {"nombre": "Chamarra Columbia", "cantidad": 1, "precio": 3499.00},
        {"nombre": "Licuadora Vitamix", "cantidad": 1, "precio": 8999.00},
        {"nombre": "Aspiradora Dyson V15", "cantidad": 1, "precio": 12999.00},
        {"nombre": "Juego de sábanas King", "cantidad": 1, "precio": 1899.00},
        {"nombre": "Cafetera Nespresso", "cantidad": 1, "precio": 3299.00},
        {"nombre": "Smart TV LG 55\"", "cantidad": 1, "precio": 14999.00},
        {"nombre": "Bocina Sonos One", "cantidad": 2, "precio": 4499.00},
        {"nombre": "Kindle Paperwhite", "cantidad": 1, "precio": 3299.00},
        {"nombre": "Mochila Herschel", "cantidad": 1, "precio": 1699.00},
        {"nombre": "Reloj Casio G-Shock", "cantidad": 1, "precio": 2499.00},
        {"nombre": "Audífonos Sony WH-1000XM5", "cantidad": 1, "precio": 6999.00},
    ]

    statuses = (
        ["delivered"] * 15
        + ["shipped"] * 5
        + ["pending"] * 3
        + ["returned"] * 1
        + ["refunded"] * 1
    )
    random.shuffle(statuses)

    now = datetime.now()
    orders = []

    for i in range(1, 26):
        order_id = f"ORD-{i:03d}"
        customer_id = f"CUST-{random.randint(1, 10):03d}"
        status = statuses[i - 1]

        num_items = random.randint(1, 3)
        selected_items = random.sample(items_catalog, num_items)
        total = sum(item["precio"] * item["cantidad"] for item in selected_items)

        tracking = None
        if status in ("shipped", "delivered"):
            tracking = f"MX{random.randint(100000000, 999999999)}BR"

        created = now - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        updated = created + timedelta(days=random.randint(0, 3))

        orders.append((
            order_id, customer_id, status, tracking, round(total, 2),
            json.dumps(selected_items, ensure_ascii=False),
            created.isoformat(), updated.isoformat()
        ))

    conn.executemany(
        "INSERT INTO orders (id, customer_id, status, tracking_number, total, items, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        orders,
    )

    # Actualizar el conteo de pedidos por cliente
    conn.execute("""
        UPDATE customers SET total_orders = (
            SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.id
        )
    """)


def seed_refunds(conn):
    """Inserta reembolsos de ejemplo."""
    now = datetime.now()
    refunds = [
        (
            "REF-001", "ORD-003", "Producto llegó dañado", 4999.00, "approved",
            (now - timedelta(days=5)).isoformat()
        ),
        (
            "REF-002", "ORD-007", "No coincide con la descripción", 1599.00, "pending",
            (now - timedelta(days=2)).isoformat()
        ),
        (
            "REF-003", "ORD-012", "Cambio de opinión", 2899.00, "rejected",
            (now - timedelta(days=8)).isoformat()
        ),
    ]

    conn.executemany(
        "INSERT INTO refunds (id, order_id, reason, amount, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        refunds,
    )


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    seed_customers(conn)
    seed_orders(conn)
    seed_refunds(conn)
    conn.commit()
    conn.close()
    print(f"Base de datos creada exitosamente en: {DB_PATH}")


if __name__ == "__main__":
    main()
