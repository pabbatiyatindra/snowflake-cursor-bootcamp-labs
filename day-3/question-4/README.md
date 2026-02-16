# Question 4: End-to-End Pipeline with Error Handling

**Duration**: ~45 minutes
**Skills**: Complete data pipeline, error handling, data quality checks, logging
**Difficulty**: ⭐⭐⭐⭐ Advanced

## 📋 Context

Real-world pipelines need:
- Multiple data sources
- Data validation
- Error recovery
- Detailed logging
- Quality metrics

Your task: Build a complete ETL pipeline that ingests customer order data with validation and error handling.

## 🎯 Your Task

Create a Snowpark Python pipeline that:
1. Reads raw orders from source table
2. Validates data (non-null amounts, valid dates)
3. Transforms (add processing date, normalize amounts)
4. Detects duplicates
5. Loads clean data to target
6. Logs validation metrics
7. Returns success/failure summary

## 📊 Sample Data

Raw input:
```
order_id | customer_id | amount | order_date
1        | 1           | 100.00 | 2024-01-15
2        | 2           | NULL   | 2024-01-16  ← INVALID
3        | 1           | 150.00 | 2024-01-15  ← DUPLICATE
4        | 3           | 200.00 | 2024-01-17
```

Expected output:
```
Status: SUCCESS
Total rows: 4
Valid rows: 3
Invalid rows: 1
Duplicate rows: 1
Loaded rows: 2
Quality: 50% (2/4)
```

## ✅ Expected Output

```
Pipeline execution report:
- Total records read: 4
- Valid records: 3
- Invalid records: 1
- Duplicate records: 1
- Final loaded: 2
- Quality score: 50%
- Status: SUCCESS
```

## 🔍 Pipeline Concepts

### Data Validation
```python
# Check for nulls
valid_df = raw_df.filter(raw_df.amount.isNotNull())

# Check for valid dates
valid_df = valid_df.filter(raw_df.order_date <= F.current_date())

# Check for positive amounts
valid_df = valid_df.filter(raw_df.amount > 0)
```

### Duplicate Detection
```python
# Window function to find duplicates
from snowflake.snowpark.window import Window

w = Window.partition_by("order_id", "customer_id")
with_rn = df.withColumn("rn", F.row_number().over(w))
unique_df = with_rn.filter(with_rn.rn == 1)
```

### Error Handling Pattern
```python
try:
    # Validation
    valid_count = valid_df.count()
    
    # Load
    unique_df.write.mode("overwrite").save_as_table("target")
    
    return {
        "status": "SUCCESS",
        "loaded": unique_df.count()
    }
except Exception as e:
    return {
        "status": "FAILED",
        "error": str(e)
    }
```

## 🚀 How to Solve

### Step 1: Read raw data
```python
raw_df = session.table("bootcamp_db.training.orders_raw")
total_rows = raw_df.count()
```

### Step 2: Validate
```python
# Remove nulls
valid_df = raw_df.filter(raw_df.amount.isNotNull())

# Valid dates
valid_df = valid_df.filter(raw_df.order_date <= F.current_date())

# Positive amounts
valid_df = valid_df.filter(raw_df.amount > 0)

valid_count = valid_df.count()
invalid_count = total_rows - valid_count
```

### Step 3: Detect duplicates
```python
from snowflake.snowpark.window import Window

w = Window.partition_by("order_id", "customer_id")
dedup_df = valid_df.withColumn(
    "rn", F.row_number().over(w)
).filter(F.col("rn") == 1).drop("rn")

duplicate_count = valid_count - dedup_df.count()
```

### Step 4: Load
```python
dedup_df.write.mode("overwrite").save_as_table("orders_clean")
loaded_count = dedup_df.count()
```

### Step 5: Calculate metrics
```python
quality_score = (loaded_count / total_rows) * 100

summary = f"""
Pipeline Results:
- Total records: {total_rows}
- Valid records: {valid_count}
- Invalid records: {invalid_count}
- Duplicates: {duplicate_count}
- Final loaded: {loaded_count}
- Quality: {quality_score:.1f}%
- Status: SUCCESS
"""

return summary
```

## 💡 Hints

**Hint 1**: Count rows at each step for metrics

**Hint 2**: Use .filter() to remove invalid data

**Hint 3**: Window functions for duplicate detection

**Hint 4**: Wrap entire pipeline in try/except

**Hint 5**: Calculate quality metrics from counts

**Hint 6**: Log progress at each step

**Hint 7**: Return detailed summary message

## 🧪 Testing

1. **Validate step-by-step**:
   ```python
   print(f"Raw: {raw_df.count()}")
   print(f"Valid: {valid_df.count()}")
   print(f"Dedup: {dedup_df.count()}")
   ```

2. **Check target table**:
   ```python
   session.table("orders_clean").show()
   ```

3. **Verify quality metrics**:
   ```python
   quality = (final / total) * 100
   print(f"Quality: {quality}%")
   ```

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Validation too strict | Adjust filter conditions (maybe NULL is OK for some columns) |
| Duplicate detection wrong | Check PARTITION BY columns (must match your data keys) |
| Quality score incorrect | Verify counts: (final / total) * 100 |
| Pipeline fails | Add try/except and log detailed error message |
| Target table empty | Check that final filtered data is not 0 rows |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How to build complete ETL pipelines
- ✅ Data validation techniques
- ✅ Duplicate detection with window functions
- ✅ Error handling and recovery
- ✅ Quality metrics and reporting
- ✅ Production-ready pipeline patterns

---

**Next**: Move to [Day 5](../../day-5/)!
