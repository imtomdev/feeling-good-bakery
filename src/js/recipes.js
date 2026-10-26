// Only the core, Navigation and A11y modules are needed (not the full bundle).
// A11y is enabled by default in the bundle: keep it for the same markup/ARIA.
import Swiper, { A11y, Navigation } from "swiper";
import "swiper/css";
import "swiper/css/navigation";

document.addEventListener("DOMContentLoaded", () => {
  const recipesContainer = document.querySelector("section.recipes");

  if (!recipesContainer) return;

  const swiperContainer = recipesContainer.querySelector(".swiper-container");
  const swiperPrev = swiperContainer.querySelector(".swiper-prev");
  const swiperNext = swiperContainer.querySelector(".swiper-next");
  const readMore = document.querySelector("button.read-more");

  const swiper = new Swiper(swiperContainer, {
    modules: [Navigation, A11y],
    loop: true,
    allowTouchMove: false,
    navigation: {
      nextEl: swiperNext,
      prevEl: swiperPrev,
    },
  });

  // Slide images are lazy-loaded; make sure the two slides on each side of the
  // active one are always loaded so a quick succession of clicks never shows
  // an empty slide (native lazy-loading alone is not early enough in Firefox).
  const preloadNeighbours = () => {
    const count = swiper.slides.length;

    for (let offset = -2; offset <= 2; offset++) {
      const slide = swiper.slides[(swiper.activeIndex + offset + count) % count];
      const img = slide && slide.querySelector("img");

      if (img && img.loading === "lazy") img.loading = "eager";
    }
  };

  preloadNeighbours();
  swiper.on("slideChange", preloadNeighbours);

  swiper.on("slideChangeTransitionEnd", function () {
    const slide = swiper.slides[swiper.activeIndex];

    readMore.dataset.id = `${slide.dataset.id}`;
  });
});
