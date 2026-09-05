document.addEventListener('DOMContentLoaded', function () {
    // Wait for the DOM to fully load before attaching event listeners

    document.querySelectorAll('button').forEach(button => {
        // Attach click event listener to each button

        button.onclick = function (event) {
            const element = event.currentTarget; // Reference to the clicked button

            if (event.target.closest(".button-edit")) {
                // If the clicked button is an edit button
                console.log(`Edit button clicked. Post number: ${button.parentElement.parentElement.dataset.id}`);

                const id = button.parentElement.parentElement.dataset.id; // Post ID
                const tweetTextElement = button.parentElement.querySelector("#tweetText"); // Text of the tweet
                const editTextArea = button.parentElement.querySelector("#edit_text"); // Edit textarea (if exists)

                if (button.innerText.trim() === "Edit") {
                    // If the button is in "Edit" state
                    const originalText = tweetTextElement.innerText; // Get the original text
                    tweetTextElement.innerHTML = `<textarea id="edit_text">${originalText}</textarea>`; // Replace text with a textarea
                    button.innerHTML = 'Save'; // Change button text to "Save"
                } else if (button.innerText.trim() === "Save") {
                    // If the button is in "Save" state
                    const newTweet = editTextArea.value; // Get the new text from textarea

                    fetch(`/edit/${id}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ tweet: newTweet }) // Send the new tweet text
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(`Edited text: ${result.new_text}`);
                        tweetTextElement.innerHTML = result.new_text; // Update the displayed text
                        button.innerHTML = '<i class="fa-regular fa-pen-to-square"></i>&nbsp;Edit'; // Reset button text
                    })
                    .catch(error => console.error("Error editing post:", error));
                };
            } else if (event.target.closest(".button-delete")) {
                // If the clicked button is a delete button
                console.log(`Delete button clicked. Post number: ${button.parentElement.parentElement.dataset.id}`);

                const id = button.parentElement.parentElement.dataset.id; // Post ID

                if (confirm("Are you sure you want to delete this post?")) {
                    // Confirm deletion
                    fetch(`/delete/${id}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log(`Post ${id} deleted successfully.`);
                            const postElement = button.closest('.post'); // Find the post element
                            if (postElement) {
                                postElement.remove(); // Remove the post from the DOM
                            }
                        } else {
                            console.error("Failed to delete post.");
                        }
                    })
                    .catch(error => console.error("Error deleting post:", error));
                }
            } else if (element.classList.contains("button-secondary") || element.classList.contains("button-like")) {
                // If the clicked button is a like button
                console.log(`Like button clicked. Post number: ${this.parentElement.parentElement.dataset.id}`);

                const id = this.parentElement.parentElement.dataset.id; // Post ID

                fetch(`/like/${id}`, {
                    method: 'POST'
                })
                .then(response => {
                    like(element); // Update the like button state
                });
            } else if (element.classList.contains("button-follow") || element.classList.contains("button-following") || element.classList.contains("button-unfollow")) {
                // If the clicked button is a follow/unfollow button
                const button = element; // Reference to the button
                const userId = document.querySelector('h2').dataset.id; // User ID
                console.log(`User number ${userId}`);

                if (button.classList.contains("button-follow")) {
                    // If it's a follow button
                    console.log("Follow button clicked");

                    fetch(`/follow/${userId}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            button.innerHTML = "Following"; // Update button text
                            button.className = "button-following"; // Update button class
                            location.reload();
                        });
                } else if (button.classList.contains("button-unfollow")) {
                    // If it's an unfollow button
                    console.log("Unfollow button clicked");

                    fetch(`/follow/${userId}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            button.innerHTML = "Follow"; // Update button text
                            button.className = "button-follow"; // Update button class
                            location.reload();
                        });
                };
            };
        };

        // Handle mouseover event for follow button
        button.onmouseover = function (event) {
            const element = event.currentTarget;

            if (element.classList.contains("button-following")) {
                element.innerHTML = "Unfollow"; // Temporarily change button text to "Unfollow"
                element.className = "button-unfollow"; // Change button class
            };
        };

        // Handle mouseout event for follow button
        button.onmouseout = function (event) {
            const element = event.currentTarget;

            if (element.classList.contains("button-unfollow")) {
                element.innerHTML = "Following"; // Reset button text to "Following"
                element.className = "button-following"; // Reset button class
            }
        };
    });

    // Ensure initial follow button state is consistent
    const followButton = document.querySelector('button.button-unfollow');

    if (followButton) {
        followButton.innerHTML = "Following"; // Set button text
        followButton.className = "button-following"; // Set button class
    };
});

