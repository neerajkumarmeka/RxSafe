-- Clean rebuild (drop in correct order)
DROP TRIGGER IF EXISTS normalize_search_log;
DROP VIEW IF EXISTS interaction_view;
DROP TABLE IF EXISTS search_logs;
DROP TABLE IF EXISTS interactions;
DROP TABLE IF EXISTS severity_levels;
DROP TABLE IF EXISTS drugs;

-- =========================
-- TABLE: drugs
-- =========================
CREATE TABLE drugs (
    drug_id TEXT PRIMARY KEY,
    drug_name TEXT UNIQUE NOT NULL
);

-- =========================
-- TABLE: severity_levels
-- =========================
CREATE TABLE severity_levels (
    severity_id INTEGER PRIMARY KEY,
    severity_name TEXT UNIQUE NOT NULL
);

-- Insert severity categories
INSERT INTO severity_levels (severity_id, severity_name) VALUES
(1, 'Minor'),
(2, 'Moderate'),
(3, 'Major'),
(4, 'Contraindicated');

-- =========================
-- TABLE: interactions
-- =========================
CREATE TABLE interactions (
    interaction_id INTEGER PRIMARY KEY,
    drug1_id TEXT NOT NULL,
    drug2_id TEXT NOT NULL,
    severity_id INTEGER NOT NULL,
    interaction_description TEXT,

    FOREIGN KEY (drug1_id) REFERENCES drugs(drug_id),
    FOREIGN KEY (drug2_id) REFERENCES drugs(drug_id),
    FOREIGN KEY (severity_id) REFERENCES severity_levels(severity_id),

    UNIQUE (drug1_id, drug2_id, severity_id)
);

-- =========================
-- TABLE: search_logs
-- =========================
CREATE TABLE search_logs (
    log_id INTEGER PRIMARY KEY,
    searched_drugs TEXT NOT NULL,
    search_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX idx_drug_name ON drugs(drug_name);
CREATE INDEX idx_drug1 ON interactions(drug1_id);
CREATE INDEX idx_drug2 ON interactions(drug2_id);

-- =========================
-- VIEW: interaction_view
-- Simplifies complex joins
-- =========================
CREATE VIEW interaction_view AS
SELECT
    d1.drug_name AS drug_1,
    d2.drug_name AS drug_2,
    s.severity_name AS severity
FROM interactions i
JOIN drugs d1 ON i.drug1_id = d1.drug_id
JOIN drugs d2 ON i.drug2_id = d2.drug_id
JOIN severity_levels s ON i.severity_id = s.severity_id;

-- =========================
-- TRIGGER: normalize_search_log
-- Automatically standardizes search logs
-- =========================
CREATE TRIGGER normalize_search_log
AFTER INSERT ON search_logs
FOR EACH ROW
BEGIN
    UPDATE search_logs
    SET searched_drugs = LOWER(TRIM(searched_drugs))
    WHERE log_id = NEW.log_id;
END;
