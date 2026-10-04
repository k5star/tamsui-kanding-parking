"""Automated checks for dist/: responsive, sticky CTA, links, prices, SEO, console, a11y (axe)."""
import json, os, re, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist'); SHOTS = os.path.join(ROOT, 'screenshots'); os.makedirs(SHOTS, exist_ok=True)
MAPS = 'https://maps.app.goo.gl/ASsbAQvR1QARp5GZ9?g_st=ac'
WIDTHS = [(375, 667), (390, 844), (430, 932), (768, 1024), (1024, 768), (1440, 900)]
PRICES = ['NT$10', 'NT$20', 'NT$80', 'NT$1,000', '前 10 分鐘', 'LINE Pay / ATM 等']
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Q, directory=DIST)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{port}/'
fails, report = [], []
def check(cond, msg):
    (report if cond else fails).append(('PASS ' if cond else 'FAIL ') + msg)
axe_src = open(os.path.join(ROOT, 'node_modules/axe-core/axe.min.js')).read()
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in WIDTHS:
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=w < 768, has_touch=w < 768)
        pg = ctx.new_page(); errs = []
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL, wait_until='load')
        own = [e for e in errs if 'google' not in e.lower() and 'gstatic' not in e.lower()]
        check(not own, f'{w}px no first-party console errors {own[:2]}')
        sw = pg.evaluate('document.documentElement.scrollWidth'); check(sw <= w, f'{w}px no horizontal scroll (scrollWidth={sw})')
        bar_vis = pg.is_visible('.mbar')
        check(bar_vis == (w < 1024), f'{w}px sticky bar visible={bar_vis}')
        if w < 1024:
            box = pg.locator('.mbar .btn-primary').bounding_box()
            check(box and box['y'] + box['height'] <= h and box['height'] >= 48, f'{w}px sticky 立即導航 in viewport, height {box and round(box["height"])}px')
            pg.mouse.wheel(0, 3000); pg.wait_for_timeout(200)
            check(pg.locator('.mbar').bounding_box()['y'] < h, f'{w}px sticky bar stays after scroll')
            pg.evaluate('scrollTo({top:0,behavior:"instant"})'); pg.wait_for_timeout(200)
        # above-the-fold: name, price, address, navigate CTA
        fold = pg.evaluate('''h=>{const t=s=>{const r=document.querySelector(s).getBoundingClientRect();return r.top>=0&&r.bottom<=h};
            return {name:t('#hero-title'),price:t('.quick'),addr:t('.hero-addr'),cta:t('.mbar .btn-primary')||t('.hero-cta .btn-primary')||t('.header-cta')}}''', h)
        check(all(fold.values()), f'{w}px above the fold {fold}')
        pg.screenshot(path=f'{SHOTS}/home-{w}.png')
        pg.screenshot(path=f'{SHOTS}/home-{w}-full.png', full_page=True)
        pg.evaluate('[...document.images].forEach(i=>i.loading="eager")'); pg.wait_for_timeout(800)
        broken = pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)')
        check(not broken, f'{w}px images load {broken}')
        if w == 390:
            pg.add_script_tag(content=axe_src)
            res = pg.evaluate('axe.run(document,{exclude:[["iframe"]]}).then(r=>r.violations.map(v=>v.id+":"+v.impact+":"+v.nodes.length))')
            check(not res, f'axe a11y violations {res}')
        ctx.close()
    # content / SEO checks once
    pg = b.new_page(); pg.goto(URL)
    text = pg.inner_text('body')
    for s in PRICES: check(s in text, f'price text present: {s}')
    check('每日最高 80 元' in text and '平日每小時 10 元' in text and '假日每小時 20 元' in text, 'price sentences consistent')
    hrefs = pg.eval_on_selector_all('a[href^="http"]', 'a=>a.map(x=>x.href)')
    check(hrefs and all(x == MAPS for x in hrefs), f'all external links are the Maps link ({len(hrefs)} links)')
    anchors = pg.eval_on_selector_all('a[href^="#"]', 'a=>a.map(x=>x.getAttribute("href"))')
    missing = [a for a in anchors if not pg.query_selector(a)]
    check(not missing, f'internal anchors resolve ({len(anchors)}) missing={missing}')
    title = pg.title(); check(title == '淡水崁頂五路停車場｜淡水夕陽・觀海長堤附近停車', 'title')
    desc = pg.get_attribute('meta[name=description]', 'content'); check('每日最高80元' in desc, 'meta description')
    check(pg.get_attribute('meta[name=robots]', 'content').startswith('index'), 'robots meta')
    check(pg.query_selector('meta[property="og:title"]') is not None, 'Open Graph tags')
    ld = [json.loads(x) for x in pg.eval_on_selector_all('script[type="application/ld+json"]', 's=>s.map(x=>x.textContent)')]
    check(len(ld) == 2 and ld[1]['@type'] == 'FAQPage' and len(ld[1]['mainEntity']) == 5, 'JSON-LD valid (ParkingFacility + FAQPage)')
    check(not any(k in ld[0] for k in ('telephone', 'geo', 'openingHours', 'aggregateRating')), 'JSON-LD has no unverified fields')
    check(pg.locator('h1').count() == 1, 'single h1')
    # Google tag + click tracking: one event per click, links keep their href/target
    check(pg.locator('script[src*="googletagmanager.com/gtag/js"]').count() == 1, 'Google tag included once')
    ev = pg.evaluate('''()=>{window.addEventListener('click',e=>e.preventDefault());
        const out=[];
        document.querySelectorAll('a[href]').forEach(a=>{const i=dataLayer.length;a.click();
            const evs=dataLayer.slice(i).filter(x=>x[0]==='event'), l=evs[0]||[];
            out.push({href:a.getAttribute('href'),sent:evs.length,name:l[1],btn:l[2]&&l[2].button_name,target:a.target});});
        return out;}''')
    nav = [e for e in ev if e['href'] == MAPS]
    check(len(nav) == 6 and all(e['sent'] == 1 and e['name'] == 'parking_navigation_click' and e['target'] == '_blank' for e in nav),
          f'parking_navigation_click once per Maps link ({len(nav)} links)')
    check(len({e['btn'] for e in nav}) == len(nav), f'navigation button_name unique {[e["btn"] for e in nav]}')
    check(all(e['sent'] == 0 for e in ev if e['href'] != MAPS), 'no tracking events for in-page links')
    b.close()
srv.shutdown()
print('\n'.join(report + fails)); print(f'\n{len(report)} passed, {len(fails)} failed')
sys.exit(1 if fails else 0)
