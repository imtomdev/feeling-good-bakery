// Lazy video playback.
//
// A <video data-lazy preload="none"> is not fetched by the browser until it is
// played. It is started only when it is displayed (not `display: none`) and
// about to enter the viewport (one viewport ahead), which avoids downloading
// the hidden mobile/desktop duplicate of the same video and the below-the-fold
// videos for visitors who never scroll to them. The hero video keeps its
// `autoplay` attribute so it starts as early as before.
document.addEventListener("DOMContentLoaded", () => {
  const videos = document.querySelectorAll("video[data-lazy]");

  if (!videos.length) return;

  const start = (video) => {
    if (video.dataset.started) return;

    video.dataset.started = "true";
    const playing = video.play();
    if (playing && typeof playing.catch === "function") playing.catch(() => {});
  };

  if (!("IntersectionObserver" in window)) {
    videos.forEach(start);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        start(entry.target);
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "100% 0px" }
  );

  videos.forEach((video) => observer.observe(video));
});
