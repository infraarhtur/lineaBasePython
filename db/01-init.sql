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

-- DROP SCHEMA public;

-- CREATE SCHEMA public AUTHORIZATION arhtur; -- Comentado porque el usuario no existe

COMMENT ON SCHEMA public IS 'standard public schema';
-- --------------------------------------------------------------------------------
-- Crear funciones de triggers antes de cualquier creación de trigger
-- para evitar errores de dependencia durante la inicialización.
-- --------------------------------------------------------------------------------

-- DROP FUNCTION public.set_created_at();

CREATE OR REPLACE FUNCTION public.set_created_at()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF NEW.created_at IS NULL THEN
    NEW.created_at := now();
  END IF;
  RETURN NEW;
END;
$function$
;

-- DROP FUNCTION public.set_updated_at();

CREATE OR REPLACE FUNCTION public.set_updated_at()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$function$
;
-- public.categories definition

-- Drop table

-- DROP TABLE public.categories;

CREATE TABLE public.categories (
	id uuid NOT NULL,
	"name" text NOT NULL,
	description text NULL,
	is_active bool DEFAULT true NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamptz NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NOT NULL,
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	CONSTRAINT categories_name_key UNIQUE (name),
	CONSTRAINT categories_pkey PRIMARY KEY (id)
);

-- Column comments

COMMENT ON COLUMN public.categories.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.categories.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.categories for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.categories for each row execute function set_created_at();


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
	is_active bool DEFAULT true NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamptz NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NOT NULL,
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	CONSTRAINT clients_email_key UNIQUE (email),
	CONSTRAINT clients_pkey PRIMARY KEY (id)
);

-- Column comments

COMMENT ON COLUMN public.clients.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.clients.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.clients for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.clients for each row execute function set_created_at();


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
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	is_active bool DEFAULT true NULL,
	updated_at timestamptz NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NOT NULL,
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	CONSTRAINT products_pkey PRIMARY KEY (id)
);

-- Column comments

COMMENT ON COLUMN public.products.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.products.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.products for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.products for each row execute function set_created_at();


-- public.providers definition

-- Drop table

-- DROP TABLE public.providers;

CREATE TABLE public.providers (
	id uuid NOT NULL,
	"name" text NOT NULL,
	phone text NULL,
	email text NULL,
	address text NULL,
	is_active bool DEFAULT true NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamptz NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NOT NULL,
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	CONSTRAINT providers_pkey PRIMARY KEY (id)
);

-- Column comments

COMMENT ON COLUMN public.providers.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.providers.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.providers for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.providers for each row execute function set_created_at();


-- public.product_categories definition

-- Drop table

-- DROP TABLE public.product_categories;

CREATE TABLE public.product_categories (
	product_id uuid NOT NULL,
	category_id uuid NOT NULL,
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	updated_at timestamptz DEFAULT now() NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT product_categories_pkey PRIMARY KEY (product_id, category_id),
	CONSTRAINT product_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE,
	CONSTRAINT product_categories_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE
);

-- Column comments

COMMENT ON COLUMN public.product_categories.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.product_categories.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.product_categories for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.product_categories for each row execute function set_created_at();


-- public.product_providers definition

-- Drop table

-- DROP TABLE public.product_providers;

CREATE TABLE public.product_providers (
	product_id uuid NOT NULL,
	provider_id uuid NOT NULL,
	purchase_price numeric(10, 2) NOT NULL,
	delivery_time int4 NOT NULL,
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	updated_at timestamptz DEFAULT now() NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT product_providers_pkey PRIMARY KEY (product_id, provider_id),
	CONSTRAINT product_providers_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE,
	CONSTRAINT product_providers_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.providers(id) ON DELETE CASCADE
);

-- Column comments

COMMENT ON COLUMN public.product_providers.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.product_providers.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.product_providers for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.product_providers for each row execute function set_created_at();


-- public.sales definition

-- Drop table

-- DROP TABLE public.sales;

CREATE TABLE public.sales (
	id uuid NOT NULL,
	client_id uuid NULL,
	sale_date timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	total_amount numeric(10, 2) NULL,
	status text DEFAULT 'pending'::text NULL,
	payment_method text NULL,
	"comment" text NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	is_active bool DEFAULT true NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamptz NULL,
	total_discount numeric(10, 2) DEFAULT 0.00 NULL,
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NOT NULL,
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	CONSTRAINT sales_pkey PRIMARY KEY (id),
	CONSTRAINT sales_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id) ON DELETE SET NULL
);

-- Column comments

COMMENT ON COLUMN public.sales.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.sales.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.sales for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.sales for each row execute function set_created_at();


-- public.sale_details definition

-- Drop table

-- DROP TABLE public.sale_details;

