#!/usr/bin/env python3
"""
Validate Snowflake connection and credentials before starting bootcamp labs.

This script tests:
1. Python packages are installed
2. Environment variables are configured
3. Can connect to Snowflake
4. Has access to bootcamp_db.training schema
5. Can create temporary tables (verify permissions)

Usage:
    python3 validate_connection.py

Success output:
    ✅ All checks passed! You're ready for the bootcamp.

Failure output:
    ❌ Check failed: [specific error]
    Fix: [suggested fix]
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Optional
import json


def check_python_packages() -> Tuple[bool, str]:
    """Check if required Python packages are installed."""
    try:
        import snowflake.connector
        from snowflake.snowpark import Session
        return True, "✅ Python packages installed"
    except ImportError as e:
        return False, f"❌ Missing packages: {e}\nFix: pip install -r requirements.txt"


def check_env_variables() -> Tuple[bool, str]:
    """Check if all required environment variables are set."""
    required_vars = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_ROLE",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        return False, (
            f"❌ Missing environment variables: {', '.join(missing)}\n"
            f"Fix: Copy .env.example to .env.local and fill in your credentials"
        )

    return True, "✅ Environment variables configured"


def test_connection() -> Tuple[bool, str]:
    """Test connection to Snowflake."""
    try:
        import snowflake.connector

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
        cursor.execute("SELECT current_database(), current_schema(), current_warehouse()")
        db, schema, warehouse = cursor.fetchone()
        conn.close()

        return True, (
            f"✅ Connected to Snowflake\n"
            f"   Database: {db}\n"
            f"   Schema: {schema}\n"
            f"   Warehouse: {warehouse}"
        )

    except Exception as e:
        return False, (
            f"❌ Connection failed: {e}\n"
            f"Fix: Check SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD\n"
            f"See: https://docs.snowflake.com/en/user-guide/admin-account-identifier.html"
        )


def test_schema_access() -> Tuple[bool, str]:
    """Test access to bootcamp_db.training schema."""
    try:
        import snowflake.connector

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
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = CURRENT_SCHEMA()"
        )
        table_count = cursor.fetchone()[0]
        conn.close()

        return True, f"✅ Can access schema (found {table_count} tables)"

    except Exception as e:
        return False, (
            f"❌ Schema access failed: {e}\n"
            f"Fix: Verify SNOWFLAKE_DATABASE and SNOWFLAKE_SCHEMA are correct"
        )


def test_permissions() -> Tuple[bool, str]:
    """Test that user has necessary permissions (CREATE TABLE, SELECT, INSERT)."""
    try:
        import snowflake.connector

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

        # Test CREATE TABLE
        cursor.execute(
            "CREATE OR REPLACE TEMPORARY TABLE bootcamp_permission_test (id INT, name VARCHAR)"
        )

        # Test INSERT
        cursor.execute("INSERT INTO bootcamp_permission_test VALUES (1, 'test')")

        # Test SELECT
        cursor.execute("SELECT * FROM bootcamp_permission_test")
        result = cursor.fetchone()

        # Clean up
        cursor.execute("DROP TABLE IF EXISTS bootcamp_permission_test")
        conn.close()

        if result and result[0] == 1 and result[1] == "TEST":  # Snowflake uppercases strings
            return True, "✅ User has required permissions (CREATE, INSERT, SELECT)"
        else:
            return False, f"❌ Unexpected result: {result}"

    except Exception as e:
        return False, (
            f"❌ Permission check failed: {e}\n"
            f"Fix: Your role may not have CREATE TABLE or INSERT permissions\n"
            f"Contact your instructor or admin"
        )


def main():
    """Run all validation checks."""
    print("🚀 Validating Snowflake Bootcamp Setup...\n")

    checks = [
        ("Python Packages", check_python_packages),
        ("Environment Variables", check_env_variables),
        ("Snowflake Connection", test_connection),
        ("Schema Access", test_schema_access),
        ("User Permissions", test_permissions),
    ]

    passed = 0
    failed = 0

    for check_name, check_func in checks:
        print(f"Checking: {check_name}...")
        success, message = check_func()

        print(f"  {message}")

        if success:
            passed += 1
        else:
            failed += 1

        print()

    # Summary
    print("=" * 60)
    if failed == 0:
        print("✅ All checks passed!")
        print("\n🎉 You're ready for the bootcamp!")
        print("\nNext steps:")
        print("1. Open Cursor: cursor .")
        print("2. Read day-1/README.md")
        print("3. Start with day-1/question-1/README.md")
        print("4. Use the prompt in prompt.txt with Cmd+L")
        print("5. Run: python3 day-1/question-1/solution_checker.py")
        return 0
    else:
        print(f"❌ {failed} check(s) failed")
        print(f"✅ {passed} check(s) passed")
        print("\nFix the errors above and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
