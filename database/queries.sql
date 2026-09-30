SELECT
    d1.drug_name AS drug_1,
    d2.drug_name AS drug_2,
    s.severity_name
FROM interactions i
JOIN drugs d1 ON i.drug1_id = d1.drug_id
JOIN drugs d2 ON i.drug2_id = d2.drug_id
JOIN severity_levels s ON i.severity_id = s.severity_id
WHERE LOWER(d1.drug_name) = 'abacavir'
AND LOWER(d2.drug_name) = 'orlistat';
