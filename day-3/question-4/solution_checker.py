#!/usr/bin/env python3
"""Solution checker for Day 3, Question 4: End-to-End Pipeline"""

import os
import sys
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate end-to-end pipeline."""
    try:
        from snowflake.snowpark import Session
        import snowflake.snowpark.types as T
        import snowflake.snowpark.functions as F
        from snowflake.snowpark.window import Window

        session = Session.builder.configs({
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        }).create()

        # Pipeline execution
        raw_df = session.table("bootcamp_db.training.orders")
        total_rows = raw_df.count()

        # Validate
        valid_df = (raw_df
            .filter(raw_df.amount.isNotNull())
            .filter(raw_df.order_date <= F.current_date())
            .filter(raw_df.amount > 0)
        )
        valid_rows = valid_df.count()

        # Dedup
        w = Window.partition_by("order_id", "customer_id")
        dedup_df = (valid_df
            .withColumn("rn", F.row_number().over(w))
            .filter(F.col("rn") == 1)
            .drop("rn")
        )
        dedup_rows = dedup_df.count()

        # Load
        dedup_df.write.mode("overwrite").save_as_table("orders_clean")

        # Metrics
        invalid_rows = total_rows - valid_rows
        dup_rows = valid_rows - dedup_rows
        quality = (dedup_rows / total_rows * 100) if total_rows > 0 else 0

        session.close()

        if dedup_rows == 0:
            return False, "No rows loaded to target table", {}

        if quality < 0 or quality > 100:
            return False, f"Invalid quality score: {quality}", {}

        return (
            True,
            f"Pipeline completed successfully! {dedup_rows} rows loaded.",
            {
                "total": total_rows,
                "valid": valid_rows,
                "invalid": invalid_rows,
                "dups": dup_rows,
                "loaded": dedup_rows,
                "quality": quality
            },
        )

    except Exception as e:
        return False, f"Pipeline error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 3, Question 4 - End-to-End Pipeline")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Pipeline executed successfully!")
        print(f"\n{message}\n")
        print("Pipeline Metrics:")
        print("-" * 70)
        print(f"  Total records:    {results.get('total')}")
        print(f"  Valid records:    {results.get('valid')}")
        print(f"  Invalid records:  {results.get('invalid')}")
        print(f"  Duplicate records: {results.get('dups')}")
        print(f"  Final loaded:     {results.get('loaded')}")
        print(f"  Quality score:    {results.get('quality', 0):.1f}%")

        print("\n" + "=" * 70)
        print("🎉 Day 3 Complete! Move to Day 4!\n")
        return 0
    else:
        print("\n❌ FAIL - Pipeline validation failed")
        print(f"\n{message}\n")
        print("Troubleshooting:")
        print("-" * 70)
        print("1. Read from: bootcamp_db.training.orders")
        print("2. Validate: amount IS NOT NULL, order_date valid, amount > 0")
        print("3. Dedup with Window: partition_by('order_id', 'customer_id')")
        print("4. Write to: orders_clean table")
        print("5. Metrics: (loaded / total) * 100")
        print("6. Error handling: try/except around entire pipeline")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
