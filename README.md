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

API de desarrollo local con GET y POST; sin autenticacion. Ejecutar solo en loopback.
PUT, PATCH y DELETE no estan implementados (405 en las rutas de coleccion).
No hay rutas de detalle aun. GET lista resultados paginados (results, count, next, previous).

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
Metodo, URL, body JSON, Send y respuesta quedan en el editor. Hay cinco POST y cinco GET.
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
