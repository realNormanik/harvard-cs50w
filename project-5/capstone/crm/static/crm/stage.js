document.addEventListener("DOMContentLoaded", function () {
    const stageList = document.getElementById("stageList");
    if (!stageList) return;

    const REORDER_URL = stageList.dataset.reorderUrl;
    const FORM_HAS_ERRORS = stageList.dataset.formHasErrors === "true";

    let draggedStage = null;

    // Read the CSRF token from the cookie (standard Django approach)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                };
            };
        };

        return cookieValue;
    };

    const CSRF_TOKEN = getCookie("csrftoken");

    // Determine the stage item the dragged element should be placed before
    function getDragAfterElement(container, y) {
        const items = [...container.querySelectorAll(".stage-item:not(.dragging)")];

        return items.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;

            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            };
        }, { offset: Number.NEGATIVE_INFINITY, element: null }).element;
    };

    // Refresh the "Position: N" label on every stage item to match the current order
    function updatePositionLabels() {
        stageList.querySelectorAll(".stage-item").forEach((item, index) => {
            const label = item.querySelector(".stage-position");

            if (label) label.textContent = `Order: ${index}`;
        });
    };

    // Persist the current stage order to the backend
    function saveStageOrder() {
        const stageIds = Array.from(stageList.querySelectorAll(".stage-item"))
            .map(item => item.dataset.stageId);

        fetch(REORDER_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify({ order: stageIds })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updatePositionLabels();
                refreshMoveButtonsState();
            } else {
                alert("The new order of stages could not be saved. Please refresh the page.");
            };
        })
        .catch(() => alert("Error connecting to the server."));
    };

    // ------------------------------------------------------------------
    // DRAG & DROP (desktop)
    // ------------------------------------------------------------------
    stageList.querySelectorAll(".stage-item").forEach(item => {
        item.addEventListener("dragstart", function () {
            draggedStage = item;
            // Add the "dragging" class on the next tick so the drag image
            // is captured before the item's opacity changes
            setTimeout(() => item.classList.add("dragging"), 0);
        });

        item.addEventListener("dragend", function () {
            item.classList.remove("dragging");
            draggedStage = null;
            saveStageOrder();
        });
    });

    stageList.addEventListener("dragover", function (e) {
        e.preventDefault();
        if (!draggedStage) return;

        // Reposition the dragged item within the list based on cursor position
        const afterElement = getDragAfterElement(stageList, e.clientY);
        if (afterElement == null) {
            stageList.appendChild(draggedStage);
        } else {
            stageList.insertBefore(draggedStage, afterElement);
        };

        // Update the disabled state live, while dragging, rather than waiting
        // for dragend and the server response (saveStageOrder).
        refreshMoveButtonsState();
    });

    // ------------------------------------------------------------------
    // MOBILE FALLBACK: arrow buttons instead of drag & drop
    // ------------------------------------------------------------------

    // Enable/disable the up/down buttons based on each item's position in the list
    function refreshMoveButtonsState() {
        const items = Array.from(stageList.querySelectorAll(".stage-item"));
        items.forEach((item, index) => {
            const upBtn = item.querySelector(".stage-move-up");
            const downBtn = item.querySelector(".stage-move-down");
            if (upBtn) upBtn.disabled = index === 0;
            if (downBtn) downBtn.disabled = index === items.length - 1;
        });
    };

    function addMobileMoveButtons() {
        // Same approach as in pipeline.js: remove the old button wrapper every
        // time and rebuild it from scratch, setting the "disabled" state right
        // when the button is created, based on the stage's current position
        // in the list.
        const items = Array.from(stageList.querySelectorAll(".stage-item"));

        items.forEach((item, index) => {
            const oldWrapper = item.querySelector(".stage-move-buttons");
            if (oldWrapper) oldWrapper.remove();

            const btnWrapper = document.createElement("div");
            btnWrapper.className = "stage-move-buttons";

            // "Move up" button
            const upBtn = document.createElement("button");
            upBtn.type = "button";
            upBtn.className = "btn btn-outline-primary p-1 stage-move-up";
            upBtn.innerHTML = '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m5 15 7-7 7 7"/></svg>';
            upBtn.disabled = index === 0;
            upBtn.addEventListener("click", function () {
                // Find the neighbor by index among the actual .stage-item elements,
                // rather than via previousElementSibling — this guarantees the swap
                // always targets the correct item regardless of other elements in
                // the DOM, and that refreshMoveButtonsState() computes "disabled"
                // against the same order that's visible on screen.
                const currentItems = Array.from(stageList.querySelectorAll(".stage-item"));
                const idx = currentItems.indexOf(item);

                if (idx > 0) {
                    stageList.insertBefore(item, currentItems[idx - 1]);
                    updatePositionLabels();
                    refreshMoveButtonsState();
                    saveStageOrder();
                };
            });

            // "Move down" button
            const downBtn = document.createElement("button");
            downBtn.type = "button";
            downBtn.className = "btn btn-outline-primary p-1 stage-move-down";
            downBtn.innerHTML = '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/></svg>';
            downBtn.disabled = index === items.length - 1;
            downBtn.addEventListener("click", function () {
                const currentItems = Array.from(stageList.querySelectorAll(".stage-item"));
                const idx = currentItems.indexOf(item);

                if (idx !== -1 && idx < currentItems.length - 1) {
                    stageList.insertBefore(currentItems[idx + 1], item);
                    updatePositionLabels();
                    refreshMoveButtonsState();
                    saveStageOrder();
                };
            });

            btnWrapper.appendChild(upBtn);
            btnWrapper.appendChild(downBtn);
            item.appendChild(btnWrapper);
        });

        refreshMoveButtonsState();
    };

    addMobileMoveButtons();

    // ------------------------------------------------------------------
    // If the "New stage" form had validation errors, reopen the modal
    // ------------------------------------------------------------------
    if (FORM_HAS_ERRORS) {
        const modalEl = document.getElementById("newStageModal");

        if (modalEl) {
            new bootstrap.Modal(modalEl).show();
        };
    };
});