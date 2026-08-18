import re
import os
import sys
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
issues = []

# 1. HTML well-formedness checks (basic tag matching)
html_files = [p for p in root.rglob('*.html') if 'node_modules' not in str(p)]
for f in html_files:
    content = f.read_text(encoding='utf-8')
    rel = f.relative_to(root)
    # Check DOCTYPE
    if '<!DOCTYPE html>' not in content:
        issues.append(f'{rel}: Missing DOCTYPE')
    # Check basic paired tags
    for tag in ['html', 'head', 'body', 'header', 'section', 'div', 'nav', 'main', 'footer', 'ul', 'ol', 'li', 'table', 'figure']:
        opens = len(re.findall(f'<{tag}[ >]', content))
        closes = len(re.findall(f'</{tag}>', content))
        if opens != closes:
            issues.append(f'{rel}: <{tag}> count mismatch (open={opens}, close={closes})')
    # Check charset meta
    if 'charset=' not in content:
        issues.append(f'{rel}: Missing charset declaration')
    # Check viewport meta
    if 'viewport' not in content:
        issues.append(f'{rel}: Missing viewport meta')
    # Check title
    if '<title>' not in content or '</title>' not in content:
        issues.append(f'{rel}: Missing <title>')

# 2. CSS brace balance
css_files = [p for p in root.rglob('*.css') if 'node_modules' not in str(p)]
for f in css_files:
    content = f.read_text(encoding='utf-8')
    rel = f.relative_to(root)
    opens = content.count('{')
    closes = content.count('}')
    if opens != closes:
        issues.append(f'{rel}: CSS brace mismatch (open={opens}, close={closes})')
    # Check for @import and @media blocks
    at_imports = len(re.findall(r'@import', content))
    at_media = len(re.findall(r'@media', content))

