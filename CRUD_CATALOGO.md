# CRUD Categoria y Producto — 2 de noviembre de 2026

Servidor local: http://127.0.0.1:8000. MariaDB: 127.0.0.1:3306, u2_p1_bd, usuario local root.
Credenciales y perfil del editor privados. Repositorio: Jomiancto/clase-02-11-26, main.
Se partio del commit f267e04. Unidad2 y el proyecto de evaluacion no se modificaron.

## Implementacion

Las diez funciones estan en pedidos_app/views.py y sus rutas en u2_proyecto1/urls.py.
Cada funcion usa @api_view con el metodo correspondiente; comparten ayudantes de validacion,
consulta y transacciones para no copiar la misma logica. Se reutilizan CategoriaSerializer y
ProductoSerializer sin cambios, y se mantienen las vistas anteriores bajo /api/.

| Funcion | Metodo y ruta | Respuesta correcta |
|---|---|---|
| crear_categoria | POST /categoria/agregar | 201 |
| listar_categorias | GET /categorias | 200, lista o [] |
| listar_categoria | GET /categorias/<id> | 200, objeto |
| modificar_categoria | PATCH /categoria/modificar | 200 |
| borrar_categoria | DELETE /categoria/eliminar | 204, sin cuerpo |
| crear_producto | POST /producto/agregar | 201 |
| listar_productos | GET /productos | 200, lista o [] |
| listar_producto | GET /productos/<id> | 200, objeto |
| modificar_producto | PATCH /producto/modificar | 200 |
| borrar_producto | DELETE /producto/eliminar | 204, sin cuerpo |

Las rutas exactas no llevan barra final. POST/PATCH/DELETE requieren objeto JSON.
PATCH y DELETE reciben id entero positivo (hasta bigint firmado); no string ni booleano.
DELETE solo admite id. PATCH requiere al menos un campo editable ademas de id.
Campos desconocidos o de solo lectura: 400. El id del PATCH solo selecciona la fila; no se actualiza.
Categoria admite nombre; Producto admite nombre, descripcion, precio, stock, activo, codigo, categorias.
No se escribe creado. Valores por defecto y restricciones son los de los modelos existentes:
precio y stock admiten 0 y rechazan negativos; codigo no es unico; categorias debe ser una lista
no vacia de IDs existentes conforme al serializer actual. No se inventaron restricciones nuevas.

Validacion invalida o conflicto de unicidad/relacion al guardar: 400 con error. ID inexistente: 404.
Categoria con productos: DELETE 409 sin tocar asociaciones. Producto con items: DELETE 409,
con comprobacion ORM y captura de ProtectedError. No se borran pedidos ni items desde estas vistas.

CREATE y PATCH se guardan dentro de transaction.atomic. PATCH bloquea la fila seleccionada;
las escrituras M2M bloquean las categorias en orden estable y guardan producto y relaciones en
la misma transaccion. Si categorias se omite en PATCH, se conserva; si se envia, reemplaza sus IDs.
Los GET incluyen categorias como lista de IDs y usan prefetch_related en el listado de productos.
No hay cambios de esquema, migraciones ni logica de Cliente.

## JSON usados realmente

~~~json
{"nombre":"TEMP Catalogo 021126 A"}
~~~

~~~json
{"id":2,"nombre":"TEMP Catalogo 021126 A editada"}
~~~

~~~json
{"nombre":"TEMP Producto","descripcion":"Prueba controlada","precio":2500,"stock":4,"activo":true,"codigo":"TEMP-CAT-021126","categorias":[2]}
~~~

~~~json
{"id":3,"nombre":"TEMP Producto editado","descripcion":"Editado desde Bruno","precio":3200,"stock":7,"activo":false,"codigo":"TEMP-CAT-021126","categorias":[3]}
~~~

DELETE Categoria: {"id":2}. DELETE Producto: {"id":3}.
Ejemplos invalidos: categoria duplicada; PATCH Producto {"id":3,"stock":-1};
precio -1, categoria 999999999 y creado enviado tambien devuelven 400.
Estos IDs describen la sesion ejecutada: los temporales ya no existen. En otra sesion usar IDs nuevos.

## Evidencia real en Bruno, HTTP y MariaDB

| Paso | Resultado |
|---|---|
| Categoria A creada desde Bruno | POST 201, ID 2 |
| Categorias lista y detalle en Bruno | GET 200, GET /categorias/2 200 |
| Nombre cambiado en Bruno y verificado por ORM/SQL | PATCH 200, A editada |
| Categoria B creada por HTTP desde Cmder | POST 201, ID 3 |
| Producto asociado a Categoria A desde Bruno | POST 201, ID 3, categorias [2] |
| Productos lista y detalle en Bruno | GET 200, GET /productos/3 200 |
| Producto modificado desde Bruno | PATCH 200, precio 3200, stock 7, activo false, categorias [3] |
| Comprobacion SQL posterior | Campos persistidos y creado sin cambios |
| PATCH HTTP omitiendo categorias | 200, descripcion Solo descripcion, categorias [3] conservadas |
| Categoria B asociada a Producto | Bruno DELETE 409, sin eliminar categoria ni relacion |
| Producto con Item temporal | Bruno DELETE 409, sin eliminar producto, item o pedido |
| Producto ya sin relaciones temporales de prueba | Bruno DELETE 204 |
| Categoria A sin productos | Bruno DELETE 204 |
| Limpieza Categoria B tras borrar el producto | HTTP DELETE 204 |
| Consultas de temporales borrados | GET 404 |

