# Question 2: User-Defined Functions (UDFs) with Snowpark Python

**Duration**: ~35 minutes
**Skills**: UDF creation, Snowpark registration, function parameters, type hints
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

SQL functions are powerful, but sometimes you need the flexibility of Python. UDFs (User-Defined Functions) let you:
- Write logic in Python
- Register as SQL-callable functions
- Use Python libraries
- Reuse across queries

Your task: Create a Python function that calculates customer lifetime value, register it as a UDF, and use it in a query.

## 🎯 Your Task

Write a Snowpark UDF that:
1. Takes customer_id as input
2. Queries their total spend
3. Applies a business rule (tier bonus multiplier)
4. Returns calculated lifetime value
5. Register as SQL-callable function
6. Use in a SELECT query

## 📊 Sample Data

Orders table:
- Customer 1: orders = $500, $200, $300 → total = $1000
- Customer 2: orders = $100, $150 → total = $250
- Customer 3: orders = $5000 → total = $5000

Business rule:
- If total > $1000: multiply by 1.2 (platinum bonus)
- If total >= $500: multiply by 1.1 (gold bonus)
- Else: multiply by 1.0 (standard)

Expected LTV:
- Customer 1: $1000 * 1.1 = $1100
- Customer 2: $250 * 1.0 = $250
- Customer 3: $5000 * 1.2 = $6000

## ✅ Expected Output

```
customer_id | customer_name | total_spend | lifetime_value
1           | Alice         | 1000.00     | 1100.00
2           | Bob           | 250.00      | 250.00
3           | Charlie       | 5000.00     | 6000.00
```

## 🔍 Python/Snowpark Concepts

### UDF Definition
```python
from snowflake.snowpark.functions import udf
import snowflake.snowpark.types as T

@udf(return_type=T.DecimalType())
def calculate_ltv(customer_id: int) -> float:
    # Logic here
    return result
```

### Type Annotations
```python
def function_name(param1: int, param2: str) -> float:
    # parameter types: int, str, float, bool, list, dict
    # return type: what the function returns
```

### Session in UDF
UDFs have access to session context for querying:
```python
@udf(return_type=T.DecimalType())
def calculate_ltv(customer_id: int) -> float:
    # Use session to query
    result = session.sql(
        f"SELECT SUM(amount) FROM orders WHERE customer_id = {customer_id}"
    ).collect()
    
    if result and result[0][0]:
        total = float(result[0][0])
    else:
        total = 0.0
    
    # Apply business logic
    if total > 1000:
        return total * 1.2
    elif total >= 500:
        return total * 1.1
    else:
        return total
```

### Registering UDF
```python
session.udf.register(
    calculate_ltv,
    return_type=T.DecimalType(),
    input_types=[T.IntegerType()],
    name="CALCULATE_LTV"
)
```

### Using UDF in SQL
```python
result = session.sql("""
    SELECT
        customer_id,
        customer_name,
        SUM(amount) as total_spend,
        CALCULATE_LTV(customer_id) as lifetime_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
""").show()
```

## 🚀 How to Solve

### Step 1: Create the function
```python
from snowflake.snowpark.functions import udf
import snowflake.snowpark.types as T

@udf(return_type=T.DecimalType())
def calculate_ltv(customer_id: int) -> float:
    # Query total spend
    result = session.sql(f"""
        SELECT SUM(amount)
        FROM bootcamp_db.training.orders
        WHERE customer_id = {customer_id}
    """).collect()
    
    total = float(result[0][0]) if result and result[0][0] else 0.0
    
    # Apply tier multiplier
    if total > 1000:
        return total * 1.2
    elif total >= 500:
        return total * 1.1
    else:
        return total
```

### Step 2: Register the UDF
```python
session.udf.register(
    calculate_ltv,
    return_type=T.DecimalType(),
    input_types=[T.IntegerType()],
    name="CALCULATE_LTV",
    replace=True  # Overwrite if exists
)
```

### Step 3: Use in query
```python
result_df = session.sql("""
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(o.amount) as total_spend,
        CALCULATE_LTV(c.customer_id) as lifetime_value
    FROM bootcamp_db.training.customers c
    LEFT JOIN bootcamp_db.training.orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY lifetime_value DESC
""")

result_df.show()
```

## 💡 Hints

**Hint 1**: Use `@udf` decorator to mark function as UDF

**Hint 2**: Specify return_type and input_types for registration

**Hint 3**: Type hints (: int, -> float) document parameter and return types

**Hint 4**: Session context available inside UDF for queries

**Hint 5**: Use session.sql() to execute SQL from inside Python

**Hint 6**: Handle NULL results from aggregations

**Hint 7**: Use replace=True to overwrite existing UDF

## 🧪 Testing

1. **Test function locally**:
   ```python
   # Test without UDF first
   result = calculate_ltv(1)
   print(f"Customer 1 LTV: {result}")
   ```

2. **Verify registration**:
   ```python
   # Check if UDF exists in Snowflake
   session.sql("SHOW FUNCTIONS LIKE 'CALCULATE_LTV'").show()
   ```

3. **Test in SQL**:
   ```python
   # Simple query with UDF
   session.sql("SELECT CALCULATE_LTV(1) as ltv").show()
   ```

4. **Full test with joins**:
   ```python
   # Complete query
   result_df.show()
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "UDF not registered" | Call session.udf.register() before using in SQL |
| Type mismatch error | Check return_type and input_types match function signature |
| NULL handling | Always check if result[0][0] is not None before using |
| Can't query in UDF | Ensure Session is imported and available in function scope |
| SQL injection risk | Use f-strings with variables - Snowflake handles escaping |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How to write Python UDFs with type hints
- ✅ How to register UDFs with Snowflake
- ✅ How to access session context inside UDFs
- ✅ How to use UDFs in SQL queries
- ✅ When to use UDFs vs SQL functions
- ✅ Error handling and NULL value management

---

**Next**: Move to [Question 3](../question-3/)!
