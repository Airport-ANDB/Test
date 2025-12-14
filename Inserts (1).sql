use AirportLuggageDB;

INSERT INTO Passenger (Document_ID, Name, Surname)
VALUES 
('P001', 'John', 'Doe'),
('P002', 'Alice', 'Smith'),
('P003', 'Michael', 'Johnson'),
('P004', 'Emily', 'Brown'),
('P005', 'David', 'Wilson');

INSERT INTO Container (Number, Max_load, Status) VALUES
('C001', 100, 'Empty'),
('C002', 150, 'Full'),
('C003', 120, 'In Transit'),
('C004', 200, 'Empty'),
('C005', 180, 'Maintenance');

INSERT INTO Airline (Name, Weight_limit, Fee, Description)
VALUES
('SkyHigh Airways', 20000.00, 10.00, 'International airline with extensive European routes'),
('BlueWing Airlines', 15000.00, 10.00, 'Regional airline focused on short-haul flights'),
('GlobalJet', 1.00, 10.00, 'Premium airline with long-haul international flights'),
('CloudNine Air', 18000.00, 10.00, 'Budget airline with domestic routes'),
('Starline Aviation', 22000.00, 10.00, 'Full-service airline operating worldwide'),
('SunFly Express', 12000.00, 10.00, 'Low-cost airline for holiday destinations'),
('AeroMax', 20000.00, 10.00, 'Business-focused airline with priority service'),
('SkyLink', 16000.00, 10.00, 'Regional carrier connecting secondary cities'),
('Falcon Airways', 19000.00, 10.00, 'Airline specialized in cargo and passenger transport'),
('EagleWings', 23000.00, 10.00, 'Luxury airline with VIP lounges and premium service');

INSERT INTO Flight (Flight_number, ID, Destination, Origin, Departure_time, Arrival_time, Airline_Name)
VALUES
('SH101', 1, 'London, UK', 'New York, USA', '2025-12-15 08:00:00', '2025-12-15 20:00:00', 'SkyHigh Airways'),
('BW202', 2, 'Paris, France', 'Berlin, Germany', '2025-12-16 09:30:00', '2025-12-16 11:30:00', 'BlueWing Airlines'),
('GJ303', 3, 'Tokyo, Japan', 'Los Angeles, USA', '2025-12-17 12:00:00', '2025-12-18 04:00:00', 'GlobalJet'),
('CN404', 4, 'Rome, Italy', 'Madrid, Spain', '2025-12-18 07:45:00', '2025-12-18 10:15:00', 'CloudNine Air'),
('SL505', 5, 'Dubai, UAE', 'London, UK', '2025-12-19 14:00:00', '2025-12-19 22:00:00', 'Starline Aviation'),
('SF606', 6, 'Barcelona, Spain', 'Lisbon, Portugal', '2025-12-20 06:00:00', '2025-12-20 07:30:00', 'SunFly Express'),
('AM707', 7, 'Chicago, USA', 'Miami, USA', '2025-12-21 10:00:00', '2025-12-21 14:00:00', 'AeroMax'),
('SL808', 8, 'Vienna, Austria', 'Prague, Czech Republic', '2025-12-22 15:00:00', '2025-12-22 16:30:00', 'SkyLink'),
('FA909', 9, 'Singapore', 'Bangkok, Thailand', '2025-12-23 20:00:00', '2025-12-23 23:30:00', 'Falcon Airways'),
('EW010', 10, 'Sydney, Australia', 'Melbourne, Australia', '2025-12-24 09:00:00', '2025-12-24 10:30:00', 'EagleWings');

INSERT INTO Baggage 
    (Weight, Fee, Status, Check_in_time, Security_time, Loading_time_start, Loading_time_end,
     Routing_time, Unloading_time_start, Unloading_time_end, Passenger_Document_ID, Flight_Number, Container_ID)
VALUES
(18.50, 0, 'Checked-in', '2025-12-11 07:50', '2025-12-11 08:10', NULL, '2025-12-11 08:45',
 '2025-12-11 12:00', '2025-12-11 15:50', '2025-12-11 16:05', 'P001', 'SH101', 1),

(22.00, 50.00, 'Checked-in', '2025-12-11 09:00', '2025-12-11 09:20', '2025-12-11 09:40', '2025-12-11 09:55',
 '2025-12-11 13:00', '2025-12-11 16:50', '2025-12-11 17:05', 'P002', 'SL505', 2);