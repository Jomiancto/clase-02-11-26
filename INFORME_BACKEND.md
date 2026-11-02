# Resultado de la clase — 2 de noviembre de 2026

## Backend y MariaDB comprobados

- Proyecto independiente en E:/cmder/clase-02-11-26.
- Fuente Unidad2: af1614d58d43db6e7360ce4b9f1c682e0e5c604d. Se conservo su modificacion local de COMANDOS_CMDER en .local/COMANDOS_UNIDAD2_original.md; el archivo original no se modifico.
- Profesor sin cambios remotos: 01966d65548bc41cb09249d956c67f2306c85b68.
- Nuevo origin exclusivo: https://github.com/Jomiancto/clase-02-11-26.git.
- Entorno virtual independiente; pip check correcto.
- MariaDB portable iniciada porque estaba detenida. Instancia existente, no inicializada otra vez.
- SELECT VERSION(), DATABASE(), @@port y @@datadir confirmaron 12.3.2, u2_p1_bd, 3306 y directorio portable E:/MariaDB.
- Se preservan las 18 tablas, incluidas productos_app_*. PK, FK, unicidad y M2M verificadas.
- showmigrations: tres migraciones pedidos_app [X]. migrate --plan vacio, migrate --check correcto, makemigrations sin cambios.
- Respaldo local antes de POST: 26123 bytes; no publicado.
- Django ejecutandose en Cmder, 127.0.0.1:8000; puerto estaba libre. Ningun proceso ajeno detenido.

## Pruebas HTTP reales desde Cmder

Cada respuesta se cotejo con su objeto recargado desde MariaDB. Primera ejecucion:

| Entidad | HTTP | ID | Datos relevantes |
|---|---|---|---|
| Categoria | 201 | 1 | Clase 02-11-2026 |
| Cliente | 201 | 1 | Cliente de clase, clase-02-11-2026@example.test |
| Producto | 201 | 1 | Producto prueba HTTP, HTTP-021126, precio 2500, stock 10, categoria 1 |
| Pedido | 201 | 1 | 2026-11-02, pagado false, cliente 1 |
| Item | 201 | 1 | cantidad 2, precio_unitario 2500, pedido 1, producto 1 |

SQL leyo el producto (1, Producto prueba HTTP, 2500, 10, HTTP-021126).
La tabla M2M contiene (producto_id 1, categoria_id 1).
Ocho POST invalidos devolvieron 400 sin variar conteos: categoria duplicada, email
invalido/duplicado, precio negativo, categoria inexistente, cliente inexistente,
cantidad negativa y pedido inexistente. PUT/PATCH/DELETE en productos devolvieron 405.
Bodies y respuestas completos: .local/pruebas_create.json y log de 08_pruebas.
Los ejemplos JSON reproducibles se conservan en README y Bruno.

## Incidencias corregidas

1. Salida netstat hacia cp1252: registro corregido a UTF-8 con sustitucion.
2. Python global dentro de subprocess: iniciador usa ruta explicita .venv/Scripts/python.exe.
3. VS Code 1.88.1 no activa Bruno 6 (crypto.subtle); preparado VS Code oficial ZIP 1.144.0 independiente.
4. Tres extensiones DB duplicadas registraban los mismos comandos: editor de clase tiene solo Database Client.
5. ZIP actual guarda resources dentro de directorio de version: deteccion ajustada sin repetir descarga.

No se implementaron UPDATE, DELETE ni Evaluacion II.

## Publicacion comprobada

Push desde Cmder correcto: commit 6a2afe0879307efbfb7904bbba0fee2e6427c966 en main.
Git ls-remote coincide. El conector GitHub recupero serializers.py y bruno/bruno.json
desde el repositorio oficial, confirmando los archivos publicados.

## Prueba visual en VS Code

Bruno oficial 6.0.0 activo en VS Code 1.144.0. Coleccion abierta y entorno Local seleccionado.
Se envio una sola vez 03 Crear producto: HTTP 201 Created, ID 2, Cuaderno Backend,
precio 2500, stock 10, activo true, codigo CLASE-021126, categorias [1].
Verificacion SQL independiente: (2, Cuaderno Backend, 2500, 10, 1, CLASE-021126).
El verificador exige un solo registro con ese codigo; no se repitio POST.
Database Client MariaDB conecto con Connection Success (287 ms).

Database Client mostro visualmente las 18 tablas, columnas de pedidos_app_producto
y sus dos filas: Producto prueba HTTP (ID 1) y Cuaderno Backend (ID 2).
La segunda fila coincide con el JSON y la respuesta 201 de Bruno.
La conexion activa de SQL queda en u2_p1_bd.

Navegador integrado de VS Code: /api/ muestra HTTP 200 OK y los cinco enlaces.
Terminal integrada abierta usando el perfil Cmder (vendor/bin/vscode_init.cmd);
Django permanece en Cmder/ConEmu externo. Los scripts de clase no dependen del terminal integrado.
Bruno guardo automaticamente productoId=2 en Local.bru despues del POST visual.

Pruebas visuales finales completadas: producto en Bruno y Database Client; navegador integrado HTTP 200.
Las cinco entidades se probaron por HTTP desde Cmder; el producto adicional se envio desde la interfaz Bruno.
No se atribuyen las otras cuatro creaciones a clicks de Bruno.


## Actualizacion READ — 02-11-2026

Se agregaron listar_clientes(request) y listar_cliente(request, id), ambas con
@api_view(['GET']). Se mantienen CREATE, serializers, modelos, migraciones y /api/.
Rutas exactas sin barra final: /clientes y /clientes/<int:id>.
Listado devuelve todos los clientes con many=True y HTTP 200 (incluido []);
detalle usa ORM get(pk=id) y devuelve 200 o 404 Cliente no encontrado.

Pruebas automaticas desde Cmder: cinco tests correctos, sin configurar base de pruebas.
Django check sin errores; makemigrations --check --dry-run sin cambios;
migrate --check correcto. No se aplicaron migraciones.
HTTP real: /clientes 200; /clientes/1 200; /clientes/999999999 404.
GET de /, /api/ y las cinco colecciones anteriores: 200.
POST invalido en /api/clientes/: 400; CREATE valido: 201 en DRF con validacion real,
comprobando la llamada a ORM create() simulada. No se ejecuto INSERT para repetir CREATE.

Bruno en VS Code ejecuto los tres GET y mostro 200, 200 y 404 con el entorno Local.
El listado mostro un cliente y el detalle devolvio:
ID 1; nombre Cliente de clase; email clase-02-11-2026@example.test.
Database Client conectado a u2_p1_bd mostro pedidos_app_cliente con exactamente esa fila.
Los hashes de todas las filas de pedidos_app_*, M2M y productos_app_* coincidieron
con la instantanea tomada antes de las pruebas. Ningun cliente fue creado, modificado o borrado.

El servidor anterior de este proyecto (PID 11548, --noreload) se identifico mediante
su cadena de procesos hasta .local/07_servidor.cmd dentro de Cmder. Solo ese proceso
se detuvo para cargar las vistas; MariaDB y procesos ajenos se conservaron.
La nueva sesion .local/22_read_servidor.cmd mantiene Django en 127.0.0.1:8000.
VS Code conserva Bruno READ, Database Client, codigo y navegador integrado disponibles.
No se implementaron PATCH, PUT, DELETE ni Evaluacion II.
