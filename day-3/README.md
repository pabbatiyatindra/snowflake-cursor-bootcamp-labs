# Day 3: Snowpark Python - Data Engineering

## Overview

**Duration**: 2.5 hours  
**Focus**: Snowpark DataFrames, UDFs, stored procedures, pipelines  
**Difficulty**: ⭐⭐⭐ - ⭐⭐⭐⭐

Transition from SQL to Python while staying in Snowflake. Build data engineering solutions using Snowpark.

## Learning Path

### Question 1: DataFrame Basics (⭐⭐)
- **Time**: 30 minutes
- **Topic**: Load, filter, transform data with Snowpark
- **Key Skills**: Session, DataFrame, filter(), select(), withColumn()
- **Real-World**: Python-based ETL operations
- **Start**: [Question 1](./question-1/)

### Question 2: User-Defined Functions (⭐⭐⭐)
- **Time**: 35 minutes
- **Topic**: Create Python UDFs and register with Snowflake
- **Key Skills**: @udf decorator, type hints, session.sql()
- **Real-World**: Reusable business logic functions
- **Start**: [Question 2](./question-2/)

### Question 3: Stored Procedures (⭐⭐⭐)
- **Time**: 40 minutes
- **Topic**: Multi-step workflows with error handling
- **Key Skills**: @sproc decorator, read/write DataFrames, logging
- **Real-World**: Complex data transformations
- **Start**: [Question 3](./question-3/)

### Question 4: End-to-End Pipeline (⭐⭐⭐⭐)
- **Time**: 45 minutes
- **Topic**: Complete ETL with validation and metrics
- **Key Skills**: Window functions, deduplication, quality checks
- **Real-World**: Production data pipelines
- **Start**: [Question 4](./question-4/)

## Key Concepts

### Snowpark DataFrames
- Lazy-evaluated (like Spark, unlike Pandas)
- Execute in Snowflake (scalable)
- Familiar Python API

### UDFs (User-Defined Functions)
- Python functions registered in Snowflake
- Callable from SQL
- Type hints for clarity

### Stored Procedures
- Multi-step workflows
- Can modify data
- Error handling and logging

### Data Validation
- Filter out invalid rows
- Detect duplicates with window functions
- Calculate quality metrics

## Workflow Pattern

```python
from snowflake.snowpark import Session
import snowflake.snowpark.functions as F

# Connect
session = Session.builder.configs({...}).create()

# Read
df = session.table("table_name")

# Transform
result = (df
  .filter(df.col > 100)
  .select(["col1", "col2"])
  .withColumn("new_col", F.upper(df.col))
)

# Show
result.show()

# Write
result.write.mode("overwrite").save_as_table("target")
```

## Progression

| Q | Topic | Skill Level | Builds On |
|---|-------|------------|-----------|
| 1 | DataFrames | Beginner | SQL knowledge |
| 2 | UDFs | Intermediate | Q1 |
| 3 | Procedures | Intermediate | Q1, Q2 |
| 4 | Pipelines | Advanced | Q1, Q2, Q3 |

## Important Concepts

### Lazy Evaluation
- Nothing executes until you call `.show()`, `.collect()`, or `.write()`
- Allows Snowflake to optimize the full plan

### Type Hints
```python
def process_data(customer_id: int, amount: float) -> str:
    return f"Processed {customer_id}: ${amount}"
```

### Window Functions in Snowpark
```python
from snowflake.snowpark.window import Window

w = Window.partition_by("customer_id").order_by("amount")
df = df.withColumn("rank", F.row_number().over(w))
```

## Common Patterns

### DataFrame Transformation
```python
result = (df
  .filter(...)
  .select(...)
  .withColumn(...)
  .groupBy(...)
  .agg(...)
)
```

### UDF Definition
```python
@udf(return_type=T.DecimalType())
def calculate_value(x: int) -> float:
    return float(x) * 1.1
```

### Deduplication
```python
from snowflake.snowpark.window import Window

w = Window.partition_by("customer_id")
df_dedup = (df
  .withColumn("rn", F.row_number().over(w))
  .filter(F.col("rn") == 1)
  .drop("rn")
)
```

## Time Estimates

| Q | Duration | Difficulty |
|---|----------|-----------|
| 1 | 30 min   | ⭐⭐     |
| 2 | 35 min   | ⭐⭐⭐   |
| 3 | 40 min   | ⭐⭐⭐   |
| 4 | 45 min   | ⭐⭐⭐⭐ |
| **Total** | **150 min** | **Advanced** |

## Key Files

- `prompt.txt`: Detailed task description for Cursor
- `README.md`: Full learning content
- `expected_output.json`: Expected results and validation rules
- `solution_checker.py`: Automated validation

## Tips

1. **Test with LIMIT**: Add LIMIT 5 to DataFrames for quick testing
2. **Check imports**: snowflake.snowpark has most functions you need
3. **Use type hints**: Help catch errors and document code
4. **Error handling**: Wrap in try/except for robustness
5. **Lazy evaluation**: Call .show() or .collect() to execute

## Moving Forward

After Day 3, you can:
- Build Python data transformations in Snowflake
- Create reusable UDFs and procedures
- Handle errors and validate data
- Build complete ETL pipelines

→ Move to [Day 5: Cortex AI](../day-5/)  
(Note: Day 4 covers streams/tasks/medallion in production environments)
