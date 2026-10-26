"""Functional checks of the built site, run against the original and the optimised build.

Usage: python -I interactions.py <base_url>

Checks: console errors / failed requests, burger menu, modals (open via button,
close via cross and via background, footer modals), Swiper navigation and the
read-more button data-id, AOS classes after scroll, videos playing, anchor links,
loader removal, number of requests.
"""
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/")
BROWSER = sys.argv[2] if len(sys.argv) > 2 else "chromium"


def check(name, ok, detail=""):
    print(f"[{'OK' if ok else 'FAIL'}] {name} {detail}")
    return ok


def run(width, height, mobile):
    with sync_playwright() as p:
        b = getattr(p, BROWSER).launch()
        ctx = b.new_context(viewport={"width": width, "height": height}, **({"is_mobile": mobile, "has_touch": mobile} if BROWSER == "chromium" else {}))
        page = ctx.new_page()
        errors, failed, requests = [], [], []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.on("request", lambda r: requests.append(r.url))
        page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        page.goto(BASE + "/", wait_until="load")
        page.wait_for_timeout(1500)
        print(f"\n== {BROWSER} {width}x{height} {'mobile' if mobile else 'desktop'}")

        check("loader removed after load", page.evaluate("!document.body.classList.contains('--loading')"))

        # Hero video
        check("hero video playing", page.evaluate("(() => { const v = document.querySelector('section.hero video'); return !v.paused && v.readyState >= 2; })()"))

        # Burger menu
        page.evaluate("document.querySelector('header .handle').click()")
        page.wait_for_timeout(400)
        check("menu opens", page.evaluate("!document.querySelector('ul.navigation').classList.contains('hidden') && document.querySelector('header .handle').classList.contains('open')"))
        page.evaluate("document.querySelector('header .handle').click()")
        page.wait_for_timeout(400)
        check("menu closes", page.evaluate("document.querySelector('ul.navigation').classList.contains('hidden')"))

        # Anchor links (smooth scroll)
        page.evaluate("document.querySelector('header .handle').click()")
        page.wait_for_timeout(300)
        page.evaluate("document.querySelector('ul.navigation a[href=\"#nos-cookies\"]').click()")
        page.wait_for_timeout(1500)
        y = page.evaluate("window.scrollY")
        target = page.evaluate("document.getElementById('nos-cookies').getBoundingClientRect().top + window.scrollY")
        check("anchor scrolls to #nos-cookies", abs(y - target) < 5, f"(scrollY {y:.0f} vs {target:.0f})")
        check("menu closed on scroll", page.evaluate("document.querySelector('ul.navigation').classList.contains('hidden')"))

        # Swiper: lazy slides must be loaded before they are shown
        loaded = page.evaluate("[...document.querySelectorAll('.swiper-slide')].map(s => (s.classList.contains('swiper-slide-active') ? '*' : '') + s.dataset.id + ':' + (s.querySelector('img').complete && s.querySelector('img').naturalWidth > 0 ? 'ok' : 'NOT'))")
        print("    slides loaded at rest:", " ".join(loaded))
        check("active/next/prev slides loaded at rest", all(x.endswith('ok') for x in loaded if any(k in x for k in ('*',))) and page.evaluate("['swiper-slide-next','swiper-slide-prev','swiper-slide-active'].every(c => { const i = document.querySelector('.' + c + ' img'); return i.complete && i.naturalWidth > 0; })"))
        flash = []
        for _ in range(9):
            upcoming = page.evaluate("(() => { const i = document.querySelector('.swiper-slide-next img'); return [i.closest('.swiper-slide').dataset.id, i.complete && i.naturalWidth > 0]; })()")
            if not upcoming[1]: flash.append(upcoming[0])
            page.evaluate("document.querySelector('.swiper-next').click()")
            page.wait_for_timeout(450)
        check("next slide always loaded before each click (9 clicks, 450 ms apart)", not flash, f"not ready: {flash}")
        first = page.evaluate("document.querySelector('.swiper-slide-active').dataset.id")
        page.evaluate("document.querySelector('.swiper-next').click()")
        page.wait_for_timeout(700)
        second = page.evaluate("document.querySelector('.swiper-slide-active').dataset.id")
        btn = page.evaluate("document.querySelector('button.read-more').dataset.id")
        check("swiper next changes slide", first != second, f"({first} -> {second})")
        check("read-more button follows the slide", btn == second, f"(button {btn})")
        page.evaluate("document.querySelector('.swiper-prev').click()")
        page.wait_for_timeout(700)
        check("swiper prev returns", page.evaluate("document.querySelector('.swiper-slide-active').dataset.id") == first)
        check("swiper slide image loaded", page.evaluate("(() => { const i = document.querySelector('.swiper-slide-active img'); return i.complete && i.naturalWidth > 0; })()"))

        # Product modal via the read-more button
        page.evaluate("document.querySelector('button.read-more').click()")
        page.wait_for_timeout(500)
        opened = page.evaluate(f"(() => {{ const m = document.querySelector('.modal.open'); return m && m.dataset.id === '{first}' && getComputedStyle(m).opacity === '1' && document.body.classList.contains('--modal-opened'); }})()")
        check("product modal opens", bool(opened))
        page.wait_for_timeout(500)
        check("modal image loaded", page.evaluate("(() => { const i = document.querySelector('.modal.open .cookie img'); return i && i.complete && i.naturalWidth > 0; })()"))
        check("modal text present", page.evaluate("document.querySelector('.modal.open h2').textContent.includes('histoire')"))
        page.evaluate("document.querySelector('.modal.open .close').click()")
        page.wait_for_timeout(400)
        check("modal closes with cross", page.evaluate("!document.querySelector('.modal.open') && !document.body.classList.contains('--modal-opened')"))
        page.evaluate("document.querySelector('button.read-more').click()")
        page.wait_for_timeout(400)
        page.evaluate("document.querySelector('section.bg').click()")
        page.wait_for_timeout(400)
        check("modal closes with background click", page.evaluate("!document.querySelector('.modal.open')"))

        # Every product modal + footer modals
        ids = ["james-brownie", "pecan-express", "s-more", "dandy", "roudoudou", "naoned", "peanut-better", "matchaman", "mamma-damia"]
        ok_all = True
        for mid in ids:
            page.evaluate(f"(() => {{ const b = document.querySelector('button.read-more'); b.dataset.id = '{mid}'; b.click(); }})()")
            page.wait_for_timeout(350)
            ok_all &= bool(page.evaluate(f"(() => {{ const m = document.querySelector('.modal.open'); return m && m.dataset.id === '{mid}' && m.querySelector('img.close') && m.querySelector('.cookie img') && m.querySelector('p').textContent.length > 50; }})()"))
            page.evaluate("document.querySelector('.modal.open .close').click()")
            page.wait_for_timeout(350)
        check("all 9 product modals open/close", ok_all)
        for mid in ("mentions-legales", "rgpd"):
            page.evaluate(f"document.querySelector('.handle-modal[data-id=\"{mid}\"]').click()")
            page.wait_for_timeout(400)
            ok = page.evaluate(f"(() => {{ const m = document.querySelector('.modal.open'); return m && m.dataset.id === '{mid}' && m.closest('footer') !== null && m.querySelectorAll('h3').length >= 3; }})()")
            check(f"footer modal {mid} opens inside footer", bool(ok))
            page.evaluate("document.querySelector('.modal.open .close').click()")
            page.wait_for_timeout(300)

        # Scroll to the bottom: AOS + lazy videos
        page.evaluate("async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y <= h; y += 300) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } }")
        page.wait_for_timeout(1500)
        aos = page.evaluate("[...document.querySelectorAll('[data-aos]')].map(e => e.classList.contains('aos-animate') || getComputedStyle(e).display === 'none')")
        check("AOS animated every visible element", all(aos), f"({sum(aos)}/{len(aos)})")
        vids = page.evaluate("""async () => { const out = []; const sleep = ms => new Promise(r => setTimeout(r, ms));
          for (const v of document.querySelectorAll('video')) {
            if (getComputedStyle(v).display === 'none') { out.push({src: v.currentSrc.split('/').pop(), display: 'none', paused: v.paused, ready: v.readyState}); continue; }
            v.scrollIntoView({block: 'center'}); await sleep(600);
            out.push({src: v.currentSrc.split('/').pop(), display: getComputedStyle(v).display, paused: v.paused, ready: v.readyState});
          } return out; }""")
        visible = [v for v in vids if v["display"] != "none"]
        hidden = [v for v in vids if v["display"] == "none"]
        check("every visible video plays when scrolled into view", all(not v["paused"] and v["ready"] >= 2 for v in visible), str(visible))
        check("hidden duplicate video not loaded", all(v["ready"] == 0 for v in hidden), str(hidden))
        imgs = page.evaluate("[...document.querySelectorAll('img')].filter(i => getComputedStyle(i).display !== 'none' && !i.closest('.modal') && !i.closest('.swiper-slide')).map(i => i.complete && i.naturalWidth > 0)")
        check("all visible images (outside carousel) loaded after scroll", all(imgs), f"({sum(imgs)}/{len(imgs)})")

        third = [u for u in requests if "axept.io" in u or "googletagmanager" in u]
        own = [u for u in requests if u.startswith(BASE)]
        print(f"requests: {len(requests)} total, {len(own)} first-party, {len(third)} third-party; gtag loaded: {any('gtag' in u for u in requests)}")
        bad_errors = [e for e in errors if "ERR_FAILED" not in e]
        check("no console error", not bad_errors, str(bad_errors[:5]))
        check("no failed / 4xx-5xx request", not failed, str(failed[:5]))
        ctx.close()
        b.close()


run(1920, 1080, False)
run(390, 844, True)
