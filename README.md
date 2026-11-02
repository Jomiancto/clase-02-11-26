# Backend — clase del 2 de noviembre de 2026

Repositorio oficial: https://github.com/Jomiancto/clase-02-11-26
Copia independiente de Unidad2 (main af1614d) mas el trabajo local conservado.
Profesor: revision 01966d65548bc41cb09249d956c67f2306c85b68, solo lectura.
No se modifica E:/cmder/Unidad2 ni se trabaja en Evaluacion II.

## Estado y alcance

Django 6.1.2, DRF 3.18.3, Python 3.12.3, mysqlclient 2.2.8.
Servidor local: http://127.0.0.1:8000/ y /api/.
MariaDB 12.3.2, 127.0.0.1:3306, base u2_p1_bd, usuario local root.
Credenciales y SECRET_KEY se leen de .env privado; consultar .env.example.
La base se comparte con el trabajo anterior: sus tablas productos_app_* se conservan.
Las tres migraciones de pedidos_app estan aplicadas; no se regeneraron ni alteraron modelos.
No hubo migraciones pendientes. Respaldo previo a pruebas en .local/respaldos, excluido de Git.

API de desarrollo local; sin autenticacion. Ejecutar solo en loopback.
Las colecciones /api/ conservan GET y POST; PUT, PATCH y DELETE responden 405 alli.
Cliente agrega PATCH /cliente/modificar y DELETE /cliente/eliminar fuera de /api/.
Bajo /api/ no hay rutas de detalle. GET /api/clientes/ conserva su paginacion (results, count, next, previous).
Las rutas READ de clases se describen abajo y devuelven una lista completa o un objeto.

## CREATE y orden de dependencias

| Orden | POST | JSON de ejemplo |
|---|---|---|
| 1 | /api/categorias/ | {"nombre":"Clase 02-11-2026"} |
| 2 | /api/clientes/ | {"nombre":"Cliente de clase","email":"clase-02-11-2026@example.test"} |
| 3 | /api/productos/ | {"nombre":"Cuaderno Backend","descripcion":"Prueba CREATE clase 02-11-2026","precio":2500,"stock":10,"activo":true,"codigo":"CLASE-021126","categorias":[1]} |
| 4 | /api/pedidos/ | {"fecha":"2026-11-02","pagado":false,"cliente":1} |
| 5 | /api/items/ | {"cantidad":2,"precio_unitario":2500,"pedido":1,"producto":1} |

Usar IDs realmente devueltos. Bruno actualiza las variables de IDs al recibir 201.
Los ejemplos categoria y cliente ya existen tras las pruebas; repetirlos devuelve 400 por unicidad.
Producto, Pedido e Item no tienen clave unica de negocio: repetir POST crea otro registro.
No ejecutar la coleccion completa sin revisar los datos. GET es reutilizable sin insertar.
El script tools/probar_create.py reconoce y reutiliza su conjunto de prueba, sin borrarlo.

Validaciones DRF: obligatorios, longitudes, correo valido, unicidad, FK/M2M existentes,
fechas, booleanos y enteros no negativos. Cero sigue admitido conforme a los modelos originales.
Producto y su M2M se guardan en una transaccion. id y creado son de solo lectura.

Relaciones originales: Pedido->Cliente CASCADE, Item->Pedido CASCADE,
Item->Producto PROTECT, Producto<->Categoria M2M. No se cambiaron related_name.
CASCADE/PROTECT describen el ORM, no acciones fisicas CASCADE de MariaDB.

## Reiniciar la clase desde Cmder

Abrir E:/cmder/Cmder.exe y ejecutar cd /d E:\cmder\clase-02-11-26.
Ejecutar ABRIR_CLASE.cmd para abrir el editor de clase y una consola Cmder de servidor.
Si ya hay servidor, la comprobacion de puerto evita iniciar otro; no detiene el existente.
Solo servidor: INICIAR_BACKEND.cmd 8000. Si esta ocupado, revisar propietario antes de elegir 8001.
Si se cambia el puerto, actualizar baseUrl en bruno/environments/Local.bru.
El iniciador no instala paquetes ni aplica migraciones. Ctrl+C detiene Django en su consola.
MariaDB se inicia solo si no escucha y se verifica la instancia portable existente, sin inicializar datos.

El editor de clase esta en E:/cmder/opt/vscode-backend (ZIP oficial Microsoft, 1.144.0).
Usa .local/editor-data y .local/editor-extensions; no reemplaza el VS Code 1.88.1 instalado.
Bruno 6 falla en el editor antiguo con crypto.subtle; por eso ABRIR_CLASE usa el editor actual.
La terminal integrada tiene perfil Cmder mediante vendor/bin/vscode_init.cmd.
El servidor se conserva en Cmder/ConEmu externo, con CMDER_ROOT y ConEmuPID comprobados.
Las tareas Clase: servidor/comprobar/entorno/bruno/database abren Cmder explicitamente.

## VS Code: Bruno y base de datos

