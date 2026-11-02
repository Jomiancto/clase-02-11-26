"""Comprueba GET sin insertar datos."""
import json, sys
from urllib.request import urlopen
port=sys.argv[1] if len(sys.argv)>1 else '8000'
for path in ['/', '/api/', '/api/categorias/', '/api/clientes/', '/api/productos/', '/api/pedidos/', '/api/items/']:
    with urlopen('http://127.0.0.1:'+port+path,timeout=10) as res:
        data=json.load(res)
        assert res.status==200
        print('GET',path,res.status,'count='+str(data['count']) if 'count' in data else 'OK')
