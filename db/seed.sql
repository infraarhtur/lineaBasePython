
-- prooducts
INSERT INTO public.products
(id, "name", description, purchase_price, sale_price, stock, created_at, is_active, updated_at, created_by, company_id, updated_by)
VALUES('6c76e214-b90b-4f57-aba9-96cb3045d861'::uuid, 'ELiminar', 'Producto a eliminar', 3000.00, 5000.00, 10, '2025-07-09 18:59:48.452', false, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.products
(id, "name", description, purchase_price, sale_price, stock, created_at, is_active, updated_at, created_by, company_id, updated_by)
VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, 'Hambuguesa doble carne', 'agua sin gas', 800.00, 1000.00, 90, '2025-07-09 07:39:39.588', true, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.products
(id, "name", description, purchase_price, sale_price, stock, created_at, is_active, updated_at, created_by, company_id, updated_by)
VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, 'Botella de jack daniels', 'este es un producto nuevo', 20000.00, 50000.00, 4, '2025-07-09 07:39:39.631', true, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.products
(id, "name", description, purchase_price, sale_price, stock, created_at, is_active, updated_at, created_by, company_id, updated_by)
VALUES('a7fb3fa8-f147-440f-bcb7-1d35923ad7fb'::uuid, 'consola xdj  RR', 'pretsamo', 100000.00, 150000.00, 14, '2025-07-09 12:56:23.262', true, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);

-- clients

INSERT INTO public.clients
(id, "name", email, phone, address, "comment", is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('594045b6-3259-471d-aac2-c2a24163677c'::uuid, 'unknown', 'unknown@gmail.com', '0000000', 'unknown', 'unknown cliente generico', true, '2025-07-09 07:39:39.646', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.clients
(id, "name", email, phone, address, "comment", is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('1a26c8e3-c7b6-45e6-a2a7-6715e97998a7'::uuid, 'la casa de arthur', 'infraarhtur@gmail.com', '3208965744', 'cll132 bis 92 33 
Piso 1 puerta grandedddd', 'es un concepto no ', true, '2025-07-09 10:52:01.636', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.clients
(id, "name", email, phone, address, "comment", is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('5d2c3708-cd3c-4bb0-8c15-d752ee2467ce'::uuid, 'Kvmikvzy', 'Kvmikvzy@gamail.rec', '567389890', 'Kvmikvzy@gamail.rec', 'este es para borrar', false, '2025-07-09 17:22:35.182', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);

-- categories

INSERT INTO public.categories
(id, "name", description, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('276dfbcf-8523-4d08-ba5b-edadf448b28f'::uuid, 'Comida', 'categoria de comida', true, '2025-07-09 07:39:39.652', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.categories
(id, "name", description, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid, 'Alcohol', 'Bebidas con alcohol', true, '2025-07-09 07:39:39.663', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.categories
(id, "name", description, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('edbee6f4-5dd7-4ed3-a9f5-113316a6e80e'::uuid, 'Sin alcohol', 'Bebidas sin alcohol', true, '2025-07-09 07:39:39.666', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.categories
(id, "name", description, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('d4dc9343-f0b9-4cd2-9637-f2ab102e471f'::uuid, 'tecnologia IA', 'categoria de tecnologia', false, '2025-07-09 20:27:53.984', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.categories
(id, "name", description, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('30c38000-63d5-48e7-a252-643fd2e1db04'::uuid, 'otra categoriaedit', 'otra categoria editada', false, '2025-07-13 12:36:50.674', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);

--product_categories--

INSERT INTO public.product_categories
(product_id, category_id, company_id, created_by, updated_by, updated_at, created_at)
VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b28f'::uuid, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:06.246', '2025-08-12 13:29:14.553');
INSERT INTO public.product_categories
(product_id, category_id, company_id, created_by, updated_by, updated_at, created_at)
VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:06.246', '2025-08-12 13:29:14.553');
INSERT INTO public.product_categories
(product_id, category_id, company_id, created_by, updated_by, updated_at, created_at)
VALUES('a7fb3fa8-f147-440f-bcb7-1d35923ad7fb'::uuid, 'edbee6f4-5dd7-4ed3-a9f5-113316a6e80e'::uuid, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:06.246', '2025-08-12 13:29:14.553');
INSERT INTO public.product_categories
(product_id, category_id, company_id, created_by, updated_by, updated_at, created_at)
VALUES('6c76e214-b90b-4f57-aba9-96cb3045d861'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b70f'::uuid, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:06.246', '2025-08-12 13:29:14.553');


-- providers --
INSERT INTO public.providers
(id, "name", phone, email, address, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 'proveedor 0', '3208965733', 'parmalat@gmail.com', 'en la pm ', true, '2025-07-09 07:39:39.688', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);
INSERT INTO public.providers
(id, "name", phone, email, address, is_active, created_at, updated_at, created_by, company_id, updated_by)
VALUES('0748801f-1386-45c2-9f01-51a639085da0'::uuid, 'proveedor 1', '3208965733', 'proveedor@example.com', 'este es el proveedor 1', true, '2025-07-09 07:39:39.691', NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL);


-- public.product_providers --

INSERT INTO public.product_providers
(product_id, provider_id, purchase_price, delivery_time, company_id, created_by, updated_by, updated_at, created_at)
VALUES('d4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 5000.00, 888, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:13.590', '2025-08-12 13:29:14.553');
INSERT INTO public.product_providers
(product_id, provider_id, purchase_price, delivery_time, company_id, created_by, updated_by, updated_at, created_at)
VALUES('b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, '0748801f-1386-45c2-9f01-51a639085da0'::uuid, 6000.00, 28, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:13.590', '2025-08-12 13:29:14.553');
INSERT INTO public.product_providers
(product_id, provider_id, purchase_price, delivery_time, company_id, created_by, updated_by, updated_at, created_at)
VALUES('a7fb3fa8-f147-440f-bcb7-1d35923ad7fb'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 0.00, 0, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:13.590', '2025-08-12 13:29:14.553');
INSERT INTO public.product_providers
(product_id, provider_id, purchase_price, delivery_time, company_id, created_by, updated_by, updated_at, created_at)
VALUES('6c76e214-b90b-4f57-aba9-96cb3045d861'::uuid, '276dfbcf-8523-4d08-ba5b-edadf448b80f'::uuid, 0.00, 0, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:13.590', '2025-08-12 13:29:14.553');



-- public.sales --

INSERT INTO public.sales
(id, client_id, sale_date, total_amount, status, payment_method, "comment", created_by, is_active, created_at, updated_at, total_discount, company_id, updated_by)
VALUES('523beedd-98a5-41e6-a0b4-69f24f4ed31f'::uuid, '594045b6-3259-471d-aac2-c2a24163677c'::uuid, '2025-07-09 12:24:01.153', 1000.00, 'pending', 'cash', 'una hamburguseita', NULL, true, '2025-07-09 12:24:36.677', NULL, 0.00, '00000000-0000-0000-0000-000000000001'::uuid, NULL);


-- public.sale_details --
INSERT INTO public.sale_details
(id, sale_id, product_id, quantity, subtotal, discount, tax, total, unit_cost, "comment", company_id, created_by, updated_by, updated_at, created_at)
VALUES('9bd6df62-413b-4ab9-9ed5-257a1343ed7e'::uuid, '523beedd-98a5-41e6-a0b4-69f24f4ed31f'::uuid, 'd4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, 1, 1000.00, 0.00, 0.00, 1000.00, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:10.349', '2025-08-12 13:36:10.495');
INSERT INTO public.sale_details
(id, sale_id, product_id, quantity, subtotal, discount, tax, total, unit_cost, "comment", company_id, created_by, updated_by, updated_at, created_at)
VALUES('a335e0df-5fda-43ba-8c74-323fd5764d32'::uuid, '02a4511e-0e10-4cbd-a4c7-59b5b288c4da'::uuid, 'd4ffc7a1-1ac0-4ce7-8d05-ed7c01602f28'::uuid, 10, 10000.00, 10.00, 0.00, 9000.00, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:10.349', '2025-08-12 13:36:10.495');
INSERT INTO public.sale_details
(id, sale_id, product_id, quantity, subtotal, discount, tax, total, unit_cost, "comment", company_id, created_by, updated_by, updated_at, created_at)
VALUES('063a8c33-890a-4697-8bbe-e2a402d0bc08'::uuid, '02a4511e-0e10-4cbd-a4c7-59b5b288c4da'::uuid, 'b86ce202-b654-4bd9-9045-0a274642f5fb'::uuid, 1, 50000.00, 10.00, 0.00, 45000.00, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:10.349', '2025-08-12 13:36:10.495');
INSERT INTO public.sale_details
(id, sale_id, product_id, quantity, subtotal, discount, tax, total, unit_cost, "comment", company_id, created_by, updated_by, updated_at, created_at)
VALUES('bc3b1d89-7693-41e2-9b32-bd922774d489'::uuid, '02a4511e-0e10-4cbd-a4c7-59b5b288c4da'::uuid, 'a7fb3fa8-f147-440f-bcb7-1d35923ad7fb'::uuid, 1, 150000.00, 20.00, 0.00, 120000.00, NULL, NULL, '00000000-0000-0000-0000-000000000001'::uuid, NULL, NULL, '2025-08-12 11:44:10.349', '2025-08-12 13:36:10.495');
