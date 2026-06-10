"""Script para criar tabelas e popular o banco de dados com dados fictícios."""

import sqlite3
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent / "data" / "shop.db"


def create_tables(conn):
    """Cria as tabelas do banco de dados."""
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
    """Insere clientes com nomes brasileiros."""
    customers = [
        ("CUST-001", "Maria Silva Santos", "maria.silva@email.com", "+55 11 91234-5678"),
        ("CUST-002", "Carlos Oliveira Souza", "carlos.oliveira@email.com", "+55 21 92345-6789"),
        ("CUST-003", "Ana Pereira Costa", "ana.pereira@email.com", "+55 31 93456-7890"),
        ("CUST-004", "José Rodrigues Lima", "jose.rodrigues@email.com", "+55 11 94567-8901"),
        ("CUST-005", "Larissa Ferreira Alves", "larissa.ferreira@email.com", "+55 41 95678-9012"),
        ("CUST-006", "Miguel Almeida Rocha", "miguel.almeida@email.com", "+55 51 96789-0123"),
        ("CUST-007", "Camila Dias Carvalho", "camila.dias@email.com", "+55 21 97890-1234"),
        ("CUST-008", "Rafael Gomes Ribeiro", "rafael.gomes@email.com", "+55 31 98901-2345"),
        ("CUST-009", "Patrícia Moreira Nunes", "patricia.moreira@email.com", "+55 61 99012-3456"),
        ("CUST-010", "Fernando Araújo Cardoso", "fernando.araujo@email.com", "+55 11 90123-4567"),
    ]

    now = datetime.now()
    for cust in customers:
        created = now - timedelta(days=random.randint(30, 180))
        conn.execute(
            "INSERT INTO customers (id, name, email, phone, total_orders, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (cust[0], cust[1], cust[2], cust[3], 0, created.isoformat()),
        )


def seed_orders(conn):
    """Insere pedidos com dados variados."""
    items_catalog = [
        {"name": "iPhone 15 Pro", "quantity": 1, "price": 10499.00},
        {"name": "MacBook Air M3", "quantity": 1, "price": 12999.00},
        {"name": "AirPods Pro", "quantity": 1, "price": 2499.00},
        {"name": "Samsung Galaxy S24", "quantity": 1, "price": 5999.00},
        {"name": "Tablet Samsung A9", "quantity": 1, "price": 1899.00},
        {"name": "Camiseta Nike Dri-FIT", "quantity": 2, "price": 199.00},
        {"name": "Calça Jeans Levi's 501", "quantity": 1, "price": 449.00},
        {"name": "Moletom Adidas", "quantity": 1, "price": 399.00},
        {"name": "Tênis Nike Air Max", "quantity": 1, "price": 899.00},
        {"name": "Jaqueta Columbia", "quantity": 1, "price": 799.00},
        {"name": "Liquidificador Vitamix", "quantity": 1, "price": 3499.00},
        {"name": "Aspirador Dyson V15", "quantity": 1, "price": 4999.00},
        {"name": "Jogo de lençóis King", "quantity": 1, "price": 499.00},
        {"name": "Cafeteira Nespresso", "quantity": 1, "price": 999.00},
        {"name": "Smart TV LG 55\"", "quantity": 1, "price": 3299.00},
        {"name": "Caixa de som Sonos One", "quantity": 2, "price": 1799.00},
        {"name": "Kindle Paperwhite", "quantity": 1, "price": 699.00},
        {"name": "Mochila Herschel", "quantity": 1, "price": 449.00},
        {"name": "Relógio Casio G-Shock", "quantity": 1, "price": 799.00},
        {"name": "Fones Sony WH-1000XM5", "quantity": 1, "price": 2799.00},
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
        total = sum(item["price"] * item["quantity"] for item in selected_items)

        tracking = None
        if status in ("shipped", "delivered"):
            tracking = f"BR{random.randint(100000000, 999999999)}BR"

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

    # Atualizar a contagem de pedidos por cliente
    conn.execute("""
        UPDATE customers SET total_orders = (
            SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.id
        )
    """)


def seed_refunds(conn):
    """Insere reembolsos de exemplo."""
    now = datetime.now()
    refunds = [
        (
            "REF-001", "ORD-003", "Produto chegou danificado", 2499.00, "approved",
            (now - timedelta(days=5)).isoformat()
        ),
        (
            "REF-002", "ORD-007", "Não corresponde à descrição", 449.00, "pending",
            (now - timedelta(days=2)).isoformat()
        ),
        (
            "REF-003", "ORD-012", "Desistência da compra", 899.00, "rejected",
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
    print(f"Banco de dados criado com sucesso em: {DB_PATH}")


if __name__ == "__main__":
    main()
