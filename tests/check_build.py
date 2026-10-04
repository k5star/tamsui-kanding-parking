"""Verify SITE_URL handling in build.py (with and without a domain), then rebuild default dist/."""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, 'dist')
fails = []
def build(url):
    env = dict(os.environ); env.pop('SITE_URL', None)
    if url: env['SITE_URL'] = url
    subprocess.run([sys.executable, 'build.py'], cwd=ROOT, env=env, check=True, capture_output=True)
    return open(f'{D}/index.html', encoding='utf-8').read()
def ok(c, m): print(('PASS ' if c else 'FAIL ') + m); c or fails.append(m)
URL = 'https://parking.example.com'
h = build(URL + '/')
ok(f'<link rel="canonical" href="{URL}/">' in h, 'canonical with SITE_URL')
ok(f'content="{URL}/"' in h and f'{URL}/assets/img/map-1000.webp' in h, 'og:url / og:image absolute')
ld = json.loads(re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S).group(1))
ok(ld.get('url') == URL + '/', 'Schema url set')
ok(os.path.exists(f'{D}/sitemap.xml') and f'<loc>{URL}/</loc>' in open(f'{D}/sitemap.xml').read(), 'sitemap.xml generated')
ok(f'Sitemap: {URL}/sitemap.xml' in open(f'{D}/robots.txt').read(), 'robots.txt references sitemap')
h = build('')
ok('canonical' not in h and '{{SITE_URL}}' not in h and 'og:url' not in h, 'no canonical/og:url without SITE_URL')
ok('"url"' not in re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S).group(1), 'no Schema url without SITE_URL')
ok(not os.path.exists(f'{D}/sitemap.xml'), 'no sitemap without SITE_URL')
ok('noindex' not in h and 'Disallow: /\n' not in open(f'{D}/robots.txt').read(), 'no noindex / no Disallow')
print(f'\n{9-len(fails)} passed, {len(fails)} failed'); sys.exit(1 if fails else 0)
