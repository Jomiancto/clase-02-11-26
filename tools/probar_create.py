"""Prueba HTTP real; reutiliza el conjunto de prueba si ya existe, sin borrar datos."""
import json, os, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
root=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','u2_proyecto1.settings')
import django
django.setup()
from pedidos_app.models import Categoria,Cliente,Producto,Pedido,Item
from django.db import connection
base='http://127.0.0.1:8000/api/'
results=[]
def request(resource,body=None,method=None):
    req=Request(base+resource+'/',data=json.dumps(body).encode() if body is not None else None,
                headers={'Content-Type':'application/json'},method=method)
    try:
        with urlopen(req,timeout=15) as res: return res.status,json.load(res)
    except HTTPError as err: return err.code,json.load(err)
def create(resource,model,lookup,body):
    matches=list(model.objects.filter(**lookup))
    assert len(matches)<=1, 'Datos de prueba ambiguos; revisar sin duplicar'
    if matches:
        obj=matches[0]; status='REUTILIZADO'; data={'id':obj.pk}
    else:
        status,data=request(resource,body); assert status==201,(resource,status,data)
        obj=model.objects.get(pk=data['id'])
    for field,value in body.items():
        if field=='categorias': assert set(obj.categorias.values_list('pk',flat=True))==set(value)
        elif field in ['cliente','pedido','producto']: assert getattr(obj,field+'_id')==value
        else: assert str(getattr(obj,field))==str(value),(field,getattr(obj,field),value)
    row={'endpoint':resource,'enviado':body,'http':status,'recibido':data,'mariadb':'coincide'}
    results.append(row);print(json.dumps(row,ensure_ascii=False));return obj.pk
cat=create('categorias',Categoria,{'nombre':'Clase 02-11-2026'},{'nombre':'Clase 02-11-2026'})
cli=create('clientes',Cliente,{'email':'clase-02-11-2026@example.test'},{'nombre':'Cliente de clase','email':'clase-02-11-2026@example.test'})
prod=create('productos',Producto,{'codigo':'HTTP-021126'},{'nombre':'Producto prueba HTTP','descripcion':'Prueba CREATE desde Cmder','precio':2500,'stock':10,'activo':True,'codigo':'HTTP-021126','categorias':[cat]})
ped=create('pedidos',Pedido,{'cliente_id':cli,'fecha':'2026-11-02'},{'fecha':'2026-11-02','pagado':False,'cliente':cli})
item=create('items',Item,{'pedido_id':ped,'producto_id':prod},{'cantidad':2,'precio_unitario':2500,'pedido':ped,'producto':prod})
counts={m.__name__:m.objects.count() for m in [Categoria,Cliente,Producto,Pedido,Item]}
invalid=[('categorias',{'nombre':'Clase 02-11-2026'}),('clientes',{'nombre':'Error','email':'correo-invalido'}),('clientes',{'nombre':'Error','email':'clase-02-11-2026@example.test'}),('productos',{'nombre':'Error','precio':-1,'stock':1,'codigo':'ERROR','categorias':[cat]}),('productos',{'nombre':'Error','precio':1,'stock':1,'codigo':'ERROR','categorias':[999999999]}),('pedidos',{'fecha':'2026-11-02','pagado':False,'cliente':999999999}),('items',{'cantidad':-1,'precio_unitario':1,'pedido':ped,'producto':prod}),('items',{'cantidad':1,'precio_unitario':1,'pedido':999999999,'producto':prod})]
for resource,body in invalid:
    status,data=request(resource,body);assert status==400,(resource,status,data)
    results.append({'endpoint':resource,'enviado':body,'http':status,'recibido':data})
assert counts=={m.__name__:m.objects.count() for m in [Categoria,Cliente,Producto,Pedido,Item]}
for method in ['PUT','PATCH','DELETE']:
    status,data=request('productos',{},method);assert status==405,(method,status,data)
    results.append({'metodo':method,'http':status})
with connection.cursor() as cursor:
    cursor.execute('SELECT id,nombre,precio,stock,codigo FROM pedidos_app_producto WHERE id=%s',[prod]);print('SQL producto:',cursor.fetchone())
    cursor.execute('SELECT producto_id,categoria_id FROM pedidos_app_producto_categorias WHERE producto_id=%s',[prod]);assert cursor.fetchall()==((prod,cat),)
(root/'.local'/'pruebas_create.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('CREATE_OK: cinco entidades persistidas; M2M/FK correctas; ocho rechazos HTTP 400 sin inserciones; PUT/PATCH/DELETE 405.')
