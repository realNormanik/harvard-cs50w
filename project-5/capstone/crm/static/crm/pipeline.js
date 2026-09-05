document.addEventListener("DOMContentLoaded", function () {
    const CSRF_TOKEN = getCookie("csrftoken");

    const board = document.getElementById("pipelineBoard");
    if (!board) return;

    let draggedCard = null;

    // ------------------------------------------------------------------
    // Read the CSRF token from the cookie (standard Django approach)
    // ------------------------------------------------------------------
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

    // ------------------------------------------------------------------
    // DRAG & DROP (desktop)
    // ------------------------------------------------------------------
    function attachDragEvents(card) {
        card.addEventListener("dragstart", function () {
            draggedCard = card;
            // Add the "dragging" class on the next tick so the drag image
            // is captured before the card's opacity changes
            setTimeout(() => card.classList.add("dragging"), 0);
        });

        card.addEventListener("dragend", function () {
            card.classList.remove("dragging");
            draggedCard = null;
        });

        // Clicking a card opens the edit modal (as long as it's not a drag)
        card.addEventListener("click", function () {
            openEditModal(card.dataset.dealId);
        });
    };

    document.querySelectorAll(".pipeline-card").forEach(attachDragEvents);

    document.querySelectorAll(".pipeline-cards").forEach(function (column) {
        column.addEventListener("dragover", function (e) {
            e.preventDefault();
            column.classList.add("drag-over");

            // Figure out where in the column the dragged card should land
            const afterElement = getDragAfterElement(column, e.clientY);

            if (!draggedCard) return;

            if (afterElement == null) {
                column.appendChild(draggedCard);
            } else {
                column.insertBefore(draggedCard, afterElement);
            };
        });

        column.addEventListener("dragleave", function () {
            column.classList.remove("drag-over");
        });

        column.addEventListener("drop", function (e) {
            e.preventDefault();
            column.classList.remove("drag-over");

            if (!draggedCard) return;

            const dealId = draggedCard.dataset.dealId;
            const newStageId = column.dataset.stageId;

            // Work out the card's new order based on its position in the DOM
            const cardsInColumn = Array.from(column.querySelectorAll(".pipeline-card"));
            const newOrder = cardsInColumn.indexOf(draggedCard);

            moveDeal(dealId, newStageId, newOrder);
        });
    });

    // Determine the card the dragged element should be placed before
    function getDragAfterElement(column, y) {
        const draggableElements = [...column.querySelectorAll(".pipeline-card:not(.dragging)")];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;

            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            };
        }, { offset: Number.NEGATIVE_INFINITY, element: null }).element;
    };

    // ------------------------------------------------------------------
    // Send the card move to the backend
    // ------------------------------------------------------------------
    function moveDeal(dealId, stageId, order) {
        fetch(`/api/deals/${dealId}/move`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify({ stage_id: stageId, order: order })
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                alert("The card could not be transferred. Please refresh the page.");
            };
        })
        .catch(() => alert("Error connecting to the server."));
    };

    // ------------------------------------------------------------------
    // MOBILE FALLBACK: "◀" / "▶" buttons instead of drag & drop
    // ------------------------------------------------------------------
    function addMobileMoveButtons() {
        const stageIds = Array.from(document.querySelectorAll(".pipeline-column"))
            .map(col => col.dataset.stageId);

        document.querySelectorAll(".pipeline-card").forEach(card => {
            // Always remove the old wrapper and rebuild the buttons from scratch.
            // The old listeners kept a stale currentIndex / targetStageId in their
            // closure from when they were first attached, so after one move the
            // buttons would stop working correctly until the page was refreshed.
            const oldWrapper = card.querySelector(".move-buttons");
            if (oldWrapper) oldWrapper.remove();

            const currentColumn = card.closest(".pipeline-cards");
            const currentStageId = currentColumn.dataset.stageId;
            const currentIndex = stageIds.indexOf(currentStageId);

            const btnWrapper = document.createElement("div");
            btnWrapper.className = "move-buttons";

            // "Move to previous stage" button
            const prevBtn = document.createElement("button");
            prevBtn.type = "button";
            prevBtn.className = "btn btn-outline-primary p-1";
            prevBtn.innerHTML = '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m5 15 7-7 7 7"/></svg>';
            prevBtn.disabled = currentIndex === 0;
            prevBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                const targetStageId = stageIds[currentIndex - 1];
                moveDeal(card.dataset.dealId, targetStageId, 0);
                relocateCardInDom(card, targetStageId);
            });

            // "Move to next stage" button
            const nextBtn = document.createElement("button");
            nextBtn.type = "button";
            nextBtn.className = "btn btn-outline-primary p-1";
            nextBtn.innerHTML = '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/></svg>';
            nextBtn.disabled = currentIndex === stageIds.length - 1;
            nextBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                const targetStageId = stageIds[currentIndex + 1];
                moveDeal(card.dataset.dealId, targetStageId, 0);
                relocateCardInDom(card, targetStageId);
            });

            btnWrapper.appendChild(prevBtn);
            btnWrapper.appendChild(nextBtn);
            card.appendChild(btnWrapper);
        });
    };

    function relocateCardInDom(card, targetStageId) {
        const targetColumn = document.querySelector(`.pipeline-cards[data-stage-id="${targetStageId}"]`);

        if (targetColumn) {
            targetColumn.appendChild(card);
            addMobileMoveButtons(); // refresh button state (disabled at the edges)
        };
    };

    addMobileMoveButtons();

    // ------------------------------------------------------------------
    // DEAL EDIT MODAL
    // ------------------------------------------------------------------
    const editModalEl = document.getElementById("editDealModal");
    const editModal = new bootstrap.Modal(editModalEl);

    // Fetch the deal's data and populate the edit modal fields
    function openEditModal(dealId) {
        fetch(`/api/deals/${dealId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById("editDealId").value = data.id;
                document.getElementById("editDealTitle").value = data.title;
                document.getElementById("editDealDescription").value = data.description || "";
                document.getElementById("editDealValue").value = data.value;
                document.getElementById("editDealPriority").value = data.priority;
                document.getElementById("editDealDueDate").value = data.due_date || "";
                updateToggleCompleteBtn(data.is_closed);
                editModal.show();
            });
    };

    // ------------------------------------------------------------------
    // "COMPLETED" / "CONTINUE" BUTTON
    // ------------------------------------------------------------------
    const toggleCompleteBtn = document.getElementById("toggleCompleteBtn");

    // Update the button's label/style based on the deal's current status
    function updateToggleCompleteBtn(isClosed) {
        toggleCompleteBtn.dataset.isClosed = isClosed ? "true" : "false";

        if (isClosed) {
            toggleCompleteBtn.textContent = "Continue";
            toggleCompleteBtn.classList.remove("btn-outline-success");
            toggleCompleteBtn.classList.add("btn-outline-secondary", "btn-edit");
        } else {
            toggleCompleteBtn.textContent = "Completed";
            toggleCompleteBtn.classList.remove("btn-outline-secondary", "btn-edit");
            toggleCompleteBtn.classList.add("btn-outline-success");
        };
    };

    toggleCompleteBtn.addEventListener("click", function () {
        const dealId = document.getElementById("editDealId").value;

        // First save the edited fields (same as "Save changes"),
        // only then toggle the completion status.
        saveDeal(dealId)
            .then(saveData => {
                if (!saveData.success) {
                    alert("The changes could not be saved.");
                    return Promise.reject();
                };

                return toggleDealComplete(dealId);
            })
            .then(toggleData => {
                if (!toggleData || !toggleData.success) {
                    alert("The deal status could not be updated.");
                    return;
                };

                location.reload(); // refresh the view, same as after "Save changes"
            })
            .catch(() => {});
    });

    function toggleDealComplete(dealId) {
        return fetch(`/api/deals/${dealId}/toggle-complete`, {
            method: "POST",
            headers: { "X-CSRFToken": CSRF_TOKEN }
        }).then(res => res.json());
    };

    // ------------------------------------------------------------------
    // SAVE THE DEAL EDIT FORM
    // ------------------------------------------------------------------

    // Collect the current values from the edit form fields
    function getDealFormPayload() {
        return {
            title: document.getElementById("editDealTitle").value,
            description: document.getElementById("editDealDescription").value,
            value: document.getElementById("editDealValue").value,
            priority: document.getElementById("editDealPriority").value,
            due_date: document.getElementById("editDealDueDate").value,
        };
    };

    function saveDeal(dealId) {
        return fetch(`/api/deals/${dealId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify(getDealFormPayload())
        }).then(res => res.json());
    };

    document.getElementById("saveDealBtn").addEventListener("click", function () {
        const dealId = document.getElementById("editDealId").value;

        saveDeal(dealId).then(data => {
            if (data.success) {
                location.reload(); // simplest way to refresh the card view
            } else {
                alert("Nie udało się zapisać zmian.");
            };
        });
    });

    document.getElementById("deleteDealBtn").addEventListener("click", function () {
        const dealId = document.getElementById("editDealId").value;
        if (!confirm("Are you sure you want to delete this deal?")) return;

        fetch(`/api/deals/${dealId}/delete`, {
            method: "POST",
            headers: { "X-CSRFToken": CSRF_TOKEN }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            };
        });
    });
});