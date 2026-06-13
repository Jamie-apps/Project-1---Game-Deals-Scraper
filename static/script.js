document.querySelectorAll(".deal-summary").forEach(summary=> {
    summary.addEventListener("click", () => {
        const dealRow = summary.parentElement;
        dealRow.classList.toggle("open");
    });
});