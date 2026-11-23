# TASKS.md - Tasks_app

Estats: `[ ]` pendent · `[/]` en procés · `[x]` completada.
Format: `Tasca X.Y: <entregable únic> — Req: <IDs> — Depèn de: <tasques>`.

## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:

- [ ] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial (`[]`). — Req: RF-01, RF-02 — Depèn de: cap
- [ ] Tasca 1.2: Implementar model de dades `Tasca` a `src/models.py` amb mètodes de serialització JSON. — Req: RF-01 — Depèn de: 1.1
- [ ] Tasca 1.3: Implementar la persistència a `src/persistencia.py` (carregar/desar, creació de `data/tasks.json` si no existeix). — Req: RF-01, RF-02 — Depèn de: 1.2
- [ ] Tasca 1.4: Desenvolupar `src/tasks_app.py` amb les opcions `add` i `list`. — Req: RF-03, RF-04 — Depèn de: 1.3
- [ ] Tasca 1.5: Crear tests d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03. — Req: GS-01, GS-02, GS-03 — Depèn de: 1.4
- [ ] Tasca 1.6: Validar l'execució i verificar que tots els tests passen (`python3 -m pytest test`). — Req: GS-01, GS-02, GS-03 — Depèn de: 1.5
