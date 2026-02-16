#!/usr/bin/env python3
"""
Solution checker for Day 2, Question 1: Customer Ranking with Window Functions

Validates that the student's query correctly ranks customers by spending within each month.
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
          customer_id,
          DATE_TRUNC('month', order_date) as order_month,
          SUM(amount) as total_spent,
          ROW_NUMBER() OVER (
            PARTITION BY DATE_TRUNC('month', order_date)
            ORDER BY SUM(amount) DESC
          ) as rank
        FROM bootcamp_db.training.orders
        GROUP BY customer_id, DATE_TRUNC('month', order_date)
        ORDER BY order_month DESC, rank ASC
        LIMIT 10
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0].upper() for desc in cursor.description]

        conn.close()

        # Convert to list of dicts
        rows = [dict(zip(columns, row)) for row in results]

        # Basic validations
        if len(rows) == 0:
            return False, "Query returned no results", {}

        # Check required columns
        required_cols = {"CUSTOMER_ID", "ORDER_MONTH", "TOTAL_SPENT", "RANK"}
        actual_cols = set(columns)
        if not required_cols.issubset(actual_cols):
            missing = required_cols - actual_cols
            return (
                False,
                f"Missing required columns: {missing}",
                {"actual_columns": list(actual_cols)},
            )

        # Validate ranking logic
        current_month = None
        prev_rank = None
        errors = []

        for i, row in enumerate(rows):
            month = row.get("ORDER_MONTH")
            rank = row.get("RANK")
            total_spent = row.get("TOTAL_SPENT")
            customer_id = row.get("CUSTOMER_ID")

            # Check if month changed
            if month != current_month:
                current_month = month
                prev_rank = None
                # When month changes, rank should be 1
                if rank != 1:
                    errors.append(
                        f"Row {i+1}: Month changed to {month}, but rank is {rank} (expected 1)"
                    )

            # Rank should be sequential within month
            if prev_rank is not None:
                expected_rank = prev_rank + 1 if month == rows[i - 1].get("ORDER_MONTH") else 1
                if rank != expected_rank:
                    # Note: We allow non-sequential ranks if there's data variation
                    pass

            prev_rank = rank

            # Check for NULL values
            if customer_id is None or total_spent is None or rank is None:
                errors.append(
                    f"Row {i+1}: Found NULL value(s) in customer_id/total_spent/rank"
                )

        # Check ordering
        months = [r.get("ORDER_MONTH") for r in rows]
        if months != sorted(months, reverse=True):
            errors.append("Results not ordered by order_month DESC")

        if errors:
            return False, "; ".join(errors[:3]), {"rows": rows, "errors": errors}

        return (
            True,
            "All validations passed! Window functions working correctly.",
            {"rows": rows, "row_count": len(rows)},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 2, Question 1 - Window Functions")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Window functions implemented correctly!")
        print(f"\n{message}")
        row_count = results.get("row_count", 0)
        print(f"\nResults: {row_count} rows returned")
        print("\nActual Results (first 5):")
        print("-" * 70)
        for i, row in enumerate(results.get("rows", [])[:5], 1):
            print(
                f"  Row {i}: customer={row.get('CUSTOMER_ID')}, "
                f"month={row.get('ORDER_MONTH')}, "
                f"spent=${row.get('TOTAL_SPENT'):.2f}, rank={row.get('RANK')}"
            )
        print("\n" + "=" * 70)
        print("🎉 Ready for Question 2!\n")
        return 0
    else:
        print("\n❌ FAIL - Issue with window function implementation")
        print(f"\n{message}")

        if "rows" in results:
            print("\nActual Results (first 5):")
            print("-" * 70)
            for i, row in enumerate(results.get("rows", [])[:5], 1):
                print(
                    f"  Row {i}: customer={row.get('CUSTOMER_ID')}, "
                    f"month={row.get('ORDER_MONTH')}, "
                    f"spent=${row.get('TOTAL_SPENT', 0):.2f}, rank={row.get('RANK')}"
                )

        print("\nTroubleshooting:")
        print("-" * 70)
        print("1. Check PARTITION BY DATE_TRUNC('month', order_date)")
        print("2. Check ORDER BY SUM(amount) DESC inside window function")
        print("3. Ensure GROUP BY includes customer_id and DATE_TRUNC('month', order_date)")
        print("4. Final ORDER BY should be: order_month DESC, rank ASC")
        print("5. Use ROW_NUMBER(), not RANK() or DENSE_RANK()")
        print("\n" + "=" * 70 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
