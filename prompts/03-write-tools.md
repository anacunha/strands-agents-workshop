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

### Debería funcionar

```
Quiero devolver mi pedido ORD-005, llegó dañado
```

```
Necesito un reembolso del pedido ORD-003, no era lo que esperaba
```

```
Devuelve ORD-007 por favor, me equivoqué de talla
```

### No debería poder hacer esto (pero lo hace sin restricciones)

```
Reembolsa ORD-005 otra vez
```

> La tool lo rechaza (ya está reembolsado) ← esto sí funciona por validación en código

```
> Reembolsa ORD-999
```

> → La tool lo rechaza (no existe) ← esto sí funciona por validación en código

```
> Reembolsa TODOS mis pedidos
```

> Podría intentar reembolsar todo sin cuestionar (no hay reglas de negocio aún)

```
> Quiero devolver un pedido que compré hace 6 meses

```
>  Lo procesa sin verificar antigüedad (no hay restricción de tiempo)

### Punto clave

El agente ahora puede actuar sobre los datos. Pero sin reglas de negocio, hace todo lo que le pidas sin cuestionar. Eso es peligroso en un producto real.

## ¿Qué aprendimos?

El agente encadenó herramientas: primero consultó el pedido (get_order_status), luego procesó el reembolso (process_refund). El loop pensar→actuar→observar en acción.

## ¿Te perdiste?

```bash
git checkout step/03-write-tools
```
