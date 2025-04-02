-- Asegurarse de que la extensión uuid-ossp está disponible
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Asegurarse de que el esquema public existe
CREATE SCHEMA IF NOT EXISTS public;

-- Permitir acceso público (opcional)
GRANT ALL ON SCHEMA public TO public;

-- DROP TABLES SI EXISTEN (opcional para desarrollo)
DROP TABLE IF EXISTS public.sale_details;
DROP TABLE IF EXISTS public.sales;
DROP TABLE IF EXISTS public.product_providers;
DROP TABLE IF EXISTS public.product_categories;
DROP TABLE IF EXISTS public.providers;
DROP TABLE IF EXISTS public.products;
DROP TABLE IF EXISTS public.clients;
DROP TABLE IF EXISTS public.categories;

-- Tabla: categories
CREATE TABLE public.categories (
	id uuid NOT NULL,
	"name" text NOT NULL,
	description text NULL,
	CONSTRAINT categories_name_key UNIQUE (name),
	CONSTRAINT categories_pkey PRIMARY KEY (id)
);
ALTER TABLE public.categories OWNER TO postgres;
GRANT ALL ON TABLE public.categories TO postgres;

-- Tabla: clients
CREATE TABLE public.clients (
	id uuid NOT NULL,
	"name" varchar(100) NOT NULL,
	email varchar NOT NULL,
	phone varchar NOT NULL,
	address text NULL,
	"comment" text NULL,
	CONSTRAINT clients_email_key UNIQUE (email),
	CONSTRAINT clients_pkey PRIMARY KEY (id)
);
ALTER TABLE public.clients OWNER TO postgres;
GRANT ALL ON TABLE public.clients TO postgres;

-- Tabla: products
CREATE TABLE public.products (
	id uuid NOT NULL,
	"name" text NOT NULL,
	description text NULL,
	purchase_price numeric(10, 2) NOT NULL,
	sale_price numeric(10, 2) NOT NULL,
	stock int4 NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT products_pkey PRIMARY KEY (id)
);
ALTER TABLE public.products OWNER TO postgres;
GRANT ALL ON TABLE public.products TO postgres;

-- Tabla: providers
CREATE TABLE public.providers (
	id uuid NOT NULL,
	"name" text NOT NULL,
	phone text NULL,
	email text NULL,
	address text NULL,
	CONSTRAINT providers_pkey PRIMARY KEY (id)
);
ALTER TABLE public.providers OWNER TO postgres;
GRANT ALL ON TABLE public.providers TO postgres;

-- Tabla: product_categories
CREATE TABLE public.product_categories (
	product_id uuid NOT NULL,
	category_id uuid NOT NULL,
	CONSTRAINT product_categories_pkey PRIMARY KEY (product_id, category_id),
	CONSTRAINT product_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE,
	CONSTRAINT product_categories_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE
);
ALTER TABLE public.product_categories OWNER TO postgres;
GRANT ALL ON TABLE public.product_categories TO postgres;

-- Tabla: product_providers
CREATE TABLE public.product_providers (
	product_id uuid NOT NULL,
	provider_id uuid NOT NULL,
	purchase_price numeric(10, 2) NOT NULL,
	delivery_time int4 NOT NULL,
	CONSTRAINT product_providers_pkey PRIMARY KEY (product_id, provider_id),
	CONSTRAINT product_providers_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE,
	CONSTRAINT product_providers_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.providers(id) ON DELETE CASCADE
);
ALTER TABLE public.product_providers OWNER TO postgres;
GRANT ALL ON TABLE public.product_providers TO postgres;

-- Tabla: sales
CREATE TABLE public.sales (
	id uuid NOT NULL,
	client_id uuid NULL,
	sale_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT sales_pkey PRIMARY KEY (id),
	CONSTRAINT sales_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id) ON DELETE SET NULL
);
ALTER TABLE public.sales OWNER TO postgres;
GRANT ALL ON TABLE public.sales TO postgres;

-- Tabla: sale_details
CREATE TABLE public.sale_details (
	id uuid NOT NULL,
	sale_id uuid NULL,
	product_id uuid NULL,
	quantity int4 NOT NULL,
	unit_price numeric(10, 2) NOT NULL,
	subtotal numeric(10, 2) NOT NULL,
	CONSTRAINT sale_details_pkey PRIMARY KEY (id),
	CONSTRAINT sale_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE,
	CONSTRAINT sale_details_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES public.sales(id) ON DELETE CASCADE
);
ALTER TABLE public.sale_details OWNER TO postgres;
GRANT ALL ON TABLE public.sale_details TO postgres;
