# Day 5: Cortex AI - Intelligent Data Processing

## Overview

**Duration**: 2.5 hours  
**Focus**: Cortex LLM, embeddings, sentiment analysis, semantic search  
**Difficulty**: ⭐⭐⭐ - ⭐⭐⭐⭐

Use Snowflake's built-in AI to process text, generate content, and build intelligent applications without external APIs.

## Learning Path

### Question 1: LLM Functions (⭐⭐⭐)
- **Time**: 30 minutes
- **Topic**: COMPLETE, SUMMARIZE, EXTRACT functions
- **Key Skills**: Cortex functions, prompt engineering, JSON parsing
- **Real-World**: Content generation, summarization, data extraction
- **Start**: [Question 1](./question-1/)

### Question 2: Embeddings & Search (⭐⭐⭐)
- **Time**: 35 minutes
- **Topic**: Vector embeddings and semantic similarity
- **Key Skills**: EMBED_TEXT_768, VECTOR_COSINE_SIMILARITY
- **Real-World**: Recommendation systems, semantic search
- **Start**: [Question 2](./question-2/)

### Question 3: Sentiment Analysis (⭐⭐⭐)
- **Time**: 30 minutes
- **Topic**: Text classification and analysis
- **Key Skills**: COMPLETE for classification, JSON parsing, aggregation
- **Real-World**: Customer feedback analysis, product intelligence
- **Start**: [Question 3](./question-3/)

### Question 4: AI-Powered Capstone (⭐⭐⭐⭐)
- **Time**: 60 minutes
- **Topic**: Complete AI analytics platform
- **Key Skills**: Integration of all Cortex functions, production system design
- **Real-World**: Building intelligent applications
- **Start**: [Question 4](./question-4/)

## Cortex Functions

### COMPLETE
Generates text based on prompt.

```sql
SNOWFLAKE.CORTEX.COMPLETE(
  'claude-3-5-sonnet',
  'Your prompt here'
)
```

### SUMMARIZE
Condenses long text.

```sql
SNOWFLAKE.CORTEX.SUMMARIZE(text)
```

### EXTRACT
Pulls structured data from unstructured text.

```sql
SNOWFLAKE.CORTEX.EXTRACT(
  'Extract sentiment keywords',
  review_text
)
```

### EMBED_TEXT_768
Converts text to 768-dimensional vector.

```sql
SNOWFLAKE.CORTEX.EMBED_TEXT_768(
  'multilingual-e5-large',
  text
)
```

## Key Concepts

### Prompt Engineering
- Clear, specific prompts get better results
- Request structured output (JSON) for parsing
- Few-shot examples improve performance

### Embeddings
- Convert text to numerical vectors
- Semantically similar texts have similar vectors
- Enable semantic search and recommendations

### Cosine Similarity
- Measures angle between vectors (0-1)
- 1.0 = identical, 0.0 = different
- Use VECTOR_COSINE_SIMILARITY()

### JSON Parsing
```sql
TRY_PARSE_JSON(response):sentiment::STRING
```

## Workflow Pattern

```sql
-- 1. Generate with COMPLETE or EXTRACT
WITH ai_analysis AS (
  SELECT id, text,
    SNOWFLAKE.CORTEX.COMPLETE(
      'claude-3-5-sonnet',
      'Analyze: ' || text
    ) as response
  FROM table
)

-- 2. Parse JSON response
SELECT id, text,
  TRY_PARSE_JSON(response):result as extracted_data
FROM ai_analysis

-- 3. Create results table
CREATE TABLE results AS [step 2 query]

-- 4. Aggregate and analyze
SELECT result, COUNT(*)
FROM results
GROUP BY result
```

## Building Systems

### Step 1: Data Enrichment
Add AI-generated columns to raw data
- Descriptions (COMPLETE)
- Sentiment (COMPLETE + JSON)
- Classifications
- Summaries (SUMMARIZE)

### Step 2: Semantic Features
Add embeddings for search
- Generate embeddings for key columns
- Store in tables for reuse
- Enable similarity-based recommendations

