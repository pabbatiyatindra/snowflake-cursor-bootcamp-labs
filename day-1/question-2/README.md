# Question 2: Calculate Tier Percentages

**Duration**: ~20 minutes
**Skills**: COUNT, SUM, arithmetic operations, ROUND, aggregation
**Difficulty**: ⭐⭐ Easy-Intermediate

## 📋 Context

Your CEO wants to understand the composition of your customer base:
- What percentage of customers are Premium vs Standard?
- Is your business weighted toward high-value customers?

## 🎯 Your Task

Write a SQL query that:
1. Counts customers in each tier
2. Calculates what percentage that is of all customers
3. Rounds to 1 decimal place
4. Orders by percentage (highest first)

## 📊 Sample Data

Same as Question 1:
- 3 total customers
- 2 Premium (66.67%)
- 1 Standard (33.33%)

## ✅ Expected Output

```
tier       percentage
Premium    66.7
Standard   33.3
```

## 🔍 SQL Concepts

### Aggregation with Multiple Functions
Count in each group AND total count at once using subqueries or window functions.

### ROUND() Function
`ROUND(number, decimal_places)` rounds to specified decimals
- `ROUND(66.666, 1)` → `66.7`
- `ROUND(33.333, 1)` → `33.3`

### Arithmetic in SQL
- Division: `COUNT(*) * 100.0 / total`
- Multiplication: `amount * quantity`
- Must use `* 100.0` (not `* 100`) to get decimal result

**Example pattern**:
```sql
SELECT
  tier,
  ROUND(
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers),
    1
  ) as percentage
FROM customers
GROUP BY tier
ORDER BY percentage DESC;
```

## 🚀 How to Solve

### Using Cursor AI
1. Open `prompt.txt`
2. Press **Cmd+L** in Cursor
3. Paste and discuss:
   - What's the formula for percentage?
   - How do we use ROUND?
   - How do we get total count?

### Key Considerations
- Total count: Need to count ALL customers, not just grouped ones
- Use a subquery: `(SELECT COUNT(*) FROM customers)`
- Or use window function: `SUM(COUNT(*)) OVER ()`
- Multiply by 100 for percentage
- Divide by total
- Round to 1 decimal

## 💡 Hints

**Hint 1**: You need the total customer count (3) as the denominator

**Hint 2**: Use `COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers)` for the percentage

**Hint 3**: Wrap the whole expression in `ROUND(..., 1)`

**Hint 4**: Use `DESC` in ORDER BY to show highest percentage first

## 🧪 Testing

1. **Manual verification**:
   - Premium: 2 customers / 3 total = 0.6667 * 100 = 66.67 → rounds to 66.7 ✓
   - Standard: 1 customer / 3 total = 0.3333 * 100 = 33.33 → rounds to 33.3 ✓

2. **Run in Snowflake**:
   - Copy your query
   - Execute
   - Verify results match above

3. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Returns integers (66, 33) | Use `100.0` not `100` for division. SQL treats 100/3 as integer division |
| Percentages don't add to 100 | That's OK due to rounding. 66.7 + 33.3 = 100, but 66.666... rounds to 66.7 |
| Subquery returns error | Ensure it's in parentheses and references correct table |
| ORDER BY doesn't work | Check you're ordering by percentage DESC (descending) |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How to use arithmetic operators in SQL (*, /, +)
- ✅ How to use subqueries for totals
- ✅ How ROUND() formats numbers
- ✅ How to aggregate with multiple levels of grouping
- ✅ Difference between integer and float division

---

**Next**: Move to [Question 3](../question-3/)!
