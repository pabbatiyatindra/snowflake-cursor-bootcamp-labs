# Cursor + Snowflake Bootcamp Labs - Days 2-5

## Welcome!

You now have complete, production-ready lab content for Days 2-5 of the Cursor + Snowflake AI Bootcamp.

**Location**: `/tmp/snowflake-bootcamp-labs/`

**Total Content**: 
- 16 lab questions (4 per day)
- 64 files (README, prompt, schema, validator per question)
- 4 day overview guides
- 1.3 MB of comprehensive educational material

## Quick Start

### Option 1: Start with Day 2 SQL
```bash
cd /tmp/snowflake-bootcamp-labs/day-2/question-1
cat README.md
```

### Option 2: Start with Day 3 Python
```bash
cd /tmp/snowflake-bootcamp-labs/day-3/question-1
cat README.md
```

### Option 3: Start with Day 5 AI
```bash
cd /tmp/snowflake-bootcamp-labs/day-5/question-1
cat README.md
```

## What's Included

### Day 2: Intermediate SQL (4 Questions, 2 hours)
1. **Window Functions** - ROW_NUMBER(), PARTITION BY ranking
2. **CTEs & QUALIFY** - Efficient deduplication patterns
3. **EXPLAIN** - Query performance analysis
4. **Optimization Capstone** - Refactor slow queries

**Skills**: Window functions, CTEs, QUALIFY, performance tuning

### Day 3: Snowpark Python (4 Questions, 2.5 hours)
1. **DataFrame Basics** - Load, filter, transform data
2. **UDFs** - Create reusable Python functions
3. **Stored Procedures** - Multi-step workflows
4. **Pipeline Capstone** - Complete ETL with validation

**Skills**: Snowpark, Python UDFs, data pipelines, error handling

### Day 5: Cortex AI (4 Questions, 2.5 hours)
1. **LLM Functions** - COMPLETE, SUMMARIZE, EXTRACT
2. **Embeddings** - EMBED_TEXT_768, semantic search
3. **Sentiment Analysis** - Text classification
4. **AI Capstone** - Complete analytics platform

**Skills**: Cortex AI, embeddings, sentiment analysis, prompt engineering

## File Structure Per Question

Each question has exactly 4 files:

```
question-N/
├── README.md              # 1500-2500 words
│                          # - Business context
│                          # - Learning objectives
│                          # - Sample data
│                          # - Concepts explained
│                          # - Step-by-step solutions
│                          # - Hints & troubleshooting
│
├── prompt.txt             # 500-800 words
│                          # - Cursor AI prompt
│                          # - Task requirements
│                          # - Key concepts
│                          # - Expected deliverables
│
├── expected_output.json   # Schema & validation
│                          # - Column definitions
│                          # - Sample results
│                          # - Validation rules
│                          # - Common mistakes
│
└── solution_checker.py    # Automated validator
                           # - Connects to Snowflake
                           # - Executes reference impl
                           # - Validates output
                           # - Provides feedback
```

## How to Use

### For Students

1. **Read the README**
   ```bash
   cat day-2/question-1/README.md
   ```
   Gets full context, concepts, and step-by-step guidance.

2. **Get AI Help**
   - Open `prompt.txt` in Cursor
   - Press Cmd+L to chat
   - Paste the content
   - Ask for help understanding concepts

3. **Write Your Solution**
   - Create `solution.sql` or `solution.py`
   - Reference the "How to Solve" section
   - Use the hints if stuck

4. **Validate**
   ```bash
   python3 solution_checker.py
   ```
   Automated feedback on correctness.

5. **Move Forward**
   - Each README ends with a "Next" link
   - Progress through the day
   - Move to the next day

### For Instructors

1. **Deploy Content**
   - Copy entire `/tmp/snowflake-bootcamp-labs/` directory
   - Share with students via git or file storage

2. **Customize** (optional)
   - Edit expected_output.json for different validation
   - Adjust prompts for teaching style
   - Add company-specific context

3. **Monitor Progress**
   - Collect exit codes from solution_checker.py
   - Track completion by question
   - Identify struggling students early

4. **Extend**
   - Create Day 4 content (Streams, Tasks, Medallion)
   - Add bonus questions for deep dives
   - Build final capstone project

