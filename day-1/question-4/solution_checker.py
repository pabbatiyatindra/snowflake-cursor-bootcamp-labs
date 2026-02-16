#!/usr/bin/env python3
"""Solution checker for Day 1, Question 4: High-Spending Premium Customers"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Tuple

from dotenv import load_dotenv

load_dotenv()


def load_expected_output() -> Dict:
    """Load expected output from JSON file."""
    expected_file = Path(__file__).parent / "expected_output.json"
    with open(expected_file) as f:
        return json.load(f)


def run_validation() -> Tuple[bool, str, Dict]:
    """Run the validation check."""
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

        cursor = conn.cursor()

        query = """
        SELECT
            c.name,
            c.tier,
            SUM(o.amount) as total_spending
        FROM bootcamp_db.training.customers c
        LEFT JOIN bootcamp_db.training.orders o ON c.customer_id = o.customer_id
        WHERE c.tier = 'Premium'
        GROUP BY c.customer_id, c.name, c.tier
        HAVING SUM(o.amount) > 100
        ORDER BY total_spending DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0].upper() for desc in cursor.description]

        conn.close()

        rows = [dict(zip(columns, row)) for row in results]

        expected = load_expected_output()
        expected_rows = expected["expected_rows"]

        if len(rows) != len(expected_rows):
            return (
                False,
                f"Expected {len(expected_rows)} row(s), got {len(rows)} row(s). Remember: WHERE tier='Premium' AND HAVING SUM > 100",
                {"actual_rows": rows, "expected_rows": expected_rows},
            )

        for i, (actual, expected_row) in enumerate(zip(rows, expected_rows)):
            actual_name = actual.get("NAME", "").upper()
            actual_tier = actual.get("TIER", "").upper()
            actual_spending = float(actual.get("TOTAL_SPENDING", 0))

            expected_name = expected_row["NAME"].upper()
            expected_tier = expected_row["TIER"].upper()
            expected_spending = float(expected_row["TOTAL_SPENDING"])

            if actual_name != expected_name:
                return (
                    False,
                    f"Row {i+1}: name mismatch. Expected {expected_name}, got {actual_name}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

            if actual_tier != expected_tier:
                return (
                    False,
                    f"Row {i+1}: tier mismatch. Expected {expected_tier}, got {actual_tier}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

            if abs(actual_spending - expected_spending) > 0.01:
                return (
                    False,
                    f"Row {i+1}: spending mismatch. Expected {expected_spending}, got {actual_spending}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

        return True, "All validations passed!", {"actual_rows": rows}

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 60)
    print("Solution Validator: Day 1, Question 4")
    print("=" * 60)

    if success:
        print("\n✅ PASS - Task completed successfully!")
        print(f"\n{message}")
        print("\nActual Results:")
        print("-" * 40)
        if "actual_rows" in results:
            for i, row in enumerate(results["actual_rows"], 1):
                print(
                    f"  Row {i}: name='{row.get('NAME')}', tier='{row.get('TIER')}', spending={row.get('TOTAL_SPENDING')}"
                )
        else:
            print("  (No rows - all customers filtered out)")
        print("\n" + "=" * 60)
        print("🎉 Day 1 Complete! Ready for Day 2!\n")
        return 0
    else:
        print("\n❌ FAIL - Task not completed")
        print(f"\n{message}")

        if "expected_rows" in results:
            print("\nExpected Results:")
            print("-" * 40)
            for i, row in enumerate(results["expected_rows"], 1):
                print(
                    f"  Row {i}: name='{row['NAME']}', tier='{row['TIER']}', spending={row['TOTAL_SPENDING']}"
                )

        if "actual_rows" in results and results["actual_rows"]:
            print("\nActual Results:")
            print("-" * 40)
            for i, row in enumerate(results["actual_rows"], 1):
                print(
                    f"  Row {i}: name='{row.get('NAME')}', tier='{row.get('TIER')}', spending={row.get('TOTAL_SPENDING')}"
                )

        print("\nTroubleshooting:")
        print("-" * 40)
        print("1. Use WHERE tier = 'Premium' to filter before grouping")
        print("2. Use HAVING SUM(o.amount) > 100 to filter groups")
        print("3. Remember: WHERE filters rows, HAVING filters groups")
        print("4. Check: Should return only Alice (Premium, $225.50)")
        print("5. Order by total_spending DESC")
        print("\n" + "=" * 60 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
