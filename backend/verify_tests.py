"""
Quick verification that test infrastructure is working
Run: python verify_tests.py
"""
import sys
from pathlib import Path

print("🔍 Verifying Test Infrastructure...\n")

# Check directory structure
required_dirs = [
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/e2e",
    "tests/fixtures",
    "docs/testing"
]

print("📁 Checking directories...")
for dir_path in required_dirs:
    full_path = Path(dir_path)
    if full_path.exists():
        print(f"  ✅ {dir_path}")
    else:
        print(f"  ❌ {dir_path} - MISSING")

# Check key files
required_files = [
    "tests/conftest.py",
    "tests/README.md",
    "tests/unit/test_models.py",
    "tests/integration/test_auth_api.py",
    "tests/integration/test_agent_api.py",
    "tests/integration/test_websocket.py",
    "tests/fixtures/test_data.py",
    "pytest.ini",
    "requirements-test.txt",
    "docs/testing/TESTING_GUIDE.md",
    "TEST_ORGANIZATION.md"
]

print("\n📄 Checking files...")
for file_path in required_files:
    full_path = Path(file_path)
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"  ✅ {file_path} ({size} bytes)")
    else:
        print(f"  ❌ {file_path} - MISSING")

# Check imports
print("\n📦 Checking dependencies...")
try:
    import pytest # type: ignore
    print(f"  ✅ pytest {pytest.__version__}")
except ImportError:
    print("  ❌ pytest - NOT INSTALLED")

try:
    import pytest_asyncio  # type: ignore
    version = getattr(pytest_asyncio, '__version__', 'installed')
    print(f"  ✅ pytest-asyncio {version}")
except ImportError:
    print("  ❌ pytest-asyncio - NOT INSTALLED")

try:
    import httpx
    print(f"  ✅ httpx {httpx.__version__}")
except ImportError:
    print("  ❌ httpx - NOT INSTALLED")

# Check old test files
old_files = [
    "test_auth.py",
    "test_agent.py",
    "test_websocket.py",
    "test_ai_chat.py",
    "test_connection.py",
    "test_psycopg2.py"
]

print("\n📦 Old test files (to be archived)...")
for file_path in old_files:
    full_path = Path(file_path)
    if full_path.exists():
        print(f"  ⚠️  {file_path} - Still in root (run scripts/reorganize_tests.py)")

print("\n" + "="*60)
print("✅ Test infrastructure verification complete!")
print("\n📚 Next steps:")
print("  1. Create test database: CREATE DATABASE medical_test;")
print("  2. Set TEST_DATABASE_URL in .env")
print("  3. Run tests: pytest tests/unit -v")
print("  4. Archive old files: python scripts/reorganize_tests.py")
print("\n📖 Read docs/testing/TESTING_GUIDE.md for complete guide")