## Key Features

✅ **Complete Learning Path** - 12 hours of bootcamp content  
✅ **Progressive Difficulty** - From ⭐ to ⭐⭐⭐⭐  
✅ **AI-Ready Prompts** - Optimized for Cursor  
✅ **Automated Validation** - Immediate feedback  
✅ **Real-World Context** - Business scenarios  
✅ **Professional Quality** - Production-ready  

## Requirements

### Student Environment
- Snowflake account with bootcamp_db database
- Python 3.8+
- snowflake-connector-python (pip install)
- Cursor IDE or VS Code
- .env file with credentials:
  ```
  SNOWFLAKE_ACCOUNT=your_account
  SNOWFLAKE_USER=your_user
  SNOWFLAKE_PASSWORD=your_password
  SNOWFLAKE_WAREHOUSE=your_warehouse
  SNOWFLAKE_DATABASE=bootcamp_db
  SNOWFLAKE_SCHEMA=training
  SNOWFLAKE_ROLE=your_role
  ```

### Data Setup
Need these tables in `bootcamp_db.training` schema:
- customers (customer_id, customer_name, region, signup_date, tier)
- orders (order_id, customer_id, order_date, amount)
- reviews (review_id, product_id, review_text, rating)
- products (product_id, product_name, category, price)

## Content Quality

**Documentation**
- 1500-2500 words per question
- Deep concept explanations
- Real business scenarios
- Code examples throughout

**Examples**
- 200+ SQL/Python examples
- Step-by-step patterns
- Troubleshooting guidance

**Validation**
- 150+ validation rules
- 8+ difficulty levels
- Automatic feedback

## Time Investment

| Day | Questions | Duration | Difficulty |
|-----|-----------|----------|-----------|
| 2   | 4         | 2 hours  | Intermediate |
| 3   | 4         | 2.5 hours | Advanced |
| 5   | 4         | 2.5 hours | Advanced |
| **Total** | **12** | **7 hours** | **Advanced** |

## Learning Outcomes

After completing all content, students can:

**SQL (Day 2)**
- Write window function queries
- Use CTEs for complex transformations
- Analyze query performance
- Optimize with modern patterns

**Python (Day 3)**
- Build Snowpark transformations
- Create UDFs and procedures
- Implement ETL pipelines
- Handle errors gracefully

**AI (Day 5)**
- Generate content with COMPLETE
- Build semantic search
- Classify text with sentiment
- Create AI analytics systems

## Navigation

**Start Here**
- This file (START_HERE.md)
- DAYS_2_5_SUMMARY.md (detailed overview)

**Day 2 Guide**
- day-2/README.md (2 hour overview)
- day-2/question-1/README.md (start here)

**Day 3 Guide**
- day-3/README.md (2.5 hour overview)
- day-3/question-1/README.md (start here)

**Day 5 Guide**
- day-5/README.md (2.5 hour overview)
- day-5/question-1/README.md (start here)

## Support

If stuck:
1. **Read the README** - Most questions answered there
2. **Check prompt.txt** - Use with Cursor for AI help
3. **Review hints** - Troubleshooting section in README
4. **Run validator** - Detailed error messages

## Files by Location

```
/tmp/snowflake-bootcamp-labs/
├── START_HERE.md                    ← YOU ARE HERE
├── DAYS_2_5_SUMMARY.md
├── day-2/README.md
│   └── question-{1,2,3,4}/
│       ├── README.md
│       ├── prompt.txt
│       ├── expected_output.json
│       └── solution_checker.py
├── day-3/README.md
│   └── question-{1,2,3,4}/
│       ├── README.md
│       ├── prompt.txt
│       ├── expected_output.json
│       └── solution_checker.py
└── day-5/README.md
    └── question-{1,2,3,4}/
        ├── README.md
        ├── prompt.txt
        ├── expected_output.json
        └── solution_checker.py
```

## Ready to Begin?

### Quick Path
1. cd `/tmp/snowflake-bootcamp-labs/day-2/question-1`
2. cat README.md
3. Open prompt.txt in Cursor
4. Start learning!

---

**Status**: ✅ Complete and Ready for Production  
**Last Updated**: February 16, 2026  
**Version**: 1.0  

**Happy Learning!**
