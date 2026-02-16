# Question 1: Count Customers by Tier

**Duration**: ~15 minutes
**Skills**: SELECT, COUNT, GROUP BY
**Difficulty**: ⭐ Easy (Foundational)

## 📋 Context

You work for a SaaS company with three service tiers: Premium, Standard, and others.

**Business Question**: How many customers do we have in each tier?

This is critical for:
- Understanding your customer base composition
- Planning support resources
- Revenue forecasting

## 🎯 Your Task

Write a SQL query that:
1. Counts the number of customers in each tier
2. Groups results by tier
3. Shows tier name and customer count
4. Orders by tier name (alphabetically)

## 📊 Sample Data

You have a `customers` table in `bootcamp_db.training`:

| customer_id | name    | tier     |
|-------------|---------|----------|
| 1           | Alice   | Premium  |
| 2           | Bob     | Standard |
| 3           | Charlie | Premium  |

## ✅ Expected Output

```
tier       customer_count
Premium    2
Standard   1
```

## 🔍 SQL Concepts

### GROUP BY
Groups rows by a column value. All rows with the same `tier` value are grouped together.

### COUNT(*)
Counts the number of rows in each group.

### ORDER BY
Sorts the results (by tier name, alphabetically).

**Example pattern**:
```sql
SELECT
  column_to_group_by,
  COUNT(*) as count_name
FROM table_name
GROUP BY column_to_group_by
ORDER BY column_to_group_by;
```

## 🚀 How to Solve

### Option 1: Use Cursor AI (Recommended)
1. Open the `prompt.txt` file
2. Press **Cmd+L** in Cursor
3. Paste the prompt and press Enter
4. Cursor generates the full query
5. Review and copy to Snowflake

### Option 2: Write Manually
1. Think about the structure:
   - Select: tier, COUNT(*)
   - From: customers table
   - Group by: tier
2. Write the query step by step
3. Execute in Snowflake

### Option 3: Learn as You Go
1. Try writing a basic SELECT first
2. Add GROUP BY
3. Add COUNT
4. Test each step

## 💡 Hints

**Hint 1**: You need `COUNT(*)` to count rows, not `COUNT(column_name)` (though both work)

**Hint 2**: Remember to include the column you're grouping by in your GROUP BY clause

**Hint 3**: Schema-qualified table names help avoid ambiguity: `bootcamp_db.training.customers`

## 🧪 Testing

1. **Run in Snowflake**:
   ```sql
   -- Your query here
   ```

2. **Verify results**:
   - Should return 2 rows (Premium, Standard)
   - Premium should show 2 customers
   - Standard should show 1 customer

3. **Run the validator**:
   ```bash
   python3 solution_checker.py
   ```

   Success output:
   ```
   ✅ PASS - Query executed successfully
   Result matches expected output:
     Row 1: tier='Premium', customer_count=2
     Row 2: tier='Standard', customer_count=1
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Query returns error | Check table name: `SELECT * FROM bootcamp_db.training.customers LIMIT 1` |
| Returns only 1 row | Did you remember GROUP BY? Verify your query has it |
| Different customer counts | Did you run setup.sql? Try `SELECT COUNT(*) FROM customers` |
| NULL tier values | All sample data has tier values. Check your WHERE clause |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How SELECT works for basic queries
- ✅ How COUNT aggregates data
- ✅ How GROUP BY organizes results
- ✅ How to use Cursor AI for code generation

## 📝 Notes

- Snowflake stores strings in **UPPERCASE** by default
  - `'premium'` is stored as `'PREMIUM'`
  - This doesn't affect GROUP BY - similar values still group together
- ORDER BY is optional but good practice for consistent results
- You can use `COUNT(*)` or `COUNT(1)` interchangeably

---

**Next**: Review your query, then move to [Question 2](../question-2/)!