CREATE TABLE public.sale_details (
	id uuid NOT NULL,
	sale_id uuid NULL,
	product_id uuid NULL,
	quantity int4 NOT NULL,
	subtotal numeric(10, 2) NOT NULL,
	discount numeric(10, 2) DEFAULT 0.00 NULL,
	tax numeric(10, 2) DEFAULT 0.00 NULL,
	total numeric(10, 2) NULL,
	unit_cost numeric(10, 2) NULL,
	"comment" text NULL,
	company_id uuid DEFAULT '00000000-0000-0000-0000-000000000001'::uuid NULL,
	created_by uuid NULL, -- Usuario que creó el registro (uuid, nullable, sin FK)
	updated_by uuid NULL, -- Último usuario que modificó el registro (uuid, nullable, sin FK)
	updated_at timestamptz DEFAULT now() NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT sale_details_pkey PRIMARY KEY (id),
	CONSTRAINT sale_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE,
	CONSTRAINT sale_details_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES public.sales(id) ON DELETE CASCADE
);

-- Column comments

COMMENT ON COLUMN public.sale_details.created_by IS 'Usuario que creó el registro (uuid, nullable, sin FK)';
COMMENT ON COLUMN public.sale_details.updated_by IS 'Último usuario que modificó el registro (uuid, nullable, sin FK)';

-- Table Triggers

create trigger trg_set_updated_at before
update
    on
    public.sale_details for each row execute function set_updated_at();
create trigger trg_set_created_at before
insert
    on
    public.sale_details for each row execute function set_created_at();



-- DROP FUNCTION public.armor(bytea);

CREATE OR REPLACE FUNCTION public.armor(bytea)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_armor$function$
;

-- DROP FUNCTION public.armor(bytea, _text, _text);

CREATE OR REPLACE FUNCTION public.armor(bytea, text[], text[])
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_armor$function$
;

-- DROP FUNCTION public.crypt(text, text);

CREATE OR REPLACE FUNCTION public.crypt(text, text)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_crypt$function$
;

-- DROP FUNCTION public.dearmor(text);

