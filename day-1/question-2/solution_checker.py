#!/usr/bin/env python3
"""
Solution checker for Day 1, Question 2: Calculate Tier Percentages

Validates that the student's query correctly calculates customer percentages.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

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

        # Run the required query
        query = """
        SELECT
            tier,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bootcamp_db.training.customers), 1) as percentage
        FROM bootcamp_db.training.customers
        GROUP BY tier
        ORDER BY percentage DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0].upper() for desc in cursor.description]

        conn.close()

        # Convert to list of dicts
        rows = [dict(zip(columns, row)) for row in results]

        # Load expected
        expected = load_expected_output()
        expected_rows = expected["expected_rows"]

        # Validate
        if len(rows) != len(expected_rows):
            return (
                False,
                f"Expected {len(expected_rows)} rows, got {len(rows)} rows",
                {"actual_rows": rows, "expected_rows": expected_rows},
            )

        # Check each row (allow small rounding differences)
        for i, (actual, expected_row) in enumerate(zip(rows, expected_rows)):
            actual_tier = actual.get("TIER", "").upper()
            actual_pct = float(actual.get("PERCENTAGE", 0))

            expected_tier = expected_row["TIER"].upper()
            expected_pct = float(expected_row["PERCENTAGE"])

            if actual_tier != expected_tier:
                return (
                    False,
                    f"Row {i+1}: tier mismatch. Expected {expected_tier}, got {actual_tier}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

            # Allow 0.1 difference for rounding
            if abs(actual_pct - expected_pct) > 0.1:
                return (
                    False,
                    f"Row {i+1}: percentage mismatch. Expected {expected_pct}, got {actual_pct}",
                    {"actual_rows": rows, "expected_rows": expected_rows},
                )

        return True, "All validations passed!", {"actual_rows": rows}

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 60)
    print("Solution Validator: Day 1, Question 2")
    print("=" * 60)

    if success:
        print("\n✅ PASS - Task completed successfully!")
        print(f"\n{message}")
        print("\nActual Results:")
        print("-" * 40)
        if "actual_rows" in results:
            for i, row in enumerate(results["actual_rows"], 1):
                print(
                    f"  Row {i}: tier='{row.get('TIER')}', percentage={row.get('PERCENTAGE')}"
                )
        print("\n" + "=" * 60)
        print("🎉 Ready for Question 3!\n")
        return 0
    else:
        print("\n❌ FAIL - Task not completed")
        print(f"\n{message}")

        if "expected_rows" in results:
            print("\nExpected Results:")
            print("-" * 40)
            for i, row in enumerate(results["expected_rows"], 1):
                print(
                    f"  Row {i}: tier='{row['TIER']}', percentage={row['PERCENTAGE']}"
                )

        if "actual_rows" in results:
            print("\nActual Results:")
            print("-" * 40)
            for i, row in enumerate(results["actual_rows"], 1):
                print(
                    f"  Row {i}: tier='{row.get('TIER')}', percentage={row.get('PERCENTAGE')}"
                )

        print("\nTroubleshooting:")
        print("-" * 40)
        print("1. Use 100.0 (float) not 100 (integer) for division")
        print("2. Use ROUND(..., 1) for 1 decimal place")
        print("3. Subquery counts total: (SELECT COUNT(*) FROM customers)")
        print("4. Order by percentage DESC")
        print("\n" + "=" * 60 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
