import re
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html_path = root / 'index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# find src and href values
patterns = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', html)

local_refs = [p for p in patterns if not p.startswith('http') and not p.startswith('//') and not p.startswith('data:')]

missing = []
for ref in local_refs:
    # strip query params and fragments
    ref_path = ref.split('?')[0].split('#')[0]
    # normalize
    ref_path = ref_path.replace('/', os.sep)
    full = root / ref_path
    if not full.exists():
        missing.append((ref, str(full)))

print('Checked', len(local_refs), 'local references.')
if missing:
    print('\nMissing files:')
    for ref, full in missing:
        print(f"- {ref} -> {full}")
    exit(2)
else:
    print('\nNo missing local assets detected.')
    exit(0)
