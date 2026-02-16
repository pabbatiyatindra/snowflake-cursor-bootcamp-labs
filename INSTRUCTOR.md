# Bootcamp Instructor Guide

Complete guide for instructors managing the Snowflake + Cursor AI bootcamp.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Student Setup](#student-setup)
4. [Snowflake Configuration](#snowflake-configuration)
5. [Managing the Course](#managing-the-course)
6. [Troubleshooting](#troubleshooting)
7. [Customization](#customization)

---

## Quick Start

### For First-Time Instructors (5 minutes)

1. **Ensure prerequisites**:
   ```bash
   # Check you have:
   - GitHub account with repo access
   - Snowflake account (at least 2 warehouses)
   - Python 3.9+ installed locally
   ```

2. **Clone the bootcamp repo**:
   ```bash
   git clone https://github.com/pabbatiyatindra/snowflake-bootcamp-labs.git
   cd snowflake-bootcamp-labs
   ```

3. **Create Snowflake resources**:
   ```bash
   # See "Snowflake Configuration" section below
   ```

4. **Share with students**:
   - Send this link: `https://github.com/pabbatiyatindra/snowflake-bootcamp-labs`
   - Or deep link to Cursor: `cursor://vscode.git/clone?url=https://github.com/pabbatiyatindra/snowflake-bootcamp-labs.git`

---

## Architecture Overview

### Repository Structure

```
snowflake-bootcamp-labs/
├── README.md                      # Student entry point
├── INSTRUCTOR.md                  # This file
├── .cursorrules                   # Cursor IDE configuration
├── validate_connection.py         # Connection test script
├── requirements.txt               # Python dependencies
├── day-1/ through day-5/          # 5 days of labs
│   ├── setup.sql                 # SQL to create day's tables
│   ├── README.md                 # Day overview
│   └── question-1/ through question-4/
│       ├── README.md             # Question context
│       ├── prompt.txt            # AI prompt for Cursor
│       ├── solution_checker.py   # Validation script
│       └── expected_output.json  # Expected results
└── .github/workflows/
    └── deploy-labs.yml           # CI/CD validation
```

### Learning Flow

**Students follow this path**:
1. Clone repo (via Cursor deep link)
2. Run `validate_connection.py` (test credentials)
3. For each day:
   - Read `day-X/README.md` (overview)
   - For each question:
     - Read `question-Y/README.md` (context)
     - Copy `prompt.txt` into Cursor (Cmd+L)
     - Implement solution
     - Run `solution_checker.py` (validate)

**Instructors manage**:
- Snowflake credentials and roles
- Course progression and assignments
- Student progress tracking
- Support and issue resolution

---

## Student Setup

### Pre-Bootcamp Requirements

Send students this checklist 1 week before bootcamp starts:

```markdown
# Bootcamp Prerequisites

## Required (1-2 hours to set up)
- [ ] Download Cursor IDE from https://cursor.sh
- [ ] Sign up for Snowflake free trial: https://snowflake.com/trial
- [ ] Install Python 3.9+: https://python.org
- [ ] Install git: https://git-scm.com
- [ ] Clone bootcamp repo (link provided by instructor)
- [ ] Run validation script: `python3 validate_connection.py`

## Optional
- [ ] Read Snowflake docs: https://docs.snowflake.com
- [ ] Explore Cursor docs: https://cursor.com/docs
- [ ] Review SQL basics: https://w3schools.com/sql

## Sign-Off
- Show instructor `validate_connection.py` output (✅ passed)
- You're ready to start Day 1!
```

### Day 1 Kickoff (30 minutes before start)

1. **All students run setup**:
   ```bash
   cd snowflake-bootcamp-labs
   python3 validate_connection.py
   ```

   Should see:
   ```
   ✅ All checks passed!
   🎉 You're ready for the bootcamp!
   ```

2. **If setup fails**, see [Troubleshooting](#troubleshooting) section

3. **Start Day 1**:
   - Students open `day-1/README.md`
   - Instructor walks through overview (15 min)
   - Students start Question 1

---

## Snowflake Configuration

### 1. Create Database and Schema

**Run as ACCOUNTADMIN**:

```sql
-- Create bootcamp database
CREATE DATABASE bootcamp_db COMMENT = 'Snowflake + Cursor AI bootcamp';

-- Create training schema
CREATE SCHEMA bootcamp_db.training COMMENT = 'Student lab workspace';

-- Create compute warehouse
CREATE WAREHOUSE compute_wh
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = FALSE
  COMMENT = 'Bootcamp student warehouse';
```

### 2. Create Custom Role with Least Privilege

**Run as SECURITYADMIN**:

```sql
-- Create custom role
CREATE ROLE bootcamp_student_role COMMENT = 'Role for bootcamp participants';

-- Grant warehouse usage
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE bootcamp_student_role;
GRANT OPERATE ON WAREHOUSE compute_wh TO ROLE bootcamp_student_role;

-- Grant database access
GRANT USAGE ON DATABASE bootcamp_db TO ROLE bootcamp_student_role;

-- Grant schema permissions
GRANT USAGE ON SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;
GRANT CREATE TABLE ON SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;

-- Grant table permissions (present and future)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;

-- Grant view permissions
GRANT SELECT ON ALL VIEWS IN SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;

-- Grant procedure execution (for Days 3-4)
GRANT USAGE ON ALL PROCEDURES IN SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;
GRANT USAGE ON FUTURE PROCEDURES IN SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;
```

### 3. Create Student Accounts

**For each student, run as ACCOUNTADMIN**:

```sql
-- Create user account
CREATE USER bootcamp_student_001
  PASSWORD = 'TemporaryPassword123!'
  DEFAULT_WAREHOUSE = 'compute_wh'
  DEFAULT_DATABASE = 'bootcamp_db'
  DEFAULT_SCHEMA = 'training'
  DEFAULT_ROLE = 'bootcamp_student_role'
  COMMENT = 'Bootcamp participant';

-- Grant role to user
GRANT ROLE bootcamp_student_role TO USER bootcamp_student_001;

-- Set MFA (optional but recommended)
-- ALTER USER bootcamp_student_001 SET DISABLE_MFA = FALSE;
```

**Generate accounts in bulk** (optional):

```bash
#!/bin/bash
# create_accounts.sh

for i in {1..30}; do
  username="bootcamp_student_$(printf "%03d" $i)"
  echo "Creating $username..."

  snowsql -u admin -q "
    CREATE OR REPLACE USER $username
      PASSWORD = 'BootcampPassword123!'
      DEFAULT_WAREHOUSE = 'compute_wh'
      DEFAULT_DATABASE = 'bootcamp_db'
      DEFAULT_SCHEMA = 'training'
      DEFAULT_ROLE = 'bootcamp_student_role';

    GRANT ROLE bootcamp_student_role TO USER $username;
  "
done
```

### 4. Share Credentials with Students

Create a secure communication (email/Slack):

```
Welcome to the Snowflake + Cursor AI Bootcamp!

Your Snowflake credentials:
- Account: xyz12345.us-east-1
- User: bootcamp_student_001
- Password: [sent separately]
- Warehouse: compute_wh
- Database: bootcamp_db
- Schema: training
- Role: bootcamp_student_role

Setup Instructions:
1. Clone repo: https://github.com/pabbatiyatindra/snowflake-bootcamp-labs
2. Create .env.local with your credentials (template in .env.example)
3. Run: python3 validate_connection.py
4. Start: Open day-1/README.md

See you on Day 1!
```

---

## Managing the Course

### Daily Schedule

**Day 1 (2.5 hours)**
- 0:00-0:15: Overview + Setup verification
- 0:15-0:40: Question 1 + Q&A
- 0:40-1:05: Question 2 + Q&A
- 1:05-1:30: Question 3 + Q&A
- 1:30-1:55: Question 4 + Q&A
- 1:55-2:30: Review + Advanced topics

**Repeat for Days 2-5** (adjust timing based on difficulty)

### Monitoring Student Progress

**Check who's finished each question**:
```bash
# SSH into their machine and check:
ls -la day-1/
# Should see question-1 through question-4 directories with their solutions

# Or check their commits:
git log --oneline
```

**Automated progress tracking** (optional):
```python
# track_progress.py
import os
import json
from pathlib import Path

def check_completion(student_dir):
    completed = {
        'day_1': [],
        'day_2': [],
        'day_3': [],
        'day_4': [],
        'day_5': [],
    }

    for day in range(1, 6):
        for q in range(1, 5):
            checker = Path(f"{student_dir}/day-{day}/question-{q}/solution_checker.py")
            if checker.exists():
                completed[f'day_{day}'].append(q)

    return completed

# Usage:
for student in Path('/students').iterdir():
    progress = check_completion(student)
    print(f"{student.name}: {progress}")
```

### Common Issues & Quick Fixes

**Issue**: Students get "connection failed" error
```
Fix: Check credentials in .env.local match Snowflake account settings
```

**Issue**: Solution checker returns "permission denied"
```
Fix: Verify role has CREATE TABLE grant on schema
     Run: GRANT CREATE TABLE ON SCHEMA bootcamp_db.training TO ROLE bootcamp_student_role;
```

**Issue**: "Table does not exist" on Day 2
```
Fix: Confirm they ran setup.sql from day-1/ before starting day-2/
     Each day needs its own setup.sql executed first
```

**Issue**: Students can't open deep link to Cursor
```
Fix: Alternative: git clone https://...snowflake-bootcamp-labs.git
     Then: cursor .
```

---

## Troubleshooting

### Pre-Bootcamp Checklist

```bash
# Run this to verify instructor setup
python3 << 'EOF'
import os
import json
from pathlib import Path

checks = {
    'Repository cloned': Path('.').resolve().name == 'snowflake-bootcamp-labs',
    'All days present': all(Path(f'day-{i}').exists() for i in range(1, 6)),
    'All questions present': all(
        Path(f'day-{d}/question-{q}').exists()
        for d in range(1, 6) for q in range(1, 5)
    ),
    'Validator scripts present': len(list(Path('.').rglob('solution_checker.py'))) >= 16,
    'Requirements file exists': Path('requirements.txt').exists(),
    '.cursorrules exists': Path('.cursorrules').exists(),
}

for check, result in checks.items():
    symbol = '✓' if result else '❌'
    print(f"{symbol} {check}")

if all(checks.values()):
    print("\n✓ All systems ready for bootcamp!")
else:
    print("\n❌ Some checks failed. Fix above before starting.")
EOF
```

### Student Connection Issues

**Common error messages**:

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_account_name` | Wrong account ID | Check Snowflake console URL for correct account |
| `password_expired` | Password expired | Reset password in Snowflake console |
| `role_does_not_exist` | Role name typo | Verify role name in .env.local |
| `database_does_not_exist` | DB not created | Run Snowflake setup SQL above |
| `warehouse_does_not_exist` | Warehouse not created | Run `CREATE WAREHOUSE compute_wh...` |

**Debug script for students**:
```bash
# debug_connection.sh
echo "Testing Snowflake connection..."
python3 validate_connection.py

echo ""
echo "Checking file structure..."
for day in 1 2 3 4 5; do
  for q in 1 2 3 4; do
    if [ ! -f "day-$day/question-$q/solution_checker.py" ]; then
      echo "❌ Missing day-$day/question-$q/solution_checker.py"
    fi
  done
done

echo ""
echo "Checking Python packages..."
python3 -c "import snowflake.connector; import snowflake.snowpark; print('✓ Snowflake packages installed')"
```

---

## Customization

### Adjust for Your Organization

**Update branding**:
```bash
# Edit README.md, .cursorrules, prompts to use your company name
# Update resources to point to your Snowflake docs
```

**Modify difficulty levels**:
```bash
# Edit day-X/question-Y/README.md to adjust:
# - Hints (fewer for more challenge)
# - Sample data size
# - Success criteria
```

**Add prerequisites**:
```bash
# Create PREREQUISITES.md with:
# - SQL basics course
# - Python tutorials
# - Snowflake fundamentals
```

**Extend the course**:
```bash
# Add day-6, day-7, etc following the same structure:
# day-X/
#   ├── setup.sql
#   ├── README.md
#   └── question-1/ through question-4/
```

### Integration with LMS

**If using Canvas, Blackboard, etc**:

```markdown
# Bootcamp Assignment Links

## Day 1
- [Question 1](https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/tree/main/day-1/question-1)
- [Question 2](https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/tree/main/day-1/question-2)
- [Question 3](https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/tree/main/day-1/question-3)
- [Question 4](https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/tree/main/day-1/question-4)

## Day 2
[Same structure...]

Submit proof of completion: screenshot of `python3 solution_checker.py` output
```

### Create Certificates

```bash
# Generate completion certificates
python3 << 'EOF'
from datetime import datetime
from pathlib import Path

def create_certificate(student_name, completion_date):
    cert = f"""
    ═══════════════════════════════════════════════════════════════════

    CERTIFICATE OF COMPLETION

    This certifies that

    {student_name.upper()}

    has successfully completed the

    SNOWFLAKE + CURSOR AI BOOTCAMP

    5 Days, 20 Questions, Production-Grade Data Engineering

    Completed: {completion_date}

    Skills Acquired:
    ✓ Advanced SQL (Window functions, CTEs, optimization)
    ✓ Snowpark Python & UDFs
    ✓ Modern Data Pipelines (Streams, Tasks, Dynamic Tables)
    ✓ AI Integration with Cortex
    ✓ Cursor IDE Mastery

    ═══════════════════════════════════════════════════════════════════
    """
    return cert

# Usage:
print(create_certificate("Jane Doe", datetime.now().strftime("%B %d, %Y")))
EOF
```

---

## Support & Resources

### For Instructors
- GitHub Issues: https://github.com/pabbatiyatindra/snowflake-bootcamp-labs/issues
- Snowflake Docs: https://docs.snowflake.com
- Cursor Support: https://cursor.com/support

### For Students
- See README.md in repository root
- Each day's README.md has FAQ section
- Use Cursor Cmd+L to ask Claude for help

---

## Frequently Asked Questions

**Q: Can I run this bootcamp for my company?**
A: Yes! This is open source. Fork the repo and customize as needed.

**Q: What's the minimum Snowflake setup?**
A: 1 database, 1 schema, 1 SMALL warehouse. Costs ~$40 for a 30-person cohort.

**Q: How long does the bootcamp take?**
A: Officially 5 days, 20 hours. Can be compressed to 3-4 days or extended to 2 weeks.

**Q: Can students work at their own pace?**
A: Yes! Remove the daily structure and let them progress through the labs independently.

**Q: How do I provide feedback on solutions?**
A: Use GitHub Issues or Code Reviews on student pull requests.

**Q: Can I add my own labs?**
A: Yes! Follow the structure: question-Y/{README.md, prompt.txt, solution_checker.py, expected_output.json}

---

**Last Updated**: February 2026
**Version**: 1.0
**Contact**: bootcamp@snowflake.dev
