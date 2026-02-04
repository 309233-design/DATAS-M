DROP TABLE IF EXISTS GlobalPowerPlant;

CREATE TABLE GlobalPowerPlant (
    country TEXT,
    country_long TEXT,
    name TEXT,
    gppd_idnr TEXT,
    capacity_mw NUMERIC,
    latitude NUMERIC,
    longitude NUMERIC,
    primary_fuel TEXT,
    other_fuel1 TEXT,
    other_fuel2 TEXT,
    other_fuel3 TEXT,
    commissioning_year NUMERIC,
    owner TEXT,
    source TEXT,
    url TEXT,
    geolocation_source TEXT,
    wepp_id TEXT,
    year_of_capacity_data NUMERIC,
    
    -- Dati Generazione Reale (2013-2019)
    generation_gwh_2013 NUMERIC,
    generation_gwh_2014 NUMERIC,
    generation_gwh_2015 NUMERIC,
    generation_gwh_2016 NUMERIC,
    generation_gwh_2017 NUMERIC,
    generation_gwh_2018 NUMERIC,
    generation_gwh_2019 NUMERIC,
    generation_data_source TEXT,
    
    -- Dati Generazione Stimata (2013-2017)
    estimated_generation_gwh_2013 NUMERIC,
    estimated_generation_gwh_2014 NUMERIC,
    estimated_generation_gwh_2015 NUMERIC,
    estimated_generation_gwh_2016 NUMERIC,
    estimated_generation_gwh_2017 NUMERIC,
    
    -- Note sulle stime
    estimated_generation_note_2013 TEXT,
    estimated_generation_note_2014 TEXT,
    estimated_generation_note_2015 TEXT,
    estimated_generation_note_2016 TEXT,
    estimated_generation_note_2017 TEXT
);

COPY GlobalPowerPlant
FROM 'C:\global_power_plant_database.csv'
WITH (
    FORMAT CSV, 
    HEADER true, 
    DELIMITER ',', 
    ENCODING 'UTF8',
    NULL ''  -- Importante: trasforma le celle vuote in NULL, non in zeri!
);