// Utility function to get a cookie value by name
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            };
        };
    };

    return cookieValue;
};

// Function to toggle like/unlike state
function like(tweet) {
    var likesElement = tweet.querySelector("#number"); // Element displaying like count
    var likes = parseInt(likesElement.innerHTML); // Current like count

    if (tweet.classList.contains("button-secondary")) {
        // If currently unliked
        tweet.className = "button-like"; // Update button class
        likes++; // Increment likes
        tweet.querySelector("i").className = "fa-solid fa-heart"; // Change icon to filled heart
    } else {
        // If currently liked
        tweet.className = "button-secondary"; // Update button class
        likes--; // Decrement likes
        tweet.querySelector("i").className = "fa-regular fa-heart"; // Change icon to outlined heart
    };

    likesElement.innerHTML = likes; // Update displayed like count
};

document.addEventListener("DOMContentLoaded", () => {
    const registerButton = document.getElementById("button-register");
    const loginButton = document.getElementById("button-login");
    const registerModal = document.getElementById("popup-register");
    const loginModal = document.getElementById("popup-login");
    const modalElements = [registerModal, loginModal, document.getElementById("popup-post")];

    // Helper function to close all modals
    const closeAllModals = () => {
        modalElements.forEach((modal) => {
            if (modal) modal.style.display = "none";
        });
    };

    // Ensure all modals are closed on page load
    closeAllModals();

    if (registerButton) {
        registerButton.addEventListener("click", (event) => {
            event.preventDefault();
            closeAllModals(); // Close other modals
            if (registerModal) registerModal.style.display = "flex";
        });
    };

    if (loginButton) {
        loginButton.addEventListener("click", (event) => {
            event.preventDefault();
            closeAllModals(); // Close other modals
            if (loginModal) loginModal.style.display = "flex";
        });
    };

    // Add event listeners to all close buttons
    document.querySelectorAll("#close-popup").forEach((closeButton) => {
        closeButton.addEventListener("click", () => {
            closeAllModals(); // Close all modals
        });
    });

    window.addEventListener("click", (event) => {
        if (event.target === registerModal) {
            registerModal.style.display = "none";
        };

        if (event.target === loginModal) {
            loginModal.style.display = "none";
        };
    });

    // Additional code for the "post" modal
    const postButton = document.querySelector(".nav-button");
    const postModal = document.getElementById("popup-post");
    const closeModalIcon = document.querySelector(".fa-solid.fa-xmark");

    if (postButton) {
        postButton.addEventListener("click", (event) => {
            event.preventDefault();
            closeAllModals(); // Close other modals
            if (postModal) postModal.style.display = "flex";
        });
    };

    if (closeModalIcon) {
        closeModalIcon.addEventListener("click", () => {
            if (postModal) postModal.style.display = "none";
        });
    };

    if (postModal) {
        window.addEventListener("click", (event) => {
            if (event.target === postModal) {
                postModal.style.display = "none";
            };
        });
    };

    const editProfileButton = document.getElementById('edit-profile-button');
    const editProfilePopup = document.getElementById('edit-profile-popup');
    const closeButton = document.getElementById('close-popup');

    if (editProfileButton) {
        editProfileButton.onclick = function() {
            editProfilePopup.style.display = "flex";
        };
    };

    closeButton.onclick = function() {
        editProfilePopup.style.display = "none";
    };

    // Close the popup if the user clicks outside of it
    window.onclick = function(event) {
        if (event.target === editProfilePopup) {
            editProfilePopup.style.display = "none";
        };
    };
});

document.addEventListener('DOMContentLoaded', () => {
    // Wait for the DOM to fully load before executing the code

    const path = window.location.pathname; // Get the current page's path
    const hiddenPaths = ['/register', '/login']; // List of paths where header and footer should be hidden

    if (hiddenPaths.includes(path)) {
        // Check if the current path matches any in the hiddenPaths list

        const header = document.querySelector('header'); // Select the <header> element
        const footer = document.querySelector('footer'); // Select the <footer> element

        if (header) header.style.display = 'none'; // Hide the header if it exists
        if (footer) footer.style.display = 'none'; // Hide the footer if it exists

        const body = document.querySelector('.body'); // Select the element with the class "body"
        if (body) body.style.minWidth = '100%'; // Adjust the body's minimum width to occupy the full screen
    };
});

