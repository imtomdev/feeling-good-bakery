"""Deterministic reference screenshots of the local build (desktop + mobile).

Usage: python -I shoot.py <base_url> <out_dir>

- Third-party scripts (Axeptio, GTM) are blocked so the banner never changes the layout.
- The 5 s loader is dismissed, the page is scrolled step by step to trigger every AOS
  animation, then scrolled back to top.
- All <video> are paused on their first frame so the capture does not depend on timing.
- CSS transitions/animations are disabled right before each capture.
"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/")
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080, "dpr": 1},
    "mobile": {"width": 390, "height": 844, "dpr": 2},
}

FREEZE_CSS = """
*, *::before, *::after {
  transition: none !important;
  animation: none !important;
  caret-color: transparent !important;
}
"""

SETTLE_JS = """
async () => {
  document.body.classList.remove('--loading');
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  // Scroll through the whole page so AOS reveals every element.
  const h = document.documentElement.scrollHeight;
  for (let y = 0; y <= h; y += 400) { window.scrollTo(0, y); await sleep(60); }
  window.scrollTo(0, h); await sleep(400);
  // Wait for every video to have its metadata (lazy ones start during the scroll).
  for (let i = 0; i < 50; i++) {
    if ([...document.querySelectorAll('video')].every(v => v.readyState >= 1 || getComputedStyle(v).display === 'none')) break;
    await sleep(100);
  }
  window.scrollTo(0, 0); await sleep(400);
  // Freeze videos on their first frame.
  for (const v of document.querySelectorAll('video')) {
    try { v.pause(); v.currentTime = 0; } catch (e) {}
  }
  await sleep(300);
  return {
    height: h,
    dom: document.getElementsByTagName('*').length,
    svgDesc: [...document.querySelectorAll('svg')].reduce((n, s) => n + s.getElementsByTagName('*').length, 0),
  };
}
"""


def shoot(page, path, **kw):
    # Videos are masked: their frame timing is not deterministic and the re-encoded
    # files are checked separately (frame-by-frame SSIM).
    page.screenshot(path=str(path), mask=[page.locator("video")], mask_color="#FF00FF", **kw)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        report = []
        for name, vp in VIEWPORTS.items():
            ctx = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                device_scale_factor=vp["dpr"],
                is_mobile=(name == "mobile"),
                has_touch=(name == "mobile"),
                reduced_motion="no-preference",
            )
            ctx.route("**/*axept.io/**", lambda r: r.abort())
            ctx.route("**/*googletagmanager.com/**", lambda r: r.abort())
            page = ctx.new_page()
            errors, failed = [], []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("requestfailed", lambda r: failed.append(r.url) if "axept" not in r.url and "googletagmanager" not in r.url else None)
            page.goto(BASE + "/", wait_until="networkidle")
            page.wait_for_timeout(500)
            info = page.evaluate(SETTLE_JS)
            page.add_style_tag(content=FREEZE_CSS)
            page.wait_for_timeout(200)

            # Clip to the viewport width: html/body hide horizontal overflow, but the
            # document scrollWidth is much larger and would inflate the capture.
            shoot(page, OUT / f"{name}-full.png", full_page=True,
                  clip={"x": 0, "y": 0, "width": vp["width"], "height": info["height"]})

            # One capture per top-level section.
            sections = page.query_selector_all("body > section:not(.bg):not(.loader):not(.modals), body > footer")
            for i, sec in enumerate(sections):
                cls = (sec.get_attribute("class") or sec.evaluate("e => e.tagName.toLowerCase()")).split()[0]
                try:
                    sec.scroll_into_view_if_needed()
                    page.wait_for_timeout(100)
                    sec.screenshot(path=str(OUT / f"{name}-{i:02d}-{cls}.png"), mask=[page.locator("video")], mask_color="#FF00FF")
                except Exception as e:  # noqa: BLE001
                    report.append(f"{name} section {cls}: {e}")

            # Modals: open each one, capture, close (from the top of the page).
            page.evaluate("() => window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
            ids = page.evaluate("() => [...document.querySelectorAll('.handle-modal')].map(e => e.dataset.id)")
            seen = set()
            for mid in ids:
                if mid in seen:
                    continue
                seen.add(mid)
                page.evaluate(
                    """(id) => {
                        const btn = document.querySelector(`.handle-modal[data-id="${id}"]`);
                        if (id !== 'mentions-legales' && id !== 'rgpd') {
                          // Product modals are driven by the swiper button: force its data-id.
                          const b = document.querySelector('button.read-more'); b.dataset.id = id; b.click();
                        } else { btn.click(); }
                    }""",
                    mid,
                )
                page.wait_for_timeout(400)
                page.evaluate("() => { for (const v of document.querySelectorAll('video')) { try { v.pause(); v.currentTime = 0; } catch (e) {} } }")
                page.wait_for_timeout(200)
                shoot(page, OUT / f"{name}-modal-{mid}.png")
                page.evaluate("() => document.querySelector('section.bg').click()")
                page.wait_for_timeout(400)

            # Mobile menu open state.
            if name == "mobile":
                page.evaluate("() => { window.scrollTo(0, 0); document.querySelector('header .handle').click(); }")
                page.wait_for_timeout(400)
                shoot(page, OUT / f"{name}-menu-open.png")
                page.evaluate("() => document.querySelector('header .handle').click()")

            # Swiper: next slide.
            page.evaluate("() => { document.querySelector('section.recipes').scrollIntoView(); document.querySelector('.swiper-next').click(); }")
            page.wait_for_timeout(600)
            page.query_selector("section.recipes").screenshot(path=str(OUT / f"{name}-recipes-slide2.png"), mask=[page.locator("video")], mask_color="#FF00FF")

            report.append(f"{name}: page height {info['height']}px, DOM {info['dom']} (svg desc {info['svgDesc']}, ecoindex count {info['dom'] - info['svgDesc']}), console errors {len(errors)}, failed requests {len(failed)}")
            for e in errors:
                report.append(f"  console error: {e}")
            for f in failed:
                report.append(f"  failed: {f}")
            ctx.close()
        browser.close()
    (OUT / "report.txt").write_text("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
