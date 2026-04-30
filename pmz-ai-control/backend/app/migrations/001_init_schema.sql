CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE roles (
    id BIGSERIAL PRIMARY KEY,
    role_name VARCHAR(64) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(128) UNIQUE NOT NULL,
    email VARCHAR(256) UNIQUE,
    password_hash TEXT NOT NULL,
    role_id BIGINT REFERENCES roles(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE materials (
    id BIGSERIAL PRIMARY KEY,
    material_code VARCHAR(64) UNIQUE NOT NULL,
    material_name TEXT NOT NULL,
    unit VARCHAR(32),
    plant VARCHAR(32),
    material_group VARCHAR(64),
    drawing_number VARCHAR(128),
    weight NUMERIC(18,6),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_code VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE plants (id BIGSERIAL PRIMARY KEY, plant_code VARCHAR(32) UNIQUE NOT NULL, plant_name TEXT NOT NULL);
CREATE TABLE departments (id BIGSERIAL PRIMARY KEY, department_code VARCHAR(32) UNIQUE NOT NULL, department_name TEXT NOT NULL);
CREATE TABLE work_centers (id BIGSERIAL PRIMARY KEY, work_center_code VARCHAR(64) UNIQUE NOT NULL, work_center_name TEXT NOT NULL);

CREATE TABLE file_imports (
    id BIGSERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    original_file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(64),
    module VARCHAR(64),
    uploaded_by BIGINT REFERENCES users(id),
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(32) NOT NULL DEFAULT 'uploaded',
    rows_total INTEGER NOT NULL DEFAULT 0,
    rows_success INTEGER NOT NULL DEFAULT 0,
    rows_error INTEGER NOT NULL DEFAULT 0,
    comment TEXT
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(64) UNIQUE NOT NULL,
    customer_order VARCHAR(64),
    customer_id BIGINT REFERENCES customers(id),
    material_id BIGINT REFERENCES materials(id),
    plant VARCHAR(32),
    quantity NUMERIC(18,6),
    unit VARCHAR(32),
    contract_number VARCHAR(128),
    required_date DATE,
    status VARCHAR(32),
    source_file_id BIGINT REFERENCES file_imports(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE production_plan (
    id BIGSERIAL PRIMARY KEY,
    plan_period VARCHAR(7) NOT NULL,
    plan_version VARCHAR(32) NOT NULL,
    order_number VARCHAR(64) NOT NULL,
    material_code VARCHAR(64),
    material_name TEXT,
    plant VARCHAR(32),
    department VARCHAR(64),
    work_center VARCHAR(64),
    planned_qty NUMERIC(18,6),
    planned_hours NUMERIC(18,6),
    planned_weight NUMERIC(18,6),
    plan_date DATE,
    source_file_id BIGINT REFERENCES file_imports(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE production_fact (
    id BIGSERIAL PRIMARY KEY,
    fact_period VARCHAR(7) NOT NULL,
    order_number VARCHAR(64) NOT NULL,
    customer_order VARCHAR(64),
    material_code VARCHAR(64),
    material_name TEXT,
    plant VARCHAR(32),
    department VARCHAR(64),
    work_center VARCHAR(64),
    order_qty NUMERIC(18,6),
    delivered_qty NUMERIC(18,6),
    confirmed_qty NUMERIC(18,6),
    fact_qty NUMERIC(18,6),
    fact_hours NUMERIC(18,6),
    start_date DATE,
    finish_date DATE,
    system_status VARCHAR(128),
    sap_order VARCHAR(64),
    source_file_id BIGINT REFERENCES file_imports(id),
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE purchase_requests (
    id BIGSERIAL PRIMARY KEY,
    request_number VARCHAR(64),
    material_code VARCHAR(64),
    material_name TEXT,
    order_number VARCHAR(64),
    required_qty NUMERIC(18,6),
    ordered_qty NUMERIC(18,6),
    delivered_qty NUMERIC(18,6),
    required_date DATE,
    expected_delivery_date DATE,
    supplier VARCHAR(255),
    status VARCHAR(32),
    comment TEXT,
    source_file_id BIGINT REFERENCES file_imports(id)
);

CREATE TABLE purchase_deliveries (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT REFERENCES purchase_requests(id),
    material_code VARCHAR(64),
    delivery_date DATE,
    delivered_qty NUMERIC(18,6),
    supplier VARCHAR(255),
    status VARCHAR(32)
);

CREATE TABLE sales_delivery (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(64),
    material_code VARCHAR(64),
    customer TEXT,
    contract_number VARCHAR(128),
    planned_delivery_qty NUMERIC(18,6),
    actual_delivery_qty NUMERIC(18,6),
    warehouse_qty NUMERIC(18,6),
    remaining_qty NUMERIC(18,6),
    delivery_date DATE,
    status VARCHAR(32),
    source_file_id BIGINT REFERENCES file_imports(id)
);

CREATE TABLE schedules (
    id BIGSERIAL PRIMARY KEY,
    schedule_name VARCHAR(128),
    schedule_version VARCHAR(32),
    order_number VARCHAR(64),
    material_code VARCHAR(64),
    stage_name VARCHAR(128),
    department VARCHAR(64),
    planned_start DATE,
    planned_finish DATE,
    fact_start DATE,
    fact_finish DATE,
    duration_days NUMERIC(10,2),
    status VARCHAR(32),
    responsible VARCHAR(128)
);

CREATE TABLE schedule_changes (
    id BIGSERIAL PRIMARY KEY,
    schedule_id BIGINT REFERENCES schedules(id) ON DELETE CASCADE,
    field_name VARCHAR(64) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    reason TEXT,
    changed_by BIGINT REFERENCES users(id),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE import_rows_raw (
    id BIGSERIAL PRIMARY KEY,
    file_import_id BIGINT NOT NULL REFERENCES file_imports(id) ON DELETE CASCADE,
    sheet_name VARCHAR(255),
    row_number INTEGER NOT NULL,
    raw_data JSONB NOT NULL,
    parsed_status VARCHAR(32) NOT NULL DEFAULT 'new',
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE import_mappings (
    id BIGSERIAL PRIMARY KEY,
    file_type VARCHAR(64) NOT NULL,
    source_column VARCHAR(255) NOT NULL,
    target_table VARCHAR(128) NOT NULL,
    target_field VARCHAR(128) NOT NULL,
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    action VARCHAR(64) NOT NULL,
    entity_type VARCHAR(64) NOT NULL,
    entity_id VARCHAR(64),
    old_value JSONB,
    new_value JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    comment TEXT
);

CREATE TABLE ai_requests (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    prompt TEXT NOT NULL,
    tool_used VARCHAR(128),
    response_text TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ai_embeddings (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(64) NOT NULL,
    entity_id VARCHAR(64) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_portfolio (
    id BIGSERIAL PRIMARY KEY,
    period VARCHAR(7) NOT NULL,
    order_number VARCHAR(64) NOT NULL,
    material_code VARCHAR(64),
    material_name TEXT,
    plant VARCHAR(32),
    qty NUMERIC(18,6),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders_history (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(64) NOT NULL,
    status VARCHAR(64),
    event_date DATE,
    comment TEXT
);

CREATE TABLE plan_versions (
    id BIGSERIAL PRIMARY KEY,
    period VARCHAR(7) NOT NULL,
    version_code VARCHAR(32) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE plan_version_rows (
    id BIGSERIAL PRIMARY KEY,
    plan_version_id BIGINT NOT NULL REFERENCES plan_versions(id) ON DELETE CASCADE,
    order_number VARCHAR(64) NOT NULL,
    material_code VARCHAR(64),
    work_center VARCHAR(64),
    planned_qty NUMERIC(18,6),
    planned_hours NUMERIC(18,6)
);

CREATE TABLE warehouse_stock (
    id BIGSERIAL PRIMARY KEY,
    material_code VARCHAR(64) NOT NULL,
    plant VARCHAR(32),
    qty NUMERIC(18,6),
    snapshot_date DATE
);

CREATE TABLE sap_orders (
    id BIGSERIAL PRIMARY KEY,
    sap_order VARCHAR(64) NOT NULL,
    order_number VARCHAR(64),
    status VARCHAR(64)
);

CREATE TABLE sap_dates (
    id BIGSERIAL PRIMARY KEY,
    sap_order VARCHAR(64) NOT NULL,
    date_type VARCHAR(32) NOT NULL,
    value_date DATE
);

CREATE TABLE labor_fact (
    id BIGSERIAL PRIMARY KEY,
    period VARCHAR(7) NOT NULL,
    order_number VARCHAR(64) NOT NULL,
    work_center VARCHAR(64),
    labor_hours NUMERIC(18,6)
);

CREATE TABLE bom_specs (
    id BIGSERIAL PRIMARY KEY,
    parent_material_code VARCHAR(64) NOT NULL,
    plant VARCHAR(32),
    component_code VARCHAR(64) NOT NULL,
    component_qty NUMERIC(18,6),
    component_unit VARCHAR(32)
);

CREATE TABLE routing_operations (
    id BIGSERIAL PRIMARY KEY,
    material_code VARCHAR(64) NOT NULL,
    plant VARCHAR(32),
    work_center VARCHAR(64) NOT NULL,
    labor_value NUMERIC(18,6),
    labor_unit VARCHAR(16)
);

ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS source_sheet VARCHAR(128);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS source_row_number INTEGER;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS year INTEGER;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS month INTEGER;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS plant VARCHAR(32);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS material_code VARCHAR(64);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS material_name TEXT;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS qty NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS source_profile VARCHAR(64);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS period VARCHAR(7);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS customer_id BIGINT;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS registration_number VARCHAR(64);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS unit VARCHAR(32);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS qty_agreed NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS qty_planned NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS qty_fact NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS qty_shipped NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS sap_order_number VARCHAR(64);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS customer_order VARCHAR(64);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS service_note_number VARCHAR(128);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS cancel_note_number VARCHAR(128);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS status_group VARCHAR(32);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS date_input DATE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS date_finish_plan DATE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS date_finish_fact DATE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS basis TEXT;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS additional_info TEXT;

CREATE TABLE IF NOT EXISTS orders_history_raw_rows (
    id BIGSERIAL PRIMARY KEY,
    file_import_id BIGINT NOT NULL REFERENCES file_imports(id) ON DELETE CASCADE,
    sheet_name VARCHAR(255) NOT NULL,
    row_number INTEGER NOT NULL,
    raw_data JSONB NOT NULL,
    detected_profile VARCHAR(64),
    parse_status VARCHAR(32),
    error_message TEXT
);

ALTER TABLE orders_history_raw_rows
    ALTER COLUMN raw_data TYPE JSONB USING raw_data::jsonb;

ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS date_registration DATE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS date_start_plan DATE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS delivery_date DATE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS qty_requested NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS planned_hours NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS fact_hours NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS labor_hours NUMERIC(18,6);
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS source_file_id BIGINT;
ALTER TABLE orders_history ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

CREATE TABLE IF NOT EXISTS orders_history_sheet_profiles (
    id BIGSERIAL PRIMARY KEY,
    profile_name VARCHAR(128) NOT NULL,
    sheet_name_pattern VARCHAR(255) NOT NULL,
    profile_type VARCHAR(64) NOT NULL,
    header_row INTEGER,
    data_start_row INTEGER,
    mapping_json TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS registration_number VARCHAR(64);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS registration_date DATE;
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS planning_variant VARCHAR(64);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS order_open_date DATE;
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS unit VARCHAR(32);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS agreed_qty NUMERIC(18,6);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS planned_qty NUMERIC(18,6);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS shipped_qty NUMERIC(18,6);
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS additional_info TEXT;
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS note TEXT;
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS planned_delivery_date DATE;
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS actual_delivery_date DATE;
ALTER TABLE order_portfolio ADD COLUMN IF NOT EXISTS order_status VARCHAR(64);

CREATE TABLE IF NOT EXISTS work_centers (
    id BIGSERIAL PRIMARY KEY,
    work_center_name VARCHAR(255) NOT NULL,
    work_center_number VARCHAR(64) NOT NULL,
    department VARCHAR(128) NOT NULL,
    plant VARCHAR(32) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    source_file_id BIGINT,
    source_sheet VARCHAR(255),
    source_row_number INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customers (
    id BIGSERIAL PRIMARY KEY,
    customer_code VARCHAR(64),
    customer_name VARCHAR(255) NOT NULL,
    short_name VARCHAR(255),
    plant VARCHAR(32),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    source_file_id BIGINT,
    source_sheet VARCHAR(255),
    source_row_number INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plants (
    id BIGSERIAL PRIMARY KEY,
    plant_code VARCHAR(32) UNIQUE NOT NULL,
    plant_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    source_file_id BIGINT,
    source_sheet VARCHAR(255),
    source_row_number INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_planning_variants (
    id BIGSERIAL PRIMARY KEY,
    variant_code VARCHAR(64) UNIQUE NOT NULL,
    variant_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_batch_import_rows (
    id BIGSERIAL PRIMARY KEY,
    file_import_id BIGINT NOT NULL REFERENCES file_imports(id) ON DELETE CASCADE,
    source_sheet VARCHAR(255),
    source_row_number INTEGER,
    plant VARCHAR(32),
    customer_name VARCHAR(255),
    planning_variant VARCHAR(64),
    year INTEGER,
    month INTEGER,
    order_number VARCHAR(64),
    order_open_date DATE,
    material_code VARCHAR(64),
    material_name TEXT,
    variant_qty NUMERIC(18,6),
    delivery_date DATE,
    status VARCHAR(64),
    note TEXT,
    validation_status VARCHAR(32),
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_duplicate_checks (
    id BIGSERIAL PRIMARY KEY,
    plant VARCHAR(32),
    customer_name VARCHAR(255),
    planning_variant VARCHAR(64),
    order_number VARCHAR(64),
    material_code VARCHAR(64),
    period VARCHAR(7),
    duplicate_count INTEGER,
    duplicate_type VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders_history_links (
    id BIGSERIAL PRIMARY KEY,
    portfolio_id BIGINT NOT NULL REFERENCES order_portfolio(id) ON DELETE CASCADE,
    history_id BIGINT NOT NULL REFERENCES orders_history(id) ON DELETE CASCADE,
    match_type VARCHAR(64),
    match_score NUMERIC(5,2),
    matched_by VARCHAR(32),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_transfers (
    id BIGSERIAL PRIMARY KEY,
    transfer_batch_id VARCHAR(64) NOT NULL,
    source_portfolio_id BIGINT,
    plant VARCHAR(32),
    customer_id BIGINT,
    material_code VARCHAR(64),
    material_name TEXT,
    qty NUMERIC(18,6),
    hours NUMERIC(18,6),
    delivery_date DATE,
    transfer_type VARCHAR(16) NOT NULL,
    planning_variant VARCHAR(128),
    status VARCHAR(64),
    created_by VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
