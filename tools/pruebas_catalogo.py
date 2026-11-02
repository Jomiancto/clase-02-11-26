import os, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
os.environ['DJANGO_SETTINGS_MODULE'] = 'u2_proyecto1.settings'
import django
django.setup()
from django.conf import settings
from django.db import connection
from django.core.management import call_command
name = 'test_clase_catalogo_20261102'
assert settings.DATABASES['default']['NAME'] == 'u2_p1_bd'
with connection.cursor() as cursor:
    cursor.execute('SHOW DATABASES LIKE %s', [name])
    assert not cursor.fetchall(), 'La base de pruebas ya existe: no sobrescribir'
settings.DATABASES['default']['TEST']['NAME'] = name
call_command('test', 'pedidos_app.test_catalogo', 'pedidos_app.test_read', 'pedidos_app.test_update_delete', verbosity=2, interactive=False)
