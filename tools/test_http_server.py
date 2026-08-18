"""Tests that the portfolio site serves all pages and assets correctly over HTTP."""
import urllib.request
import urllib.error
import urllib.parse
import sys

BASE = "http://localhost:8080"

FILES = [
    "index.html",
    "projects.html",
    "research/ssh-pivoting-lab.html",
    "css/style.css",
    "css/research.css",
    "js/script.js",
    "js/typed.js/typed.min.js",
    "assets/profile/profile.png",
    "assets/resume/Resume.pdf",
    "image/BG.png",
    "image/icon-browser.png",
    "image/PP.png",
    "image/11gif.gif",
    "image/11png.png",
    "sitemap.xml",
]

# Also verify a few referenced image assets from certificates/gallery/research
FILES += [
    "assets/certificates/cisco/Screenshot 2026-08-13 192839.png",
    "assets/certificates/codefest/img5.jpg",
    "assets/gallery/ctf/1.jpg",
    "assets/research/ssh-pivoting/01-lab-topology.png",
]

failed = []
passed = 0

for f in FILES:
    # URL-encode the path (handles spaces in filenames)
    encoded_path = urllib.parse.quote(f)
    url = f"{BASE}/{encoded_path}"
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        data = resp.read()
        status = resp.status
        print(f"  OK  {f} -> {status} ({len(data)} bytes)")
        passed += 1
    except urllib.error.HTTPError as e:
        print(f"  FAIL {f} -> HTTP {e.code}")
        failed.append(f)
    except Exception as e:
        print(f"  FAIL {f} -> {e}")
        failed.append(f)

print()
print(f"Tested {len(FILES)} files: {passed} passed, {len(failed)} failed.")
if failed:
    print("Failed files:", ", ".join(failed))
    sys.exit(1)
print("All HTTP responses OK.")
sys.exit(0)