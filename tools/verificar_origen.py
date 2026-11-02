"""Comprueba los archivos que esta clase debe conservar intactos."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent.parent
source=Path(r'E:\cmder\Unidad2')
files=[Path('pedidos_app/models.py'),*map(lambda p:p.relative_to(source),(source/'pedidos_app/migrations').glob('*.py'))]
for path in files:
    assert (source/path).read_bytes()==(root/path).read_bytes(),str(path)
    print('Conservado',path,hashlib.sha256((root/path).read_bytes()).hexdigest())
print('Modelos y migraciones originales intactos. Fuente no modificada.')
