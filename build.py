#!/usr/bin/env python3
"""Build static site: src/ -> dist/.
Usage: SITE_URL=https://example.netlify.app python3 build.py
If SITE_URL is empty, canonical / og:url / og:image / sitemap are omitted (TODO until domain is known)."""
import os, re, shutil, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, DIST = os.path.join(ROOT, 'src'), os.path.join(ROOT, 'dist')
site = os.environ.get('SITE_URL', '').rstrip('/')
html = open(os.path.join(SRC, 'index.html'), encoding='utf-8').read()
block = re.compile(r'<!--SITE_URL_BLOCK-->\n(.*?)<!--/SITE_URL_BLOCK-->\n', re.S)
html = block.sub(lambda m: m.group(1).replace('{{SITE_URL}}', site) if site else '', html)
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(os.path.join(DIST, 'assets/img'))
open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(html)
# copy only images referenced by the page
for name in sorted(set(re.findall(r'assets/img/([\w.-]+)', html))):
    shutil.copy(os.path.join(SRC, 'assets/img', name), os.path.join(DIST, 'assets/img', name))
robots = 'User-agent: *\nAllow: /\n' + (f'Sitemap: {site}/sitemap.xml\n' if site else '')
open(os.path.join(DIST, 'robots.txt'), 'w').write(robots)
if site:
    today = datetime.date.today().isoformat()
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{site}/</loc><lastmod>{today}</lastmod></url>\n</urlset>\n')
# Netlify headers: cache images long, html short
open(os.path.join(DIST, '_headers'), 'w').write(
    '/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/\n  Cache-Control: public, max-age=300\n')
print('built dist/', '(SITE_URL=%s)' % (site or 'unset'))
