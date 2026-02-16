# Snowflake + Cursor AI Bootcamp Labs

Welcome to the **5-Day Hands-On Bootcamp** for AI-powered Snowflake development!

This repository contains all lab questions, solution checkers, and AI prompts for the bootcamp. Each day has 4 hands-on questions that progressively build your skills from SQL basics to production-grade data pipelines with Cortex AI.

## 🚀 Quick Start

### 1. Clone This Repository
```bash
git clone https://github.com/pabbatiyatindra/snowflake-cursor-bootcamp-labs.git
cd snowflake-bootcamp-labs
```

### 2. Set Up Environment
```bash
# Copy environment template
cp .env.example .env.local

# Edit with your Snowflake credentials
# SNOWFLAKE_ACCOUNT=A5701997473071-MPA05784
# SNOWFLAKE_USER=<your_username>
# SNOWFLAKE_PASSWORD=<your_password>
# SNOWFLAKE_DATABASE=dm_db
# SNOWFLAKE_SCHEMA=training
# SNOWFLAKE_WAREHOUSE=mit_sandbox_wh
# SNOWFLAKE_ROLE=bootcamp_student_role
```

### 3. Validate Connection
```bash
python3 validate_connection.py
```

If successful, you'll see:
```
✅ Connected to Snowflake successfully!
✅ Database: dm_db
✅ Schema: training
✅ Role: bootcamp_student_role
```

### 4. Open in Cursor and Start Day 1
```bash
cursor .
```

## 📚 Course Structure

### Day 1: Setup + Cursor Basics + Snowflake 101
- **Q1**: Count customers by tier (GROUP BY)
- **Q2**: Calculate tier percentages (Aggregation)
- **Q3**: Join customers with orders (LEFT JOIN)
- **Q4**: Find premium customers with high spending (WHERE + HAVING)

**Skills**: Basic SQL, SELECT, GROUP BY, JOINs, aggregations

### Day 2: Intermediate SQL + AI Refactoring
- **Q1**: Window functions for customer ranking (ROW_NUMBER, RANK)
- **Q2**: CTEs and QUALIFY for deduplication
- **Q3**: Performance optimization using EXPLAIN
- **Q4**: AI-refactored query with best practices

**Skills**: Window functions, CTEs, performance optimization, AI assistance

### Day 3: Snowpark Python + Cursor IDE
- **Q1**: DataFrame API for data transformation
- **Q2**: User-Defined Functions (UDFs) in Python
- **Q3**: Stored procedures for complex logic
- **Q4**: End-to-end transformation pipeline

**Skills**: Snowpark, Python, UDFs, stored procedures

### Day 4: Modern Pipelines
- **Q1**: Change Data Capture with Streams
- **Q2**: Task orchestration for automated pipelines
- **Q3**: Dynamic Tables for auto-refresh
- **Q4**: Complete medallion architecture (bronze/silver/gold)

**Skills**: Streams, Tasks, Dynamic Tables, medallion pattern

### Day 5: Cortex AI + Capstone
- **Q1**: LLM functions for text analysis
- **Q2**: Embeddings for semantic search
- **Q3**: Sentiment analysis at scale
- **Q4**: AI-enriched capstone project

**Skills**: Cortex LLM, embeddings, AI integration, capstone project

## 📋 For Each Question

Each question directory contains:

```
day-1/question-1/
├── README.md                  # Question description and context
├── prompt.txt                 # AI prompt for Cursor (use Cmd+L)
├── solution_checker.py        # Python validator (run after completing)
└── expected_output.json       # Expected results (reference)
```

### How to Use Each Question

1. **Read** `README.md` - Understand the business context and requirements
2. **Use Cursor** - Open `prompt.txt`, copy into Cmd+L chat, implement solution
3. **Execute** - Run your SQL/Python in Snowflake or locally
4. **Validate** - Run `python3 solution_checker.py` to verify your work
5. **Move to Next** - If ✅ PASS, proceed to next question

## 🛠️ Tools & Setup

