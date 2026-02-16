# Question 3: Join Customers with Orders

**Duration**: ~20 minutes
**Skills**: LEFT JOIN, GROUP BY, aggregation, COALESCE
**Difficulty**: ⭐⭐ Intermediate

## 📋 Context

You need to see spending patterns across your customer base:
- How much has each customer spent?
- Include customers who haven't placed any orders yet (they're still valuable!)
- This data helps with customer retention and upsell strategies

## 🎯 Your Task

Write a SQL query that:
1. Joins customers table with orders table
2. Uses LEFT JOIN to include customers with NO orders
3. Shows customer name, tier, and total spending
4. Sums order amounts for each customer
5. Orders by spending (highest first)

## 📊 Sample Data

**Customers Table**:
| customer_id | name    | tier     |
|-------------|---------|----------|
| 1           | Alice   | Premium  |
| 2           | Bob     | Standard |
| 3           | Charlie | Premium  |

**Orders Table**:
| order_id | customer_id | amount  |
|----------|-------------|---------|
| 1        | 1           | 150.00  |
| 2        | 1           | 75.50   |
| 3        | 2           | 200.00  |
| 4        | 3           | 50.00   |

## ✅ Expected Output

```
name      tier       total_spending
Alice     Premium    225.50
Bob       Standard   200.00
Charlie   Premium    50.00
```

## 🔍 SQL Concepts

### JOIN Types
- **INNER JOIN**: Only matching rows (customers with orders)
- **LEFT JOIN**: All rows from left table + matching rows from right
  - Keeps customers with NO orders
  - Unmatched order columns are NULL

### COALESCE() Function
Replaces NULL with a value
- `COALESCE(NULL, 0)` → `0`
- Useful for "no orders yet" → "0 spending"

### SUM() with GROUP BY
When you GROUP BY, you must SUM columns that aren't part of the group

**Example pattern**:
```sql
SELECT
  c.customer_id,
  c.name,
  c.tier,
  COALESCE(SUM(o.amount), 0) as total_spending
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.tier
ORDER BY total_spending DESC;
```

## 🚀 How to Solve

### Key Steps
1. **SELECT**: customer name, tier, SUM(order amount)
2. **FROM**: customers table (use alias `c`)
3. **LEFT JOIN**: orders table ON `c.customer_id = o.customer_id` (use alias `o`)
4. **GROUP BY**: all customer columns
5. **ORDER BY**: total_spending DESC

### Why LEFT JOIN?
- Shows all customers (even those with no orders)
- For customers with no orders, `SUM(o.amount)` would be NULL
- Wrap with `COALESCE(..., 0)` to show 0 instead of NULL

## 💡 Hints

**Hint 1**: Remember to use table aliases (c for customers, o for orders)

**Hint 2**: JOIN condition: `ON c.customer_id = o.customer_id`

**Hint 3**: GROUP BY must include all non-aggregated columns

**Hint 4**: Use `COALESCE(SUM(o.amount), 0)` to handle NULL for no-order customers

## 🧪 Testing

1. **Verify join logic**:
   - Alice: Orders 1 + 2 = $225.50 ✓
   - Bob: Order 3 = $200.00 ✓
   - Charlie: Order 4 = $50.00 ✓

2. **Left JOIN verification**:
   - All 3 customers appear (not just those with orders)
   - No NULL spending values

3. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Only 2 rows returned | Use LEFT JOIN not INNER JOIN to include all customers |
| NULL in spending column | Use COALESCE(SUM(...), 0) to convert NULL to 0 |
| Query error on GROUP BY | Include ALL non-aggregated columns in GROUP BY |
| Wrong spending totals | Check JOIN condition and verify aliases are consistent |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How INNER JOIN vs LEFT JOIN work
- ✅ When to use COALESCE for NULL handling
- ✅ How to aggregate data from multiple tables
- ✅ Table aliases and their purpose
- ✅ GROUP BY with JOINs

---

**Next**: Move to [Question 4](../question-4/)!
