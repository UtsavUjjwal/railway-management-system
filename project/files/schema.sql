-- Railway Management System - SQLite Schema

CREATE TABLE IF NOT EXISTS trains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_number TEXT UNIQUE NOT NULL,
    train_name TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL,
    fare REAL NOT NULL,
    days_of_operation TEXT NOT NULL  -- e.g., "Mon,Tue,Wed,Thu,Fri,Sat,Sun"
);

CREATE TABLE IF NOT EXISTS passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pnr TEXT UNIQUE NOT NULL,
    train_id INTEGER NOT NULL,
    passenger_id INTEGER NOT NULL,
    journey_date TEXT NOT NULL,
    seat_number TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    status TEXT DEFAULT 'CONFIRMED',  -- CONFIRMED, CANCELLED, WAITING
    total_fare REAL NOT NULL,
    FOREIGN KEY (train_id) REFERENCES trains(id),
    FOREIGN KEY (passenger_id) REFERENCES passengers(id)
);

-- Seed data: popular Indian train routes
INSERT OR IGNORE INTO trains (train_number, train_name, source, destination, departure_time, arrival_time, total_seats, available_seats, fare, days_of_operation) VALUES
('12301', 'Rajdhani Express', 'New Delhi', 'Howrah', '16:55', '09:55', 100, 87, 1450.00, 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
('12302', 'Rajdhani Express', 'Howrah', 'New Delhi', '14:05', '07:55', 100, 63, 1450.00, 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
('12951', 'Mumbai Rajdhani', 'New Delhi', 'Mumbai Central', '16:00', '08:15', 120, 45, 1350.00, 'Mon,Wed,Fri,Sun'),
('12952', 'Mumbai Rajdhani', 'Mumbai Central', 'New Delhi', '17:00', '08:35', 120, 78, 1350.00, 'Tue,Thu,Sat'),
('12009', 'Shatabdi Express', 'Mumbai Central', 'Ahmedabad', '06:25', '12:55', 150, 112, 720.00, 'Mon,Tue,Wed,Thu,Fri,Sat'),
('12010', 'Shatabdi Express', 'Ahmedabad', 'Mumbai Central', '14:45', '21:10', 150, 99, 720.00, 'Mon,Tue,Wed,Thu,Fri,Sat'),
('12621', 'Tamil Nadu Express', 'New Delhi', 'Chennai Central', '22:30', '07:10', 180, 134, 1620.00, 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
('12622', 'Tamil Nadu Express', 'Chennai Central', 'New Delhi', '22:00', '06:40', 180, 56, 1620.00, 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
('12423', 'Dibrugarh Rajdhani', 'New Delhi', 'Dibrugarh', '21:35', '05:00', 90, 23, 1980.00, 'Mon,Wed,Fri'),
('12431', 'Trivandrum Rajdhani', 'New Delhi', 'Trivandrum', '11:00', '16:35', 110, 67, 2100.00, 'Mon,Wed,Thu,Sat');
