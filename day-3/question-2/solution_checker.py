#!/usr/bin/env python3
"""Solution checker for Day 3, Question 2: UDF Creation"""

import os
import sys
from pathlib import Path
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate UDF creation and functionality."""
    try:
        from snowflake.snowpark import Session
        import snowflake.snowpark.types as T
        from snowflake.snowpark.functions import udf

        session = Session.builder.configs({
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        }).create()

        # Define the UDF
        @udf(return_type=T.DecimalType())
        def calculate_ltv(customer_id: int) -> float:
            result = session.sql(f"""
                SELECT SUM(amount) FROM bootcamp_db.training.orders
                WHERE customer_id = {customer_id}
            """).collect()
            
            total = float(result[0][0]) if result and result[0][0] else 0.0
            if total > 1000:
                return total * 1.2
            elif total >= 500:
                return total * 1.1
            else:
                return total

        # Register
        session.udf.register(
            calculate_ltv,
            return_type=T.DecimalType(),
            input_types=[T.IntegerType()],
            name="CALCULATE_LTV",
            replace=True
        )

        # Test
        result_df = session.sql("""
            SELECT
                c.customer_id,
                c.customer_name,
                COALESCE(SUM(o.amount), 0) as total_spend,
                CALCULATE_LTV(c.customer_id) as lifetime_value
            FROM bootcamp_db.training.customers c
            LEFT JOIN bootcamp_db.training.orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.customer_name
            ORDER BY c.customer_id
        """)

        rows = result_df.collect()
        session.close()

        if len(rows) == 0:
            return False, "No results from UDF query", {}

        # Verify tier multipliers
        for row in rows:
            total = float(row.TOTAL_SPEND)
            ltv = float(row.LIFETIME_VALUE)
            
            if total > 1000:
                expected = total * 1.2
            elif total >= 500:
                expected = total * 1.1
            else:
                expected = total
            
            # Allow small rounding differences
            if abs(ltv - expected) > 0.01:
                return (
                    False,
                    f"Customer {row.CUSTOMER_ID}: LTV {ltv} != expected {expected}",
                    {"row": row.as_dict()},
                )

        return (
            True,
            f"UDF registration and execution successful! {len(rows)} customers processed.",
            {"rows": len(rows)},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 3, Question 2 - UDF Creation")
    print("=" * 70)

    if success:
        print("\n✅ PASS - UDF registration and execution successful!")
        print(f"\n{message}\n")
        print("=" * 70)
        print("🎉 Ready for Question 3!\n")
        return 0
    else:
        print("\n❌ FAIL - UDF validation failed")
        print(f"\n{message}\n")
        print("Troubleshooting:")
        print("-" * 70)
        print("1. Use @udf(return_type=T.DecimalType()) decorator")
        print("2. Add type hints: def func(param: int) -> float")
        print("3. Use session.sql() for queries inside UDF")
        print("4. Register with: session.udf.register(..., name='CALCULATE_LTV')")
        print("5. Handle NULL results: if result and result[0][0]")
        print("6. Apply tier multipliers: >1000: 1.2x, >=500: 1.1x, else: 1.0x")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
