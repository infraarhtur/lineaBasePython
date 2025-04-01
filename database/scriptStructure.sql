
-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION arhtur;

COMMENT ON SCHEMA public IS 'standard public schema';
-- public.categories definition

-- Drop table

-- DROP TABLE public.categories;

CREATE TABLE public.categories (
	id uuid NOT NULL,
	"name" text NOT NULL,
	description text NULL,
	CONSTRAINT categories_name_key UNIQUE (name),
	CONSTRAINT categories_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.categories OWNER TO postgres;
GRANT ALL ON TABLE public.categories TO postgres;


-- public.clients definition

-- Drop table

-- DROP TABLE public.clients;

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

-- Permissions

ALTER TABLE public.clients OWNER TO postgres;
GRANT ALL ON TABLE public.clients TO postgres;


-- public.products definition

-- Drop table

-- DROP TABLE public.products;

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

-- Permissions

ALTER TABLE public.products OWNER TO postgres;
GRANT ALL ON TABLE public.products TO postgres;


-- public.providers definition

-- Drop table

-- DROP TABLE public.providers;

CREATE TABLE public.providers (
	id uuid NOT NULL,
	"name" text NOT NULL,
	phone text NULL,
	email text NULL,
	address text NULL,
	CONSTRAINT providers_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.providers OWNER TO postgres;
GRANT ALL ON TABLE public.providers TO postgres;


-- public.product_categories definition

-- Drop table

-- DROP TABLE public.product_categories;

CREATE TABLE public.product_categories (
	product_id uuid NOT NULL,
	category_id uuid NOT NULL,
	CONSTRAINT product_categories_pkey PRIMARY KEY (product_id, category_id),
	CONSTRAINT product_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE,
	CONSTRAINT product_categories_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE public.product_categories OWNER TO postgres;
GRANT ALL ON TABLE public.product_categories TO postgres;


-- public.product_providers definition

-- Drop table

-- DROP TABLE public.product_providers;

CREATE TABLE public.product_providers (
	product_id uuid NOT NULL,
	provider_id uuid NOT NULL,
	purchase_price numeric(10, 2) NOT NULL,
	delivery_time int4 NOT NULL,
	CONSTRAINT product_providers_pkey PRIMARY KEY (product_id, provider_id),
	CONSTRAINT product_providers_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE,
	CONSTRAINT product_providers_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.providers(id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE public.product_providers OWNER TO postgres;
GRANT ALL ON TABLE public.product_providers TO postgres;


-- public.sales definition

-- Drop table

-- DROP TABLE public.sales;

CREATE TABLE public.sales (
	id uuid NOT NULL,
	client_id uuid NULL,
	sale_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT sales_pkey PRIMARY KEY (id),
	CONSTRAINT sales_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id) ON DELETE SET NULL
);

-- Permissions

ALTER TABLE public.sales OWNER TO postgres;
GRANT ALL ON TABLE public.sales TO postgres;


-- public.sale_details definition

-- Drop table

-- DROP TABLE public.sale_details;

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

-- Permissions

ALTER TABLE public.sale_details OWNER TO postgres;
GRANT ALL ON TABLE public.sale_details TO postgres;




-- Permissions

--GRANT ALL ON SCHEMA public TO arhtur;
GRANT ALL ON SCHEMA public TO public;