CREATE OR REPLACE FUNCTION public.dearmor(text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_dearmor$function$
;

-- DROP FUNCTION public.decrypt(bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.decrypt(bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_decrypt$function$
;

-- DROP FUNCTION public.decrypt_iv(bytea, bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.decrypt_iv(bytea, bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_decrypt_iv$function$
;

-- DROP FUNCTION public.digest(text, text);

CREATE OR REPLACE FUNCTION public.digest(text, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_digest$function$
;

-- DROP FUNCTION public.digest(bytea, text);

CREATE OR REPLACE FUNCTION public.digest(bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_digest$function$
;

-- DROP FUNCTION public.encrypt(bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.encrypt(bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_encrypt$function$
;

-- DROP FUNCTION public.encrypt_iv(bytea, bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.encrypt_iv(bytea, bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_encrypt_iv$function$
;

-- DROP FUNCTION public.gen_random_bytes(int4);

CREATE OR REPLACE FUNCTION public.gen_random_bytes(integer)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_random_bytes$function$
;

-- DROP FUNCTION public.gen_random_uuid();

CREATE OR REPLACE FUNCTION public.gen_random_uuid()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE
AS '$libdir/pgcrypto', $function$pg_random_uuid$function$
;

-- DROP FUNCTION public.gen_salt(text);

CREATE OR REPLACE FUNCTION public.gen_salt(text)
 RETURNS text
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_gen_salt$function$
;

-- DROP FUNCTION public.gen_salt(text, int4);

CREATE OR REPLACE FUNCTION public.gen_salt(text, integer)
 RETURNS text
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_gen_salt_rounds$function$
;

-- DROP FUNCTION public.get_sales_by_products(date, date, text);

CREATE OR REPLACE FUNCTION public.get_sales_by_products(start_date date, end_date date, sale_status text)
 RETURNS TABLE(product_name text, purchase_price numeric, sale_price numeric, total_units_sold bigint, total_revenue numeric, total_discount numeric)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        p.name AS product_name,
        p.purchase_price,
        p.sale_price,
        SUM(sd.quantity) AS total_units_sold,
        SUM(sd.total) AS total_revenue,
        SUM(sd.subtotal - sd.total) AS total_discount
    FROM sale_details sd
    JOIN sales s ON sd.sale_id = s.id
    JOIN products p ON sd.product_id = p.id
    WHERE s.sale_date >= start_date
      AND s.sale_date < end_date
      AND s.status = sale_status
      AND s.is_active = TRUE
    GROUP BY p.id, p.name, p.purchase_price, p.sale_price
    ORDER BY total_units_sold DESC, total_revenue DESC;
END;
$function$
;

-- DROP FUNCTION public.get_sales_summary_by_payment_method(date, date);

CREATE OR REPLACE FUNCTION public.get_sales_summary_by_payment_method(start_date date, end_date date)
 RETURNS TABLE(payment_method_label text, total_sales integer, total_amount numeric, total_discount numeric)
 LANGUAGE sql
AS $function$
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
$function$
;

-- DROP FUNCTION public.hmac(bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.hmac(bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_hmac$function$
;

-- DROP FUNCTION public.hmac(text, text, text);

CREATE OR REPLACE FUNCTION public.hmac(text, text, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pg_hmac$function$
;

-- DROP FUNCTION public.pgp_armor_headers(in text, out text, out text);

CREATE OR REPLACE FUNCTION public.pgp_armor_headers(text, OUT key text, OUT value text)
 RETURNS SETOF record
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_armor_headers$function$
;

-- DROP FUNCTION public.pgp_key_id(bytea);

CREATE OR REPLACE FUNCTION public.pgp_key_id(bytea)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_key_id_w$function$
;

-- DROP FUNCTION public.pgp_pub_decrypt(bytea, bytea);

CREATE OR REPLACE FUNCTION public.pgp_pub_decrypt(bytea, bytea)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_decrypt_text$function$
;

-- DROP FUNCTION public.pgp_pub_decrypt(bytea, bytea, text, text);

CREATE OR REPLACE FUNCTION public.pgp_pub_decrypt(bytea, bytea, text, text)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_decrypt_text$function$
;

-- DROP FUNCTION public.pgp_pub_decrypt(bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_pub_decrypt(bytea, bytea, text)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_decrypt_text$function$
;

-- DROP FUNCTION public.pgp_pub_decrypt_bytea(bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_pub_decrypt_bytea(bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_decrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_pub_decrypt_bytea(bytea, bytea);

CREATE OR REPLACE FUNCTION public.pgp_pub_decrypt_bytea(bytea, bytea)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_decrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_pub_decrypt_bytea(bytea, bytea, text, text);

CREATE OR REPLACE FUNCTION public.pgp_pub_decrypt_bytea(bytea, bytea, text, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_decrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_pub_encrypt(text, bytea);

CREATE OR REPLACE FUNCTION public.pgp_pub_encrypt(text, bytea)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_encrypt_text$function$
;

-- DROP FUNCTION public.pgp_pub_encrypt(text, bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_pub_encrypt(text, bytea, text)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_encrypt_text$function$
;

-- DROP FUNCTION public.pgp_pub_encrypt_bytea(bytea, bytea);

CREATE OR REPLACE FUNCTION public.pgp_pub_encrypt_bytea(bytea, bytea)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_encrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_pub_encrypt_bytea(bytea, bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_pub_encrypt_bytea(bytea, bytea, text)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_pub_encrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_sym_decrypt(bytea, text, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_decrypt(bytea, text, text)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_decrypt_text$function$
;

-- DROP FUNCTION public.pgp_sym_decrypt(bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_decrypt(bytea, text)
 RETURNS text
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_decrypt_text$function$
;

-- DROP FUNCTION public.pgp_sym_decrypt_bytea(bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_decrypt_bytea(bytea, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_decrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_sym_decrypt_bytea(bytea, text, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_decrypt_bytea(bytea, text, text)
 RETURNS bytea
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_decrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_sym_encrypt(text, text, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_encrypt(text, text, text)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_encrypt_text$function$
;

-- DROP FUNCTION public.pgp_sym_encrypt(text, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_encrypt(text, text)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_encrypt_text$function$
;

-- DROP FUNCTION public.pgp_sym_encrypt_bytea(bytea, text, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_encrypt_bytea(bytea, text, text)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_encrypt_bytea$function$
;

-- DROP FUNCTION public.pgp_sym_encrypt_bytea(bytea, text);

CREATE OR REPLACE FUNCTION public.pgp_sym_encrypt_bytea(bytea, text)
 RETURNS bytea
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/pgcrypto', $function$pgp_sym_encrypt_bytea$function$
;


-- DROP FUNCTION public.uuid_generate_v1();

CREATE OR REPLACE FUNCTION public.uuid_generate_v1()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v1$function$
;

-- DROP FUNCTION public.uuid_generate_v1mc();

CREATE OR REPLACE FUNCTION public.uuid_generate_v1mc()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v1mc$function$
;

-- DROP FUNCTION public.uuid_generate_v3(uuid, text);

CREATE OR REPLACE FUNCTION public.uuid_generate_v3(namespace uuid, name text)
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v3$function$
;

-- DROP FUNCTION public.uuid_generate_v4();

CREATE OR REPLACE FUNCTION public.uuid_generate_v4()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v4$function$
;

-- DROP FUNCTION public.uuid_generate_v5(uuid, text);

CREATE OR REPLACE FUNCTION public.uuid_generate_v5(namespace uuid, name text)
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v5$function$
;

-- DROP FUNCTION public.uuid_nil();

CREATE OR REPLACE FUNCTION public.uuid_nil()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_nil$function$
;

-- DROP FUNCTION public.uuid_ns_dns();

CREATE OR REPLACE FUNCTION public.uuid_ns_dns()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_dns$function$
;

-- DROP FUNCTION public.uuid_ns_oid();

CREATE OR REPLACE FUNCTION public.uuid_ns_oid()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_oid$function$
;

-- DROP FUNCTION public.uuid_ns_url();

CREATE OR REPLACE FUNCTION public.uuid_ns_url()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_url$function$
;

-- DROP FUNCTION public.uuid_ns_x500();

CREATE OR REPLACE FUNCTION public.uuid_ns_x500()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_x500$function$
;