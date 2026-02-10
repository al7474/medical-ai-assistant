# Script to Reorganize Test Files
# Run this to move old test files to archive

import shutil
from pathlib import Path

# Paths
backend = Path(__file__).parent.parent  # Go up from scripts/ to backend/
archive_dir = backend / "tests" / "_archive_old_tests"

# Old test files to archive
old_test_files = [
    "test_psycopg2.py",
    "test_connection.py",
    "test_ai_chat.py",
    "quick_test.py",
]

# Create archive directory
archive_dir.mkdir(exist_ok=True)

print("📦 Archiving old test files...\n")

for filename in old_test_files:
    old_path = backend / filename
    if old_path.exists():
        new_path = archive_dir / filename
        shutil.move(str(old_path), str(new_path))
        print(f"✅ Moved: {filename} -> tests/_archive_old_tests/")
    else:
        print(f"⏭️  Skipped: {filename} (not found)")

print("\n✅ Done! Old tests archived.")
print(f"📁 Location: {archive_dir}")
print("\n💡 Legacy test files are in tests/_archive_old_tests/")
print("   New tests use pytest framework in tests/unit and tests/integration")
