-- produts ----

INSERT INTO public.products (id, "name", description, purchase_price, sale_price, stock, created_at)
VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28', 'agua sin gas', 'agua sin gas', 0, 1000, 100, CURRENT_TIMESTAMP);

INSERT INTO public.products (id, "name", description, purchase_price, sale_price, stock, created_at)
VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, 'tercer producto', 'este es un producto nuevo', 20000.00, 50000.00, 5, CURRENT_TIMESTAMP);

INSERT INTO public.products (id, "name", description, purchase_price, sale_price, stock, created_at)
VALUES('0748801f-1386-45c2-9f01-51a639095da0',	'este es el segundo producto',	'este es un producto nuevo',	15000.00,	20000.00,	5,	CURRENT_TIMESTAMP);

-- clients --

INSERT INTO public.clients (id, "name", email, phone, address, "comment") VALUES('edbee6f4-5dd7-4ed3-a9f5-113316a6e26e'::uuid, 'prueba2 xxx', 'prueba1@example.com', '+1234567890', 'avenida siempre viva 123', 'este es un usuario de prueba 2');
INSERT INTO public.clients (id, "name", email, phone, address, "comment") VALUES('276dfbcf-8523-4d08-ba5b-edadf448b65f'::uuid, 'cliente 1', 'prueba@example.com', '+1234567890', 'avenida siempre viva 123', 'este es un usuario de prueba 2');

-- categories--

INSERT INTO public.categories (id, "name", description) VALUES('276dfbcf-8523-4d08-ba5b-edadf448b28f'::uuid, 'Comida', 'categoria de comida');
INSERT INTO public.categories (id, "name", description) VALUES('276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid, 'Alcohol', 'Bebidas con alcohol');
INSERT INTO public.categories (id, "name", description) VALUES('edbee6f4-5dd7-4ed3-a9f5-113316a6e80e'::uuid, 'Sin alcohol', 'Bebidas sin alcohol');

--product_categories--

INSERT INTO public.product_categories (product_id, category_id) VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b28f'::uuid);
INSERT INTO public.product_categories (product_id, category_id) VALUES('0748801f-1386-45c2-9f01-51a639095da0'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid);

--providers--

INSERT INTO public.providers (id, "name", phone, email, address) VALUES('276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 'proveedor 0', '3208965733', 'parmalat@gmail.com', 'en la pm ');
INSERT INTO public.providers (id, "name", phone, email, address) VALUES('0748801f-1386-45c2-9f01-51a639085da0'::uuid, 'proveedor 1', '3208965733', 'proveedor@example.com', 'este es el proveedor 1');


-- public.product_providers --

INSERT INTO public.product_providers (product_id, provider_id, purchase_price, delivery_time) VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 5000, 888);
INSERT INTO public.product_providers (product_id, provider_id, purchase_price, delivery_time) VALUES('0748801f-1386-45c2-9f01-51a639095da0'::uuid, '0748801f-1386-45c2-9f01-51a639085da0'::uuid, 6000, 28);

-- public.sales --

INSERT INTO public.sales
(id, client_id, sale_date, total_amount, status, payment_method, "comment", created_by)
VALUES (
    uuid_generate_v4(), -- id
    '276dfbcf-8523-4d08-ba5b-edadf448b65f', -- client_id
    CURRENT_TIMESTAMP, -- sale_date
    30000, -- total_amount
    'paid', -- status
    'tarjeta de crédito', -- payment_method
    'es una factura dummy', -- comment
    uuid_generate_v4() -- created_by (reemplaza si tienes un usuario específico)
);

-- public.sale_details--

INSERT INTO public.sale_details
(id, sale_id, product_id, quantity, subtotal, discount, tax, total, unit_cost, "comment")
VALUES(
    uuid_generate_v4(), -- 🔹 id: genera automáticamente un UUID para el detalle de la venta

    'c3135910-3b90-4894-9c96-8c39516694fa', -- sale_id: ID de la venta a la que pertenece este detalle

    'b86ce202-b654-4bd9-9045-0a274642f5fb', --  product_id: ID del producto que se vendió

    2, -- quantity: se vendieron 2 unidades del producto

    100000, -- subtotal: precio total antes de descuento/impuestos (ej. 2 * 50000)

    5000, --  discount: descuento aplicado al subtotal (ej. promoción, rebaja)

    0, --  tax: impuesto aplicado (en este caso, 0)

    95000, --  total: subtotal - discount + tax (100000 - 5000 + 0)

    50000, -- unit_cost: costo unitario del producto en el momento de la venta (útil para calcular utilidad)

    'esta es un caso de prueba' -- 🔹 comment: observaciones adicionales para este ítem
);

