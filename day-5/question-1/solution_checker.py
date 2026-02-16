#!/usr/bin/env python3
"""Solution checker for Day 5, Question 1: Cortex LLM Functions"""

import os
import sys
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate Cortex function usage."""
    try:
        import snowflake.connector

        conn = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
        )

        cursor = conn.cursor()

        # Test COMPLETE
        cursor.execute("""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
          'claude-3-5-sonnet',
          'Write one sentence about machine learning'
        ) as result
        LIMIT 1
        """)
        complete_result = cursor.fetchone()

        # Test SUMMARIZE
        cursor.execute("""
        SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
          'Machine learning is a subset of artificial intelligence that uses statistical techniques to enable computers to learn and improve from experience.'
        ) as result
        """)
        summarize_result = cursor.fetchone()

        # Test EXTRACT
        cursor.execute("""
        SELECT SNOWFLAKE.CORTEX.EXTRACT(
          'Extract main topics as JSON array.',
          'Machine learning, AI, data science'
        ) as result
        """)
        extract_result = cursor.fetchone()

        conn.close()

        if not complete_result[0] or not summarize_result[0] or not extract_result[0]:
            return False, "One or more Cortex functions returned NULL", {}

        return (
            True,
            "Cortex LLM functions working correctly!",
            {
                "complete": bool(complete_result[0]),
                "summarize": bool(summarize_result[0]),
                "extract": bool(extract_result[0])
            },
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 5, Question 1 - Cortex LLM Functions")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Cortex functions working!")
        print(f"\n{message}\n")
        print("=" * 70)
        print("🎉 Ready for Question 2!\n")
        return 0
    else:
        print("\n❌ FAIL - Cortex function validation failed")
        print(f"\n{message}\n")
        print("Troubleshooting:")
        print("-" * 70)
        print("1. Use SNOWFLAKE.CORTEX.COMPLETE(model, prompt)")
        print("2. Model: 'claude-3-5-sonnet'")
        print("3. SUMMARIZE: SNOWFLAKE.CORTEX.SUMMARIZE(text)")
        print("4. EXTRACT: SNOWFLAKE.CORTEX.EXTRACT(prompt, text)")
        print("5. Test with LIMIT 1 first")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
