// Modals live in <template> elements and are only added to the document the
// first time they are opened: their markup and images do not weigh on the
// initial page. To keep the first opening as immediate as before, the images
// of a modal are prefetched as soon as its trigger is hovered, focused or
// touched.
document.addEventListener("DOMContentLoaded", () => {
  const handleModals = document.querySelectorAll(".handle-modal");
  const bg = document.querySelector("section.bg");
  const templates = document.querySelectorAll("template.modals");
  const prefetched = new Set();

  function findTemplateModal(id) {
    for (const template of templates) {
      const modal = template.content.querySelector(`.modal[data-id="${id}"]`);

      if (modal) return { modal, template };
    }

    return null;
  }

  function prefetchModal(id) {
    if (prefetched.has(id)) return;

    const found = findTemplateModal(id);

    if (!found) return;

    prefetched.add(id);
    found.modal.querySelectorAll("img[src]").forEach((img) => {
      new Image().src = img.getAttribute("src");
    });
  }

  function getModal(id) {
    let modal = document.querySelector(`.modal[data-id="${id}"]`);

    if (modal) return modal;

    const found = findTemplateModal(id);

    if (!found) return null;

    modal = document.importNode(found.modal, true);
    // Insert it where the static markup used to be (same parent, same CSS).
    found.template.parentNode.insertBefore(modal, found.template);
    modal.querySelector(".close").addEventListener("click", closeModal);
    // Force a style computation so the opacity transition plays on opening.
    void modal.offsetWidth;

    return modal;
  }

  // open selected modal
  handleModals.forEach((handleModal) => {
    ["mouseenter", "focus", "touchstart"].forEach((type) => {
      handleModal.addEventListener(type, () => prefetchModal(handleModal.dataset.id), {
        passive: true,
      });
    });

    handleModal.addEventListener("click", () => {
      const modal = getModal(handleModal.dataset.id);

      if (!modal) return;

      document.body.classList.add("--modal-opened");
      modal.classList.add("open");
    });
  });

  // click outside equal to click bg section
  bg.addEventListener("click", closeModal);

  function closeModal(e) {
    let modal = e.currentTarget.closest(".modal.open");

    if (e.currentTarget.classList.contains("bg"))
      modal = document.querySelector(".modal.open");

    if (!modal) return;

    document.body.classList.remove("--modal-opened");
    modal.classList.remove("open");
  }
});
