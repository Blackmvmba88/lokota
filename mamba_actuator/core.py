"""Offline, fail-closed metacommand parsing and dry-run execution."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import re
import uuid

ALLOWED = frozenset({"window.list", "window.focus", "window.close", "app.launch", "queue.cancel"})

@dataclass(frozen=True)
class Request:
    request_id: str
    action: str
    app: str | None = None
    dry_run: bool = True
    requires_confirmation: bool = False


def parse(text: str) -> Request:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Empty command")
    phrase = re.sub(r"\\s+", " ", text.strip()).casefold()
    if phrase in ("lista las ventanas", "listar ventanas", "qué ventanas hay", "que ventanas hay"):
        action, app = "window.list", None
    elif phrase in ("detente", "cancela la cola", "cancelar cola"):
        action, app = "queue.cancel", None
    else:
        match = re.fullmatch(r"(cierra (?:la ventana de |ventana de )|enfoca |abre (?:la aplicación |la aplicacion )?)([\\w .-]{1,80})", phrase)
        if not match:
            raise ValueError("Unrecognized or ambiguous command")
        verb, app = match.groups()
        app = app.strip(" .")
        if not app:
            raise ValueError("Missing app")
        if verb.startswith("cierra"):
            action = "window.close"
        elif verb.startswith("enfoca"):
            action = "window.focus"
        else:
            action = "app.launch"
    return Request(str(uuid.uuid4()), action, app, True, action == "window.close")


def simulate(request: Request) -> dict:
    if request.action not in ALLOWED or not request.dry_run:
        return {"request_id": request.request_id, "status": "denied", "reason": "MVP is dry-run only"}
    return {"request_id": request.request_id, "status": "simulated", "request": asdict(request), "executed": False,
            "message": "No desktop action was performed"}
