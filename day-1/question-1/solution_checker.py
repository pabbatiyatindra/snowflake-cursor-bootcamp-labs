#!/usr/bin/env python3
"""
Solution checker for Day 1, Question 1: Count Customers by Tier

This script validates that the student's solution:
1. Connects to Snowflake successfully
2. Executes the required query
3. Returns the expected results

Usage:
    python3 solution_checker.py
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

# Load environment variables from .env.local if it exists
from dotenv import load_dotenv

load_dotenv()


def load_expected_output() -> Dict:
    """Load expected output from JSON file."""
    expected_file = Path(__file__).parent / "expected_output.json"
    with open(expected_file) as f:
        return json.load(f)


def check_connection() -> Tuple[bool, str]:
    """Test Snowflake connection."""
    try:
        import snowflake.connector

        conn = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE"),
        )
        conn.close()
        return True, "Connected to Snowflake"
    except Exception as e:
        return False, f"Connection failed: {e}"


def run_validation() -> Tuple[bool, str, Dict]:
    """
    Run the validation check.

    Returns:
        Tuple of (success: bool, message: str, results: Dict)
    """
    try:
        import snowflake.connector

        # Connect to Snowflake
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

        # Check if customers table exists
        cursor.execute(
            """
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = CURRENT_SCHEMA()
            AND table_name = 'CUSTOMERS'
            """
        )
        if cursor.fetchone()[0] == 0:
            return False, "customers table not found. Run setup.sql first.", {}

        # Run the required query
        query = """
        SELECT
            tier,
            COUNT(*) as customer_count
        FROM bootcamp_db.training.customers
        GROUP BY tier
        ORDER BY tier
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0].upper() for desc in cursor.description]

        conn.close()

        # Convert to list of dicts
        rows = [dict(zip(columns, row)) for row in results]

        # Load expected output
        expected = load_expected_output()
        expected_rows = expected["expected_rows"]

        # Validate results
        if len(rows) != len(expected_rows):
            return (
                False,
                f"Expected {len(expected_rows)} rows, got {len(rows)} rows",
                {"actual_rows": rows, "expected_rows": expected_rows},
            )

        # Check each row
        for i, (actual, expected_row) in enumerate(zip(rows, expected_rows)):
            actual_tier = actual.get("TIER", "").upper()
            actual_count = actual.get("CUSTOMER_COUNT", 0)

            expected_tier = expected_row["TIER"].upper()
            expected_count = expected_row["CUSTOMER_COUNT"]

            if actual_tier != expected_tier:
                return (
                    False,
                    f"Row {i+1}: tier mismatch. Expected {expected_tier}, got {actual_tier}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

            if actual_count != expected_count:
                return (
                    False,
                    f"Row {i+1}: customer_count mismatch. Expected {expected_count}, got {actual_count}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

        return True, "All validations passed!", {"actual_rows": rows}

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 60)
    print("Solution Validator: Day 1, Question 1")
    print("=" * 60)

    if success:
        print("\n✅ PASS - Task completed successfully!")
        print(f"\n{message}")
        print("\nActual Results:")
        print("-" * 40)
        if "actual_rows" in results:
            for i, row in enumerate(results["actual_rows"], 1):
                print(
                    f"  Row {i}: tier='{row.get('TIER')}', customer_count={row.get('CUSTOMER_COUNT')}"
                )
        print("\n" + "=" * 60)
        print("🎉 Ready for Question 2!\n")
        return 0
    else:
        print("\n❌ FAIL - Task not completed")
        print(f"\n{message}")

        if "expected_rows" in results:
            print("\nExpected Results:")
            print("-" * 40)
            for i, row in enumerate(results["expected_rows"], 1):
                print(
                    f"  Row {i}: tier='{row['TIER']}', customer_count={row['CUSTOMER_COUNT']}"
                )

        if "actual_rows" in results:
            print("\nActual Results:")
            print("-" * 40)
            for i, row in enumerate(results["actual_rows"], 1):
                print(
                    f"  Row {i}: tier='{row.get('TIER')}', customer_count={row.get('CUSTOMER_COUNT')}"
                )

        print("\nTroubleshooting:")
        print("-" * 40)
        print("1. Verify setup.sql was executed: SELECT COUNT(*) FROM customers;")
        print("2. Check your query uses GROUP BY tier")
        print("3. Check your query uses COUNT(*) or COUNT(1)")
        print("4. Make sure results are ordered by tier")
        print("\n" + "=" * 60 + "\n")
        return 1


def main():
    """Main validation function."""
    # Check connection first
    conn_ok, conn_msg = check_connection()
    if not conn_ok:
        print(f"\n❌ Connection check failed: {conn_msg}")
        print("Fix your environment variables and try again.")
        print(f"See ../.env.example for template")
        return 1

    # Run validation
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
