"""
Settings de prueba (settings_demo.py)

- Hereda todo de settings.py
- Cambia la BD por db_demo.sqlite3
- Añade FIXTURE_DIRS para buscar fixtures/demo.json
"""

from .settings import *  # Importa la configuración base

# ----------------------------------------------------------------------------------
# Base de datos de demo (SQLite separada)
# ----------------------------------------------------------------------------------
DATABASES["default"]["NAME"] = BASE_DIR / "db_demo.sqlite3"

# ----------------------------------------------------------------------------------
# Fixtures de demostración
# ----------------------------------------------------------------------------------
# Django buscará cualquier <nombre>.json dentro de BASE_DIR / "fixtures"
FIXTURE_DIRS = [BASE_DIR / "TiendaHistorias" / "fixtures"]
# ----------------------------------------------------------------------------------
# DEBUG activo para servir static y media en desarrollo
# ----------------------------------------------------------------------------------
DEBUG = True        # Ya suele estar en settings.py; aquí lo reafirmamos por claridad
ALLOWED_HOSTS = []  # Mantén vacío mientras uses runserver local
