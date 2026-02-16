# Day 1: Setup + Cursor Basics + Snowflake 101

**Duration**: ~2.5 hours
**Learning Path**: 1 of 5 days
**Focus**: SQL fundamentals with AI assistance

## 📚 What You'll Learn

### Lessons
1. **AI-Native Development Stack** - Understand when to use Cursor, Snowflake, and Claude
2. **Environment Setup** - Install Cursor, Snowflake, configure .cursorrules
3. **Snowflake Architecture** - Three-layer design: compute, storage, metadata
4. **Cursor Shortcuts** - Master Cmd+L, Cmd+I, Cmd+K for fast development

### Hands-On Labs
1. **Count customers by tier** - GROUP BY basics
2. **Calculate tier percentages** - Aggregation and math
3. **Join customers with orders** - LEFT JOIN concepts
4. **Find high-spending premium customers** - WHERE + HAVING + ORDER BY

## 🎯 Learning Objectives

By the end of Day 1, you will:
- ✅ Understand when to use AI tools in your workflow
- ✅ Have Cursor, Snowflake, and Python set up correctly
- ✅ Know Snowflake's architecture and design principles
- ✅ Master 4 essential SQL patterns with GROUP BY, JOINs, and aggregations
- ✅ Be comfortable using Cursor AI for code generation

## ⚙️ Prerequisites

Before starting:
1. ✅ Complete `../validate_connection.py` - confirms setup is working
2. ✅ Have Cursor IDE open
3. ✅ Have Snowflake console open in browser
4. ✅ Have read the root-level README.md

## 🗂️ Today's Questions

### [Question 1: Count Customers by Tier](./question-1/)
**Skills**: SELECT, COUNT, GROUP BY
**Context**: Understand customer distribution across service tiers
**Time**: ~15 min

**Task**: Write a query that counts customers in each tier
**Expected Result**:
```
tier       customer_count
Premium    2
Standard   1
```

### [Question 2: Calculate Tier Percentages](./question-2/)
**Skills**: COUNT, SUM, division, ROUND, QUALIFY
**Context**: Calculate market segment sizes
**Time**: ~20 min

**Task**: Show percentage of customers in each tier (rounded to 1 decimal)
**Expected Result**:
```
tier       percentage
Premium    66.7
Standard   33.3
```

### [Question 3: Join Customers with Orders](./question-3/)
**Skills**: LEFT JOIN, GROUP BY, aggregation, schema-qualified names
**Context**: See spending patterns across customer tiers
**Time**: ~20 min

**Task**: Show customer name, tier, and total spending (including customers with no orders)
**Expected Result**:
```
name      tier       total_spending
Alice     Premium    225.50
Bob       Standard   200.00
Charlie   Premium    50.00
```

### [Question 4: High-Spending Premium Customers](./question-4/)
**Skills**: WHERE, GROUP BY, HAVING, ORDER BY, JOIN
**Context**: Identify top customers for special programs
**Time**: ~25 min

**Task**: Find Premium tier customers who spent more than $100, ordered by spending
**Expected Result**:
```
name   tier     total_spending
Alice  Premium  225.50
```

## 🚀 Getting Started

### 1. Run the Setup Script
Execute the Day 1 setup in your Snowflake console:

```sql
-- Copy and paste this into Snowflake console
USE DATABASE bootcamp_db;
USE SCHEMA training;

-- Then copy and paste the full contents of setup.sql
-- File: day-1/setup.sql
```

Or if you prefer command line:
```bash
cd day-1
# Copy setup.sql contents into Snowflake console and run
```

After setup, verify:
```sql
SELECT COUNT(*) FROM customers;  -- Should return 3
SELECT COUNT(*) FROM orders;     -- Should return 4
```

### 2. Start Question 1
1. Open `question-1/README.md` - Read the full context
2. Open `question-1/prompt.txt` - Copy into Cursor
3. Press **Cmd+L** in Cursor and paste the prompt
4. Implement the SQL query
5. Run in Snowflake console
6. Run validator: `python3 question-1/solution_checker.py`

### 3. Repeat for Questions 2-4
Each question follows the same pattern:
- Read the README context
- Use Cursor (Cmd+L) with the prompt
- Execute in Snowflake
- Validate with the solution checker

## 💡 Tips for Success

### Use Cursor Effectively
- **Cmd+L**: Chat with Claude - paste the prompt and ask follow-ups
- **Cmd+I**: Inline code generation - write comments describing what you want
- **Tab**: Autocomplete - lets AI suggest based on context
- **Cmd+K**: Refactor - highlight code and ask for improvements

### SQL Best Practices (Day 1 Focus)
- Use **schema-qualified names**: `bootcamp_db.training.customers` (not just `customers`)
- Use **UPPERCASE** for SQL keywords: `SELECT`, `WHERE`, `GROUP BY`
- Use **WHERE** first to filter, then **GROUP BY** to aggregate
- Use **HAVING** to filter after grouping
- Use **LEFT JOIN** to keep all rows from the left table

### Debugging
If your query fails:
1. Check table names: `SELECT * FROM information_schema.tables`
2. Check column names: `SELECT * FROM bootcamp_db.training.customers LIMIT 1`
3. Remember: Snowflake stores strings in UPPERCASE by default
4. Use `EXPLAIN` to understand query performance

## ✅ Success Criteria

You've completed Day 1 when:
- [ ] Question 1: Solution validates (✅ PASS)
- [ ] Question 2: Solution validates (✅ PASS)
- [ ] Question 3: Solution validates (✅ PASS)
- [ ] Question 4: Solution validates (✅ PASS)
- [ ] You understand GROUP BY, JOINs, and aggregation
- [ ] You're comfortable using Cursor for code generation

## 📊 What You've Built

After Day 1, you have:
- 4 working SQL queries demonstrating core patterns
- Experience using Cursor for AI-assisted development
- Understanding of Snowflake's architecture
- Foundation for more complex queries in Day 2

## 🔗 Next Steps

### After Day 1
- ✅ Go to Day 2: Advanced SQL + Window Functions
- ✅ Review your queries - understand what each does
- ✅ Try variations: What if you used `INNER JOIN` instead of `LEFT JOIN`?

### Resources
- [Snowflake Documentation](https://docs.snowflake.com)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Cursor Documentation](https://cursor.com/docs)

## 📞 Stuck?

If you get stuck on a question:

1. **Read the README carefully** - Full context is there
2. **Use Cursor Cmd+L** - Paste the prompt and ask follow-ups
3. **Compare to expected output** - In `expected_output.json`
4. **Check solution_checker.py** - Tells you what's wrong
5. **Ask your instructor** - Office hours or bootcamp Slack

---

**Ready?** Start with [Question 1](./question-1/)! 🚀
