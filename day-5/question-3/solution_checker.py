#!/usr/bin/env python3
"""Solution checker for Day 5, Question 3: Sentiment Analysis"""

import os
import sys
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate sentiment classification."""
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

        # Create sentiment analysis
        cursor.execute("""
        WITH sentiment_analysis AS (
          SELECT
            review_id,
            review_text,
            SNOWFLAKE.CORTEX.COMPLETE(
              'claude-3-5-sonnet',
              'Classify this review sentiment: "' || review_text || '"
               Return JSON: {"sentiment": "POSITIVE|NEGATIVE|NEUTRAL", "confidence": 0-1}'
            ) as response
          FROM bootcamp_db.training.reviews
          LIMIT 5
        )
        CREATE OR REPLACE TABLE review_sentiment AS
        SELECT
          review_id,
          review_text,
          TRY_PARSE_JSON(response):sentiment::STRING as sentiment,
          TRY_PARSE_JSON(response):confidence::FLOAT as confidence
        FROM sentiment_analysis
        """)

        # Verify results
        cursor.execute("""
        SELECT COUNT(*), 
          COUNTIF(sentiment IN ('POSITIVE', 'NEGATIVE', 'NEUTRAL'))
        FROM review_sentiment
        """)

        count, valid_count = cursor.fetchone()

        if count == 0:
            return False, "No sentiment results", {}

        if valid_count != count:
            return False, f"Invalid sentiment values found ({valid_count}/{count})", {}

        # Check confidence range
        cursor.execute("""
        SELECT COUNT(*) FROM review_sentiment
        WHERE confidence < 0 OR confidence > 1
        """)

        invalid_confidence = cursor.fetchone()[0]

        if invalid_confidence > 0:
            return False, f"{invalid_confidence} rows with invalid confidence", {}

        conn.close()

        return (
            True,
            f"Sentiment analysis completed! {count} reviews classified.",
            {"reviews_classified": count},
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 5, Question 3 - Sentiment Analysis")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Sentiment classification working!")
        print(f"\n{message}\n")
        print("=" * 70)
        print("🎉 Ready for Question 4!\n")
        return 0
    else:
        print("\n❌ FAIL - Sentiment validation failed")
        print(f"\n{message}\n")
        print("Troubleshooting:")
        print("-" * 70)
        print("1. Use SNOWFLAKE.CORTEX.COMPLETE() for classification")
        print("2. Request JSON format in prompt")
        print("3. Use TRY_PARSE_JSON(response):sentiment")
        print("4. Sentiment values: POSITIVE, NEGATIVE, NEUTRAL")
        print("5. Confidence: 0.0-1.0 float")
        print("6. Create review_sentiment table")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
