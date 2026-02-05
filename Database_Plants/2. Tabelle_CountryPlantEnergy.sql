-- TABELLA COUNTRY
CREATE TABLE COUNTRY (
    id_country VARCHAR(3),                  -- Es. IT, FR, DE
	Country_Name VARCHAR(100) NOT NULL,     -- Chiave Primaria
    PRIMARY KEY (id_country)            
);

--TABELLA PLANT
CREATE TABLE PLANT (
    ID_Plant VARCHAR(50) NOT NULL,        -- Chiave Primaria
    id_country VARCHAR(3),                -- Chiave Esterna che punta a id_country
    name VARCHAR (500),
	Commissioning_Year NUMERIC(4),
    Primary_Fuel VARCHAR(50),             -- Es. Gas, Wind, Solar
    Capacity_MW DECIMAL(10, 2),           -- Capacità in MW
    Latitude DECIMAL(10, 6),              -- Precisione geografica
    Longitude DECIMAL(10, 6),
    PRIMARY KEY (ID_Plant),
    FOREIGN KEY (id_country) REFERENCES COUNTRY(id_country)
);

-- TABELLA ENERGY
CREATE TABLE ENERGY (
    ID_Plant VARCHAR(50) NOT NULL,
    Generation_2013_GWh DECIMAL(15, 2),            -- Produzione reale
	Generation_2014_GWh DECIMAL(15, 2),
	Generation_2015_GWh DECIMAL(15, 2),
	Generation_2016_GWh DECIMAL(15, 2),
	Generation_2017_GWh DECIMAL(15, 2),
	Generation_2018_GWh DECIMAL(15, 2),
	Generation_2019_GWh DECIMAL(15, 2),
    
    PRIMARY KEY (ID_Plant),      
    FOREIGN KEY (ID_Plant) REFERENCES PLANT(ID_Plant)
);