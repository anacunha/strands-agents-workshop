# Paso 4: Guardrails y reglas de negocio

## Contexto

Nuestro agente ya puede consultar y actuar, pero no tiene límites. Puede reembolsar cualquier cosa sin restricción. En un producto real, necesitas reglas de negocio. El system prompt es donde viven esas reglas.

## Prompt para tu agente de código

---

```
Modifica el system prompt en shopfast/agent.py para agregar reglas de negocio.

Agrega estas restricciones:
- Solo procesar reembolsos de pedidos con estado "delivered" o "shipped"
- NO procesar reembolsos de pedidos "pending" (se pueden cancelar directamente)
- NO procesar pedidos ya reembolsados
- Si el monto es mayor a $10,000 MXN, informar que necesita aprobación de supervisor y NO procesar
- Siempre confirmar con el cliente antes de procesar: mostrar datos del pedido y preguntar si desea continuar

También agrega instrucciones de tono:
- Amable, profesional y empático
- Responder en español
- Conciso pero informativo
- Si no puede resolver, explicar por qué
```

---

## Pruébalo

```
> Quiero reembolso del pedido ORD-002
→ (Si es un pedido de más de $10,000) El agente rechaza: necesita aprobación de supervisor

> Quiero devolver mi pedido ORD-010
→ (Si está en "pending") El agente sugiere cancelar en vez de reembolsar

> Devuelve ORD-008
→ (Si es elegible) El agente muestra los datos y PREGUNTA antes de procesar
```

## ¿Qué aprendimos?

El system prompt son las políticas de tu producto. Sin cambiar una línea de código en las tools, cambiaste el comportamiento del agente. Esto es lo que hace que un agente sea seguro para tus usuarios.

## ¿Te perdiste?

```bash
git checkout step/04-guardrails
```
