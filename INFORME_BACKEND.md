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
