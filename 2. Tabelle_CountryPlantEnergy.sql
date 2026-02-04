-- TABELLA COUNTRY
CREATE TABLE COUNTRY (
    Country_Name VARCHAR(100) NOT NULL,   -- Chiave Primaria
    Country VARCHAR(10),                  -- Es. IT, FR, DE
    PRIMARY KEY (Country_Name)            
);

-- TABELLA PLANT
CREATE TABLE PLANT (
    ID_Plant VARCHAR(50) NOT NULL,        -- Chiave Primaria 
    Country_Name VARCHAR(100),            -- Chiave Esterna che punta a COUNTRY
    Owner VARCHAR(255),                   
    Commissioning_Year NUMERIC(4),
    Primary_Fuel VARCHAR(50),             -- Es. Gas, Wind, Solar
    Other_1 VARCHAR(50),
    Other_2 VARCHAR(50),
    Other_3 VARCHAR(50),
    Capacity_MW DECIMAL(10, 2),           -- Capacità in MW (es. 1050.50)
    Latitude DECIMAL(10, 6),              -- Precisione geografica GPS
    Longitude DECIMAL(10, 6),
    Source VARCHAR(255),                  
    PRIMARY KEY (ID_Plant),
    FOREIGN KEY (Country_Name) REFERENCES COUNTRY(Country_Name)
);

-- TABELLA ENERGY
CREATE TABLE ENERGY (
    ID_Plant VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Generation_GWh DECIMAL(15, 2),            -- Produzione reale 
    Generation_Data_Source VARCHAR(100),      
    Estimated_Generation_GWh DECIMAL(15, 2),  -- Produzione stimata
    Estimated_Note VARCHAR(255),              
     -- La chiave primaria è la combinazione di Impianto e Anno
    PRIMARY KEY (ID_Plant, Year),      
    FOREIGN KEY (ID_Plant) REFERENCES PLANT(ID_Plant)
);

