#!/usr/bin/env python3
"""Solution checker for Day 3, Question 3: Stored Procedures"""

import os
import sys
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate stored procedure execution."""
    try:
        from snowflake.snowpark import Session
        import snowflake.snowpark.types as T
        from snowflake.snowpark.functions import sproc
        import snowflake.snowpark.functions as F

        session = Session.builder.configs({
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        }).create()

        # Register procedure
        @sproc(return_type=T.StringType())
        def transform_customers() -> str:
            source_df = session.table("bootcamp_db.training.customers")
            transformed_df = source_df.select(
                source_df.customer_id,
                (F.lit("PREFIX_") + F.upper(source_df.customer_name)).alias("customer_name_clean"),
                F.upper(source_df.region).alias("region_clean"),
                F.current_date().alias("transformed_date")
            )
            
            row_count = transformed_df.count()
            transformed_df.write.mode("overwrite").save_as_table("customer_staging")
            
            return f"Status: SUCCESS\nRows processed: {row_count}"

        session.sproc.register(
            transform_customers,
            return_type=T.StringType(),
            name="TRANSFORM_CUSTOMERS",
            replace=True
        )

        # Execute procedure
        result = session.sql("CALL TRANSFORM_CUSTOMERS()").collect()
        msg = result[0][0] if result else ""

        # Verify target table
        target_df = session.table("customer_staging")
        target_rows = target_df.collect()

        session.close()

        if not msg or "SUCCESS" not in msg:
            return False, f"Procedure failed: {msg}", {}

        if len(target_rows) == 0:
            return False, "Target table is empty", {}

        # Verify transformations
        for row in target_rows:
            name = str(row.CUSTOMER_NAME_CLEAN).upper()
            if not name.startswith("PREFIX_"):
                return False, f"Name not prefixed: {name}", {"row": row.as_dict()}
            
            region = str(row.REGION_CLEAN).upper()
            if region != region.upper():
                return False, f"Region not uppercase: {region}", {"row": row.as_dict()}

        return (
            True,
            f"Stored procedure executed successfully! {len(target_rows)} rows transformed.",
            {"rows": len(target_rows)},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 3, Question 3 - Stored Procedures")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Stored procedure executed successfully!")
        print(f"\n{message}\n")
        print("=" * 70)
        print("🎉 Ready for Question 4!\n")
        return 0
    else:
        print("\n❌ FAIL - Procedure validation failed")
        print(f"\n{message}\n")
        print("Troubleshooting:")
        print("-" * 70)
        print("1. Use @sproc(return_type=T.StringType()) decorator")
        print("2. Read from: bootcamp_db.training.customers")
        print("3. Add PREFIX_ to names: F.lit('PREFIX_') + F.upper(col)")
        print("4. Uppercase regions: F.upper(region)")
        print("5. Add date: F.current_date()")
        print("6. Write with: .write.mode('overwrite').save_as_table()")
        print("7. Return success message")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
