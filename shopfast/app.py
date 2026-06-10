"""Aplicação web de suporte ao cliente para ShopFast."""

from pathlib import Path

import markdown as md
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markupsafe import Markup

import database

from agent import invoke_agent

app = FastAPI(title="ShopFast Suporte")

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def render_markdown(text: str) -> Markup:
    """Converte texto markdown (tabelas, listas, quebras de linha) em HTML seguro."""
    html = md.markdown(text or "", extensions=["tables", "nl2br", "sane_lists"])
    return Markup(html)


templates.env.filters["markdown"] = render_markdown


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal com resumo de suporte."""
    return templates.TemplateResponse(request, "index.html", {
        "total_orders": database.get_orders_count(),
        "pending_orders": database.get_pending_orders_count(),
        "pending_refunds": database.get_pending_refunds_count(),
        "recent_orders": database.get_recent_orders(5),
    })


@app.get("/orders", response_class=HTMLResponse)
async def orders_list(request: Request):
    """Lista de todos os pedidos."""
    return templates.TemplateResponse(request, "orders.html", {
        "orders": database.get_all_orders(),
    })


@app.get("/orders/{order_id}", response_class=HTMLResponse)
async def order_detail(request: Request, order_id: str):
    """Detalhe de um pedido específico."""
    order = database.get_order(order_id)
    if not order:
        return HTMLResponse(content="Pedido não encontrado", status_code=404)
    return templates.TemplateResponse(request, "order_detail.html", {
        "order": order,
    })


@app.get("/customers", response_class=HTMLResponse)
async def customers_list(request: Request):
    """Lista de todos os clientes."""
    return templates.TemplateResponse(request, "customers.html", {
        "customers": database.get_all_customers(),
    })


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Interface de chat de suporte."""
    return templates.TemplateResponse(request, "chat.html", {
        "messages": [],
    })


@app.post("/chat", response_class=HTMLResponse)
async def chat_send(request: Request, message: str = Form(...)):
    """Processa uma mensagem do chat de suporte."""
    messages = []

    # Reconstruir histórico a partir de campos ocultos
    form_data = await request.form()
    history_entries = form_data.getlist("history")
    for entry in history_entries:
        role, content = entry.split(":", 1)
        messages.append({"role": role, "content": content})

    # Adicionar mensagem do usuário
    messages.append({"role": "user", "content": message})

    # O agente é definido em shopfast/agent.py.
    response = invoke_agent(message, messages[:-1])

    messages.append({"role": "assistant", "content": response})

    return templates.TemplateResponse(request, "chat.html", {
        "messages": messages,
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