# 3. JS syntax check via node
js_files = [p for p in root.rglob('*.js') if 'node_modules' not in str(p) and 'typed' not in str(p)]
for f in js_files:
    rel = f.relative_to(root)
    try:
        result = subprocess.run(
            ['node', '--check', str(f)],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            issues.append(f'{rel}: JS syntax error: {result.stderr.strip()[:300]}')
    except FileNotFoundError:
        issues.append(f'{rel}: Node.js not available for JS syntax check')
        break
    except subprocess.TimeoutExpired:
        issues.append(f'{rel}: JS syntax check timed out')

# 4. Verify all asset images referenced exist and are non-empty
for f in html_files:
    content = f.read_text(encoding='utf-8')
    rel = f.relative_to(root)
    refs = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
    for ref in refs:
        if ref.startswith(('http', '//', 'data:', 'tel:', 'mailto:', '#', 'javascript:', 'ftp:')):
            continue
        clean = ref.split('?')[0].split('#')[0]
        if not clean:
            continue
        target = (f.parent / clean).resolve()
        if not target.exists():
            issues.append(f'{rel}: Missing asset: {ref}')
        elif target.is_file() and target.stat().st_size == 0:
            issues.append(f'{rel}: Empty file: {ref}')

# 5. Verify sitemap URLs have corresponding local files
sitemap = root / 'sitemap.xml'
if sitemap.exists():
    content = sitemap.read_text(encoding='utf-8')
    locs = re.findall(r'<loc>([^<]+)</loc>', content)
    for loc in locs:
        local_name = loc.replace('https://raufbuyante.github.io/portfolio/', '')
        if not local_name:
            continue
        candidate = root / local_name
        if not candidate.exists():
            issues.append(f'sitemap.xml: URL references non-existent file: {loc}')
else:
    issues.append('sitemap.xml not found')

# 6. Check internal cross-page links resolve
for f in html_files:
    content = f.read_text(encoding='utf-8')
    rel = f.relative_to(root)
    refs = re.findall(r'href=["\']([^"\']+)["\']', content)
    for ref in refs:
        if ref.startswith(('http', '//', 'data:', 'tel:', 'mailto:', '#', 'javascript:', 'ftp:')):
            continue
        clean = ref.split('?')[0].split('#')[0]
        if not clean:
            continue
        if clean.endswith('.html') or clean.endswith('.pdf'):
            target = (f.parent / clean).resolve()
            if not target.exists():
                issues.append(f'{rel}: Broken internal link: {ref}')

# 7. Check for base href usage and icon classes
fa_icons = 0
for f in html_files:
    content = f.read_text(encoding='utf-8')
    fa_icons += len(re.findall(r'class="[^"]*\bfa[bsr]?-[a-z0-9-]+', content))
    # Check FontAwesome CDN is linked
    if 'font-awesome' not in content and 'fontawesome' not in content:
        issues.append(f'{f.relative_to(root)}: FontAwesome CDN not linked')

# 8. Verify research page images exist
research_html = root / 'research' / 'ssh-pivoting-lab.html'
if research_html.exists():
    content = research_html.read_text(encoding='utf-8')
    imgs = re.findall(r'src=["\']([^"\']+)["\']', content)
    missing_research = []
    for img in imgs:
        if img.startswith(('http', 'data:')):
            continue
        target = (research_html.parent / img).resolve()
        if not target.exists():
            missing_research.append(img)
        elif not target.is_file() or target.stat().st_size == 0:
            missing_research.append(f'{img} (empty or not a file)')
    if missing_research:
        issues.append(f'research/ssh-pivoting-lab.html: Missing research images: {missing_research}')

# 9. Verify asset directories have expected contents
expected_dirs = [
    ('assets/profile', ['*.png', '*.jpg', '*.jpeg', '*.webp']),
    ('assets/resume', ['*.pdf']),
    ('assets/certificates/cisco', ['*.png', '*.jpg', '*.jpeg']),
    ('assets/certificates/codefest', ['*.png', '*.jpg', '*.jpeg']),
    ('assets/gallery/ctf', ['*.png', '*.jpg', '*.jpeg']),
    ('assets/research/ssh-pivoting', ['*.png', '*.jpg', '*.jpeg']),
]
for dirname, patterns in expected_dirs:
    d = root / dirname
    if not d.exists():
        issues.append(f'Missing expected directory: {dirname}')
        continue
    contents = list(d.iterdir())
    if not contents:
        issues.append(f'Empty directory: {dirname}')
    else:
        files = [p for p in d.iterdir() if p.is_file()]
        if not files:
            issues.append(f'Directory has no files: {dirname}')

# 10. Verify JS files exist and typed.js is included
typed_js = root / 'js' / 'typed.js' / 'typed.min.js'
if not typed_js.exists():
    issues.append('js/typed.js/typed.min.js not found')
elif typed_js.stat().st_size == 0:
    issues.append('js/typed.js/typed.min.js is empty')

script_js = root / 'js' / 'script.js'
if not script_js.exists():
    issues.append('js/script.js not found')

# 11. Check for suspicious hidden base64 comment (potential flag leak)
for f in html_files:
    content = f.read_text(encoding='utf-8')
    rel = f.relative_to(root)
    # Look for base64-looking comments
    b64_comments = re.findall(r'<!--\s*([A-Za-z0-9+/=]{20,})\s*-->', content)
    for comment in b64_comments:
        issues.append(f'{rel}: Suspicious base64-encoded comment found: {comment[:50]}...')

# Summary
print(f'{"=" * 60}')
print(f'COMPREHENSIVE IMPLEMENTATION TEST REPORT')
print(f'{"=" * 60}')
print(f'HTML files checked:    {len(html_files)}')
print(f'CSS files checked:     {len(css_files)}')
print(f'JS files checked:      {len(js_files)}')
print(f'FontAwesome icons:     {fa_icons}')

if issues:
    print(f'\n{"=" * 60}')
    print(f'ISSUES FOUND: {len(issues)}')
    print(f'{"=" * 60}')
    for i, issue in enumerate(issues, 1):
        print(f'  {i}. {issue}')
    sys.exit(1)
else:
    print(f'\n{"=" * 60}')
    print('ALL CHECKS PASSED')
    print('  - HTML structure: OK (DOCTYPE, paired tags, charset, viewport, title)')
    print('  - CSS brace balance: OK')
    print('  - JS syntax: OK')
    print('  - All asset references resolve: OK')
    print('  - Sitemap entries valid: OK')
    print('  - Internal links valid: OK')
    print('  - Asset directories populated: OK')
    print('  - No suspicious content: OK')
    print(f'{"=" * 60}')
    sys.exit(0)