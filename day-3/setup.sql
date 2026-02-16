-- Day 3: Snowpark Python + Cursor IDE
-- Setup for Python transformation labs

USE DATABASE bootcamp_db;
USE SCHEMA training;

-- Base tables from previous days
CREATE OR REPLACE TABLE products (
    product_id INT,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

INSERT INTO products VALUES
    (1, 'Laptop', 'Electronics', 999.99),
    (2, 'Mouse', 'Electronics', 29.99),
    (3, 'Desk', 'Furniture', 299.99),
    (4, 'Monitor', 'Electronics', 399.99);

SELECT '✅ Day 3 setup complete!' as status;
