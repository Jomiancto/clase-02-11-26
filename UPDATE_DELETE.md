# UPDATE y DELETE de Cliente — 02-11-2026

Servidor: http://127.0.0.1:8000. Coleccion Bruno: Backend Unidad 2 - CRUD.
Referencia del profesor: https://github.com/enriquepalaciosc/pbe-2026_u2_proyecto2
Se conservaron CREATE, READ, modelos, serializers, migraciones y todos los endpoints /api/.

## Contrato JSON

| Metodo | Ruta exacta, sin barra final | Resultado |
|---|---|---|
| PATCH | /cliente/modificar | 200 y cliente actualizado |
| DELETE | /cliente/eliminar | 204 sin cuerpo |

Ambos reciben Content-Type: application/json. El ID se envia en el cuerpo, como entero positivo
(no string, booleano ni decimal); no se toma de query parameters. Falta de ID o JSON no valido: 400.
PATCH admite solo id, nombre y email, requiere al menos un campo a modificar y usa partial=True.
El ID identifica una unica fila y no se puede modificar. Campos desconocidos: 400.
ID inexistente: 404. Correo invalido/duplicado, nombre vacio o demasiado largo: 400.
DELETE admite exclusivamente id. Si el cliente tiene pedidos devuelve 409 con el motivo;
conserva el cliente, sus pedidos y sus items. No hay borrado en cascada permitido por esta vista.
Los modelos originales siguen teniendo CASCADE; otras herramientas con acceso directo al ORM
no estan cubiertas por esta proteccion de la API.

Ejemplo PATCH (reemplazar 2 por el ID del temporal que se acaba de crear):

~~~json
{"id":2,"nombre":"Temporal PATCH actualizado"}
~~~

~~~json
{"id":2,"email":"crud-temp-patch-actualizado-021126@example.test"}
~~~

Ejemplo DELETE (reemplazar 3 por el ID real del temporal sin pedidos):

~~~json
{"id":3}
~~~

modificar_cliente y borrar_cliente son funciones con @api_view, registradas en u2_proyecto1/urls.py.
Usan una transaccion y bloqueo de la fila Cliente (select_for_update). PATCH valida con el
ClienteSerializer existente y guarda solo el objeto seleccionado; el correo unico se valida
y un conflicto concurrente de unicidad responde 400. DELETE comprueba Pedido antes de eliminar.
No se crearon migraciones ni se cambiaron operaciones existentes.

## Flujo visual en VS Code

Seleccionar Local en cada nueva pestana Bruno; mantener Database Client conectado a
127.0.0.1:3306, base u2_p1_bd, usuario local root (credenciales privadas).
Abrir pedidos_app_cliente, DATA y Refresh para ver los datos actuales.

1. Crear una vez cada temporal con 09 TEMP crear para PATCH y 10 TEMP crear para DELETE.
   Son POST reales a /api/clientes/. Sus scripts guardan el ID retornado solo con HTTP 201.
2. Comprobar en Database Client que son nuevos y no tienen pedidos. Nunca usar ID 1.
3. Enviar 11 PATCH nombre parcial y 12 PATCH correo parcial; comprobar 200 y actualizar la tabla.
4. Enviar 13 DELETE temporal; comprobar 204 y ausencia de la fila despues de Refresh.
5. Enviar 14 DELETE inexistente y, opcionalmente, 15 PATCH inexistente: 404.
6. Retirar el temporal de PATCH solo despues de verificar su identidad y que no tiene pedidos.

Los guardas de 11/12/13 rechazan variables con ID <= 1. Se dejan clientePatchId y
clienteDeleteId en 0 en Git para exigir crear temporales nuevos. Revisar los IDs antes de Send.
No ejecutar toda la coleccion indiscriminadamente: contiene POST con efectos reales.
Los ejemplos fijos tienen correo unico; repetir POST sobre una fila existente devuelve 400.

## Resultados realmente comprobados

- Antes de cambiar codigo: CREATE/READ y API anteriores correctos; respaldo privado realizado.
- Bruno en VS Code: POST 09 => 201, ID 2; POST 10 => 201, ID 3.
- Cliente 2 antes: Temporal PATCH CRUD, crud-temp-patch-021126@example.test.
- PATCH nombre en Bruno => 200: Temporal PATCH actualizado; correo anterior conservado.
- PATCH correo en Bruno => 200: crud-temp-patch-actualizado-021126@example.test; nombre conservado.
- ORM/SQL de MariaDB confirmaron ambos estados. Database Client mostro los temporales
  antes y la fila 2 actualizada despues; al borrar 3 mostro que solo quedaban 1 y 2.
- DELETE de 3 desde Bruno => 204; MariaDB sin fila 3 y GET /clientes/3 => 404.
- DELETE de 999999999 desde Bruno => 404. PATCH de ese ID por HTTP => 404.
- HTTP real: correo invalido/duplicado, nombre vacio, PATCH sin cambios, IDs booleano/string
  y DELETE sin ID => 400; la fila temporal permanecio igual ante errores.
- Se retiro despues el temporal 2 por DELETE => 204. Ambos temporales ya no existen.
- Hashes de todas las filas originales de negocio iguales al inicio y al final, incluyendo
  cliente 1, pedidos e items. El contador AUTO_INCREMENT avanzo por los dos INSERT autorizados.
- La proteccion 409 con pedidos se comprobo con prueba automatica que exige no llamar delete;
  no se envio DELETE al cliente original ni se crearon pedidos de prueba.

## Comprobaciones desde Cmder

~~~bat
.venv\Scripts\python.exe manage.py test pedidos_app.test_read pedidos_app.test_update_delete --verbosity 2
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.venv\Scripts\python.exe manage.py migrate --check
.venv\Scripts\python.exe tools\verificar_read.py 8000
~~~

15 pruebas SimpleTestCase correctas (5 READ, 10 UPDATE/DELETE); usan dobles del ORM/transacciones,
no crean base de pruebas ni escriben datos reales. Cubren partial=True, errores, metodos,
identificacion de una fila, eliminacion sin pedidos y bloqueo de eliminacion con pedidos.
Las pruebas de MariaDB y HTTP real anteriores complementan esos dobles.
verificar_read.py comprueba GET anteriores y CREATE invalido 400; valida CREATE 201 con
create simulado sin insertar. Los POST reales 201 se comprobaron aparte en Bruno.

Para una nueva sesion controlada, tools/verificar_update_delete.py ofrece etapas --preparar,
--registrar, --nombre, --correo, --validaciones, --eliminado y --limpiar; ejecutar cada etapa
solo en el punto correspondiente del flujo visual. Conserva su estado privado en .local.
--preparar rechaza otra sesion previa; no elimina automaticamente estados ni datos previos.
--limpiar solo borra el temporal PATCH verificado de esa sesion y exige la verificacion del
DELETE anterior. Cada etapa compara las filas originales. No cambiar manualmente ese estado.

Todos los comandos ejecutados, directorios y resultados estan en COMANDOS_CMDER.md.
Inicio: ABRIR_CLASE.cmd o INICIAR_BACKEND.cmd 8000 desde Cmder.
