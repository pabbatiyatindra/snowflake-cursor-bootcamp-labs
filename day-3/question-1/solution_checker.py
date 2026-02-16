#!/usr/bin/env python3
"""
Solution checker for Day 3, Question 1: DataFrame Basics

Validates Snowpark DataFrame transformation.
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Dict

from dotenv import load_dotenv

load_dotenv()


def run_validation() -> Tuple[bool, str, Dict]:
    """Run the validation check."""
    try:
        from snowflake.snowpark import Session
        from snowflake.snowpark.functions import year

        # Connect
        session = Session.builder.configs({
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA"),
            "role": os.getenv("SNOWFLAKE_ROLE"),
        }).create()

        # Load and transform
        customers_df = session.table("bootcamp_db.training.customers")
        
        result_df = (customers_df
            .filter(customers_df.region == "US-West")
            .select(["customer_id", "customer_name", "region", "signup_date"])
            .withColumn("signup_year", year(customers_df.signup_date))
        )

        # Collect results
        rows = result_df.collect()
        
        session.close()

        if len(rows) == 0:
            return False, "No rows returned from filtered DataFrame", {}

        if len(rows) != 2:
            return (
                False,
                f"Expected 2 US-West customers, got {len(rows)}",
                {"actual_rows": len(rows)},
            )

        # Check columns
        expected_cols = {"CUSTOMER_ID", "CUSTOMER_NAME", "REGION", "SIGNUP_DATE", "SIGNUP_YEAR"}
        row_dict = rows[0].as_dict()
        actual_cols = set(row_dict.keys())
        
        if not expected_cols.issubset(actual_cols):
            missing = expected_cols - actual_cols
            return (
                False,
                f"Missing columns: {missing}",
                {"actual_columns": list(actual_cols)},
            )

        # Verify data
        regions = set(row.REGION for row in rows)
        if regions != {"US-WEST"}:
            return (
                False,
                f"Found regions other than US-WEST: {regions}",
                {"regions": list(regions)},
            )

        signup_years = set(row.SIGNUP_YEAR for row in rows)
        if not all(y == 2023 for y in signup_years):
            return (
                False,
                f"Not all signup years are 2023: {signup_years}",
                {"years": list(signup_years)},
            )

        return (
            True,
            "DataFrame transformation successful!",
            {"rows": len(rows), "columns": list(expected_cols)},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 3, Question 1 - DataFrame Basics")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Snowpark DataFrame transformation working!")
        print(f"\n{message}")
        print(f"\nResults: {results.get('rows')} rows with columns")
        print(f"Columns: {', '.join(results.get('columns', []))}")

        print("\n" + "=" * 70)
        print("🎉 Ready for Question 2!\n")
        return 0
    else:
        print("\n❌ FAIL - DataFrame transformation failed")
        print(f"\n{message}\n")

        print("Troubleshooting:")
        print("-" * 70)
        print("1. Create Session with: Session.builder.configs({...}).create()")
        print("2. Load table with: session.table('bootcamp_db.training.customers')")
        print("3. Filter with: .filter(df.region == 'US-West')")
        print("4. Select with: .select(['customer_id', ...])")
        print("5. Add column: .withColumn('signup_year', year(df.signup_date))")
        print("6. Display: .show() or rows = .collect()")
        print("\n" + "=" * 70 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
