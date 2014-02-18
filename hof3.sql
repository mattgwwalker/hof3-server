PRAGMA foreign_keys = ON; -- Turn on foreign key constraints.

CREATE TABLE Admin (
  Version TEXT
);
INSERT INTO Admin(Version) VALUES("0.7");


CREATE TABLE Membranes (
  MembraneID INTEGER PRIMARY KEY,
  Name TEXT NOT NULL UNIQUE,
  Description TEXT,
  MWCO INTEGER,                  -- Daltons
  MaxInletPressure REAL,         -- bar
  MaxAlongMembranePressure REAL, -- bar
  MaxTransMembranePressure REAL, -- bar
  MaxBackPressure REAL,          -- bar
  MinTemperature REAL,           -- degrees C
  MaxTemperature REAL,           -- degrees C
  MinPH REAL,
  MaxPH REAL,
  Retired BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE Products (
  ProductID INTEGER PRIMARY KEY,
  Name TEXT NOT NULL UNIQUE,
  Description TEXT,
  MinTemperature REAL,           -- degrees C
  MaxTemperature REAL,           -- degrees C
  Retired BOOLEAN NOT NULL DEFAULT 0
);



CREATE TABLE Runs (
  RunID INTEGER PRIMARY KEY,
  Description TEXT,
  MembraneID INTEGER REFERENCES Membranes(MembraneID),
  BagFilter TEXT,                -- a description of the bag filter in use
  ProductID INTEGER REFERENCES Products(ProductID)
);



CREATE TABLE CleaningChemicals (
  ChemicalID INTEGER PRIMARY KEY,
  Retired BOOLEAN NOT NULL DEFAULT 0,
  Name TEXT NOT NULL UNIQUE,
  Description TEXT,
  MinTemperature REAL,           -- degrees C
  MaxTemperature REAL,           -- degrees C
  DosedManually BOOLEAN NOT NULL -- true if the chemcial is added over the edge of the tank
);

CREATE TABLE CleaningRegimes (
  RegimeID INTEGER PRIMARY KEY,
  Retired BOOLEAN NOT NULL DEFAULT 0,
  Name TEXT NOT NULL UNIQUE,
  Description TEXT
);

CREATE TABLE CleaningRegimeSteps (
  RegimeID INTEGER NOT NULL,
  StepNumber INTEGER NOT NULL,
  Duration INTEGER,              -- Duration of step, in seconds
  CleaningChemicalStrength REAL, -- Strength as percentage by volume; NULL if no chemicals
  Temperature REAL,              -- degrees C; null if not rinsing or washing or don't care
  DumpDuration INTEGER,          -- Dump duration in seconds; NULL if no dump
  FOREIGN KEY(RegimeID) REFERENCES CleaningRegimes(RegimeID)
);

CREATE TABLE Actions (
  ActionID INTEGER PRIMARY KEY,
  MembraneID INTEGER NOT NULL,
  ActionType INTEGER NOT NULL,   -- 1: Clean, 2:
  DateStarted INTEGER,
  DateFinished INTEGER,          -- NULL if cancelled rather than finished
  DateCancelled INTEGER,         -- NULL if finished and not cancelled
  FOREIGN KEY(MembraneID) REFERENCES Membranes(MembraneID)
);

CREATE TABLE Cleans (
  CleanID INTEGER PRIMARY KEY,
  ActionID INTEGER NOT NULL,
  ChemicalID INTEGER,
  FOREIGN KEY(ActionID) REFERENCES Actions(ActionID),
  FOREIGN KEY(ChemicalID) REFERENCES CleaningChemicals(ChemicalID)
);

CREATE TABLE WaterFluxTests (
  WaterFluxTestID INTEGER PRIMARY KEY,
  ActionID INTEGER NOT NULL,
  AvgTemperature REAL NOT NULL,  -- Data are averages over 2 minutes, after 1 minute
  AvgPH REAL NOT NULL,
  AvgPressure1 REAL NOT NULL,
  AvgPressure2 REAL NOT NULL,
  AvgPressure3 REAL NOT NULL,
  AvgPressure4 REAL NOT NULL,
  AvgFlow1 REAL NOT NULL,
  AvgFlow2 REAL NOT NULL,
  AvgFlow3 REAL NOT NULL,
  AvgPump1Speed REAL NOT NULL,
  FOREIGN KEY(ActionID) REFERENCES Actions(ActionID)
);

CREATE TABLE ContinuousConcentrations (
  ContinuousID INTEGER PRIMARY KEY,
  ActionID INTEGER NOT NULL,
  ProductID INTEGER NOT NULL,
  FOREIGN KEY(ProductID) REFERENCES Products(ProductID)
);
