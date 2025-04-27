CREATE DATABASE IF NOT EXISTS inventory_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
USE inventory_db;  

-- Таблиця користувачів  
CREATE TABLE users (  
    id INT PRIMARY KEY AUTO_INCREMENT,  
    username VARCHAR(50) UNIQUE NOT NULL,  
    email VARCHAR(120) UNIQUE NOT NULL,  
    password_hash VARCHAR(255) NOT NULL,  
    role ENUM('admin', 'user', 'guest') DEFAULT 'guest',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);  

-- Таблиця вулиць  
CREATE TABLE streets (  
    id INT PRIMARY KEY AUTO_INCREMENT,  
    name VARCHAR(100) UNIQUE NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);  

-- Таблиця тарифів  
CREATE TABLE tariffs (  
    id INT PRIMARY KEY AUTO_INCREMENT,  
    name VARCHAR(50) NOT NULL,  
    price DECIMAL(10,2) NOT NULL,  
    description TEXT,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);  

-- Таблиця клієнтів  
CREATE TABLE clients (  
    id INT PRIMARY KEY AUTO_INCREMENT,  
    uid VARCHAR(50) UNIQUE NOT NULL,  
    full_name VARCHAR(100) NOT NULL,  
    street_id INT,  
    house_number VARCHAR(10) NOT NULL,  
    apartment VARCHAR(10),  
    tariff_id INT,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (street_id) REFERENCES streets(id),  
    FOREIGN KEY (tariff_id) REFERENCES tariffs(id)  
);  

-- Таблиця обладнання  
CREATE TABLE equipment (  
    id INT PRIMARY KEY AUTO_INCREMENT,  
    manufacturer VARCHAR(100) NOT NULL,  
    model VARCHAR(100) NOT NULL,  
    serial_number VARCHAR(100) UNIQUE NOT NULL,  
    mac_address VARCHAR(17) UNIQUE,  
    status ENUM('in_use', 'available', 'written_off') DEFAULT 'available',  
    client_id INT,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  
    written_off_at TIMESTAMP NULL,  
    FOREIGN KEY (client_id) REFERENCES clients(id)  
);  

-- Таблиця логів  
CREATE TABLE logs (  
    id INT PRIMARY KEY AUTO_INCREMENT,  
    user_id INT,  
    action VARCHAR(255) NOT NULL,  
    details TEXT,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (user_id) REFERENCES users(id)  
);  

-- Створення адміністратора за замовчуванням  
INSERT INTO users (username, email, password_hash, role)   
VALUES ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdoBPYyQHxwgH6.', 'admin');