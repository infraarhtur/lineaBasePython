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
	is_active bool DEFAULT true NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp NULL,
	created_by uuid NULL,
	CONSTRAINT categories_name_key UNIQUE (name),
	CONSTRAINT categories_pkey PRIMARY KEY (id)
);

-- Tabla: clients
CREATE TABLE public.clients (
	id uuid NOT NULL,
	"name" varchar(100) NOT NULL,
	email varchar NOT NULL,
	phone varchar NOT NULL,
	address text NULL,
	"comment" text NULL,
	is_active bool DEFAULT true NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp NULL,
	created_by uuid NULL,
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
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	is_active bool DEFAULT true NULL,
	updated_at timestamp NULL,
	created_by uuid NULL,
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
	is_active bool DEFAULT true NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp NULL,
	created_by uuid NULL,
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
CREATE TABLE sales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- Unique sale ID
    client_id UUID,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2), -- Total of the sale
	total_discount numeric(10, 2) DEFAULT 0.00 NULL,
    status TEXT DEFAULT 'pending', -- Status: pending, paid, canceled, etc.
    payment_method TEXT, -- e.g., 'tarjeta de crédito'
    comment TEXT, -- Additional notes	
	is_active bool DEFAULT true NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp NULL,
    created_by UUID, -- User who created the sale
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
);

ALTER TABLE public.sales OWNER TO postgres;
GRANT ALL ON TABLE public.sales TO postgres;

-- Tabla: sale_details
CREATE TABLE sale_details (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- Unique sale detail ID
    sale_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0), -- Or use NUMERIC if fractional quantities are needed
    discount DECIMAL(10,2) DEFAULT 0.00,
    tax DECIMAL(10,2) DEFAULT 0.00,
    subtotal DECIMAL(10,2) NOT NULL, -- Based on quantity * product.sale_price
    total DECIMAL(10,2), -- subtotal - discount + tax
    unit_cost DECIMAL(10,2), -- Cost of the product at sale time (optional, for profit analysis)
    comment TEXT,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
ALTER TABLE public.sale_details OWNER TO postgres;
GRANT ALL ON TABLE public.sale_details TO postgres;

--FUNCTIONs
-- Función para obtener el resumen de ventas por método de pago
CREATE OR REPLACE FUNCTION public.get_sales_summary_by_payment_method(
    start_date DATE,
    end_date DATE
)
RETURNS TABLE (
    payment_method_label TEXT,
    total_sales INTEGER,
    total_amount NUMERIC(10,2),
    total_discount NUMERIC(10,2)
)
LANGUAGE SQL
AS $$
    SELECT
        COALESCE(payment_method, 'Grand Total') AS payment_method_label,
        COUNT(*) AS total_sales,
        SUM(total_amount) AS total_amount,
        SUM(total_discount) AS total_discount
    FROM public.sales
    WHERE sale_date >= start_date
      AND sale_date < end_date
      AND is_active = TRUE
      AND status = 'paid'
    GROUP BY GROUPING SETS (
        (payment_method),
        ()
    )
    ORDER BY
        CASE WHEN payment_method IS NULL THEN 1 ELSE 0 END,
        payment_method_label;
$$;