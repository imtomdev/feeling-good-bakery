import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { defineConfig } from "vite";

/**
 * Inline every `<img class="js-inject-me" src="*.svg">` of index.html at build time.
 *
 * This replaces the runtime SVGInjector library, which fetched each SVG a second
 * time over XHR (31 requests for 16 files). The resulting markup is the same as what
 * SVGInjector produced: the `id`, `title`, `style` and `data-*` attributes of the
 * `<img>` are copied to the `<svg>` root and the classes are merged with `injected-svg`.
 * The `alt` text is exposed through `role="img"` + `aria-label`.
 */
function inlineSvgPlugin() {
  const IMG_RE = /<img\s+([^>]*?\bclass="[^"]*\bjs-inject-me\b[^"]*"[^>]*?)\/?>/g;
  const ATTR_RE = /([\w:-]+)="([^"]*)"/g;

  function parseAttrs(raw) {
    const attrs = {};
    for (const [, name, value] of raw.matchAll(ATTR_RE)) attrs[name] = value;
    return attrs;
  }

  function loadSvg(file) {
    let svg = readFileSync(file, "utf8");
    svg = svg.replace(/<\?xml[^>]*\?>/, "");
    svg = svg.replace(/<!--[\s\S]*?-->/g, "");
    // An `<h1>` is not valid inside an inline SVG and was never rendered: drop it.
    svg = svg.replace(/<h1>[\s\S]*?<\/h1>/g, "");
    // Collapse whitespace-only text nodes between tags.
    svg = svg.replace(/>\s+</g, "><").trim();
    return svg;
  }

  function escapeAttr(value) {
    return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
  }

  return {
    name: "inline-svg",
    transformIndexHtml: {
      enforce: "pre",
      transform(html, ctx) {
        const htmlDir = dirname(ctx.filename);
        return html.replace(IMG_RE, (match, rawAttrs) => {
          const attrs = parseAttrs(rawAttrs);
          if (!attrs.src || !attrs.src.endsWith(".svg")) return match;

          const svg = loadSvg(resolve(htmlDir, attrs.src));
          const rootMatch = svg.match(/^<svg\b([^>]*)>/);
          if (!rootMatch) throw new Error(`inline-svg: no <svg> root in ${attrs.src}`);
          const rootAttrs = parseAttrs(rootMatch[1]);

          const classes = [
            ...(rootAttrs.class || "").split(/\s+/),
            "injected-svg",
            ...attrs.class.split(/\s+/),
          ].filter(Boolean);
          const merged = {
            ...rootAttrs,
            class: [...new Set(classes)].join(" "),
          };
          if (attrs.id) merged.id = attrs.id;
          if (attrs.title) merged.title = attrs.title;
          if (attrs.style) merged.style = attrs.style;
          for (const [name, value] of Object.entries(attrs)) {
            if (name.startsWith("data-")) merged[name] = value;
          }
          if (attrs.alt) {
            merged.role = "img";
            merged["aria-label"] = attrs.alt;
          }

          const rootTag = `<svg ${Object.entries(merged)
            .map(([name, value]) => `${name}="${escapeAttr(value)}"`)
            .join(" ")}>`;
          return rootTag + svg.slice(rootMatch[0].length);
        });
      },
    },
  };
}

export default defineConfig({
  plugins: [inlineSvgPlugin()],
});
