# TASKS.md - Tasks_app

Estats: `[ ]` pendent · `[/]` en procés · `[x]` completada.
Format: `Tasca X.Y: <entregable únic> — Req: <IDs> — Depèn de: <tasques>`.

## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial (`[]`). — Req: RF-01, RF-02 — Depèn de: cap
- [x] Tasca 1.2: Implementar model de dades `Tasca` a `src/models.py` amb mètodes de serialització JSON. — Req: RF-01 — Depèn de: 1.1
- [x] Tasca 1.3: Implementar la persistència a `src/persistencia.py` (carregar/desar, creació de `data/tasks.json` si no existeix). — Req: RF-01, RF-02 — Depèn de: 1.2
- [x] Tasca 1.4: Desenvolupar `src/tasks_app.py` amb les opcions `add` i `list`. — Req: RF-03, RF-04 — Depèn de: 1.3
- [x] Tasca 1.5: Crear tests d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03. — Req: GS-01, GS-02, GS-03 — Depèn de: 1.4
- [x] Tasca 1.6: Validar l'execució i verificar que tots els tests passen (`python3 -m pytest test`). — Req: GS-01, GS-02, GS-03 — Depèn de: 1.5

## Increment 2: Data límit, edició, completat i indicadors

Objectiu: Permetre registrar una data límit, corregir tasques, completar-les i veure les caducades i urgents al llistat.

### Tasques d'Execució:

- [x] Tasca 2.1: Actualitzar `SPECIFICATIONS.md` a la v2.0 (US-03..US-06, RF-05..RF-14, RNF, GS-04..GS-17, glossari, traçabilitat). — Req: tots els de la v2.0 — Depèn de: 1.6
- [x] Tasca 2.2: Actualitzar `AGENTS.md` (comandes amb `.venv`, límits "Mai…", convenció de commits i de noms de test). — Req: RNF-02 — Depèn de: 2.1
- [x] Tasca 2.3: Afegir `data_limit` (opcional) al model `Tasca` mantenint la compatibilitat amb el JSON de la v1.0, amb test unitari. — Req: RNF-01, GS-16 — Depèn de: 2.1
- [x] Tasca 2.4: Gestió d'errors: excepció `ErrorTasques`, sortida a `stderr` amb codi 1 a `main()` i JSON invàlid sense sobreescriure, amb tests. — Req: RNF-03, RNF-05, GS-17 — Depèn de: 2.3
- [x] Tasca 2.5: Implementar `validar_data` a `src/logica.py`, amb tests unitaris. — Req: RF-06 — Depèn de: 2.4
- [ ] Tasca 2.6: Afegir l'opció `--due` al comandament `add`, amb tests. — Req: RF-05, RF-06, GS-04, GS-05 — Depèn de: 2.5
- [ ] Tasca 2.7: Implementar `cercar_per_id` a `src/logica.py` amb l'error d'ID inexistent, amb tests unitaris. — Req: RF-08 — Depèn de: 2.4
- [ ] Tasca 2.8: Implementar el comandament `edit`, amb tests. — Req: RF-07, RF-08, RF-09, GS-06, GS-07, GS-08, GS-09 — Depèn de: 2.5, 2.7
- [ ] Tasca 2.9: Implementar el comandament `complete`, amb tests. — Req: RF-10, RF-11, RF-08, GS-08, GS-10, GS-11 — Depèn de: 2.7
- [ ] Tasca 2.10: Implementar `calcular_indicador(tasca, avui)` a `src/logica.py`, amb tests unitaris de límits. — Req: RF-13, RF-14, GS-14, GS-15 — Depèn de: 2.3
- [ ] Tasca 2.11: Mostrar la data límit i els indicadors `[CADUCADA]` i `[URGENT]` al comandament `list`, amb tests. — Req: RF-12, RF-13, RF-14, GS-12, GS-13 — Depèn de: 2.10
- [ ] Tasca 2.12: Completar i revisar els tests d'integració dels escenaris GS-04..GS-17 i executar la regressió (`python3 -m pytest test`). — Req: GS-01..GS-17 — Depèn de: 2.6, 2.8, 2.9, 2.11
