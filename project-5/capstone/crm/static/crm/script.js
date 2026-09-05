document.addEventListener('DOMContentLoaded', function () {
    // References to the checkbox inside the switch and to the <html> element
    const toggleInput = document.querySelector('#theme-toggle .input');
    const root = document.documentElement;
 
    // The Theme Update Feature
    function updateTheme(isDark) {
        root.setAttribute('data-theme', isDark ? 'dark' : 'light');
        toggleInput.checked = isDark;
    };
 
    // Reading and Using a Saved Theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    const isDarkTheme = savedTheme === 'dark';
    updateTheme(isDarkTheme);
 
    // Monitoring changes to the checkbox state and switching themes
    toggleInput.addEventListener('change', function () {
        const isDark = toggleInput.checked;
        updateTheme(isDark);
 
        // Saving the current theme to localStorage
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});