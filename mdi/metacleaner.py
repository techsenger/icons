# to run the script:
#   npm install -g svgo
#   python3 metacleaner.py

import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
cleaned = 0
failed = 0

for svg in sorted(root.rglob("*.svg")):
    content = svg.read_text(encoding="utf-8", errors="ignore")
    if "<metadata" not in content:
        continue
    result = subprocess.run(["svgo", svg.name, "-o", svg.name], cwd=svg.parent, capture_output=True, text=True)
    if result.returncode == 0:
        print("cleaned:", svg.relative_to(root))
        cleaned += 1
    else:
        print("FAILED :", svg.relative_to(root), result.stderr.strip(), file=sys.stderr)
        failed += 1

print(f"Done: cleaned {cleaned}, failed {failed}")
