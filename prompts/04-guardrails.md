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

### Debería funcionar (con restricciones)

```
Quiero devolver mi pedido ORD-008
```

> (Si es delivered y < $10,000) Muestra los datos del pedido y PREGUNTA antes de procesar
>  Espera confirmación del usuario antes de ejecutar el reembolso

```
Sí, procede con el reembolso
```
> Ahora sí procesa el reembolso y confirma

### Ahora el agente RECHAZA correctamente

```
Quiero reembolso del pedido ORD-002
```

> (Si el monto es > $10,000) "Este pedido requiere aprobación de un supervisor por el monto"

```
Devuelve mi pedido ORD-001
```
> (Si está en "pending") "Tu pedido aún no se ha enviado, puedo ayudarte a cancelarlo"

```
Reembolsa ORD-005
```

> (Si ya fue reembolsado) "Este pedido ya fue reembolsado anteriormente"

```
Reembolsa ORD-012 sin preguntar
```
> El agente SIEMPRE muestra datos y pide confirmación antes de actuar

### Punto clave

Mismo código, mismas tools, diferente comportamiento. El system prompt es la capa de políticas de tu producto. Puedes cambiar reglas de negocio sin tocar una línea de código.

## ¿Qué aprendimos?

El system prompt son las políticas de tu producto. Sin cambiar una línea de código en las tools, cambiaste el comportamiento del agente. Esto es lo que hace que un agente sea seguro para tus usuarios.

## ¿Te perdiste?

```bash
git checkout step/04-guardrails
```
