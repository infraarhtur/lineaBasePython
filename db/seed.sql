



-- produts ----


INSERT INTO public.products (id, "name", description, purchase_price, sale_price, stock, created_at,is_active, updated_at, created_by)
VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28', 'Hambuguesa doble carne', 'agua sin gas', 800, 1000, 100, CURRENT_TIMESTAMP,true, NULL, NULL);

INSERT INTO public.products (id, "name", description, purchase_price, sale_price, stock, created_at,is_active, updated_at, created_by)
VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, 'Botella de jack daniels', 'este es un producto nuevo', 20000.00, 50000.00, 5, CURRENT_TIMESTAMP,true, NULL, NUll);


-- clients --
INSERT INTO public.clients (id, "name", email, phone, address, "comment",  is_active, created_at, updated_at, created_by) 
VALUES('594045b6-3259-471d-aac2-c2a24163677c'::uuid, 'unknown', 'unknown@gmail.com', '0000000', 'unknown', 'unknown cliente generico', true, CURRENT_TIMESTAMP, NULL,NULL);



-- categories--

INSERT INTO public.categories (id, "name", description, is_active, created_at, updated_at, created_by)
VALUES('276dfbcf-8523-4d08-ba5b-edadf448b28f'::uuid, 'Comida', 'categoria de comida', true, CURRENT_TIMESTAMP, NULL,NULL);

INSERT INTO public.categories (id, "name", description, is_active, created_at, updated_at, created_by) 
VALUES('276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid, 'Alcohol', 'Bebidas con alcohol', true, CURRENT_TIMESTAMP, NULL,NULL);

INSERT INTO public.categories (id, "name", description, is_active, created_at, updated_at, created_by) 
VALUES('edbee6f4-5dd7-4ed3-a9f5-113316a6e80e'::uuid, 'Sin alcohol', 'Bebidas sin alcohol',  true, CURRENT_TIMESTAMP, NULL,NUll);

--product_categories--

INSERT INTO public.product_categories (product_id, category_id) VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b28f'::uuid);
INSERT INTO public.product_categories (product_id, category_id) VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid);


--providers--

INSERT INTO public.providers (id, "name", phone, email, address, is_active, created_at, updated_at, created_by)
VALUES('276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 'proveedor 0', '3208965733', 'parmalat@gmail.com', 'en la pm ',true, CURRENT_TIMESTAMP, NULL,NUll);
INSERT INTO public.providers (id, "name", phone, email, address, is_active, created_at, updated_at, created_by)
VALUES('0748801f-1386-45c2-9f01-51a639085da0'::uuid, 'proveedor 1', '3208965733', 'proveedor@example.com', 'este es el proveedor 1',true, CURRENT_TIMESTAMP, NULL,NUll);


-- public.product_providers --

INSERT INTO public.product_providers (product_id, provider_id, purchase_price, delivery_time)
VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 5000, 888);
INSERT INTO public.product_providers (product_id, provider_id, purchase_price, delivery_time)
VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, '0748801f-1386-45c2-9f01-51a639085da0'::uuid, 6000, 28);


-- public.sales --
INSERT INTO public.sales
(id, client_id, sale_date, total_amount, status, payment_method, "comment", is_active, created_at, updated_at, created_by)
VALUES('523beedd-98a5-41e6-a0b4-69f24f4ed31f'::uuid, '594045b6-3259-471d-aac2-c2a24163677c'::uuid, '2025-07-09 17:24:01.153', 1000.00, 'pending', 'cash', 'una hamburguseita', true, '2025-07-09 17:24:36.677', NULL, NULL);

-- public.sale_details--

INSERT INTO public.sale_details
(id, sale_id, product_id, quantity, discount, tax, subtotal, total, unit_cost, "comment")
VALUES('9bd6df62-413b-4ab9-9ed5-257a1343ed7e'::uuid, '523beedd-98a5-41e6-a0b4-69f24f4ed31f'::uuid, 'd4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, 1, 0.00, 0.00, 1000.00, 1000.00, NULL, NULL);

