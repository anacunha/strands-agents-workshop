# Paso 2: Herramientas de consulta

## Contexto

Nuestro agente ya responde, pero inventa información porque no tiene acceso a los datos reales. Vamos a darle herramientas para consultar la base de datos.

## Prompt para tu agente de código

---

```
Crea un archivo shopfast/tools.py con dos herramientas para Strands Agents.

La base de datos está en shopfast/data/shop.db (SQLite). Las tablas son:
- customers: id, name, email, phone, total_orders, created_at
- orders: id, customer_id, status, tracking_number, total, items (JSON), created_at, updated_at
- refunds: id, order_id, reason, amount, status, created_at

Herramienta 1: get_order_status
- Recibe order_id (str)
- Consulta la tabla orders
- Retorna estado, tracking, total y fecha
- Si no existe, retorna mensaje claro
- Usa el decorador @tool de strands
- El docstring debe explicar cuándo usar la herramienta

Herramienta 2: get_customer_orders
- Recibe email (str)
- Busca el cliente por email y retorna todos sus pedidos
- Retorna lista con id, estado, total y fecha de cada pedido
- Si no hay resultados, retorna mensaje claro

Luego modifica shopfast/agent.py para importar ambas tools y pasarlas al Agent en el parámetro tools=[].
```

---

## Pruébalo

### Debería funcionar

```
¿Cuál es el estado de mi pedido ORD-001?
```

```
Soy maria.garcia@email.com, ¿qué pedidos tengo?
```

```
¿Ya llegó mi pedido ORD-003?
```

```
Mi email es carlos.hernandez@email.com, ¿tengo algo pendiente?
```

### No debería poder hacer esto

```
Quiero devolver mi pedido ORD-005
```

```
Cancela mi pedido ORD-001
```

```
Cambia la dirección de envío de mi pedido
```

### Punto clave

El agente ahora puede LEER datos reales, pero no puede ESCRIBIR. Consulta pero no actúa.

## ¿Qué aprendimos?

El modelo decide cuándo usar cada herramienta basándose en el docstring. Tú no escribes if/else, el modelo razona.

## ¿Te perdiste?

```bash
git checkout step/02-read-tools
```