### Prerequisites
- **Cursor IDE**: Download from [cursor.sh](https://cursor.sh)
- **Snowflake Account**: Free trial at [snowflake.com/trial](https://snowflake.com/trial)
- **Python 3.9+**: For solution validators
- **Git**: For cloning this repo

### Required Python Packages
```bash
pip install -r requirements.txt
```

Includes:
- `snowflake-connector-python` - Connect to Snowflake
- `snowflake-snowpark-python` - Snowpark API for Python

### Snowflake Role & Privileges
Your bootcamp instructor will provide:
- Snowflake account credentials
- `bootcamp_student_role` with least-privilege access to:
  - `bootcamp_db.training` schema
  - `compute_wh` warehouse
  - Source and working tables

**See**: `docs/snowflake-setup.md` for detailed RBAC configuration

## 📖 Using Cursor Effectively

### Cmd+L: Chat with Claude
```
"I need to count customers by tier and calculate percentages.
Write a SQL query that returns tier name and percentage rounded to 1 decimal."
```

### Cmd+I: Inline Code Generation
```
-- Count distinct customers per region, show region and count
[Press Cmd+I - Claude completes the query]
```

### Cmd+K: Smart Refactoring
```
[Highlight slow query]
Press Cmd+K → "Optimize this using Snowflake best practices"
```

### Tab: Autocomplete
Start typing and Tab auto-completes based on context and .cursorrules

## ✅ Validation & Success Criteria

Each question provides:
- ✅ **Success criteria** in README.md
- ✅ **Solution checker** (Python script with pass/fail)
- ✅ **Expected output** (JSON for reference)

Run validator:
```bash
python3 day-1/question-1/solution_checker.py
```

Success output:
```
✅ PASS - Task completed successfully!
Result matches expected output:
  Row 1: tier='Premium', customer_count=2
  Row 2: tier='Standard', customer_count=1
```

Failure output:
```
❌ FAIL - Task not completed
Expected 2 rows, got 1 row
Check your query: [error details]
```

## 🔐 Security & Credentials

### Environment Variables
All credentials stored in `.env.local` (never committed to git):
```bash
SNOWFLAKE_ACCOUNT=xyz12345.us-east-1
SNOWFLAKE_USER=your_bootcamp_user
SNOWFLAKE_PASSWORD=your_secure_password
SNOWFLAKE_DATABASE=bootcamp_db
SNOWFLAKE_SCHEMA=training
SNOWFLAKE_WAREHOUSE=compute_wh
SNOWFLAKE_ROLE=bootcamp_student_role
```

### Never Commit
- ❌ `.env.local` - Contains passwords
- ❌ `credentials.json` - Contains secrets
- ✅ `.gitignore` already configured

### .cursorrules Configuration
The `.cursorrules` file pre-configures Cursor for Snowflake development:
- Snowflake SQL best practices
- Snowpark Python conventions
- Schema-qualified table names
- Error handling patterns

## 📞 Support & FAQ

### "I get a connection error"
Run `validate_connection.py` to diagnose:
```bash
python3 validate_connection.py
```

See `docs/troubleshooting.md` for solutions.

### "Solution checker says FAIL but I think I'm right"
1. Check the `expected_output.json` in the question directory
2. Compare your results row-by-row
3. See `README.md` in question folder for detailed success criteria

### "How do I use Cursor for this?"
1. Open the `prompt.txt` file
2. Press **Cmd+L** in Cursor
3. Copy the prompt into the chat
4. Ask follow-up questions as needed

### "I'm stuck on a question"
1. Read the `README.md` context carefully
2. Use the AI prompt in `prompt.txt` to get unstuck
3. Check `docs/sql-patterns.md` for reference solutions (patterns only, not direct answers)

## 🚀 After Bootcamp

### What You'll Have
- ✅ Production-ready Snowflake SQL & Python skills
- ✅ Experience with Cursor AI for accelerated development
- ✅ Understanding of modern data pipelines (streams, tasks, dynamic tables)
- ✅ Cortex AI integration knowledge
- ✅ A complete bootcamp portfolio project

### Next Steps
1. Apply skills to your own Snowflake projects
2. Explore [Snowflake Documentation](https://docs.snowflake.com)
3. Join [Snowflake Community](https://community.snowflake.com)
4. Get certified: [Snowflake University](https://learn.snowflake.com)

## 📝 Course Info

- **Duration**: 5 days, 20 hours
- **Format**: Hands-on labs with AI assistance
- **Level**: Intermediate (requires basic SQL knowledge)
- **Tools**: Cursor, Snowflake, Python
- **Cost**: Free (for bootcamp participants)

---

## 🤝 Contributing

Found an issue or have a suggestion?
- 📧 Email: support@snowflake-bootcamp.dev
- 🐙 GitHub Issues: [Report a bug](https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/issues)
- 💬 Discussions: [Ask a question](https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/discussions)

---

**Happy coding! 🎓**

Accelerate your Snowflake development with Cursor + Claude AI.
