document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const html = document.documentElement;
    const logo = document.querySelector(".logo");

    // Function to update the theme
    function updateTheme(isDark) {
        if (isDark) {
            html.setAttribute("data-theme", "dark");
            themeToggle.textContent = "Theme: dark";
            logo.src = "/static/encyclopedia/logo-dark.webp";
            logo.alt = "Encyclopedia dark mode";
        } else {
            html.setAttribute("data-theme", "light");
            themeToggle.textContent = "Theme: light";
            logo.src = "/static/encyclopedia/logo-light.webp";
            logo.alt = "Encyclopedia light mode";
        };
    };

    // Check and apply the saved theme preference from localStorage
    const savedTheme = localStorage.getItem("theme");
    const isDarkTheme = savedTheme === "dark";
    updateTheme(isDarkTheme);

    // Add a click event listener to toggle between dark and light themes
    themeToggle.addEventListener("click", function () {
        const isDark = html.getAttribute("data-theme") !== "dark";

        updateTheme(isDark);

        // Save the current theme preference to localStorage
        localStorage.setItem("theme", isDark ? "dark" : "light");
    });
});