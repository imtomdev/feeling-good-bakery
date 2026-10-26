import "../scss/style.scss";
import AOS from "aos";
// Trimmed copy of aos.css: only the animations used on this page.
import "../vendor/aos.css";

import "./consent";
import "./header";
import "./videos";
import "./recipes";

import "./components/modal";

// Safety net: never keep the loader on screen for more than 5 s.
setTimeout(() => document.body.classList.remove("--loading"), 5000);

document.addEventListener("DOMContentLoaded", () => {
  AOS.init({
    duration: 600,
  });

  const anchors = document.querySelectorAll('a[href^="#');

  anchors.forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      e.preventDefault();
      const href = anchor.href;
      const id = href.split("#")[1];
      const target = document.getElementById(id);

      target.scrollIntoView({ behavior: "smooth" });
    });
  });
});

document.onreadystatechange = function () {
  if (document.readyState == "complete") {
    document.body.classList.remove("--loading");
  }
};
