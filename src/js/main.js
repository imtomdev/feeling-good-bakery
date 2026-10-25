import "../scss/style.scss";
import AOS from "aos";
import "aos/dist/aos.css";

import "./header";
import "./recipes";

import "./components/modal";

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
