document.addEventListener("DOMContentLoaded", function () {
    // Grab the search input and the container where results will be rendered
    const searchInput = document.getElementById("clientSearchInput");
    const resultsBox = document.getElementById("clientSearchResults");

    // Bail out if either element is missing from the page
    if (!searchInput || !resultsBox) return;

    let debounceTimer;

    searchInput.addEventListener("input", function () {
        // Reset the debounce timer on every keystroke
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        // Don't search for very short queries — clear any previous results
        if (query.length < 2) {
            resultsBox.innerHTML = "";
            return;
        };

        debounceTimer = setTimeout(() => {
            // Fetch matching clients from the API
            fetch(`/api/clients/search?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    // Clear previous results before rendering new ones
                    resultsBox.innerHTML = "";
                    data.results.forEach(client => {
                        // Build a clickable list item for each matching client
                        const item = document.createElement("button");
                        item.type = "button";
                        item.className = "list-group-item list-group-item-action";
                        item.textContent = client.name;
                        item.addEventListener("click", () => {
                            // On selection, store the client id, fill the input,
                            // and close the results list
                            document.getElementById("selectedClientId").value = client.id;
                            searchInput.value = client.name;
                            resultsBox.innerHTML = "";
                        });
                        resultsBox.appendChild(item);
                    });
                });
        }, 300); // 300ms debounce so we don't hit the server on every keystroke
    });

    // Close the results list when clicking outside of it
    document.addEventListener("click", function (e) {
        if (!resultsBox.contains(e.target) && e.target !== searchInput) {
            resultsBox.innerHTML = "";
        };
    });
});