# Question 3: Sentiment Analysis with Cortex

**Duration**: ~30 minutes
**Skills**: Sentiment classification, text analysis, Cortex COMPLETE
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

Classify customer reviews as positive, negative, or neutral using AI, without manual coding or ML models.

Use Cortex COMPLETE to:
- Analyze sentiment
- Extract confidence scores
- Explain reasoning
- Categorize feedback types

## 🎯 Your Task

Write SQL queries to:
1. Classify review sentiment (positive/negative/neutral)
2. Extract confidence score (0-1)
3. Extract specific reason for classification
4. Aggregate sentiment by product
5. Identify problem areas (high negative rate)

## ✅ Expected Output

Review sentiment analysis:
```
review_id | review_text | sentiment | confidence | reason
1         | [positive text] | POSITIVE | 0.95 | Strong language, clear satisfaction
2         | [negative text] | NEGATIVE | 0.88 | Complaints about quality and delivery
3         | [neutral text]  | NEUTRAL  | 0.72 | Mentions product features without emotion
```

Product sentiment summary:
```
product_id | total_reviews | positive_pct | negative_pct | avg_confidence
1          | 5             | 80%          | 20%          | 0.85
2          | 3             | 33%          | 67%          | 0.79
```

## 🔍 SQL Concepts

### Sentiment Extraction with COMPLETE
```sql
SELECT review_id, review_text,
  SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'Classify sentiment of: "' || review_text || '"
     Return JSON: {"sentiment": "POSITIVE|NEGATIVE|NEUTRAL", "confidence": 0.0-1.0, "reason": "..."}'
  ) as sentiment_analysis
FROM reviews;
```

### Parsing JSON Response
```sql
WITH sentiment_raw AS (
  SELECT
    review_id,
    SNOWFLAKE.CORTEX.COMPLETE(...) as response_json
  FROM reviews
)
SELECT
  review_id,
  TRY_PARSE_JSON(response_json):sentiment as sentiment,
  TRY_PARSE_JSON(response_json):confidence as confidence,
  TRY_PARSE_JSON(response_json):reason as reason
FROM sentiment_raw;
```

### Aggregating by Product
```sql
SELECT
  product_id,
  COUNT(*) as total_reviews,
  COUNTIF(sentiment = 'POSITIVE') * 100.0 / COUNT(*) as positive_pct,
  COUNTIF(sentiment = 'NEGATIVE') * 100.0 / COUNT(*) as negative_pct,
  AVG(confidence) as avg_confidence
FROM product_reviews_sentiment
GROUP BY product_id
ORDER BY negative_pct DESC;
```

## 🚀 How to Solve

### Step 1: Classify sentiment
```sql
WITH sentiment_analysis AS (
  SELECT
    review_id,
    review_text,
    SNOWFLAKE.CORTEX.COMPLETE(
      'claude-3-5-sonnet',
      'Analyze this review: "' || review_text || '"
       Respond with JSON: {"sentiment": "POSITIVE|NEGATIVE|NEUTRAL", "confidence": score 0-1, "reason": "brief explanation"}'
    ) as response
  FROM bootcamp_db.training.reviews
)
SELECT
  review_id,
  review_text,
  TRY_PARSE_JSON(response):sentiment as sentiment,
  TRY_PARSE_JSON(response):confidence as confidence,
  TRY_PARSE_JSON(response):reason as reason
FROM sentiment_analysis;
```

### Step 2: Store results
```sql
CREATE OR REPLACE TABLE review_sentiment AS
[Step 1 query above];
```

### Step 3: Product summary
```sql
SELECT
  r.product_id,
  COUNT(*) as total_reviews,
  COUNTIF(rs.sentiment = 'POSITIVE') * 100.0 / COUNT(*) as positive_pct,
  COUNTIF(rs.sentiment = 'NEGATIVE') * 100.0 / COUNT(*) as negative_pct,
  ROUND(AVG(rs.confidence), 2) as avg_confidence
FROM bootcamp_db.training.reviews r
JOIN review_sentiment rs ON r.review_id = rs.review_id
GROUP BY r.product_id
ORDER BY negative_pct DESC;
```

## 💡 Hints

**Hint 1**: Use COMPLETE with clear JSON format request

**Hint 2**: TRY_PARSE_JSON handles JSON errors gracefully

**Hint 3**: Confidence scores 0.5-1.0 typical (model uncertainty)

**Hint 4**: COUNTIF for conditional counting

**Hint 5**: LIMIT 10 for testing before full dataset

## 🧪 Testing

1. **Single review sentiment**:
   ```sql
   SELECT SNOWFLAKE.CORTEX.COMPLETE(
     'claude-3-5-sonnet',
     'Is this review positive or negative: "Great shoes!"'
   );
   ```

2. **Parse JSON response**:
   ```sql
   SELECT TRY_PARSE_JSON(response):sentiment
   FROM [sentiment table];
   ```

3. **Check confidence distribution**:
   ```sql
   SELECT sentiment, COUNT(*), AVG(confidence)
   FROM review_sentiment
   GROUP BY sentiment;
   ```

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ How to classify text with Cortex COMPLETE
- ✅ JSON parsing in SQL (TRY_PARSE_JSON)
- ✅ Confidence scoring and interpretation
- ✅ Aggregating sentiment results
- ✅ Identifying product issues via sentiment analysis
- ✅ Building business intelligence from text data

---

**Next**: Move to [Question 4](../question-4/)!
