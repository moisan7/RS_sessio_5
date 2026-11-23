# AGENTS.md — Directives per a l'agent de programació

## Entorn i Stack Tècnic
- Llenguatge: Python 3.11+ (només biblioteca estàndard; `pytest` només per als tests).
- Interfície: Línia de comandes (CLI) amb mòdul `argparse`.
- Manteniment de Dades: Fitxer JSON local (`data/tasks.json`), relatiu a la carpeta des d'on s'executa.
- Estructura: `src/` (codi), `test/` (tests), `data/` (dades), fitxers de govern a l'arrel.

## Comandes de Desenvolupament
- Executar aplicació: `python3 src/tasks_app.py list`
- Executar tots els tests: `python3 -m pytest test`
- Executar test únic: `python3 -m pytest test/test_tasks_app.py`
- Variant amb entorn virtual (Windows): `.venv/Scripts/python -m pytest test`
- Instal·lar dependències autoritzades: `pip install -r requirements.txt`

## Convencions de Codi
- Estil: PEP8.
- Idioma del codi i comentaris: Català (mantenir consistència en noms de variables).
- Els tests no han de modificar mai el `data/tasks.json` real: executen l'aplicació en una carpeta temporal.
- Cada test porta l'ID de l'escenari a `SPECIFICATIONS.md`, per exemple `test_gs_04_...`, i cita el requisit al docstring.

## Regles de Gestió de Tasques (`TASKS.md`)
1. Llegeix `TASKS.md` i identifica la següent tasca amb estat `[ ]`.
2. Canvia l'estat de la tasca actual a `[/]` abans d'iniciar la codificació.
3. Executa ÚNICAMENT una sola tasca per torn.
4. Verifica que el codi compleixi els requisits i escenaris Gherkin de `SPECIFICATIONS.md`.
5. Quan estigui completada i verificada, canvia l'estat a `[x]`.
6. Atura't i demana confirmació a l'usuari abans de passar a la següent tasca.

## Regles de Git
- Un commit per cada tasca finalitzada, amb el canvi a `[x]` de `TASKS.md` inclòs.
- Format del missatge: `feat(T2.6): descripció breu (RF-05)`; també `test(...)`, `docs(...)`.
- Els canvis a `SPECIFICATIONS.md` i a `AGENTS.md` van en commits propis, abans del codi que els implementa.
- Al tancar un sprint: `git commit -m 'feat: Iteracio inicial completada'`, `'feat: Iteracio 2 completada'` o `'feat: Iteracio 3 completada'`.

## Restriccions de Desenvolupament
- No instal·lis llibreries externes no autoritzades.
- Només es pot modificar `src/`, `test/`, `data/` i els fitxers `AGENTS.md`, `SPECIFICATIONS.md`, `TASKS.md` i `repositori.txt`.
- Mai modifiquis `.devcontainer/` ni `requirements.txt`.
- Mai ometis, esborris ni desactivis un test que falla per fer-lo passar: corregeix el codi.
- Mai facis commit de claus secretes, de `.venv/` ni de fitxers generats (`__pycache__/`, `.pytest_cache/`).
