# Question 2: Vector Embeddings & Semantic Search

**Duration**: ~35 minutes
**Skills**: Vector embeddings, semantic similarity, Cortex EMBED_TEXT_768
**Difficulty**: ⭐⭐⭐ Intermediate

## 📋 Context

Embeddings convert text to numerical vectors (768-dimensional). You can:
- Find semantically similar content
- Implement semantic search
- Cluster similar items
- Recommend related products

Example: Find reviews similar to "great quality, highly recommend"

## 🎯 Your Task

Write SQL queries to:
1. Generate embeddings for product reviews using CORTEX.EMBED_TEXT_768
2. Calculate cosine similarity between reviews
3. Find most similar reviews to a target review
4. Store embedding vectors in a table
5. Build a simple semantic search function

## 📊 Sample Data

Reviews:
```
review_id | review_text
1         | "Great quality shoes, very comfortable, highly recommend!"
2         | "Excellent product, perfect for running, amazing!"
3         | "Poor packaging, damaged on arrival, waste of money"
4         | "Fantastic item, best purchase ever, love it"
```

Expected similar reviews to #1:
- #2 (similar positive, product quality)
- #4 (similar positive sentiment)

Expected dissimilar reviews:
- #3 (negative sentiment, different topic)

## ✅ Expected Output

Embeddings table:
```
review_id | review_text | embedding (768 dimensions)
1         | [text]      | [0.123, 0.456, ..., 0.789]
2         | [text]      | [0.125, 0.450, ..., 0.790]
```

Similarity search (top 3 similar to review #1):
```
review_id | similar_review_id | similarity_score | similarity_text
1         | 2                 | 0.92             | "Excellent product..."
1         | 4                 | 0.88             | "Fantastic item..."
1         | 3                 | 0.34             | "Poor packaging..."
```

## 🔍 SQL Concepts

### EMBED_TEXT_768 Function
Converts text to 768-dimensional vector.

**Syntax**:
```sql
SELECT review_id,
  SNOWFLAKE.CORTEX.EMBED_TEXT_768(
    'multilingual-e5-large',
    review_text
  ) as embedding_vector
FROM reviews;
```

Models available:
- multilingual-e5-large: 768 dimensions, multilingual
- snowflake-arctic-embed: Domain-specific

### Cosine Similarity
Measures angle between vectors (0-1, higher = more similar).

**Formula**:
```sql
VECTOR_COSINE_SIMILARITY(embedding1, embedding2)
```

Returns value between -1 and 1 (typically 0-1 for text).

### Implementation Pattern
```sql
WITH review_embeddings AS (
  SELECT
    review_id,
    review_text,
    SNOWFLAKE.CORTEX.EMBED_TEXT_768(
      'multilingual-e5-large',
      review_text
    ) as embedding
  FROM reviews
),
similarity_scores AS (
  SELECT
    re1.review_id as source_review_id,
    re2.review_id as similar_review_id,
    re2.review_text,
    VECTOR_COSINE_SIMILARITY(re1.embedding, re2.embedding) as similarity
  FROM review_embeddings re1
  CROSS JOIN review_embeddings re2
  WHERE re1.review_id != re2.review_id
)
SELECT *
FROM similarity_scores
WHERE source_review_id = 1
ORDER BY similarity DESC
LIMIT 3;
```

## 🚀 How to Solve

### Step 1: Generate embeddings
```sql
CREATE OR REPLACE TABLE review_embeddings AS
SELECT
  review_id,
  review_text,
  SNOWFLAKE.CORTEX.EMBED_TEXT_768(
    'multilingual-e5-large',
    review_text
  ) as embedding_vector
FROM bootcamp_db.training.reviews;
```

### Step 2: Find similar reviews
```sql
WITH embeddings AS (
  SELECT * FROM review_embeddings
),
target_review AS (
  SELECT embedding_vector FROM embeddings WHERE review_id = 1
)
SELECT
  e.review_id,
  e.review_text,
  VECTOR_COSINE_SIMILARITY(
    e.embedding_vector,
    (SELECT embedding_vector FROM target_review)
  ) as similarity_score
FROM embeddings e
WHERE e.review_id != 1
ORDER BY similarity_score DESC
LIMIT 3;
```

### Step 3: Semantic search query
```sql
SELECT
  review_id,
  review_text,
  VECTOR_COSINE_SIMILARITY(
    embedding_vector,
    SNOWFLAKE.CORTEX.EMBED_TEXT_768(
      'multilingual-e5-large',
      'great product highly recommend'
    )
  ) as relevance_score
FROM review_embeddings
ORDER BY relevance_score DESC
LIMIT 5;
```

## 💡 Hints

**Hint 1**: Embeddings are expensive - cache them in a table

**Hint 2**: Use VECTOR_COSINE_SIMILARITY for comparison

**Hint 3**: Similarity scores are 0-1 for normalized embeddings

**Hint 4**: Filter review_id != target to avoid comparing with self

**Hint 5**: Pre-compute embeddings for performance

**Hint 6**: LIMIT results to save on compute

## 🧪 Testing

1. **Generate single embedding**:
   ```sql
   SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768(
     'multilingual-e5-large',
     'Hello world'
   ) as vector;
   ```

2. **Check embedding shape**:
   ```sql
   SELECT ARRAY_SIZE(embedding_vector) as vector_dimensions
   FROM review_embeddings
   LIMIT 1;
   ```

3. **Test similarity**:
   ```sql
   SELECT VECTOR_COSINE_SIMILARITY(
     (SELECT embedding_vector FROM review_embeddings WHERE review_id = 1),
     (SELECT embedding_vector FROM review_embeddings WHERE review_id = 2)
   ) as similarity;
   ```

4. **Run validator**:
   ```bash
   python3 solution_checker.py
   ```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Embedding NULL | Check review_text is not NULL, has content |
| Similarity = 1.0 | Only matches if comparing same vectors (filter != ) |
| Performance slow | Limit rows, use indexed searches |
| Wrong dimensions | Check model 'multilingual-e5-large' is correct |

## 🎓 Learning Objectives

After this question, you should understand:
- ✅ What embeddings are and how they work
- ✅ How to generate embeddings with Cortex
- ✅ Cosine similarity for semantic search
- ✅ Building recommendation systems
- ✅ Performance optimization (caching, limiting)
- ✅ Real-world applications (search, recommendations, clustering)

---

**Next**: Move to [Question 3](../question-3/)!
