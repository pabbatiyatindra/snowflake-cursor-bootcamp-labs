# Question 1: Cortex LLM Functions - Text Processing with AI

**Duration**: ~30 minutes
**Skills**: Cortex COMPLETE, SUMMARIZE, EXTRACT SQL functions
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

Snowflake's Cortex AI functions let you process text using Claude directly in SQL:
- COMPLETE: Generate text
- SUMMARIZE: Condense text
- EXTRACT: Pull structured data from text
- TRANSLATE: Translate text
- SENTIMENT: Classify sentiment

No APIs, no external calls - everything runs in Snowflake!

## 🎯 Your Task

Write SQL queries using Cortex functions to:
1. Use COMPLETE to generate product descriptions from names
2. Use SUMMARIZE to condense long reviews
3. Use EXTRACT to find sentiment keywords
4. Apply across multiple rows in a table
5. Store results in a new table

## 📊 Sample Data

Products table:
```
product_id | product_name
1          | Blue Running Shoes
2          | Wireless Headphones
3          | Gaming Laptop
```

Reviews table:
```
review_id | product_id | review_text
1         | 1          | "These shoes are amazing! Very comfortable, lightweight, and perfect for marathons. I've run 100+ miles in them."
2         | 2          | "Good sound quality but the battery life is disappointing. They charge too slowly."
```

## ✅ Expected Output

Product descriptions (COMPLETE):
```
product_id | product_name | description
1          | Blue Running Shoes | High-performance running footwear designed for athletes seeking comfort and speed...
```

Review summaries (SUMMARIZE):
```
review_id | original_review | summary
1         | [long text]     | Excellent running shoes, very comfortable, lightweight, ideal for marathons
```

Extracted sentiment (EXTRACT):
```
review_id | positive_keywords | negative_keywords
1         | amazing, comfortable, lightweight | (none)
2         | good | disappointing, slow
```

## 🔍 SQL Concepts

### COMPLETE Function
Generates text based on prompt.

**Syntax**:
```sql
SELECT SNOWFLAKE.CORTEX.COMPLETE(
  'claude-3-5-sonnet',
  'Write a product description for: ' || product_name
) as description
FROM products;
```

### SUMMARIZE Function
Condenses text to key points.

**Syntax**:
```sql
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
  review_text
) as summary
FROM reviews;
```

### EXTRACT Function
Pulls structured data from unstructured text.

**Syntax**:
```sql
SELECT SNOWFLAKE.CORTEX.EXTRACT(
  'Extract positive and negative keywords from this review. Return as JSON.',
  review_text
) as extracted_keywords
FROM reviews;
```

### Model Selection
Available models:
- claude-3-5-sonnet (fastest, good quality)
- claude-3-opus (best quality, slower)
- mistral-large (alternative)

### Cost Considerations
- Cortex functions charged per token (like API)
- COMPLETE/EXTRACT more expensive (longer output)
- SUMMARIZE cheaper (shorter output)
- Use filters to limit rows processed

## 🚀 How to Solve

### Step 1: Generate descriptions with COMPLETE
```sql
SELECT
  product_id,
  product_name,
  SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'Write a 1-2 sentence product description for: ' || product_name
  ) as description
FROM bootcamp_db.training.products
LIMIT 3;
```

### Step 2: Summarize reviews with SUMMARIZE
```sql
SELECT
  review_id,
  product_id,
  review_text,
  SNOWFLAKE.CORTEX.SUMMARIZE(
    review_text
  ) as summary
FROM bootcamp_db.training.reviews
LIMIT 3;
```

### Step 3: Extract keywords with EXTRACT
```sql
SELECT
  review_id,
  review_text,
  SNOWFLAKE.CORTEX.EXTRACT(
    'Extract positive keywords and negative keywords from this review. Return as JSON with keys "positive" and "negative".',
    review_text
  ) as keywords_json
FROM bootcamp_db.training.reviews
LIMIT 3;
```

### Step 4: Store results in table
```sql
CREATE OR REPLACE TABLE product_descriptions AS
SELECT
  product_id,
  product_name,
  SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'Write a 1-2 sentence product description for: ' || product_name
  ) as description
FROM bootcamp_db.training.products;
```

## 💡 Hints

**Hint 1**: Use LIMIT to test before processing large datasets

**Hint 2**: CORTEX functions are available in Snowflake - no setup needed

**Hint 3**: Always quote model names: 'claude-3-5-sonnet'

**Hint 4**: Combine || to build prompts dynamically

**Hint 5**: Results are strings - parse JSON responses if needed

**Hint 6**: Some Cortex functions may need explicit schema qualification

## 🧪 Testing

1. **Test COMPLETE**:
   ```sql
   SELECT SNOWFLAKE.CORTEX.COMPLETE(
     'claude-3-5-sonnet',
     'Hello! What is machine learning?'
   ) as response;
   ```

2. **Test SUMMARIZE**:
   ```sql
   SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
     'This is a long review with many details about the product...'
   ) as summary;
   ```

3. **Test on single row first**:
   ```sql
   SELECT
     product_id,
     product_name,
     SNOWFLAKE.CORTEX.COMPLETE(...)
   FROM products
   WHERE product_id = 1;
   ```

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Function not found" | Use fully qualified: SNOWFLAKE.CORTEX.COMPLETE() |
| Rate limit error | Add LIMIT 10, process in batches |
| Incorrect format | Check model name 'claude-3-5-sonnet' (dash, not underscore) |
| Empty results | Check input text is not null, add default: COALESCE(...) |
| JSON parsing failed | EXTRACT returns string, parse with TRY_PARSE_JSON() |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How Cortex LLM functions work in Snowflake
- ✅ When to use COMPLETE, SUMMARIZE, EXTRACT
- ✅ How to build dynamic prompts
- ✅ Cost implications of Cortex
- ✅ Practical applications (descriptions, summaries, extraction)
- ✅ How to process data at scale with AI

---

**Next**: Move to [Question 2](../question-2/)!
