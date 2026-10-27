#!/usr/bin/env python3
"""Build the GitHub Pages files from src/chord-sketch.html (the single source).
- index.html: the app page with PWA head tags and service-worker registration
- sw.js: cache name stamped with the app version (so installed apps update)
Run from the repo root: python3 tools/build.py"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'src/chord-sketch.html').read_text(encoding='utf-8')
# the first two lines (<title>, claude viewport meta) are for the claude.ai artifact only
body = src.split('\n', 2)[2]
ver = re.search(r'PhraseNote v([0-9][0-9.]*)', src).group(1)
head = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>PhraseNote</title>
<meta name="theme-color" content="#0e0f11">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-192.png">
</head><body>
'''
tail = '''
<script>
if('serviceWorker' in navigator && location.protocol.indexOf('http')===0){
  window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});
}
</script>
</body></html>
'''
(root / 'index.html').write_text(head + body + tail, encoding='utf-8')
sw = (root / 'sw.js').read_text(encoding='utf-8')
sw = re.sub(r"const CACHE='phrasenote-v[^']*';", "const CACHE='phrasenote-v%s';" % ver, sw)
(root / 'sw.js').write_text(sw, encoding='utf-8')
print('built v' + ver)
