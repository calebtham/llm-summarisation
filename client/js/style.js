const cards = document.querySelectorAll(".card");
cards.forEach((card) => {
  card.addEventListener("mousemove", (e) => {
    const rect = card.getBoundingClientRect();
    const left = e.clientX - rect.left;
    const top = e.clientY - rect.top;
    card.style.setProperty("--left", `${left}px`);
    card.style.setProperty("--top", `${top}px`);
  });
});