### Step 3: Analytics
Aggregate and analyze enriched data
- Sentiment distribution
- Confidence metrics
- Classification patterns
- Recommendations

### Step 4: Applications
Build intelligent features
- Semantic search
- Recommendations
- Filtering by sentiment
- Intelligent dashboards

## Progression

| Q | Topic | Skills | Builds On |
|---|-------|--------|-----------|
| 1 | LLM Functions | COMPLETE, SUMMARIZE, EXTRACT | SQL |
| 2 | Embeddings | EMBED_TEXT_768, similarity | Q1 |
| 3 | Sentiment | Classification, aggregation | Q1, Q2 |
| 4 | Capstone | Complete system | All 3 |

## Time Estimates

| Q | Duration | Difficulty |
|---|----------|-----------|
| 1 | 30 min   | ⭐⭐⭐   |
| 2 | 35 min   | ⭐⭐⭐   |
| 3 | 30 min   | ⭐⭐⭐   |
| 4 | 60 min   | ⭐⭐⭐⭐ |
| **Total** | **155 min** | **Advanced** |

## Common Patterns

### Sentiment Classification
```sql
WITH sentiment AS (
  SELECT id, text,
    SNOWFLAKE.CORTEX.COMPLETE(
      'claude-3-5-sonnet',
      'Classify sentiment of: "' || text || '"
       Return JSON: {"sentiment": "POS|NEG|NEUTRAL"}'
    ) as response
  FROM reviews
)
SELECT id,
  TRY_PARSE_JSON(response):sentiment as sentiment,
  TRY_PARSE_JSON(response):confidence as confidence
FROM sentiment
```

### Semantic Search
```sql
SELECT product_id, name,
  VECTOR_COSINE_SIMILARITY(
    embedding,
    SNOWFLAKE.CORTEX.EMBED_TEXT_768(
      'multilingual-e5-large',
      'search query'
    )
  ) as relevance
FROM products
ORDER BY relevance DESC
LIMIT 10
```

### Aggregation
```sql
SELECT sentiment, COUNT(*) as count,
  AVG(confidence) as avg_confidence
FROM review_sentiment
GROUP BY sentiment
ORDER BY count DESC
```

## Tips for Success

1. **Start small**: Test with LIMIT 5 first
2. **Cost awareness**: Cortex functions use tokens
3. **JSON format**: Always request structured output
4. **Error handling**: Use TRY_PARSE_JSON
5. **Cache embeddings**: Pre-compute and store vectors

## Advanced Topics

### Prompt Optimization
- Provide context for better results
- Use examples (few-shot learning)
- Ask for reasoning
- Request specific formats

### Cost Optimization
- Cache embeddings in tables
- Limit expensive operations
- Batch process when possible
- Use LIMIT for testing

### Performance
- Pre-compute expensive operations
- Store results in tables
- Use indexes on key columns
- Aggregate at query time

## Real-World Applications

✅ Customer feedback analysis  
✅ Product descriptions generation  
✅ Review summarization  
✅ Sentiment tracking by product  
✅ Recommendation systems  
✅ Content moderation  
✅ FAQ automation  
✅ Intelligent search  

## After Day 5

You can:
- Generate content with AI
- Analyze customer feedback at scale
- Build recommendation systems
- Create semantic search
- Process text intelligently

**Capstone Achievement**: Build an AI-powered product intelligence platform combining all bootcamp skills!

## Resources

- [Cortex Functions Docs](https://docs.snowflake.com/en/user-guide/ml-functions.html)
- [Embeddings Guide](https://docs.snowflake.com/en/user-guide/ml-functions-embedding.html)
- [Prompt Engineering Tips](https://platform.openai.com/docs/guides/prompt-engineering)

---

🎉 **Congratulations on completing the Cursor + Snowflake Bootcamp!**

You've mastered:
- Advanced SQL
- Python data engineering
- AI-powered analytics

**Next Steps**:
- Deploy to production
- Explore real-time pipelines
- Integrate with applications
- Specialize in your area

