#!/usr/bin/env python3
"""
Solution checker for Day 2, Question 2: Deduplication with CTEs and QUALIFY

Validates that the student correctly deduplicates orders using CTE and QUALIFY.
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
        WITH latest_orders AS (
          SELECT
            customer_id,
            order_id,
            order_date,
            amount
          FROM bootcamp_db.training.orders
          QUALIFY ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date DESC
          ) = 1
        )
        SELECT * FROM latest_orders
        ORDER BY customer_id
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0].upper() for desc in cursor.description]

        conn.close()

        # Convert to list of dicts
        rows = [dict(zip(columns, row)) for row in results]

        # Validation checks
        if len(rows) == 0:
            return False, "Query returned no results", {}

        # Check required columns
        required_cols = {"CUSTOMER_ID", "ORDER_ID", "ORDER_DATE", "AMOUNT"}
        actual_cols = set(columns)
        if not required_cols.issubset(actual_cols):
            missing = required_cols - actual_cols
            return (
                False,
                f"Missing required columns: {missing}",
                {"actual_columns": list(actual_cols)},
            )

        # Deduplication check: one row per customer
        customer_ids = [r.get("CUSTOMER_ID") for r in rows]
        unique_customers = set(customer_ids)
        
        if len(customer_ids) != len(unique_customers):
            duplicates = [cid for cid in customer_ids if customer_ids.count(cid) > 1]
            return (
                False,
                f"Deduplication failed! Found duplicate customers: {set(duplicates)}",
                {"rows": rows, "duplicate_customers": list(set(duplicates))},
            )

        # Check for NULL values
        errors = []
        for i, row in enumerate(rows):
            if row.get("CUSTOMER_ID") is None:
                errors.append(f"Row {i+1}: NULL customer_id")
            if row.get("ORDER_ID") is None:
                errors.append(f"Row {i+1}: NULL order_id")
            if row.get("ORDER_DATE") is None:
                errors.append(f"Row {i+1}: NULL order_date")

        if errors:
            return False, "; ".join(errors[:3]), {"rows": rows}

        # Verify latest dates per customer
        # Group results by customer and verify date ordering
        customer_data = {}
        for row in rows:
            cid = row.get("CUSTOMER_ID")
            order_date = row.get("ORDER_DATE")
            if cid not in customer_data:
                customer_data[cid] = order_date

        return (
            True,
            f"Deduplication successful! One row per customer, all rows contain latest orders.",
            {"rows": rows, "unique_customers": len(unique_customers), "total_rows": len(rows)},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 2, Question 2 - CTEs and QUALIFY")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Deduplication with CTE/QUALIFY working correctly!")
        print(f"\n{message}")
        
        unique_count = results.get("unique_customers", 0)
        total_count = results.get("total_rows", 0)
        print(f"\nResults: {unique_count} unique customers, {total_count} total rows")
        print("(1 row per customer = correct deduplication)")

        print("\nActual Results (first 5):")
        print("-" * 70)
        for i, row in enumerate(results.get("rows", [])[:5], 1):
            print(
                f"  Row {i}: customer={row.get('CUSTOMER_ID')}, "
                f"order_id={row.get('ORDER_ID')}, "
                f"date={row.get('ORDER_DATE')}, "
                f"amount=${row.get('AMOUNT'):.2f}"
            )

        print("\n" + "=" * 70)
        print("🎉 Ready for Question 3!\n")
        return 0
    else:
        print("\n❌ FAIL - CTE/QUALIFY deduplication not working")
        print(f"\n{message}")

        if "rows" in results:
            print("\nActual Results (first 5):")
            print("-" * 70)
            for i, row in enumerate(results.get("rows", [])[:5], 1):
                print(
                    f"  Row {i}: customer={row.get('CUSTOMER_ID')}, "
                    f"order_id={row.get('ORDER_ID')}"
                )

        print("\nTroubleshooting:")
        print("-" * 70)
        print("1. Use WITH cte_name AS (...) to define CTE")
        print("2. Use QUALIFY (not WHERE) with ROW_NUMBER()")
        print("3. Check PARTITION BY customer_id groups by customer")
        print("4. Check ORDER BY order_date DESC (newest first)")
        print("5. ROW_NUMBER() = 1 keeps first (most recent) row")
        print("6. Reference CTE in main SELECT: SELECT * FROM cte_name")
        print("7. Expected: one row per customer (deduplication)")
        print("\n" + "=" * 70 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
