# MAMBA ACTUATOR 🐍

**BlackMamba RECORDS · Iyari Gomez**  
**Estado:** diseño inicial; sin agente de escritorio instalado.

## Concepto
Un puente entre órdenes habladas o escritas y acciones verificables en una computadora autorizada. El usuario puede decir «cierra la ventana de Blender». La IA interpreta la intención, un agente local autorizado identifica la ventana, aplica la política de seguridad, ejecuta la operación y verifica el resultado.

**No se trata de darle libertad irrestricta a la IA, sino capacidad de acción limitada, observable y auditable.**

## Flujo
```text
Usuario (voz/texto) → OÍDO / interfaz → parser de metacomandos
  → solicitud tipada → WARPBLACK (política y autorización)
  → agente local MAMBA ACTUATOR (macOS)
  → API de Accesibilidad / automatización
  → nueva lectura de estado → comparación → respuesta con evidencia
```

### Ejemplo de metacomando
Usuario: «Cierra la ventana de Blender».

```json
{
  "request_id": "UUID",
  "action": "window.close",
  "target": {"app": "Blender", "window_id": "id-obtenido-de-la-observacion"},
  "dry_run": true
}
```

El agente primero enumera ventanas; si hay más de una coincidencia solicita precisión. Nunca inventa identificadores. Si detecta cambios sin guardar, solicita confirmación antes de cerrar.

Respuesta esperada:
```json
{
  "request_id": "UUID",
  "status": "verified",
  "evidence": {"window_present_after": false}
}
```
El estado `verified` solo se emite después de una lectura de comprobación real; si no puede comprobarse se responde `uncertain`, `denied` o `failed`.

## Metacomandos MVP
- `window.list`: listar ventanas; solo lectura.
- `window.focus`: enfocar una ventana.
- `window.close`: cerrar ventana con precauciones para documentos sin guardar.
- `app.launch`: abrir aplicación de la lista permitida.
- `queue.cancel`: cancelar acciones pendientes.

## Principios técnicos y de seguridad
- Agente local y autenticado; privilegios mínimos y permisos expresos de macOS.
- Denegar acciones no reconocidas; no ejecutar comandos de shell arbitrarios desde lenguaje natural.
- `dry_run` como comportamiento inicial; confirmación para acciones de impacto.
- Identificación inequívoca de objetivo, IDs únicos de solicitud e idempotencia.
- Política de aprobación para borrar, enviar información, pagos o pérdida de datos.
- Log de auditoría sin secretos, comprobación posterior y reporte transparente de fallos.
- Respetar las barreras de autorización y el protocolo de WARPBLACK.

## Roadmap
1. Inventario de ventanas macOS en modo solo lectura.
2. Esquemas JSON y validador de metacomandos.
3. Motor de políticas y simulación `dry_run`.
4. Actuadores `window.focus` y `window.close` con pruebas.
5. Verificador por lectura posterior, registro de auditoría y adaptador WARPBLACK.
6. Integraciones optativas con Observador, OÍDO y Blender.

## Estado actual
Este commit únicamente documenta la idea. **No instala software, no habilita clics remotos ni controla la Mac todavía.**

El README anterior de **BlackMamba University** se conservó íntegro en [docs/BLACKMAMBA_UNIVERSITY_ORIGINAL.md](docs/BLACKMAMBA_UNIVERSITY_ORIGINAL.md).

**READ → PLAN → AUTHORIZE → ACT → READ BACK → COMPARE → CERTIFY**

## Prototipo ejecutable (v0.1.0)

El repositorio incluye ahora un parser de metacomandos y simulador **sin efectos sobre macOS**: `mamba_actuator/core.py`, una CLI y pruebas unitarias.

Desde la raíz del repositorio, con Python 3.10+:

```bash
python3 -m mamba_actuator "lista las ventanas"
python3 -m mamba_actuator "cierra la ventana de Blender"
python3 -m unittest discover -s tests -v
```

La salida de la CLI será JSON con `status: simulated` y `executed: false`. Una orden desconocida se deniega. **Las pruebas están escritas, pero su ejecución en macOS/GitHub Actions aún no se ha verificado.** No hay integración activa con WARPBLACK ni acceso al escritorio.
