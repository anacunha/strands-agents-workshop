# Paso 3: Herramienta de acción

## Contexto

Nuestro agente ya consulta datos, pero no puede hacer nada con ellos. Ahora le vamos a dar la capacidad de ACTUAR: procesar un reembolso que modifica la base de datos.

## Prompt para tu agente de código

---

```
Agrega una nueva herramienta en shopfast/tools.py llamada process_refund.

Requisitos:
- Recibe order_id (str) y reason (str)
- Verifica que el pedido existe en la tabla orders
- Verifica que no esté ya reembolsado (status != "refunded")
- Crea un registro en la tabla refunds con: id auto-generado (REF-XXX), order_id, reason, amount (el total del pedido), status "approved", created_at
- Actualiza el status del pedido a "refunded" en la tabla orders
- Retorna confirmación con el ID del reembolso y monto
- Si hay error (pedido no existe, ya reembolsado), retorna mensaje claro

El docstring debe indicar que esta herramienta se usa cuando el cliente quiere devolver un producto.

Agrega la tool al agente en agent.py.
```

---

## Pruébalo

```
> Quiero devolver mi pedido ORD-005, llegó dañado
→ El agente consulta el pedido, verifica que es elegible, procesa el reembolso
```

Ahora ve a http://localhost:8000/orders/ORD-005 en el navegador.
→ El estado cambió a "refunded"

## ¿Qué aprendimos?

El agente encadenó herramientas: primero consultó el pedido (get_order_status), luego procesó el reembolso (process_refund). El loop pensar→actuar→observar en acción.

## ¿Te perdiste?

```bash
git checkout step/03-write-tools
```
