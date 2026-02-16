#!/usr/bin/env python3
"""Solution checker for Day 5, Question 2: Vector Embeddings & Semantic Search"""

import os
import sys
from typing import Tuple, Dict
from dotenv import load_dotenv

load_dotenv()

def run_validation() -> Tuple[bool, str, Dict]:
    """Validate embedding generation and similarity search."""
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

        # Create embeddings table
        cursor.execute("""
        CREATE OR REPLACE TABLE review_embeddings AS
        SELECT
          review_id,
          review_text,
          SNOWFLAKE.CORTEX.EMBED_TEXT_768(
            'multilingual-e5-large',
            review_text
          ) as embedding_vector
        FROM bootcamp_db.training.reviews
        LIMIT 5
        """)

        # Check embeddings created
        cursor.execute("SELECT COUNT(*) FROM review_embeddings")
        count = cursor.fetchone()[0]

        if count == 0:
            return False, "No embeddings created", {}

        # Test similarity search
        cursor.execute("""
        WITH embeddings AS (
          SELECT * FROM review_embeddings
        ),
        target_review AS (
          SELECT embedding_vector FROM embeddings WHERE review_id = 1
        )
        SELECT
          e.review_id,
          VECTOR_COSINE_SIMILARITY(
            e.embedding_vector,
            (SELECT embedding_vector FROM target_review)
          ) as similarity_score
        FROM embeddings e
        WHERE e.review_id != 1
        ORDER BY similarity_score DESC
        LIMIT 3
        """)

        results = cursor.fetchall()

        conn.close()

        if len(results) == 0:
            return False, "Similarity search returned no results", {}

        # Check similarity scores are in valid range
        for row in results:
            sim_score = float(row[1])
            if not (0.0 <= sim_score <= 1.0):
                return False, f"Invalid similarity score: {sim_score}", {"scores": [r[1] for r in results]}

        return (
            True,
            f"Embeddings generated and similarity search working! {count} reviews embedded.",
            {
                "embeddings_created": count,
                "similarity_results": len(results),
                "sample_scores": [float(r[1]) for r in results[:3]]
            },
        )

    except Exception as e:
        return False, f"Validation error: {e}", {}

def print_results(success: bool, message: str, results: Dict):
    """Print formatted results."""
    print("\n" + "=" * 70)
    print("Solution Validator: Day 5, Question 2 - Embeddings & Search")
    print("=" * 70)

    if success:
        print("\n✅ PASS - Embeddings and semantic search working!")
        print(f"\n{message}\n")
        print(f"Embeddings created: {results.get('embeddings_created')}")
        print(f"Similarity results: {results.get('similarity_results')}")
        print(f"Sample scores: {results.get('sample_scores')}")

        print("\n" + "=" * 70)
        print("🎉 Ready for Question 3!\n")
        return 0
    else:
        print("\n❌ FAIL - Embeddings/similarity validation failed")
        print(f"\n{message}\n")
        print("Troubleshooting:")
        print("-" * 70)
        print("1. Use SNOWFLAKE.CORTEX.EMBED_TEXT_768('multilingual-e5-large', text)")
        print("2. Create embeddings table first")
        print("3. Use VECTOR_COSINE_SIMILARITY(vec1, vec2)")
        print("4. Check similarity scores 0.0-1.0")
        print("5. Filter where review_id != target (exclude self-comparison)")
        print("\n" + "=" * 70 + "\n")
        return 1

def main():
    success, message, results = run_validation()
    return print_results(success, message, results)

if __name__ == "__main__":
    sys.exit(main())
