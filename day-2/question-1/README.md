# Question 1: Customer Ranking with Window Functions

**Duration**: ~25 minutes
**Skills**: Window functions, ROW_NUMBER(), PARTITION BY, ORDER BY
**Difficulty**: ⭐⭐ Easy-Intermediate

## 📋 Context

Your product team wants to rank customers by total spending to identify top spenders. They need:
- Which customer spent the most in each month?
- What's their rank among all customers?
- How much did they spend?

Window functions let you calculate rank without collapsing rows - perfect for analysis!

## 🎯 Your Task

Write a SQL query that:
1. Partitions customers by month (from order_date)
2. Ranks customers by total spending in that month
3. Shows: customer_id, order_month, total_spent, rank
4. Orders by month DESC, then rank ASC
5. Returns top 10 ranked customers

## 📊 Sample Data

Using `bootcamp_db.training.orders` table with columns:
- order_id
- customer_id
- order_date
- amount

Sample rows:
- Customer 1: Jan orders = $500, Feb orders = $300
- Customer 2: Jan orders = $600, Feb orders = $200
- Customer 3: Jan orders = $400, Feb orders = $400

Expected ranking (January):
1. Customer 2: $600 (rank 1)
2. Customer 1: $500 (rank 2)
3. Customer 3: $400 (rank 3)

## ✅ Expected Output

```
customer_id  order_month  total_spent  rank
1            2024-02      300.00       1
2            2024-02      200.00       2
3            2024-02      400.00       1
1            2024-01      500.00       2
2            2024-01      600.00       1
3            2024-01      400.00       3
```

## 🔍 SQL Concepts

### Window Functions Basics
Window functions perform calculations across rows related to the current row WITHOUT collapsing results.

**Syntax**:
```sql
FUNCTION() OVER (PARTITION BY col1 ORDER BY col2)
```

### ROW_NUMBER()
Assigns sequential number to rows within a partition.
```sql
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC)
```
- First row gets 1, second gets 2, etc.
- Resets when PARTITION changes
- Deterministic tie-breaking (consistent ordering)

### PARTITION BY
Divides rows into logical groups. Each group is independent.
```sql
PARTITION BY DATE_TRUNC('month', order_date)
```
- Without PARTITION BY: whole result set is one partition
- Multiple partitions: window function recalculates per group

### ORDER BY (in window function)
Determines order within partition for ranking.
```sql
ORDER BY amount DESC  -- Largest first
```
- DESC = highest values get lower rank numbers
- ASC = lowest values get lower rank numbers

### DATE_TRUNC
Truncates date to specified unit.
```sql
DATE_TRUNC('month', '2024-01-15') → '2024-01-01'
DATE_TRUNC('day', '2024-01-15 14:30:00') → '2024-01-15'
```

## 🚀 How to Solve

### Using Cursor AI
1. Open `prompt.txt`
2. Press **Cmd+L** in Cursor
3. Discuss:
   - What's a window function?
   - How does PARTITION BY work?
   - Why use ROW_NUMBER()?
   - How to extract year-month from date?

### Step-by-Step Approach

**Step 1**: Aggregate spending by customer and month
```sql
SELECT
  customer_id,
  DATE_TRUNC('month', order_date) as order_month,
  SUM(amount) as total_spent
FROM bootcamp_db.training.orders
GROUP BY 1, 2
```

**Step 2**: Add window function to rank
```sql
SELECT
  customer_id,
  DATE_TRUNC('month', order_date) as order_month,
  SUM(amount) as total_spent,
  ROW_NUMBER() OVER (
    PARTITION BY DATE_TRUNC('month', order_date)
    ORDER BY SUM(amount) DESC
  ) as rank
FROM bootcamp_db.training.orders
GROUP BY 1, 2
ORDER BY order_month DESC, rank ASC
LIMIT 10
```

## 💡 Hints

**Hint 1**: First aggregate with GROUP BY, THEN apply window function

**Hint 2**: Window functions go in SELECT, not WHERE

**Hint 3**: PARTITION BY DATE_TRUNC('month', order_date) creates groups per month

**Hint 4**: ORDER BY DESC inside window makes customer with highest amount get rank 1

**Hint 5**: Final ORDER BY is separate from window function ORDER BY

## 🧪 Testing

1. **Understand your data**:
   ```sql
   SELECT
     customer_id,
     DATE_TRUNC('month', order_date) as month,
     SUM(amount) as total
   FROM bootcamp_db.training.orders
   GROUP BY 1, 2
   ORDER BY month DESC, total DESC
   ```

2. **Verify ranking logic**:
   - Highest amount per month should have rank 1
   - Partitions reset by month
   - No ties (ROW_NUMBER always unique)

3. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Window function not allowed here" | Window functions only go in SELECT or ORDER BY, never in WHERE |
| All ranks are 1 | Missing PARTITION BY - add it to divide into groups |
| Wrong months | Use DATE_TRUNC('month', ...) not MONTH() function |
| Ties not handled | ROW_NUMBER() handles ties by assigning different numbers based on input order |
| Aggregate function error | Wrap SUM() inside the window function ORDER BY, don't reference it in PARTITION BY |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ What window functions do and why they're powerful
- ✅ How PARTITION BY creates independent groups
- ✅ How ROW_NUMBER() ranks without collapsing rows
- ✅ The difference between GROUP BY and PARTITION BY
- ✅ How to combine aggregation with window functions
- ✅ The order of operations: GROUP BY → window function → ORDER BY

---

**Next**: Move to [Question 2](../question-2/)!
