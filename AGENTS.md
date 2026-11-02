# Backend clase 02-11-2026

- Raiz E:/cmder/clase-02-11-26. Origin exclusivo https://github.com/Jomiancto/clase-02-11-26.git, main.
- Unidad2 y profesor: solo lectura. No modificar ni publicar alli.
- Ejecutar comandos mediante Cmder.exe y tareas .task; registrar comandos reales.
- Conservar modelos, relaciones y las tres migraciones originales.
- .env, .venv, .local y respaldos privados y excluidos de Git.
- u2_p1_bd compartida: preservar tablas y datos, incluidos productos_app_*.
- Revisar plan y respaldo antes de migrar. No migrar automaticamente al iniciar.
- Alcance CRUD Cliente: CREATE existente, READ con @api_view en /clientes y /clientes/<int:id>, PATCH /cliente/modificar y DELETE /cliente/eliminar. No PUT nuevo ni Evaluacion II.
- DELETE rechaza clientes con pedidos (409); las pruebas solo usan clientes temporales sin pedidos, nunca ID 1.
- No repetir POST indiscriminadamente. tools/probar_create.py reutiliza sus datos.
- No detener procesos ajenos ni usar force push.

- Alcance ampliado: CRUD Categoria y Producto con funciones @api_view, conservando /api/.
- Categoria con productos y Producto con items: DELETE 409. Probar solo temporales propios.
- Pruebas de persistencia: tools/pruebas_catalogo.py crea una base MariaDB exclusiva si no existe; nunca sobrescribir una base de pruebas existente.
