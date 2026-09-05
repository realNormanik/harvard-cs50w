document.addEventListener("DOMContentLoaded", function () {
    // Automatically clear the form after closing the “New Deal”,
    // modal so that old data isn't retained when it's reopened.
    const newDealModal = document.getElementById("newDealModal");
    if (newDealModal) {
        newDealModal.addEventListener("hidden.bs.modal", function () {
            const form = newDealModal.querySelector("form");
            if (form) form.reset();
        });
    }

    // Prevent the edit modal from opening when the user finishes dragging a tile
    // (to avoid accidental clicks after drag-and-drop)
    let wasDragging = false;
    document.querySelectorAll(".pipeline-card").forEach(card => {
        card.addEventListener("dragstart", () => { wasDragging = true; });
        card.addEventListener("click", function (e) {
            if (wasDragging) {
                e.stopImmediatePropagation();
                wasDragging = false;
            }
        });
    });
});