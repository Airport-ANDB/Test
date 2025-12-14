use AirportLuggageDB;

CREATE TABLE Airline (
    Name VARCHAR(100) PRIMARY KEY,
    Weight_limit DECIMAL(10, 2),
    Fee DECIMAL (5,2),
    Description VARCHAR(100)
);

CREATE TABLE Passenger (
    Document_ID VARCHAR(50) PRIMARY KEY,            
    Name VARCHAR(50) NOT NULL,
    Surname VARCHAR(50) NOT NULL
);


CREATE TABLE Flight (
    Flight_number VARCHAR(20) PRIMARY KEY,
    ID INT UNIQUE NOT NULL,           
    Destination VARCHAR(100) NOT NULL,
    Origin VARCHAR(100) NOT NULL,
    Departure_time DATETIME NOT NULL,
    Arrival_time DATETIME NOT NULL,
    Airline_Name VARCHAR(100) NOT NULL,    

    FOREIGN KEY (Airline_Name) REFERENCES Airline(Name)
);

CREATE TABLE Container (
    ID INT IDENTITY PRIMARY KEY,
    Number VARCHAR(50) NOT NULL, 
    Max_load INT NOT NULL,
    Status VARCHAR(50)
);

CREATE TABLE Baggage (
    Baggage_ID INT IDENTITY PRIMARY KEY,
    Weight DECIMAL(5, 2) NOT NULL,
    Fee DECIMAL(5,2),
    Status VARCHAR(50) NOT NULL,
    Check_in_time DATETIME2(0),
    Security_time DATETIME2(0),
    Loading_time_start DATETIME2(0),
    Loading_time_end DATETIME2(0),
    Routing_time DATETIME2(0),
    Unloading_time_start DATETIME2(0),
    Unloading_time_end DATETIME2(0),


    Passenger_Document_ID VARCHAR(50) NOT NULL, 
    Flight_Number VARCHAR(20) NOT NULL,         
    Container_ID INT,                         

    FOREIGN KEY (Passenger_Document_ID) REFERENCES Passenger(Document_ID),
    FOREIGN KEY (Flight_Number) REFERENCES Flight(Flight_number),
    FOREIGN KEY (Container_ID) REFERENCES Container(ID)
);
