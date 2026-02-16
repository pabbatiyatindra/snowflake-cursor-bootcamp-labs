# Question 1: DataFrame Basics - Customer Data Transformation

**Duration**: ~30 minutes
**Skills**: Snowpark DataFrames, SELECT, filter(), select(), show()
**Difficulty**: ⭐⭐ Easy-Intermediate

## 📋 Context

You've been writing SQL your entire bootcamp. Now it's time for Python! Snowpark DataFrames are like Pandas DataFrames but execute in Snowflake.

Key advantage: Write Python, execute in Snowflake (scalable, no data transfer).

Your task: Transform customer data using Snowpark Python instead of SQL.

## 🎯 Your Task

Write Python code that:
1. Creates a Snowpark Session
2. Loads customers table into a DataFrame
3. Filters to customers in a specific region
4. Selects specific columns
5. Adds a new calculated column
6. Shows the results

## 📊 Sample Data

`bootcamp_db.training.customers` table:
```
customer_id | customer_name | region   | signup_date
1           | Alice         | US-West  | 2023-01-15
2           | Bob           | US-East  | 2023-02-20
3           | Charlie       | EU-West  | 2023-01-10
4           | Diana         | US-West  | 2023-03-05
5           | Eve           | APAC     | 2023-02-28
```

## ✅ Expected Output

```
CUSTOMER_ID | CUSTOMER_NAME | REGION  | SIGNUP_DATE | SIGNUP_YEAR
1           | Alice         | US-West | 2023-01-15  | 2023
4           | Diana         | US-West | 2023-03-05  | 2023
```

## 🔍 Python/Snowpark Concepts

### Session - Your Connection to Snowflake
```python
from snowflake.snowpark import Session

session = Session.builder.configs(connection_params).create()
```
- `session` is your gateway to Snowflake
- Use it to load data, execute queries, etc.

### DataFrame - Python representation of Snowflake table
```python
df = session.table("bootcamp_db.training.customers")
```
- Not loaded into memory yet (lazy evaluation)
- Executes in Snowflake when you call `.show()` or `.collect()`

### filter() - WHERE clause
```python
df_filtered = df.filter(df.region == "US-West")
```
- Logical operators: `==`, `!=`, `>`, `<`, `&`, `|`

### select() - Choose columns
```python
df_selected = df.select(["customer_id", "customer_name", "region"])
# or
df_selected = df.select(df.customer_id, df.customer_name, df.region)
```

### withColumn() - Add calculated column
```python
from snowflake.snowpark.functions import year

df_with_year = df.withColumn("signup_year", year(df.signup_date))
```

### Method Chaining
```python
result = (df
  .filter(df.region == "US-West")
  .select(["customer_id", "customer_name", "region", "signup_date"])
  .withColumn("signup_year", year(df.signup_date))
)
```

### show() - Display results
```python
result.show()  # Executes and displays
```

### collect() - Get as list of Row objects
```python
rows = result.collect()
for row in rows:
    print(row["customer_id"], row["customer_name"])
```

## 🚀 How to Solve

### Step 1: Set up Session
```python
from snowflake.snowpark import Session

connection_params = {
    "account": "your_account",
    "user": "your_user",
    "password": "your_password",
    "warehouse": "your_warehouse",
    "database": "bootcamp_db",
    "schema": "training"
}

session = Session.builder.configs(connection_params).create()
```

### Step 2: Load DataFrame
```python
customers_df = session.table("customers")
# or fully qualified:
customers_df = session.table("bootcamp_db.training.customers")
```

### Step 3: Filter
```python
us_west_df = customers_df.filter(customers_df.region == "US-West")
```

### Step 4: Select columns
```python
selected_df = us_west_df.select([
    "customer_id",
    "customer_name", 
    "region",
    "signup_date"
])
```

### Step 5: Add calculated column
```python
from snowflake.snowpark.functions import year

result_df = selected_df.withColumn(
    "signup_year",
    year(selected_df.signup_date)
)
```

### Step 6: Display
```python
result_df.show()
# or
result_df.select("*").show()
```

## 💡 Hints

**Hint 1**: Use `session.table()` to load a table

**Hint 2**: Column names are case-insensitive in Snowflake

**Hint 3**: Use `df.column_name` to reference columns in filters

**Hint 4**: Chain operations with `.method()` syntax

**Hint 5**: Import functions from `snowflake.snowpark.functions`

**Hint 6**: `.show()` executes the query; `.collect()` gets results as list

## 🧪 Testing

1. **Load and show all data**:
   ```python
   customers_df = session.table("customers")
   customers_df.show()
   ```

2. **Test filter**:
   ```python
   us_west_df = customers_df.filter(customers_df.region == "US-West")
   print(f"Found {us_west_df.count()} US-West customers")
   ```

3. **Test with year extraction**:
   ```python
   from snowflake.snowpark.functions import year
   df_with_year = customers_df.withColumn("signup_year", year(customers_df.signup_date))
   df_with_year.show()
   ```

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Session not created" | Check connection params (account, user, password) |
| "Table not found" | Use fully qualified name: bootcamp_db.training.customers |
| Column not found error | Check column names in table (case-insensitive in Snowflake) |
| ".filter() not working" | Use `df.column_name` not string, use `==` not `=` |
| Results not showing | Call `.show()` or `.collect()` - DataFrames are lazy |
| Import errors | Ensure snowflake-snowpark-python installed |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ What Snowpark DataFrames are and how they work
- ✅ How to create a Session and connect to Snowflake
- ✅ How to load tables into DataFrames
- ✅ How to filter, select, and transform data with Snowpark
- ✅ Lazy evaluation (queries don't run until `.show()` or `.collect()`)
- ✅ How to add calculated columns with `withColumn()`

---

**Next**: Move to [Question 2](../question-2/)!
