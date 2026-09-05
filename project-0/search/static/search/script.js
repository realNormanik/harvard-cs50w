async function fetchCountry() {
    try {
        // Fetch the user's IP-based location data from the API
        const response = await fetch('https://api.my-ip.io/v2/ip.json');

        // If the fetch fails, throw an error
        if (!response.ok) {
            throw new Error('Failed to fetch country');
        };

        // Parse the response as JSON and extract the country name
        const data = await response.json();
        const country = data.country.name;

        // Update the content of the "country" element with the detected country
        document.getElementById('country').textContent = `${country}`;
    } catch (error) {
        // If an error occurs, display a fallback message and log the error
        document.getElementById('country').textContent = 'Could not detect your location.';
        console.error(error);
    };
};

// Immediately call the fetchCountry function to fetch location on page load
fetchCountry();


document.addEventListener('DOMContentLoaded', function () {
    // Reference to the clickable theme toggle element and to <html>
    const toggleButton = document.querySelector('#theme-toggle');
    const root = document.documentElement;

    // The Theme Update Feature
    function updateTheme(isDark) {
        root.setAttribute('data-theme', isDark ? 'dark' : 'light');
        toggleButton.textContent = `Theme: ${isDark ? 'dark' : 'light'}`;
    }

    // Reading and Using a Saved Theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    const isDarkTheme = savedTheme === 'dark';
    updateTheme(isDarkTheme);

    // Monitoring clicks on the toggle and switching themes
    toggleButton.addEventListener('click', function () {
        const isDark = root.getAttribute('data-theme') !== 'dark';
        updateTheme(isDark);

        // Saving the current theme to localStorage
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});


// Keyboard script
const keyboardContainer = document.getElementById('keyboard-container');
const searchInput = document.getElementById('search-input');
const keyboardToggle = document.getElementById('keyboard-toggle');
let keyboard;

if (keyboardToggle) {
    // Toggle keyboard visibility
    keyboardToggle.addEventListener('click', () => {
        if (keyboardContainer.style.display === 'none' || !keyboardContainer.style.display) {
            keyboardContainer.style.display = 'block';
            
            if (!keyboard) initKeyboard();
        } else {
            keyboardContainer.style.display = 'none';
        };
    });

    // Initialize the virtual keyboard
    function initKeyboard() {
        keyboard = new SimpleKeyboard.default({
            onChange: input => searchInput.value = input,
            onKeyPress: button => handleKeyPress(button),
            inputName: "default",
            theme: "hg-theme-default hg-layout-default",
            debug: true
        });
    };

    // Handle special keypresses
    function handleKeyPress(button) {
        if (button === "{shift}") {
            toggleShift();
        };
    };

    function toggleShift() {
        const currentLayout = keyboard.options.layoutName;
    
        keyboard.setOptions({
            layoutName: currentLayout === "default" ? "shift" : "default"
        });
    };

    const popup = document.getElementById('keyboard-popup');
    const popupHeader = document.getElementById('keyboard-popup-header');
    let offsetX = 0, offsetY = 0, isDragging = false;

    // Show the popup when toggling keyboard
    keyboardToggle.addEventListener('click', () => {
        popup.style.display = popup.style.display === 'none' || !popup.style.display ? 'block' : 'none';
    
        if (!keyboard) initKeyboard();
    });

    // Drag functionality
    popupHeader.addEventListener('mousedown', (e) => {
        isDragging = true;
        offsetX = e.clientX - popup.offsetLeft;
        offsetY = e.clientY - popup.offsetTop;
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            popup.style.left = `${e.clientX - offsetX}px`;
            popup.style.top = `${e.clientY - offsetY}px`;
        };
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
    });

    const popupCloseButton = document.getElementById('popup-close');

    // Close the popup when clicking the "X" button
    popupCloseButton.addEventListener('click', () => {
        popup.style.display = 'none';
    });
};


// Microphone icon selection
const microphoneIcon = document.querySelector('.icon.microphone');

if (microphoneIcon) {
    // Check for Web Speech API availability
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        // Speech recognition configuration
        recognition.lang = 'en-US'; // You can change this to 'pl-PL' for Polish language
        recognition.interimResults = false; // Only final results
        recognition.maxAlternatives = 1; // Number of alternative results

        // Handle microphone icon click
        microphoneIcon.addEventListener('click', () => {
            recognition.start(); // Start speech recognition
        });

        // When speech is recognized
        recognition.addEventListener('result', (event) => {
            const spokenText = event.results[0][0].transcript; // Retrieve recognized text

            searchInput.value = spokenText; // Insert text into the search field
            console.log(`Recognized text: ${spokenText}`);
        });

        // Handle recognition errors
        recognition.addEventListener('error', (event) => {
            console.error('Speech recognition error:', event.error);
            alert('Failed to recognize speech. Please try again.');
        });
    } else {
        // If the API is not supported
        console.warn('Web Speech API is not supported in this browser.');

        microphoneIcon.addEventListener('click', () => {
            alert('Speech recognition is not supported in this browser.');
        });
    };
};


const lensIcon = document.getElementById('lens-icon');
const closeIcon = document.getElementById('close-icon');
const searchBarLens = document.querySelector('.lens-search');

if (lensIcon) {
    lensIcon.addEventListener('click', () => {
        searchBarLens.style.display = 'flex';
    });

    closeIcon.addEventListener('click', () => {
        searchBarLens.style.display = 'none';
    });

    document.addEventListener('DOMContentLoaded', function () {
        // Retrieve the input element with the id 'lens-input'
        const lensInput = document.getElementById("lens-input");

        // Listen for keydown events in the input field
        lensInput.addEventListener("keydown", function (event) {
            // Check if the Enter key was pressed
            if (event.key === "Enter") {
                const imageUrl = lensInput.value;

                if (imageUrl) {
                    // Construct the full URL for Google Lens
                    const lensUrl = `https://lens.google.com/uploadbyurl?url=${encodeURIComponent(imageUrl)}`;

                    // Decode the URL for better readability in the console
                    const decodedUrl = decodeURIComponent(lensUrl);

                    // Open the link in a new tab
                    window.open(lensUrl, "_blank");
                } else {
                    console.log("Image url not found.");
                };
            };
        });
    });
};