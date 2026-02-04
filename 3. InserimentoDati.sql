-- 1. INSERIMENTO PAESI (Tabella COUNTRY)
INSERT INTO COUNTRY (Country_Name, Country)
SELECT DISTINCT country_long, country
FROM GlobalPowerPlant
ON CONFLICT (Country_Name) DO NOTHING;

-- 2. INSERIMENTO IMPIANTI (Tabella PLANT)
INSERT INTO PLANT (
    ID_Plant, Country_Name, Owner, Commissioning_Year, 
    Primary_Fuel, Other_1, Other_2, Other_3, 
    Capacity_MW, Latitude, Longitude, Source
)
SELECT DISTINCT 
    gppd_idnr, country_long, owner, commissioning_year, 
    primary_fuel, other_fuel1, other_fuel2, other_fuel3, 
    capacity_mw, latitude, longitude, source
FROM GlobalPowerPlant
ON CONFLICT (ID_Plant) DO NOTHING;

-- 3. INSERIMENTO PRODUZIONE (Tabella ENERGY)
-- Include anni dal 2013 al 2019
INSERT INTO ENERGY (ID_Plant, Year, Generation_GWh, Generation_Data_Source, Estimated_Generation_GWh, Estimated_Note)

-- ANNO 2013
SELECT gppd_idnr, 2013, generation_gwh_2013, generation_data_source, estimated_generation_gwh_2013, estimated_generation_note_2013
FROM GlobalPowerPlant
WHERE generation_gwh_2013 IS NOT NULL OR estimated_generation_gwh_2013 IS NOT NULL

UNION ALL

-- ANNO 2014
SELECT gppd_idnr, 2014, generation_gwh_2014, generation_data_source, estimated_generation_gwh_2014, estimated_generation_note_2014
FROM GlobalPowerPlant
WHERE generation_gwh_2014 IS NOT NULL OR estimated_generation_gwh_2014 IS NOT NULL

UNION ALL

-- ANNO 2015
SELECT gppd_idnr, 2015, generation_gwh_2015, generation_data_source, estimated_generation_gwh_2015, estimated_generation_note_2015
FROM GlobalPowerPlant
WHERE generation_gwh_2015 IS NOT NULL OR estimated_generation_gwh_2015 IS NOT NULL

UNION ALL

-- ANNO 2016
SELECT gppd_idnr, 2016, generation_gwh_2016, generation_data_source, estimated_generation_gwh_2016, estimated_generation_note_2016
FROM GlobalPowerPlant
WHERE generation_gwh_2016 IS NOT NULL OR estimated_generation_gwh_2016 IS NOT NULL

UNION ALL

-- ANNO 2017
SELECT gppd_idnr, 2017, generation_gwh_2017, generation_data_source, estimated_generation_gwh_2017, estimated_generation_note_2017
FROM GlobalPowerPlant
WHERE generation_gwh_2017 IS NOT NULL OR estimated_generation_gwh_2017 IS NOT NULL

UNION ALL

-- ANNO 2018 (Qui forziamo NULL sulle stime perché le colonne non esistono nel CSV)
SELECT gppd_idnr, 2018, generation_gwh_2018, generation_data_source, NULL, NULL
FROM GlobalPowerPlant
WHERE generation_gwh_2018 IS NOT NULL

UNION ALL

-- ANNO 2019 (Idem come sopra)
SELECT gppd_idnr, 2019, generation_gwh_2019, generation_data_source, NULL, NULL
FROM GlobalPowerPlant
WHERE generation_gwh_2019 IS NOT NULL

-- Gestione conflitti: se rilanci lo script non si blocca
ON CONFLICT (ID_Plant, Year) DO NOTHING;