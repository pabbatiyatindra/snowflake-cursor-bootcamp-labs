# Question 4: AI-Enriched Analytics Capstone Project

**Duration**: ~60 minutes
**Skills**: Complete AI-powered analytics pipeline, integration of all Cortex functions
**Difficulty**: ⭐⭐⭐⭐ Advanced

## 📋 Context

Build a complete, production-ready analytics system that combines:
- SQL data transformation
- Cortex LLM functions (COMPLETE, SUMMARIZE, EXTRACT)
- Vector embeddings for search
- Sentiment analysis
- Business intelligence

This is your bootcamp capstone - applying everything from all 5 days!

## 🎯 Your Task

Create an end-to-end AI-powered product intelligence system:

1. **Data Ingestion**: Load raw reviews and product data
2. **AI Enrichment**: 
   - Generate product descriptions (COMPLETE)
   - Summarize reviews (SUMMARIZE)
   - Classify sentiment (COMPLETE + JSON parsing)
3. **Semantic Search**: Build embeddings for content discovery
4. **Analytics**: Compute product metrics and insights
5. **Reporting**: Create executive dashboard queries

## ✅ Expected Output

**Enriched product table**:
```
product_id | product_name | ai_description | avg_sentiment | total_reviews
1          | Running Shoes | "High-performance athletic..." | POSITIVE | 24
```

**Review intelligence**:
```
product_id | review_count | positive_pct | negative_pct | avg_confidence | main_issues
1          | 24           | 79.2%        | 20.8%        | 0.87           | "Quality, Durability, Comfort"
```

**Semantic search results** (query: "best shoes for running"):
```
product_id | product_name | relevance_score | review_summary
1          | Running Shoes | 0.94           | "Excellent for marathons, comfortable..."
```

## 🔍 System Architecture

```
Raw Data
  ↓
[Data Cleaning & Validation] ← SQL
  ↓
[AI Enrichment]
  ├─ COMPLETE: Generate descriptions
  ├─ SUMMARIZE: Condense reviews
  ├─ EXTRACT: Sentiment + keywords
  └─ EMBED_TEXT_768: Vector search
  ↓
[Analytics & Aggregation]
  ├─ Sentiment scoring by product
  ├─ Confidence metrics
  ├─ Issue identification
  └─ Performance scoring
  ↓
[Business Intelligence]
  ├─ Dashboard queries
  ├─ Trend analysis
  ├─ Recommendations
  └─ Action items
```

## 🚀 How to Solve

### Phase 1: Data Preparation
```sql
-- Clean and validate source data
WITH raw_products AS (
  SELECT * FROM bootcamp_db.training.products
  WHERE product_id IS NOT NULL
),
raw_reviews AS (
  SELECT * FROM bootcamp_db.training.reviews
  WHERE review_id IS NOT NULL AND review_text IS NOT NULL
)
SELECT * FROM raw_products;
```

### Phase 2: AI Enrichment
```sql
-- Generate descriptions
CREATE OR REPLACE TABLE product_descriptions AS
SELECT
  product_id,
  product_name,
  SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'Write a 2-3 sentence product description for: ' || product_name
  ) as ai_description
FROM bootcamp_db.training.products;

-- Classify review sentiment
CREATE OR REPLACE TABLE enriched_reviews AS
WITH sentiment_analysis AS (
  SELECT
    review_id,
    product_id,
    review_text,
    SNOWFLAKE.CORTEX.COMPLETE(
      'claude-3-5-sonnet',
      'Classify: "' || review_text || '"
       Return JSON: {"sentiment": "POSITIVE|NEGATIVE|NEUTRAL", "confidence": 0-1}'
    ) as response
  FROM bootcamp_db.training.reviews
)
SELECT
  review_id,
  product_id,
  review_text,
  TRY_PARSE_JSON(response):sentiment::STRING as sentiment,
  TRY_PARSE_JSON(response):confidence::FLOAT as confidence
FROM sentiment_analysis;

-- Generate embeddings for search
CREATE OR REPLACE TABLE review_embeddings AS
SELECT
  review_id,
  product_id,
  review_text,
  SNOWFLAKE.CORTEX.EMBED_TEXT_768(
    'multilingual-e5-large',
    review_text
  ) as embedding_vector
FROM bootcamp_db.training.reviews;
```