Extension oficial bruno-api-client.bruno 6.0.0. Coleccion: bruno/, Backend Unidad 2 - CRUD.
Abrir una peticion .bru con Bruno Request Editor y seleccionar entorno Local.
Metodo, URL, body JSON, Send y respuesta quedan en el editor. Las peticiones CREATE/READ se conservan y se agregaron temporales, PATCH y DELETE.
No se necesita la aplicacion Bruno independiente. Bruno CLI no estaba instalado (bru no encontrado).
Si se instala mas adelante, ejecutar primero solo peticiones GET desde Cmder; no repetir todos los POST.

Database Client: cweijan.vscode-database-client2. Se aisla de otras dos extensiones DB duplicadas.
Conexion local MySQL/MariaDB: host 127.0.0.1, puerto 3306, usuario root, base u2_p1_bd.
No guardar credenciales en archivos versionados. La configuracion del editor queda en .local.
Consultas de lectura: sql/verificar_create.sql. Seleccionar conexion y ejecutar cada SELECT.
En Database expandir Tables, una tabla y sus columnas; abrirla para ver registros.

## Verificacion y registro

Desde Cmder: activar .venv con call .venv\Scripts\activate.bat.
Comprobar con python manage.py check, python manage.py migrate --check y
python manage.py makemigrations --check --dry-run.
Prueba HTTP real y persistencia: python tools\probar_create.py (servidor activo en 8000).
Inspeccion de PK, FK, unicidad y tablas: python tools\inspeccionar_bd.py --despues.
COMANDOS_CMDER.md registra comandos reales, directorios, resultados, errores y soluciones.
INFORME_BACKEND.md distingue comprobaciones automaticas de pruebas visuales.

.env, .venv, .local, respaldos, datos, logs y credenciales estan excluidos.
Se versionan codigo, migraciones, requirements, Bruno, SQL de lectura, tareas e iniciadores.
Origin debe apuntar unicamente al repositorio oficial; nunca al profesor.

Estado visual comprobado: Bruno envio Cuaderno Backend (ID 2) con HTTP 201; Database Client mostro la fila y las columnas; navegador integrado /api/ HTTP 200. La conexion queda guardada en el perfil privado de clase.

Distribucion del editor: [ZIP oficial de Microsoft](https://code.visualstudio.com/docs/setup/windows).


## READ con decoradores — avance de clase

Las vistas existentes bajo /api/ y todos los serializers se conservan.

| Metodo | Ruta exacta (sin barra final) | Respuesta |
|---|---|---|
| GET | /clientes | 200 y lista de clientes; [] cuando no hay resultados |
| GET | /clientes/<id> | 200 y un cliente; 404 si no existe |

pedidos_app/views.py implementa listar_clientes con @api_view(['GET']),
Cliente.objects.all(), ClienteSerializer(clientes, many=True) y Response HTTP 200.
listar_cliente(request, id) usa Cliente.objects.get(pk=id), serializa un solo objeto
y captura Cliente.DoesNotExist para devolver 404 con detail: Cliente no encontrado.
Las rutas se registran en u2_proyecto1/urls.py, fuera del prefijo /api/.
Solo se aceptan IDs enteros no negativos en la URL; una URL no coincidente devuelve 404.

Bruno incluye 06 READ listar clientes, 07 READ cliente por ID y 08 READ cliente inexistente.
Seleccionar entorno Local en cada nueva pestana; clienteId=1 consulta el cliente existente.
El ID 999999999 se comprobo inexistente en esta base antes de la prueba 404.
Estas tres peticiones son GET y se pueden repetir sin crear registros.

Pruebas desde Cmder:

- .venv/Scripts/python.exe manage.py test pedidos_app.test_read --verbosity 2
- .venv/Scripts/python.exe tools/verificar_read.py 8000

Las cinco pruebas de SimpleTestCase no crean base de pruebas ni escriben en MariaDB.
Cubren listado, lista vacia, detalle existente, 404 y rechazo de POST en las nuevas rutas.
verificar_read.py compara HTTP real con ORM, comprueba los endpoints anteriores y
POST invalido 400. Para comprobar CREATE valido 201 sin insertar filas, ejecuta DRF
con validacion real y simula unicamente Cliente.objects.create, comprobando sus argumentos.
No debe confundirse esa comprobacion de regresion con un nuevo INSERT HTTP real.
El script compara hashes de todas las filas de negocio antes y despues.

Verificado el 02-11-2026: Bruno 200 para /clientes y /clientes/1; 404 para
/clientes/999999999. El cliente existente es ID 1, Cliente de clase,
clase-02-11-2026@example.test. Los datos de negocio permanecieron intactos.
En ese avance READ no se agregaron migraciones ni operaciones PATCH, PUT o DELETE.

## UPDATE y DELETE de Cliente

Implementados con funciones @api_view, ORM y ClienteSerializer. Ver [contrato, pruebas y flujo seguro de Bruno](UPDATE_DELETE.md).
PATCH /cliente/modificar recibe id entero y nombre/email; DELETE /cliente/eliminar recibe solo id.
Clientes con pedidos no se eliminan: HTTP 409. No se alteraron modelos, serializers ni migraciones.
