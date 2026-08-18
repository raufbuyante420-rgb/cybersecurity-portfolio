import re
import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html_files = [p for p in root.rglob('*.html') if 'node_modules' not in str(p)]

# Schemes that should never be treated as local file references
SKIP_SCHEMES = ('http://', 'https://', '//', 'data:', 'tel:', 'mailto:', 'ftp:', 'javascript:', '#')

missing = []
total_local_refs = 0

for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # find src and href values
    patterns = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', html)

    local_refs = [p for p in patterns if not p.startswith(SKIP_SCHEMES)]

    total_local_refs += len(local_refs)

    for ref in local_refs:
        # strip query params, fragments, and anchor-only links
        ref_path = ref.split('?')[0].split('#')[0]
        if not ref_path:
            continue
        # normalize path separators
        ref_path = ref_path.replace('/', os.sep)
        full = (html_path.parent / ref_path).resolve()
        if not full.exists():
            missing.append((str(html_path.relative_to(root)), ref, str(full)))

print(f'Checked {len(html_files)} HTML file(s) with {total_local_refs} local references.')
if missing:
    print(f'\nMissing files ({len(missing)}):')
    for page, ref, full in missing:
        print(f"- [{page}] {ref} -> {full}")
    sys.exit(2)
else:
    print('\nAll local asset references resolve correctly.')
    sys.exit(0)