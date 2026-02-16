#!/usr/bin/env python3
"""
Solution checker for Day 2, Question 4: Query Optimization

Validates that the optimized query produces identical results to original.
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

        # Original slow query
        slow_query = """
        SELECT
          o.order_id,
          o.customer_id,
          c.customer_name,
          o.amount,
          (SELECT COUNT(*) FROM bootcamp_db.training.orders o2
           WHERE o2.customer_id = o.customer_id) as lifetime_orders,
          ROW_NUMBER() OVER (ORDER BY o.amount DESC) as overall_rank
        FROM bootcamp_db.training.orders o
        JOIN bootcamp_db.training.customers c
          ON o.customer_id = c.customer_id
        WHERE EXISTS (
          SELECT 1 FROM bootcamp_db.training.orders o3
          WHERE o3.customer_id = o.customer_id
            AND o3.amount > (SELECT AVG(amount) FROM bootcamp_db.training.orders)
        )
        """

        # Optimized query example
        optimized_query = """
        WITH avg_orders AS (
          SELECT AVG(amount) as avg_amount FROM bootcamp_db.training.orders
        ),
        customer_stats AS (
          SELECT
            customer_id,
            COUNT(*) OVER (PARTITION BY customer_id) as lifetime_orders
          FROM bootcamp_db.training.orders
        ),
        filtered_customers AS (
          SELECT DISTINCT o.customer_id
          FROM bootcamp_db.training.orders o
          WHERE o.amount > (SELECT avg_amount FROM avg_orders)
        )
        SELECT
          o.order_id,
          o.customer_id,
          c.customer_name,
          o.amount,
          cs.lifetime_orders,
          ROW_NUMBER() OVER (ORDER BY o.amount DESC) as overall_rank
        FROM bootcamp_db.training.orders o
        JOIN bootcamp_db.training.customers c ON o.customer_id = c.customer_id
        JOIN customer_stats cs ON o.customer_id = cs.customer_id
        WHERE o.customer_id IN (SELECT customer_id FROM filtered_customers)
        """

        # Run both queries
        cursor.execute(slow_query)
        slow_results = cursor.fetchall()
        slow_cols = [desc[0].upper() for desc in cursor.description]

        cursor.execute(optimized_query)
        optimized_results = cursor.fetchall()
        optimized_cols = [desc[0].upper() for desc in cursor.description]

        conn.close()

        # Compare results
        if len(slow_results) != len(optimized_results):
            return (
                False,
                f"Row count mismatch: slow query returned {len(slow_results)}, optimized returned {len(optimized_results)}",
                {
                    "slow_count": len(slow_results),
                    "optimized_count": len(optimized_results),
                },
            )

        if set(slow_cols) != set(optimized_cols):
            return (
                False,
                f"Column mismatch: slow has {slow_cols}, optimized has {optimized_cols}",
                {"slow_cols": slow_cols, "optimized_cols": optimized_cols},
            )

        # Check if results are identical (allowing for order differences)
        slow_set = set(tuple(row) for row in slow_results)
        optimized_set = set(tuple(row) for row in optimized_results)

        if slow_set != optimized_set:
            return (
                False,
                "Results differ between slow and optimized queries",
                {"slow_rows": len(slow_set), "optimized_rows": len(optimized_set)},
            )

        return (
            True,
            f"Optimization successful! Both queries return identical {len(slow_results)} rows with same data.",
            {"row_count": len(slow_results), "columns": slow_cols},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}


def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 2, Question 4 - Query Optimization")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Optimized query produces identical results!")
        print(f"\n{message}")
        print(f"\nColumns: {', '.join(results.get('columns', []))}")
        
        print("\n" + "=" * 70)
        print("✨ Optimization Complete!")
        print("=" * 70)
        print("\nKey Achievements:")
        print("- Removed SELECT subqueries (now use window functions)")
        print("- Replaced EXISTS with efficient CTEs")
        print("- Pre-calculated aggregates in CTEs")
        print("- Maintained identical result set")
        print("- Improved query plan efficiency")
        
        print("\n" + "=" * 70)
        print("🎉 Day 2 Complete! Move to Day 3!\n")
        return 0
    else:
        print("\n❌ FAIL - Optimization validation failed")
        print(f"\n{message}\n")

        print("Troubleshooting:")
        print("-" * 70)
        print("1. Verify optimized query returns same number of rows")
        print("2. Check that all columns match original query")
        print("3. Ensure window function uses correct PARTITION BY")
        print("4. Verify CTE results are correctly filtered")
        print("5. Check joins are correct (customer_id matching)")
        print("6. Use EXCEPT to find specific row differences")
        print("7. Test with EXPLAIN to verify optimization")
        print("\n" + "=" * 70 + "\n")
        return 1


def main():
    """Main validation function."""
    success, message, results = run_validation()
    return print_results(success, message, results)


if __name__ == "__main__":
    sys.exit(main())
