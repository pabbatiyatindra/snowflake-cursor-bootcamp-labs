-- Day 2: Intermediate SQL + AI Refactoring
-- Setup for window functions, CTEs, and query optimization

USE DATABASE bootcamp_db;
USE SCHEMA training;

-- Ensure Day 1 tables exist
CREATE OR REPLACE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    tier VARCHAR(20)
);

INSERT INTO customers VALUES
    (1, 'Alice', 'Premium'),
    (2, 'Bob', 'Standard'),
    (3, 'Charlie', 'Premium'),
    (4, 'Diana', 'Standard'),
    (5, 'Eve', 'Premium');

CREATE OR REPLACE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10, 2),
    order_date DATE
);

INSERT INTO orders VALUES
    (1, 1, 150.00, '2024-01-15'),
    (2, 1, 75.50, '2024-01-20'),
    (3, 2, 200.00, '2024-02-10'),
    (4, 3, 50.00, '2024-02-15'),
    (5, 1, 100.00, '2024-02-20'),
    (6, 4, 125.00, '2024-03-01'),
    (7, 5, 300.00, '2024-03-05');

SELECT '✅ Day 2 setup complete!' as status;
