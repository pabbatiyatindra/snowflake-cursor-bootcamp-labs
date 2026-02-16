# Question 3: Query Performance Analysis with EXPLAIN

**Duration**: ~25 minutes
**Skills**: EXPLAIN command, query plan reading, performance optimization concepts
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

Your DBA noticed a slow query. Before optimizing, you need to understand HOW Snowflake executes it. The EXPLAIN command shows the execution plan - what operations run and in what order.

Understanding query plans helps you:
- Identify bottlenecks (full table scans, expensive operations)
- See if indexes/clustering would help
- Compare query plan before/after optimization

## 🎯 Your Task

Use EXPLAIN to analyze two queries:
1. A non-optimized query (full table scan)
2. An optimized query (with WHERE clause)

Compare their execution plans and identify:
- Number of operations in each plan
- Scan types (Sequential Scan vs Prune Partitions)
- Cost differences
- Why the second query is faster

## 📊 Sample Data

Using `bootcamp_db.training.orders` table with:
- 100k+ rows
- customer_id, order_date, amount
- No specific indexes (relying on Snowflake clustering)

## ✅ Expected Output

**Query 1 (Unoptimized)**:
```
EXPLAIN SELECT * FROM bootcamp_db.training.orders WHERE amount > 100;
```
Shows:
- Full sequential scan
- Higher cost estimate
- More rows processed

**Query 2 (Optimized)**:
```
EXPLAIN SELECT * FROM bootcamp_db.training.orders WHERE amount > 100 AND customer_id = 1;
```
Shows:
- Partition pruning (scans fewer blocks)
- Lower cost estimate
- More specific filtering

## 🔍 SQL Concepts

### EXPLAIN Command
Shows the query execution plan without running the query.

**Syntax**:
```sql
EXPLAIN SELECT ... FROM ...;
```

Returns:
- Operation type (TableScan, Filter, HashJoin, etc.)
- Number of rows processed
- Cost estimate (CPU, Memory, I/O)
- Scan type (Sequential, Partition Prune)

### Reading an Execution Plan

Key metrics:
- **Rows**: How many rows this operation processes
- **Cost**: Estimated execution cost (higher = slower)
- **Operation**: What Snowflake does (scan, filter, aggregate, join)
- **Scan Type**: Sequential (all data) vs Pruned (selective)

### Query Optimization Pattern

**Unoptimized**:
```sql
SELECT * FROM orders
WHERE MONTH(order_date) = 1
  AND amount > 100;
```
Problem: MONTH() on date column prevents partition pruning

**Optimized**:
```sql
SELECT * FROM orders
WHERE order_date >= '2024-01-01'
  AND order_date < '2024-02-01'
  AND amount > 100;
```
Benefit: Direct date comparison allows partition pruning

### Common Performance Issues

1. **Functions on filter columns**: `WHERE MONTH(date) = 1` scans everything
2. **Non-sargable predicates**: Conditions Snowflake can't use indexes for
3. **Implicit type conversion**: `WHERE amount = '100'` (string comparison)
4. **OR in WHERE clause**: May prevent pruning

## 🚀 How to Solve

### Step 1: Run EXPLAIN on unoptimized query
```sql
EXPLAIN SELECT
  customer_id,
  order_date,
  amount
FROM bootcamp_db.training.orders
WHERE amount > 100;
```

Observe:
- Plan shows TableScan operation
- Cost estimate
- Number of rows examined

### Step 2: Run EXPLAIN on optimized query
```sql
EXPLAIN SELECT
  customer_id,
  order_date,
  amount
FROM bootcamp_db.training.orders
WHERE amount > 100
  AND customer_id IN (1, 2, 3);
```

Observe:
- Plan shows partition pruning
- Lower cost estimate
- Fewer rows examined

### Step 3: Compare the plans
Note differences:
- Scan type (Sequential vs Pruned)
- Cost differences
- Filter pushdown effectiveness

## 💡 Hints

**Hint 1**: EXPLAIN doesn't execute the query, just shows the plan

**Hint 2**: Look for "Sequential Scan" vs "Partition Prune" in output

**Hint 3**: Lower cost estimates indicate better optimization

**Hint 4**: Adding specific filters (customer_id) can enable pruning

**Hint 5**: Avoid functions on filter columns for better pruning

## 🧪 Testing

1. **Run EXPLAIN without filters**:
   ```sql
   EXPLAIN SELECT * FROM bootcamp_db.training.orders;
   ```
   Note the high cost and rows processed.

2. **Run EXPLAIN with good filters**:
   ```sql
   EXPLAIN SELECT * FROM bootcamp_db.training.orders
   WHERE customer_id = 5
     AND order_date >= '2024-01-01';
   ```
   Note lower cost and fewer rows.

3. **Compare the output**.

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| EXPLAIN doesn't show details | Use EXPLAIN SELECT (not EXPLAIN SELECT *, more compact) |
| Can't parse plan output | Focus on "Cost" number and "Rows" - higher = slower |
| Two plans look similar | Try more selective filters (add customer_id column) |
| No "Partition Prune" shown | Using function on column prevents pruning (e.g., MONTH()) |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ What EXPLAIN does and how to read execution plans
- ✅ How to identify bottlenecks in queries
- ✅ The difference between sequential scans and partition pruning
- ✅ How to write sargable predicates for better performance
- ✅ The impact of WHERE clauses on query cost
- ✅ Why function placement matters (columns vs literals)

---

**Next**: Move to [Question 4](../question-4/)!
