#!/usr/bin/env python3
"""Solution checker for Day 5, Question 4: AI-Enriched Analytics Capstone"""

import os
import sys
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate capstone project completion."""
    try:
        import snowflake.connector

        conn = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
        )

        cursor = conn.cursor()

        # Check for required tables (Phase 2 & 3)
        required_tables = [
            "product_descriptions",
            "enriched_reviews",
            "product_intelligence"
        ]

        tables_found = {}
        for table in required_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                tables_found[table] = count
            except:
                tables_found[table] = 0

        # Check at least one enrichment table exists and has data
        enrichment_tables_with_data = sum(1 for v in tables_found.values() if v > 0)

        if enrichment_tables_with_data < 1:
            return (
                False,
                "No AI enrichment tables created with data",
                {"tables": tables_found},
            )

        # Check product_intelligence table
        if tables_found.get("product_intelligence", 0) > 0:
            cursor.execute("""
            SELECT
              COUNT(*) as products,
              COUNT(CASE WHEN positive_pct IS NOT NULL THEN 1 END) as with_sentiment
            FROM product_intelligence
            """)
            products, sentiment_products = cursor.fetchone()

            if sentiment_products == 0:
                return (
                    False,
                    "Product intelligence missing sentiment analysis",
                    {"products": products, "with_sentiment": sentiment_products},
                )

            conn.close()

            return (
                True,
                f"Capstone project complete! {products} products analyzed with AI enrichment.",
                {
                    "tables_created": tables_found,
                    "products_analyzed": products,
                    "ai_enrichments_applied": enrichment_tables_with_data
                },
            )
        else:
            # At least enriched_reviews or product_descriptions exists
            conn.close()

            return (
                True,
                f"AI enrichment in progress! {enrichment_tables_with_data} enrichment tables created.",
                {"tables_created": tables_found},
            )

    except Exception as e:
        return False, f"Validation error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 5, Question 4 - Capstone Project")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Capstone project implemented!")
        print(f"\n{message}\n")

        if "tables_created" in results:
            print("Tables created:")
            for table, count in results.get("tables_created", {}).items():
                if count > 0:
                    print(f"  ✓ {table}: {count} rows")

        print("\n" + "=" * 70)
        print("🎉 CONGRATULATIONS!")
        print("=" * 70)
        print("\nYou've completed the Cursor + Snowflake Bootcamp!")
        print("\nKey Accomplishments:")
        print("  • SQL: Window functions, CTEs, optimization")
        print("  • Python: Snowpark, UDFs, stored procedures")
        print("  • Pipelines: Validation, error handling, quality metrics")
        print("  • AI: Cortex LLM, embeddings, sentiment analysis")
        print("  • Systems: End-to-end analytics platform")
        print("\nNext steps:")
        print("  1. Deploy to production")
        print("  2. Add real-time updates (Streams & Tasks)")
        print("  3. Build custom dashboards")
        print("  4. Explore RAG and specialized models")
        print("\n" + "=" * 70 + "\n")
        return 0
    else:
        print("\n❌ FAIL - Capstone validation incomplete")
        print(f"\n{message}\n")

        print("To complete the capstone, you need:")
        print("-" * 70)
        print("Phase 1: Clean and validate raw data")
        print("Phase 2: Apply AI enrichment")
        print("  - COMPLETE: Generate descriptions")
        print("  - COMPLETE: Classify sentiment")
        print("  - EMBED_TEXT_768: Create embeddings")
        print("Phase 3: Build analytics aggregations")
        print("  - Sentiment percentages")
        print("  - Confidence scores")
        print("  - Issue severity classification")
        print("Phase 4: Create dashboard queries")
        print("  - Top products")
        print("  - Products needing attention")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
