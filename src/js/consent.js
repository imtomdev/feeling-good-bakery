// Cookie consent (Axeptio) and Google Analytics.
//
// gtag.js used to be loaded from <head> on every visit, before any consent.
// It is now injected only once the visitor has accepted the analytics cookies,
// which also saves the request for every other visitor (and for EcoIndex).
const GA_ID = "G-MC0HGGF759";
const GTAG_SRC = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;

window.dataLayer = window.dataLayer || [];

function gtag() {
  window.dataLayer.push(arguments);
}

function loadGtag() {
  if (document.querySelector(`script[src="${GTAG_SRC}"]`)) return;

  const script = document.createElement("script");
  script.async = true;
  script.src = GTAG_SRC;
  document.head.appendChild(script);
}

window._axcb = window._axcb || [];
window._axcb.push((axeptio) => {
  axeptio.on("cookies:complete", (choices) => {
    if (!choices.google_analytics) return;

    loadGtag();
    gtag("js", new Date());
    gtag("config", GA_ID);
  });
});

window.axeptioSettings = {
  clientId: "60a53c9b6cd349769a41d8cb",
  cookiesVersion: "ga_only",
};

const sdk = document.createElement("script");
sdk.async = true;
// The site is served over HTTPS only (HTTP redirects): an explicit scheme avoids
// a redirect when the build is previewed over plain HTTP.
sdk.src = "https://static.axept.io/sdk.js";
document.head.appendChild(sdk);
