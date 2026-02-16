# Question 2: Customer Deduplication with CTEs and QUALIFY

**Duration**: ~30 minutes
**Skills**: CTEs (Common Table Expressions), QUALIFY clause, window functions, PARTITION BY
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

Your data quality team discovered duplicate customer records in the orders table. Some customers have multiple rows for the same order! You need to:
- Keep only the LATEST order for each customer
- Remove duplicate rows
- Use a CTE to make the logic readable
- Use QUALIFY to filter within the window function

This is a real-world pattern for data cleaning in data warehouses.

## 🎯 Your Task

Write a SQL query that:
1. Uses a CTE to identify the latest order date for each customer
2. Uses QUALIFY to filter: keep only rows with ROW_NUMBER() = 1
3. Partitions by customer_id
4. Orders by order_date DESC (latest first)
5. Returns: customer_id, order_id, order_date, amount
6. Returns only the most recent order per customer

## 📊 Sample Data

Orders table has duplicates:
```
order_id | customer_id | order_date  | amount
1        | 1           | 2024-01-15  | 100.00
1        | 1           | 2024-01-15  | 100.00  ← DUPLICATE
2        | 1           | 2024-02-20  | 200.00  ← LATEST
3        | 2           | 2024-01-10  | 150.00
3        | 2           | 2024-01-10  | 150.00  ← DUPLICATE
4        | 2           | 2024-01-20  | 175.00  ← LATEST
```

Expected output (latest only, no duplicates):
```
customer_id | order_id | order_date | amount
1           | 2        | 2024-02-20 | 200.00
2           | 4        | 2024-01-20 | 175.00
```

## ✅ Expected Output

```
customer_id  order_id  order_date    amount
1            2         2024-02-20    200.00
2            4         2024-01-20    175.00
3            5         2024-03-01    250.00
```

## 🔍 SQL Concepts

### Common Table Expressions (CTEs)
CTEs define named result sets that you can reference later. Makes complex queries readable.

**Syntax**:
```sql
WITH cte_name AS (
  SELECT ... FROM ...
)
SELECT ... FROM cte_name;
```

**Benefits**:
- Breaking complex logic into steps
- Reusing same subquery multiple times
- Improving readability
- Building incrementally

### QUALIFY Clause
QUALIFY filters rows AFTER window function calculation. It's like WHERE, but for window functions.

**Syntax**:
```sql
SELECT ... FROM table
QUALIFY ROW_NUMBER() OVER (PARTITION BY col ORDER BY col) = 1;
```

**vs WHERE**:
- WHERE: filters BEFORE window function (can't use window functions)
- QUALIFY: filters AFTER window function (requires window functions)

### Window Function Deduplication Pattern
This is the most efficient way to deduplicate:
```sql
ROW_NUMBER() OVER (
  PARTITION BY customer_id
  ORDER BY order_date DESC
) = 1
```
- ROW_NUMBER() = 1: first row in partition
- PARTITION BY customer_id: groups by customer
- ORDER BY order_date DESC: newest first
- Result: keep newest row, drop rest

### CTE Reusability
You can reference CTEs multiple times:
```sql
WITH customer_orders AS (
  SELECT customer_id, SUM(amount) as total
  FROM orders
  GROUP BY customer_id
)
SELECT * FROM customer_orders WHERE total > 1000;
```

## 🚀 How to Solve

### Step 1: Write the basic query without CTE
```sql
SELECT
  customer_id,
  order_id,
  order_date,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY order_date DESC
  ) as rn
FROM bootcamp_db.training.orders
```

### Step 2: Add QUALIFY to filter
```sql
SELECT
  customer_id,
  order_id,
  order_date,
  amount
FROM bootcamp_db.training.orders
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY customer_id
  ORDER BY order_date DESC
) = 1
```

### Step 3: Wrap in CTE for clarity
```sql
WITH latest_orders AS (
  SELECT
    customer_id,
    order_id,
    order_date,
    amount
  FROM bootcamp_db.training.orders
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY order_date DESC
  ) = 1
)
SELECT * FROM latest_orders
ORDER BY customer_id
```

## 💡 Hints

**Hint 1**: CTEs go at the START of query with `WITH ... AS (...)`

**Hint 2**: QUALIFY comes in SELECT statement, not WHERE

**Hint 3**: ROW_NUMBER() = 1 means "first row in partition"

**Hint 4**: PARTITION BY customer_id divides by customer

**Hint 5**: ORDER BY order_date DESC puts newest first (rank 1)

**Hint 6**: You don't need to SELECT the ROW_NUMBER() column if you use QUALIFY

## 🧪 Testing

1. **Check for duplicates first**:
   ```sql
   SELECT customer_id, order_id, COUNT(*)
   FROM bootcamp_db.training.orders
   GROUP BY 1, 2
   HAVING COUNT(*) > 1
   ```

2. **Verify your CTE works**:
   ```sql
   WITH latest_orders AS (
     SELECT customer_id, order_id, order_date, amount
     FROM bootcamp_db.training.orders
     QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1
   )
   SELECT COUNT(*) as unique_customers FROM latest_orders
   ```

3. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "CTE not found" or syntax error | CTEs must come BEFORE main SELECT with WITH keyword |
| "QUALIFY not recognized" | QUALIFY is Snowflake-specific; make sure you're in Snowflake |
| "Window function in WHERE clause" | Use QUALIFY, not WHERE, for window function filtering |
| Multiple rows per customer | QUALIFY missing or ROW_NUMBER() != 1 condition wrong |
| Wrong "latest" order | Check ORDER BY order_date DESC (DESC = newest first) |
| CTE defined but not used | Reference CTE name in FROM clause of main SELECT |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ What CTEs are and when to use them
- ✅ How to write readable multi-step queries with CTEs
- ✅ The difference between WHERE and QUALIFY
- ✅ How QUALIFY filters based on window function results
- ✅ The deduplication pattern (ROW_NUMBER() = 1)
- ✅ How to structure queries for maintainability

---

**Next**: Move to [Question 3](../question-3/)!
