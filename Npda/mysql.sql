-- Create the database
CREATE DATABASE npda_db;

-- Use the database
USE npda_db;

-- Create the users table with the password column
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    aadhaar VARCHAR(20),
    balance DECIMAL(10, 2),
    document VARCHAR(255),
    password VARCHAR(255) NOT NULL
);

-- Create the stamp_store table
CREATE TABLE stamp_store (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stamp_name VARCHAR(255) NOT NULL,
    stamp_value DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the stamps table with the stamp_id column
CREATE TABLE stamps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    stamp_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (stamp_id) REFERENCES stamp_store(id) ON DELETE CASCADE
);

-- Insert some sample stamps into the stamp_store
INSERT INTO stamp_store (stamp_name, stamp_value) VALUES
('Stamp A', 10.00),
('Stamp B', 20.00),
('Stamp C', 30.00);

-- Check users table
SELECT * FROM users;

-- Check stamp_store table
SELECT * FROM stamp_store;

-- Check stamps table
SELECT * FROM stamps;
CREATE TABLE gift_npda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_name VARCHAR(100) NOT NULL,
    recipient_email VARCHAR(100) NOT NULL,
    deposit_amount FLOAT NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from gift_npda;