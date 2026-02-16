-- Day 5: Cortex AI + Capstone
-- Setup for AI-powered data enrichment

USE DATABASE bootcamp_db;
USE SCHEMA training;

-- Sample data for text analysis
CREATE OR REPLACE TABLE reviews (
    review_id INT,
    customer_id INT,
    review_text VARCHAR,
    created_at DATE
);

INSERT INTO reviews VALUES
    (1, 1, 'Great product, highly recommend!', '2024-01-15'),
    (2, 2, 'Terrible quality, waste of money', '2024-01-20'),
    (3, 3, 'Average, nothing special', '2024-02-01');

SELECT '✅ Day 5 setup complete!' as status;
