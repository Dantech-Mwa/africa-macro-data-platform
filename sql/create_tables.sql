-- =========================================
-- AFRICA MACROECONOMIC DATA WAREHOUSE
-- =========================================

-- Drop table if exists (safe reset for dev)
DROP TABLE IF EXISTS africa_macro_data;

-- =========================================
-- MAIN FACT TABLE
-- =========================================
CREATE TABLE africa_macro_data (
    id SERIAL PRIMARY KEY,

    -- Dimensions
    country TEXT NOT NULL,
    year INT NOT NULL,

    -- Economic Indicators (Raw)
    gdp DOUBLE PRECISION,
    population DOUBLE PRECISION,
    inflation DOUBLE PRECISION,

    -- Engineered Metrics
    gdp_per_capita DOUBLE PRECISION,
    growth_rate DOUBLE PRECISION,
    real_growth_proxy DOUBLE PRECISION,

    -- Metadata (optional but good practice)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- PERFORMANCE INDEX (OPTIONAL TABLE)
-- (Useful for dashboard optimization)
-- =========================================
CREATE TABLE africa_economic_index (
    id SERIAL PRIMARY KEY,

    country TEXT NOT NULL,
    year INT NOT NULL,

    gdp_score DOUBLE PRECISION,
    wealth_score DOUBLE PRECISION,
    growth_score DOUBLE PRECISION,
    stability_score DOUBLE PRECISION,

    africa_economic_strength_index DOUBLE PRECISION,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- INDEXES (VERY IMPORTANT FOR POWER BI)
-- =========================================

-- Fast filtering by country + year
CREATE INDEX idx_africa_country_year
ON africa_macro_data(country, year);

-- Index for analytical queries
CREATE INDEX idx_africa_year
ON africa_macro_data(year);

-- Index for index table
CREATE INDEX idx_index_country_year
ON africa_economic_index(country, year);
