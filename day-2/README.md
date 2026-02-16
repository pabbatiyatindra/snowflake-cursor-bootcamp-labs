# Day 2: Intermediate SQL - Advanced Query Patterns

## Overview

**Duration**: 2 hours  
**Focus**: Window functions, CTEs, QUALIFY, performance optimization  
**Difficulty**: ⭐⭐ - ⭐⭐⭐⭐

This day takes your SQL skills from basic to advanced. You'll learn patterns used by senior data engineers and analytics professionals.

## Learning Path

### Question 1: Window Functions (⭐⭐)
- **Time**: 25 minutes
- **Topic**: Customer ranking by spending with ROW_NUMBER()
- **Key Skills**: PARTITION BY, ORDER BY, window functions
- **Real-World**: Identifying top customers, ranking results without collapsing rows
- **Start**: [Question 1](./question-1/)

### Question 2: CTEs & QUALIFY (⭐⭐⭐)
- **Time**: 30 minutes
- **Topic**: Customer deduplication with CTEs and QUALIFY
- **Key Skills**: WITH clause, QUALIFY filtering, subquery replacement
- **Real-World**: Data cleaning, removing duplicates efficiently
- **Start**: [Question 2](./question-2/)

### Question 3: Performance Analysis (⭐⭐⭐)
- **Time**: 25 minutes
- **Topic**: Query optimization with EXPLAIN
- **Key Skills**: Understanding execution plans, partition pruning, sargable predicates
- **Real-World**: Diagnosing slow queries, optimizing data warehouse performance
- **Start**: [Question 3](./question-3/)

### Question 4: Query Optimization (⭐⭐⭐⭐)
- **Time**: 35 minutes
- **Topic**: Refactoring slow queries with Cursor AI
- **Key Skills**: CTE decomposition, window function optimization, performance tuning
- **Real-World**: Working with AI to optimize complex queries
- **Start**: [Question 4](./question-4/)

## Key Concepts Covered

### Window Functions
- Calculate ranks, running totals, lead/lag within partitions
- PARTITION BY: Create independent groups
- ORDER BY: Determine ranking order
- ROW_NUMBER(), RANK(), DENSE_RANK()

### CTEs (Common Table Expressions)
- Reusable named result sets
- Improve query readability
- Multi-step transformations
- Recursive CTEs for hierarchies

### QUALIFY Clause
- Filter based on window function results
- Alternative to WHERE for window functions
- Cleaner deduplication logic

### Performance Optimization
- EXPLAIN: Understand query execution
- Partition pruning: Read only relevant data
- Sargable predicates: Conditions that can use indexes
- Cost-based optimization

## How to Use These Labs

1. **Read the README** in each question folder
2. **Open the prompt.txt** in Cursor for AI assistance
3. **Reference the expected_output.json** to understand requirements
4. **Run your solution** and execute solution_checker.py
5. **Review troubleshooting** if validation fails

## Common Patterns

### Window Function Pattern
```sql
SELECT
  col1,
  ROW_NUMBER() OVER (PARTITION BY col2 ORDER BY col3 DESC) as rank
FROM table
```

### CTE Pattern
```sql
WITH base_data AS (
  SELECT ... FROM ...
),
aggregated AS (
  SELECT ... FROM base_data
)
SELECT * FROM aggregated
```

### QUALIFY Pattern
```sql
SELECT col1, col2
FROM table
QUALIFY ROW_NUMBER() OVER (PARTITION BY col1 ORDER BY col2) = 1
```

## Validation

Each question includes:
- **prompt.txt**: Detailed instructions for Cursor AI
- **expected_output.json**: Schema and validation rules
- **solution_checker.py**: Automated validation script

Run validation with:
```bash
python3 solution_checker.py
```

## Progression

- Q1: Learn window functions fundamentals
- Q2: Apply QUALIFY for practical deduplication
- Q3: Understand performance with EXPLAIN
- Q4: Optimize complex queries with AI help

## Time Estimates

| Question | Duration | Difficulty | Prerequisite |
|----------|----------|------------|--------------|
| 1        | 25 min   | ⭐⭐      | Day 1       |
| 2        | 30 min   | ⭐⭐⭐    | Q1          |
| 3        | 25 min   | ⭐⭐⭐    | Q1, Q2      |
| 4        | 35 min   | ⭐⭐⭐⭐  | Q1, Q2, Q3  |
| **Total**| **115 min** | **Advanced** | Day 1+ |

## Resources

- [Snowflake Window Functions Docs](https://docs.snowflake.com/en/sql-reference/functions/row_number.html)
- [Snowflake CTEs](https://docs.snowflake.com/en/user-guide/queries-cte.html)
- [EXPLAIN in Snowflake](https://docs.snowflake.com/en/sql-reference/sql/explain.html)

## Tips for Success

1. **Test step-by-step**: Build queries incrementally
2. **Use LIMIT**: Test with small datasets first
3. **Read the error messages**: Snowflake gives good feedback
4. **Compare plans**: Use EXPLAIN to understand optimization
5. **Ask Claude**: Use Cursor /ask for explanations

## Next Steps

After Day 2:
- You understand advanced SQL patterns
- You can optimize complex queries
- You know how to analyze performance
- You're ready for Python and Snowpark!

→ Move to [Day 3: Snowpark Python](../day-3/)
