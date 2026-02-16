#!/usr/bin/env python3
"""
Solution checker for Day 2, Question 3: Query Performance with EXPLAIN

Validates understanding of EXPLAIN plans and optimization concepts.
"""

import os
import sys
import json
from pathlib import Path
from typing import Tuple, Dict

from dotenv import load_dotenv

load_dotenv()


def run_validation() -> Tuple[bool, str, Dict]:
    """Run the validation check."""
    try:
        import snowflake.connector

        # Connect
        conn = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE"),
        )

        cursor = conn.cursor()

        # Run EXPLAIN on unoptimized query
        query1 = """
        EXPLAIN SELECT
          customer_id,
          order_date,
          amount
        FROM bootcamp_db.training.orders
        WHERE amount > 100
        """

        # Run EXPLAIN on optimized query
        query2 = """
        EXPLAIN SELECT
          customer_id,
          order_date,
          amount
        FROM bootcamp_db.training.orders
        WHERE amount > 100
          AND customer_id > 0
        """

        cursor.execute(query1)
        results1 = cursor.fetchall()
        
        cursor.execute(query2)
        results2 = cursor.fetchall()

        conn.close()

        # Convert results to strings for analysis
        explain1_text = "\n".join([str(row[0]) for row in results1])
        explain2_text = "\n".join([str(row[0]) for row in results2])

        # Check that both plans have content
        if not explain1_text.strip() or not explain2_text.strip():
            return (
                False,
                "One or both EXPLAIN queries returned empty results",
                {"explain1": explain1_text, "explain2": explain2_text},
            )

        # Both queries should successfully generate plans
        # The comparison is more important than exact metrics
        
        return (
            True,
            "Both EXPLAIN plans generated successfully. Analyze the differences:",
            {
                "plan1": explain1_text,
                "plan2": explain2_text,
                "note": "Query 2 may show better optimization with additional filters"
            },
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 2, Question 3 - Query EXPLAIN Analysis")
    print("=" * 70)

    if success:
        print("\n✅ PASS - EXPLAIN plans successfully generated!")
        print(f"\n{message}\n")

        print("UNOPTIMIZED QUERY PLAN:")
        print("-" * 70)
        print(results.get("plan1", "No plan")[:500])
        print("\n(... full plan may be longer ...)\n")

        print("OPTIMIZED QUERY PLAN:")
        print("-" * 70)
        print(results.get("plan2", "No plan")[:500])
        print("\n(... full plan may be longer ...)\n")

        print("ANALYSIS TODO:")
        print("-" * 70)
        print("1. Compare the total cost numbers in both plans")
        print("2. Look for 'Sequential Scan' vs 'Partition Prune' in operations")
        print("3. Count rows processed by each plan")
        print("4. Identify which query is more optimized (lower cost)")
        print("5. Note: Adding customer_id filter may help with partition pruning")

        print("\n" + "=" * 70)
        print("🎉 Ready for Question 4!\n")
        return 0
    else:
        print("\n❌ FAIL - Could not generate EXPLAIN plans")
        print(f"\n{message}\n")

        print("Troubleshooting:")
        print("-" * 70)
        print("1. Ensure Snowflake connection is active")
        print("2. Verify table bootcamp_db.training.orders exists")
        print("3. Check table has data (amount > 100 condition)")
        print("4. EXPLAIN syntax: EXPLAIN SELECT ... (no FROM is OK)")
        print("5. Make sure columns exist: customer_id, order_date, amount")
        print("\n" + "=" * 70 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
