-- Solo lectura; seleccionar la conexion u2_p1_bd en Database Client.
SELECT id, nombre FROM pedidos_app_categoria ORDER BY id;
SELECT id, nombre, descripcion, precio, stock, activo, creado, codigo
FROM pedidos_app_producto ORDER BY id;
SELECT pc.id, pc.producto_id, p.nombre AS producto, pc.categoria_id, c.nombre AS categoria
FROM pedidos_app_producto_categorias pc
JOIN pedidos_app_producto p ON p.id = pc.producto_id
JOIN pedidos_app_categoria c ON c.id = pc.categoria_id ORDER BY pc.id;
SELECT id, pedido_id, producto_id, cantidad, precio_unitario FROM pedidos_app_item ORDER BY id;
-- Al terminar la sesion controlada no deben existir estos temporales.
SELECT id FROM pedidos_app_producto WHERE codigo = 'TEMP-CAT-021126';
SELECT id FROM pedidos_app_categoria WHERE nombre LIKE 'TEMP Catalogo 021126%';
