# 📦 Modules

- `config.py` — configuration via Pydantic
- `database/` — database manager, ORM models (Peewee + SQLite3)
- `adapter.py` — Data Server integration
- `core/` — parsing logic (extractor, parser, saver)
- `cli.py`, `cli_db.py` — interactive CLI tools
- `http_client` — ready-to-use HTTP client with workers and proxy support

> Each module is a separate responsibility zone, KISS principle. 