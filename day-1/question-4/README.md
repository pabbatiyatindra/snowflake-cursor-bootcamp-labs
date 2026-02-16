# Question 4: High-Spending Premium Customers

**Duration**: ~25 minutes
**Skills**: WHERE, GROUP BY, HAVING, ORDER BY, JOIN, multiple conditions
**Difficulty**: ⭐⭐⭐ Intermediate-Advanced

## 📋 Context

Your marketing team wants to launch a "VIP Customer Rewards" program.

**Criteria**:
- Must be Premium tier
- Must have spent more than $100 total

This query identifies customers eligible for the program.

## 🎯 Your Task

Write a SQL query that:
1. Joins customers with orders (like Question 3)
2. Filters to ONLY Premium tier customers (`WHERE tier = 'Premium'`)
3. Groups by customer
4. Filters to those who spent > $100 (`HAVING SUM(amount) > 100`)
5. Orders by spending descending

## 📊 Sample Data

Same customers and orders as before:
- Alice (Premium) - $225.50 total - **QUALIFIES** ✓
- Bob (Standard) - $200.00 total - Does not qualify (not Premium)
- Charlie (Premium) - $50.00 total - Does not qualify (< $100)

## ✅ Expected Output

Only Alice qualifies:

```
name   tier     total_spending
Alice  Premium  225.50
```

## 🔍 SQL Concepts

### WHERE vs HAVING
- **WHERE**: Filter BEFORE grouping
  - Filters individual rows
  - Example: `WHERE tier = 'Premium'` (filter customers first)

- **HAVING**: Filter AFTER grouping
  - Filters groups/aggregates
  - Example: `HAVING SUM(amount) > 100` (filter groups based on sum)

### Order of Execution
1. **FROM / JOIN**: Get data from tables
2. **WHERE**: Filter rows BEFORE grouping
3. **GROUP BY**: Group data
4. **HAVING**: Filter groups AFTER grouping
5. **ORDER BY**: Sort results
6. **SELECT**: Choose columns to display

**Example pattern**:
```sql
SELECT
  c.name,
  c.tier,
  SUM(o.amount) as total_spending
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.tier = 'Premium'           -- Filter customers first
GROUP BY c.customer_id, c.name, c.tier
HAVING SUM(o.amount) > 100         -- Filter groups after aggregation
ORDER BY total_spending DESC;
```

## 🚀 How to Solve

### Key Differences from Question 3
1. **Add WHERE tier = 'Premium'** - Filter to premium only
2. **Add HAVING SUM(amount) > 100** - Filter to high spenders
3. Everything else is the same!

### Critical Distinction
- **WHERE tier = 'Premium'**: Filters which customers to include
- **HAVING SUM(amount) > 100**: Filters which GROUPS to show

If you use only `WHERE SUM(amount) > 100`, you'll get an error because WHERE can't use aggregates!

## 💡 Hints

**Hint 1**: Add WHERE BEFORE GROUP BY

**Hint 2**: Add HAVING AFTER GROUP BY

**Hint 3**: Remember: WHERE filters rows, HAVING filters groups

**Hint 4**: HAVING must use the same aggregate function as SELECT

## 🧪 Testing

1. **Mental trace**:
   - Start with customers + orders (3 customers, 4 orders)
   - WHERE tier = 'Premium': Keep Alice & Charlie only
   - GROUP BY: Aggregate their orders
     - Alice: $225.50 total
     - Charlie: $50.00 total
   - HAVING SUM(amount) > 100: Keep only Alice
   - Result: 1 row (Alice)

2. **Run in Snowflake**:
   - Copy your query
   - Execute
   - Verify only Alice appears

3. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Returns 2 rows (Alice + Charlie) | Did you add HAVING SUM(amount) > 100? |
| Returns 0 rows | Did you add WHERE tier = 'Premium'? Check if you used > or >= |
| Error with HAVING | Can't use aliases in HAVING, use full expression: HAVING SUM(o.amount) > 100 |
| Wrong order | Use ORDER BY total_spending DESC |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ Difference between WHERE and HAVING
- ✅ When to use multiple filtering conditions
- ✅ How to combine WHERE, GROUP BY, and HAVING
- ✅ Difference between row filtering and aggregate filtering
- ✅ Complete SQL query execution order

## 🏆 You've Completed Day 1!

After finishing this question, you've learned:
- ✅ Basic SELECT and COUNT (Q1)
- ✅ Aggregation and arithmetic (Q2)
- ✅ JOINs and GROUP BY (Q3)
- ✅ Multiple filters: WHERE and HAVING (Q4)

---

**🎉 Congratulations on Day 1!** Tomorrow: [Day 2 - Window Functions and CTEs](../../day-2/)