Bruno ejecuto las diez operaciones principales y las dos pruebas 409 en VS Code.
Los errores 400 (unicidad, negativos, FK inexistente, creado) y 404 de PATCH/DELETE se
comprobaron por HTTP real desde Cmder; sus ejemplos tambien se guardan en la coleccion.
Database Client mostro Categoria A renombrada y Categoria B, Producto 3 modificado y el Item 2.
Al terminar se actualizaron las tablas para mostrar solo los registros originales.

Para PROTECT se crearon exclusivamente Cliente 4, Pedido 2 e Item 2 temporales.
Tras confirmar 409 se retiro solo ese Item y ese Pedido; DELETE del Cliente 4 devolvio 204.
No se retiro ningun registro original para habilitar un borrado. Las nuevas vistas no ofrecen
borrado de pedidos/items: la limpieza controlada fue una operacion ORM del verificador de pruebas.

La regresion real de Cliente cubrio POST 201, GET lista/detalle 200, PATCH 200 y DELETE 204
sobre Cliente 4. Ademas se verificaron GET /clientes/1 200, ID inexistente 404 y los cinco /api/ 200.
Las filas completas de todas las tablas de negocio coincidieron al inicio y al final, incluidas
las tablas M2M y productos_app_*. Solo avanzaron los contadores AUTO_INCREMENT por las pruebas.

## Repetir comprobaciones desde Cmder

Ejecutar .venv/Scripts/python.exe tools/pruebas_catalogo.py.
El ejecutor comprueba que test_clase_catalogo_20261102 no exista, crea esa base de pruebas
separada, aplica alli las migraciones originales, corre 36 pruebas y retira esa base al terminar.
Nunca sobrescribe una base de pruebas existente ni hace flush sobre u2_p1_bd.

21 pruebas nuevas usan ORM y serializers reales con TestCase y rollback por prueba.
Cubren 200/201/204/400/404/409, campos invalidos, unicidad, listas vacias, M2M, PATCH parcial,
creado inmutable, rechazo PROTECT, persistencia y regresion completa de Cliente. Una prueba
inyecta IntegrityError despues de INSERT y M2M para comprobar rollback de ambos.
Se ejecutan ademas las 15 pruebas anteriores READ/UPDATE/DELETE de Cliente: 36 correctas.
check correcto; makemigrations --check --dry-run sin cambios; migrate --check correcto.

Primer intento del ejecutor: KeyError MIRROR por reemplazar el diccionario TEST completo.
Se corrigio para cambiar solo TEST.NAME y conservar los valores predeterminados de Django.
El fallo fue previo a crear la base. No se detectaron errores funcionales en las 36 pruebas.

## Sesion visual y seguridad de los temporales

Bruno: carpetas CRUD Categoria y CRUD Producto. Abrir cada solicitud y seleccionar Local.
09/10 de Cliente y los POST de otras actividades siguen conservados; no ejecutar toda la coleccion.
Los IDs temporales nuevos se publican en 0. Los POST nuevos guardan sus IDs solo con respuesta 201.
La segunda categoria de prueba se crea con el verificador y su ID se copia a categoriaSegundaId.
Los guardas PATCH/DELETE requieren un ID temporal mayor que 1; revisar siempre su identidad.

El script tools/verificar_catalogo.py conserva .local/catalogo_sesion.json con las filas iniciales
y los IDs propios. Se uso por etapas: --preparar, --categoria, --categoria-modificada, --producto,
--producto-modificado, --validar, --proteger, --liberar y --final, intercaladas con los Send de Bruno.
No ejecutar etapas fuera de orden: algunas crean o retiran fixtures propios. El estado terminado
se conserva como evidencia privada y rechaza repetir la sesion. Para otra clase revisar el estado
y preparar conscientemente una nueva sesion; nunca sobrescribirlo para ocultar temporales pendientes.

SQL de lectura: sql/verificar_catalogo.sql. En Database Client seleccionar la conexion de clase.
Django queda activo en Cmder, fase 44_catalogo_servidor, puerto 8000. El perfil Cmder integrado
y los iniciadores ABRIR_CLASE.cmd e INICIAR_BACKEND.cmd se conservan.
Todos los comandos ejecutados y sus resultados estan en COMANDOS_CMDER.md.