document.addEventListener('DOMContentLoaded', () => {
    import('https://cdn.jsdelivr.net/npm/@joeattardi/emoji-button@latest/dist/index.min.js')
        .then(({ EmojiButton }) => {
            const button = document.querySelector('#emoji-button');
            const textarea = document.querySelector('#post-textarea');
            const picker = new EmojiButton({
                theme: 'dark',
                position: 'bottom-start',
            });

            button.addEventListener('click', (event) => {
                event.preventDefault();
                picker.togglePicker(button);
            });

            picker.on('emoji', (emoji) => {
                textarea.value += emoji.emoji;
            });
        })
        .catch((error) => {
            console.error('EmojiButton failed to load:', error);
        });
});

function setActiveLabel(inputId) {
    // Activate the label for the specified input field by adding the "active" class

    const label = document.querySelector(`label[for="${inputId}"]`); // Select the label associated with the input field
    if (label) {
        label.classList.add('active'); // Add the "active" class to the label if it exists
    };
};

function checkInput(inputId) {
    // Check if the input field is not empty and toggle the "active" class on its label accordingly

    const input = document.getElementById(inputId); // Get the input field by its ID
    const label = document.querySelector(`label[for="${inputId}"]`); // Select the label associated with the input field

    if (input.value.trim() !== '') {
        // If the input field is not empty, add the "active" class to the label
        label.classList.add('active');
    } else {
        // If the input field is empty, remove the "active" class from the label
        label.classList.remove('active');
    };
};

document.addEventListener('DOMContentLoaded', () => {
    // Check if the element with ID 'profile-picture-input' exists
    const profilePictureInput = document.getElementById('profile-picture-input');

    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function(event) {
            const file = event.target.files[0]; // Get the selected file
        
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Check if the element 'profile-picture-preview' exists
                    const profilePicturePreview = document.getElementById('profile-picture-preview');
                    if (profilePicturePreview) {
                        // Update the src of the image preview
                        profilePicturePreview.src = e.target.result;
                    };
                };
                reader.readAsDataURL(file); // Convert file to Data URL
            };
        });
    };

    // Check if the element with ID 'close-popup' exists
    const closePopupButton = document.getElementById('close-popup');

    if (closePopupButton) {
        closePopupButton.addEventListener('click', function() {
            const editProfilePopup = document.getElementById('edit-profile-popup');
            
            if (editProfilePopup) {
                editProfilePopup.style.display = 'none';
            };
        });
    };
});

document.addEventListener('DOMContentLoaded', () => {
    // Wait for the DOM to fully load before attaching event listeners

    // Attach an event listener to the image input field
    document.getElementById('image-input').addEventListener('change', function(event) {
        const imageInput = event.target; // Reference to the input element
        const previewContainer = document.getElementById('image-preview-container'); // Container for the image preview
        const previewImage = document.getElementById('image-preview'); // Image element for displaying the preview

        if (imageInput.files && imageInput.files[0]) {
            // If a file is selected in the input field
            const file = imageInput.files[0]; // Get the selected file
            const reader = new FileReader(); // Create a FileReader to read the file

            reader.onload = function(e) {
                // When the file is loaded, set the preview image's source to the file's data URL
                previewImage.src = e.target.result;
                previewContainer.style.display = 'flex'; // Show the preview container
                previewContainer.style.justifyContent = 'center';
            };

            reader.readAsDataURL(file); // Read the file as a data URL
        } else {
            // If no file is selected, hide the preview container and clear the preview image
            previewContainer.style.display = 'none';
            previewImage.src = '';
        };
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Wait for the DOM to fully load before attaching event listeners

    // Attach an event listener to the image icon button
    document.getElementById('image-icon-button').addEventListener('click', function() {
        document.getElementById('image-input').click(); 
        // Simulate a click on the hidden file input when the button is clicked
    });

    // Attach an event listener to handle changes in the image input field
    document.getElementById('image-input').addEventListener('change', function(event) {
        const imageInput = event.target; // Reference to the input element
        const previewContainer = document.getElementById('image-preview-container'); // Container for the image preview
        const previewImage = document.getElementById('image-preview'); // Image element for displaying the preview

        if (imageInput.files && imageInput.files[0]) {
            // If a file is selected in the input field
            const file = imageInput.files[0]; // Get the selected file
            const reader = new FileReader(); // Create a FileReader to read the file

            reader.onload = function(e) {
                // When the file is loaded, set the preview image's source to the file's data URL
                previewImage.src = e.target.result;
                previewContainer.style.display = 'flex'; // Show the preview container
                previewContainer.style.justifyContent = 'center';
            };

            reader.readAsDataURL(file); // Read the file as a data URL
        } else {
            // If no file is selected, hide the preview container and clear the preview image
            previewContainer.style.display = 'none';
            previewImage.src = '';
        };
    });
});