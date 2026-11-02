-- Database Client: seleccionar u2_p1_bd y ejecutar consultas de lectura.
SELECT id, nombre FROM pedidos_app_categoria;
SELECT id, nombre, email FROM pedidos_app_cliente;
SELECT id, nombre, descripcion, precio, stock, activo, codigo FROM pedidos_app_producto;
SELECT id, fecha, pagado, cliente_id FROM pedidos_app_pedido;
SELECT id, cantidad, precio_unitario, pedido_id, producto_id FROM pedidos_app_item;
SELECT producto_id, categoria_id FROM pedidos_app_producto_categorias;
