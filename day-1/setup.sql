-- Day 1: Setup + Cursor Basics + Snowflake 101
-- This script sets up the sample data for Day 1 labs

-- Make sure we're in the right database and schema
USE DATABASE bootcamp_db;
USE SCHEMA training;

-- Create customers table (for all labs)
CREATE OR REPLACE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    tier VARCHAR(20)
);

-- Insert sample data
INSERT INTO customers VALUES
    (1, 'Alice', 'Premium'),
    (2, 'Bob', 'Standard'),
    (3, 'Charlie', 'Premium');

-- Create orders table (for tasks 3-4)
CREATE OR REPLACE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Insert sample orders
INSERT INTO orders VALUES
    (1, 1, 150.00),
    (2, 1, 75.50),
    (3, 2, 200.00),
    (4, 3, 50.00);

-- Verify setup
SELECT 'Customers:' as table_name;
SELECT * FROM customers ORDER BY customer_id;

SELECT 'Orders:' as table_name;
SELECT * FROM orders ORDER BY order_id;

SELECT '✅ Day 1 setup complete!' as status;
