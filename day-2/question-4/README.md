# Question 4: Optimize a Slow Query with Cursor AI

**Duration**: ~35 minutes
**Skills**: Query optimization, CTEs, window functions, Cursor AI assistance
**Difficulty**: ⭐⭐⭐⭐ Advanced

## 📋 Context

You received a slow query from the analytics team. It joins multiple tables, uses subqueries, and calculates window functions - but it's timing out on large datasets.

Your mission:
1. Understand what the query does
2. Identify the bottlenecks
3. Use Cursor AI to refactor for performance
4. Test both versions and compare speed

This is a realistic end-to-end optimization task using AI assistance.

## 🎯 Your Task

SLOW QUERY (DO NOT COPY - just reference):
```sql
SELECT
  o.order_id,
  o.customer_id,
  c.customer_name,
  o.amount,
  (SELECT COUNT(*) FROM bootcamp_db.training.orders o2
   WHERE o2.customer_id = o.customer_id) as lifetime_orders,
  ROW_NUMBER() OVER (ORDER BY o.amount DESC) as overall_rank
FROM bootcamp_db.training.orders o
JOIN bootcamp_db.training.customers c
  ON o.customer_id = c.customer_id
WHERE EXISTS (
  SELECT 1 FROM bootcamp_db.training.orders o3
  WHERE o3.customer_id = o.customer_id
    AND o3.amount > (SELECT AVG(amount) FROM bootcamp_db.training.orders)
);
```

Problems:
- Subquery in SELECT (runs for EVERY row)
- Correlated subquery in WHERE
- Multiple aggregations
- Inefficient filtering

Your task:
1. Use Cursor to discuss optimization strategies
2. Create an optimized version using:
   - CTEs to pre-calculate aggregates
   - Window functions instead of subqueries
   - Join-based filtering instead of EXISTS
3. Verify results are identical
4. Compare execution plans

## ✅ Expected Output

Same results as original query, but faster execution:
```
order_id  customer_id  customer_name  amount   lifetime_orders  overall_rank
1         1            Alice          100.00   3                5
2         1            Alice          150.00   3                3
5         2            Bob            200.00   2                1
```

## 🔍 SQL Concepts

### Optimization Patterns

**Problem 1: Subquery in SELECT**
```sql
-- SLOW: Runs for every row
SELECT
  order_id,
  (SELECT COUNT(*) FROM orders o2 WHERE o2.customer_id = o.customer_id) as total
FROM orders o;
```

**Solution**: Use window function
```sql
-- FAST: Calculates once per partition
SELECT
  order_id,
  COUNT(*) OVER (PARTITION BY customer_id) as total
FROM orders;
```

**Problem 2: Correlated WHERE Subquery**
```sql
-- SLOW: Evaluates subquery per row
WHERE EXISTS (
  SELECT 1 FROM orders o2
  WHERE o2.customer_id = o.customer_id
);
```

**Solution**: Use CTE + JOIN
```sql
-- FAST: Filter once, join once
WITH customers_with_orders AS (
  SELECT DISTINCT customer_id FROM orders
)
WHERE o.customer_id IN (
  SELECT customer_id FROM customers_with_orders
);
```

**Problem 3: Multiple Aggregations**
```sql
-- SLOW: Calculates avg multiple times
WHERE amount > (SELECT AVG(amount) FROM orders)
  AND customer_id IN (SELECT ...)
```

**Solution**: CTE with single aggregation
```sql
WITH avg_amount AS (
  SELECT AVG(amount) as avg_amt FROM orders
)
WHERE amount > (SELECT avg_amt FROM avg_amount)
```

### CTEs for Performance
Break complex logic into readable, reusable steps:
```sql
WITH customer_stats AS (
  SELECT
    customer_id,
    COUNT(*) as lifetime_orders,
    AVG(amount) as avg_order,
    MAX(amount) as max_order
  FROM orders
  GROUP BY customer_id
),
customer_above_avg AS (
  SELECT DISTINCT customer_id
  FROM orders o
  JOIN customer_stats cs ON o.customer_id = cs.customer_id
  WHERE o.amount > (SELECT AVG(amount) FROM orders)
)
SELECT
  o.order_id,
  o.customer_id,
  c.customer_name,
  o.amount,
  cs.lifetime_orders,
  ROW_NUMBER() OVER (ORDER BY o.amount DESC) as overall_rank
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN customer_stats cs ON o.customer_id = cs.customer_id
WHERE o.customer_id IN (SELECT customer_id FROM customer_above_avg)
ORDER BY overall_rank;
```

## 🚀 How to Solve

### Step 1: Use Cursor AI to analyze the slow query
1. Open `prompt.txt`
2. Press **Cmd+L** in Cursor
3. Ask:
   - What's the most expensive operation?
   - How can we replace subqueries with CTEs?
   - Where should we use window functions?

### Step 2: Discuss optimization with Cursor
Key questions:
- "Why is the SELECT subquery slow?" (runs per row)
- "How can we pre-calculate customer counts?" (CTE + window function)
- "How do we eliminate correlated subqueries?" (CTE + JOIN)

### Step 3: Have Cursor write the optimized version
Request:
- "Rewrite using CTEs and window functions"
- "Avoid subqueries in SELECT clause"
- "Make it readable with clear CTE names"

### Step 4: Test both versions
```sql
-- Slow version (original)
-- ... 

-- Fast version (optimized)
-- ...

-- Verify same results
SELECT COUNT(*) FROM (
  SELECT * FROM slow_version
  EXCEPT
  SELECT * FROM fast_version
) as differences;
-- Should return 0 differences
```

## 💡 Hints

**Hint 1**: Replace SELECT subqueries with window functions

**Hint 2**: Replace WHERE subqueries with CTEs + JOINs

**Hint 3**: Pre-aggregate in CTE instead of calculating in main query

**Hint 4**: Use COUNT() OVER (PARTITION BY) instead of COUNT(*)

**Hint 5**: CTE + DISTINCT + JOIN faster than EXISTS

**Hint 6**: One CTE for aggregations, one for filtering conditions

## 🧪 Testing

1. **Count results from both versions**:
   ```sql
   SELECT COUNT(*) FROM slow_version;
   SELECT COUNT(*) FROM fast_version;
   -- Should match
   ```

2. **Check for duplicates**:
   ```sql
   SELECT * FROM slow_version
   EXCEPT ALL
   SELECT * FROM fast_version;
   -- Should return 0 rows
   ```

3. **Run EXPLAIN on both**:
   Compare execution plans to see efficiency gains

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Results don't match | Use EXCEPT to find differences, adjust JOIN logic |
| Still getting NULL values | Check if window function needs ORDER BY clause |
| Performance not improved | Verify CTEs are actually used (not just defined) |
| Syntax errors in CTE chain | Check CTE references, ensure correct FROM clause |
| Join producing duplicates | Add DISTINCT after GROUP BY aggregations |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How to identify performance bottlenecks in queries
- ✅ When to use CTEs vs subqueries
- ✅ How window functions eliminate subqueries
- ✅ The performance impact of correlated subqueries
- ✅ How to refactor complex queries for readability and speed
- ✅ How to use Cursor AI for real-world optimization tasks

---

**Next**: Move to [Day 3](../../day-3/)!
