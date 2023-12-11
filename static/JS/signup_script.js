document.addEventListener('DOMContentLoaded', function () {
    // Get references to the button, overlay, and login form container
    var loginButton = document.getElementById("loginDropdownButton");
    var overlay = document.getElementById("overlay");
    var loginContainer = document.getElementById("loginDropdownContainer");

    // Attach a click event listener to the button
    loginButton.addEventListener('click', function () {
        toggleLoginDropdown();
    });

    // Attach a click event listener to the overlay to hide the login form
    overlay.addEventListener('click', function () {
        hideLoginDropdown();
    });

    // Initially hide the login form and overlay
    loginContainer.style.display = "none";
    overlay.style.display = "none";
});

function toggleLoginDropdown() {
    var loginContainer = document.getElementById("loginDropdownContainer");
    var overlay = document.getElementById("overlay");

    loginContainer.style.display = "inline";
    overlay.style.display = "block";
}

function hideLoginDropdown() {
    var loginContainer = document.getElementById("loginDropdownContainer");
    var overlay = document.getElementById("overlay");

    loginContainer.style.display = "none";
    overlay.style.display = "none";
}



