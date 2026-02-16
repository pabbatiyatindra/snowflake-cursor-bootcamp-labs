# Question 3: Stored Procedures with Snowpark Python

**Duration**: ~40 minutes
**Skills**: Stored procedures, data transformation, logging, error handling
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

Stored procedures are like UDFs but for multi-step workflows. They can:
- Execute multiple queries
- Insert/update data
- Log progress
- Handle complex logic

Your task: Create a stored procedure that transforms customer data and logs the transformation.

## 🎯 Your Task

Create a Snowpark stored procedure that:
1. Reads customers from source table
2. Transforms data (add prefix to names, standardize regions)
3. Inserts into target table
4. Logs the transformation (rows processed, timestamp)
5. Returns summary statistics

## 📊 Sample Data

Source:
```
customer_id | customer_name | region
1           | alice         | us-west
2           | bob           | US-EAST
3           | charlie       | eu-west
```

Target (after transformation):
```
customer_id | customer_name_clean | region_clean | transformed_date
1           | PREFIX_ALICE        | US-WEST      | 2024-02-16
2           | PREFIX_BOB          | US-EAST      | 2024-02-16
3           | PREFIX_CHARLIE      | EU-WEST      | 2024-02-16
```

## ✅ Expected Output

Procedure returns:
```
Status: SUCCESS
Rows processed: 3
Rows inserted: 3
Transformation date: 2024-02-16
Duration: 1.23 seconds
```

## 🔍 Python/Snowpark Concepts

### Procedure Definition
```python
from snowflake.snowpark.functions import sproc
import snowflake.snowpark.types as T

@sproc(return_type=T.StringType())
def transform_customers() -> str:
    # Multi-step logic
    return result_message
```

### Executing SQL from Procedure
```python
@sproc(return_type=T.StringType())
def transform_customers() -> str:
    # Read source
    source_df = session.table("source_customers")
    
    # Transform
    transformed = source_df.select(
        source_df.customer_id,
        (F.lit("PREFIX_") + F.upper(source_df.customer_name)).alias("customer_name_clean"),
        F.upper(source_df.region).alias("region_clean"),
        F.current_date().alias("transformed_date")
    )
    
    # Write
    transformed.write.mode("append").save_as_table("target_customers")
    
    return f"Transformed {transformed.count()} rows"
```

### Error Handling in Procedures
```python
try:
    # Transformation logic
    row_count = transformed.count()
    transformed.write.mode("append").save_as_table("target")
    return f"SUCCESS: {row_count} rows"
except Exception as e:
    return f"ERROR: {str(e)}"
```

## 🚀 How to Solve

### Step 1: Define procedure structure
```python
from snowflake.snowpark.functions import sproc
import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F
import time

@sproc(return_type=T.StringType())
def transform_customers() -> str:
    start_time = time.time()
    
    try:
        # Step 1: Read source
        source_df = session.table("bootcamp_db.training.customers")
        
        # Step 2: Transform
        transformed_df = source_df.select(
            source_df.customer_id,
            (F.lit("PREFIX_") + F.upper(source_df.customer_name)).alias("customer_name_clean"),
            F.upper(source_df.region).alias("region_clean"),
            F.current_date().alias("transformed_date")
        )
        
        # Step 3: Write to target
        row_count = transformed_df.count()
        transformed_df.write.mode("append").save_as_table("customer_staging")
        
        # Step 4: Log
        duration = time.time() - start_time
        result = f"""
        Status: SUCCESS
        Rows processed: {row_count}
        Duration: {duration:.2f} seconds
        """
        
        return result.strip()
        
    except Exception as e:
        return f"Status: ERROR\nMessage: {str(e)}"
```

### Step 2: Register procedure
```python
session.sproc.register(
    transform_customers,
    return_type=T.StringType(),
    name="TRANSFORM_CUSTOMERS",
    replace=True
)
```

### Step 3: Call procedure
```python
result = session.sql("CALL TRANSFORM_CUSTOMERS()").collect()
print(result[0][0])
```

## 💡 Hints

**Hint 1**: Use @sproc decorator for procedures (vs @udf for functions)

**Hint 2**: Procedures can execute multiple queries and transformations

**Hint 3**: Use session.table() to read, .write.mode("append") to write

**Hint 4**: F.lit(), F.upper(), F.current_date() for transformations

**Hint 5**: Wrap in try/except for error handling

**Hint 6**: Use .count() to get rows processed

**Hint 7**: Return summary message as string

## 🧪 Testing

1. **Check source data**:
   ```python
   session.table("bootcamp_db.training.customers").show()
   ```

2. **Run procedure**:
   ```python
   result = session.sql("CALL TRANSFORM_CUSTOMERS()").collect()
   print(result[0][0])
   ```

3. **Verify target**:
   ```python
   session.table("customer_staging").show()
   ```

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Table not found | Use fully qualified name: bootcamp_db.training.customers |
| Write mode error | Use .write.mode("append") or "overwrite" |
| String concatenation error | Use F.lit("PREFIX_") + F.upper(col) |
| Procedure not registering | Check return_type matches function signature |
| count() returns 0 | Verify source table has data |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How to write multi-step stored procedures
- ✅ How to read and write DataFrames
- ✅ How to transform data with Snowpark functions
- ✅ Error handling in procedures
- ✅ Logging and progress tracking
- ✅ When to use procedures vs UDFs

---

**Next**: Move to [Question 4](../question-4/)!
