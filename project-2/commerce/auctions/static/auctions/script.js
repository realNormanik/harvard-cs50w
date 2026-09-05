function setActiveLabel(inputId) {
    const label = document.querySelector(`label[for="${inputId}"]`);
    if (label) {
        label.classList.add("active");
    };
};

function checkInput(inputId) {
    const input = document.getElementById(inputId);
    const label = document.querySelector(`label[for="${inputId}"]`);
    if (input.value.trim() !== "") {
        label.classList.add("active");
    } else {
        label.classList.remove("active");
    };
};

document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#emoji-button");
    if (!button) return;
    
    import("https://cdn.jsdelivr.net/npm/@joeattardi/emoji-button@latest/dist/index.min.js")
        .then(({ EmojiButton }) => {
            const button = document.querySelector("#emoji-button");
            const textarea = document.querySelector("#id_comment");
            const picker = new EmojiButton({
                theme: "dark",
                position: "bottom-start",
            });

            button.addEventListener("click", (event) => {
                event.preventDefault();
                picker.togglePicker(button);
            });

            picker.on("emoji", (emoji) => {
                textarea.value += emoji.emoji;
            });
        })
        .catch((error) => {
            console.error("EmojiButton failed to load:", error);
        });
});

document.addEventListener("DOMContentLoaded", function () {
    const imageIcon = document.getElementById("image-comment-icon");
    const imageInput = document.querySelector("input[name='image']");

    if (imageIcon && imageInput) {
        imageIcon.addEventListener("click", function () {
            imageInput.click();
        });

        imageInput.addEventListener("change", function () {
            if (this.files.length > 0) {
                alert(`Selected file: ${this.files[0].name}`);
            };
        });
    };
});

document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("image-input");
    const imageIcon = document.getElementById("image-upload-empty");
    const imagePreview = document.getElementById("image-preview");
    const uploadContainer = document.getElementById("image-upload-container");

    if (uploadContainer) {
        // Handle click on the icon to trigger file input
        uploadContainer.addEventListener("click", () => {
            imageInput.click();
        });
    };
    

    if (imageInput) {
        // Handle file input change to update preview
        imageInput.addEventListener("change", function () {
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    // Hide the icon and show the preview
                    imageIcon.style.display = "none";
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = "block";
                };
        
                reader.readAsDataURL(file);
            } else {
                // Show the icon and hide the preview if no file is selected
                imageIcon.style.display = "block";
                imagePreview.style.display = "none";
            };
        });
    };
});