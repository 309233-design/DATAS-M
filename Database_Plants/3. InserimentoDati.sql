-- 1. INSERIMENTO PAESI (Tabella COUNTRY)
INSERT INTO COUNTRY (Country_Name, id_country)
SELECT DISTINCT country_long, country
FROM GlobalPowerPlant
ON CONFLICT (id_country) DO NOTHING;

-- 2. INSERIMENTO IMPIANTI (Tabella PLANT)
INSERT INTO PLANT (
    ID_Plant, id_country, name, Commissioning_Year, 
    Primary_Fuel, Capacity_MW, Latitude, Longitude 
	)
SELECT DISTINCT 
    gppd_idnr, country, name, commissioning_year, 
    primary_fuel, capacity_mw, latitude, longitude
FROM GlobalPowerPlant
ON CONFLICT (ID_Plant) DO NOTHING;

-- 3. INSERIMENTO PRODUZIONE (Tabella ENERGY)
-- Include anni dal 2013 al 2019
INSERT INTO ENERGY (ID_Plant, Generation_2013_GWh, 
	Generation_2014_GWh, Generation_2015_GWh, 
	Generation_2016_GWh, Generation_2017_GWh, 
	Generation_2018_GWh, Generation_2019_GWh
	)

SELECT DISTINCT 
	gppd_idnr, generation_gwh_2013, generation_gwh_2014, 
	generation_gwh_2015, generation_gwh_2016, generation_gwh_2017,
	generation_gwh_2018, generation_gwh_2019
FROM GlobalPowerPlant

--UNION ALL

-- Gestione conflitti: se rilanci lo script non si blocca
ON CONFLICT (ID_Plant) DO NOTHING;

-- 4. PULIZIA: Rimozione tabella temporanea GlobalPowerPlant
DROP TABLE IF EXISTS GlobalPowerPlant;