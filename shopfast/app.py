"""Aplicación web de soporte al cliente para ShopFast."""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

import database
from agent import invoke_agent

app = FastAPI(title="ShopFast Soporte")

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal con resumen de soporte."""
    return templates.TemplateResponse(request, "index.html", {
        "total_orders": database.get_orders_count(),
        "pending_orders": database.get_pending_orders_count(),
        "pending_refunds": database.get_pending_refunds_count(),
        "recent_orders": database.get_recent_orders(5),
    })


@app.get("/orders", response_class=HTMLResponse)
async def orders_list(request: Request):
    """Lista de todos los pedidos."""
    return templates.TemplateResponse(request, "orders.html", {
        "orders": database.get_all_orders(),
    })


@app.get("/orders/{order_id}", response_class=HTMLResponse)
async def order_detail(request: Request, order_id: str):
    """Detalle de un pedido específico."""
    order = database.get_order(order_id)
    if not order:
        return HTMLResponse(content="Pedido no encontrado", status_code=404)
    return templates.TemplateResponse(request, "order_detail.html", {
        "order": order,
    })


@app.get("/customers", response_class=HTMLResponse)
async def customers_list(request: Request):
    """Lista de todos los clientes."""
    return templates.TemplateResponse(request, "customers.html", {
        "customers": database.get_all_customers(),
    })


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Interfaz de chat de soporte."""
    return templates.TemplateResponse(request, "chat.html", {
        "messages": [],
    })


@app.post("/chat", response_class=HTMLResponse)
async def chat_send(request: Request, message: str = Form(...)):
    """Procesa un mensaje del chat de soporte (placeholder)."""
    messages = []

    # Reconstruir historial desde campos ocultos
    form_data = await request.form()
    history_entries = form_data.getlist("history")
    for entry in history_entries:
        role, content = entry.split(":", 1)
        messages.append({"role": role, "content": content})

    # Agregar mensaje del usuario
    messages.append({"role": "user", "content": message})

    # Llamar al agente con el mensaje y el historial
    response = invoke_agent(message, messages[:-1])
    messages.append({"role": "assistant", "content": response})

    return templates.TemplateResponse(request, "chat.html", {
        "messages": messages,
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