### Phase 3: Analytics & Aggregation
```sql
-- Product intelligence report
CREATE OR REPLACE TABLE product_intelligence AS
SELECT
  p.product_id,
  p.product_name,
  pd.ai_description,
  COUNT(er.review_id) as total_reviews,
  COUNTIF(er.sentiment = 'POSITIVE') * 100.0 / COUNT(er.review_id) as positive_pct,
  COUNTIF(er.sentiment = 'NEGATIVE') * 100.0 / COUNT(er.review_id) as negative_pct,
  ROUND(AVG(er.confidence), 2) as avg_confidence,
  CASE
    WHEN COUNTIF(er.sentiment = 'NEGATIVE') * 100.0 / COUNT(er.review_id) > 30
    THEN 'HIGH'
    WHEN COUNTIF(er.sentiment = 'NEGATIVE') * 100.0 / COUNT(er.review_id) > 15
    THEN 'MEDIUM'
    ELSE 'LOW'
  END as issue_severity
FROM bootcamp_db.training.products p
LEFT JOIN product_descriptions pd ON p.product_id = pd.product_id
LEFT JOIN enriched_reviews er ON p.product_id = er.product_id
GROUP BY p.product_id, p.product_name, pd.ai_description;
```

### Phase 4: Executive Dashboard Queries
```sql
-- Top performing products
SELECT
  product_id,
  product_name,
  total_reviews,
  positive_pct,
  issue_severity
FROM product_intelligence
ORDER BY positive_pct DESC
LIMIT 10;

-- Products needing attention
SELECT
  product_id,
  product_name,
  negative_pct,
  avg_confidence,
  issue_severity
FROM product_intelligence
WHERE issue_severity IN ('HIGH', 'MEDIUM')
ORDER BY negative_pct DESC;
```

## 💡 Implementation Strategy

**Step 1**: Start with data cleaning (SQL)
**Step 2**: Add AI enrichment one function at a time
**Step 3**: Build aggregation queries for analytics
**Step 4**: Create dashboard/reporting queries
**Step 5**: Document business insights

## 🧪 Testing

1. **Verify each phase independently**:
   ```sql
   SELECT COUNT(*) FROM product_descriptions;
   SELECT COUNT(*) FROM enriched_reviews WHERE sentiment IS NOT NULL;
   SELECT COUNT(*) FROM review_embeddings WHERE embedding_vector IS NOT NULL;
   ```

2. **Check aggregation logic**:
   ```sql
   SELECT sentiment, COUNT(*) FROM enriched_reviews GROUP BY sentiment;
   ```

3. **Run full dashboard**:
   ```sql
   SELECT * FROM product_intelligence ORDER BY positive_pct DESC;
   ```

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Phase fails partway | Test each phase independently first |
| NULL values in results | Check source data has content, use COALESCE |
| Performance slow | Use LIMIT for testing, optimize queries later |
| Sentiment parsing fails | Verify JSON format, use TRY_PARSE_JSON |
| Embeddings slow | Cache them, limit rows for testing |

## 🎓 Learning Objectives

After this capstone, you should understand:
- ✅ Complete end-to-end AI analytics pipeline
- ✅ Integrating multiple Cortex functions
- ✅ Data preparation and validation at scale
- ✅ Building production-ready systems
- ✅ Creating business value from AI
- ✅ Testing and optimization strategies

---

**🎉 Congratulations! You've completed the Cursor + Snowflake Bootcamp!**

**Next Steps**:
- Deploy this system to production
- Add real-time updates with Streams & Tasks
- Implement more complex workflows
- Explore advanced Cortex features (RAG, specialized models)

