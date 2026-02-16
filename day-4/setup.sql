-- Day 4: Modern Pipelines
-- Setup for Streams, Tasks, and Dynamic Tables

USE DATABASE bootcamp_db;
USE SCHEMA training;

-- Source table for streams
CREATE OR REPLACE TABLE orders_raw (
    order_id INT,
    customer_id INT,
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    created_at TIMESTAMP
);

-- Insert initial data
INSERT INTO orders_raw VALUES
    (1, 1, 150.00, 'completed', CURRENT_TIMESTAMP());

SELECT '✅ Day 4 setup complete!' as status;
