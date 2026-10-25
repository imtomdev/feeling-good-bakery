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

  swiper.on("slideChangeTransitionEnd", function () {
    const slide = swiper.slides[swiper.activeIndex];

    readMore.dataset.id = `${slide.dataset.id}`;
  });
});
