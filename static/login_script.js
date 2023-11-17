// document.addEventListener('DOMContentLoaded', function () {
//     // Get references to the button, overlay, and login form container
//     var loginButton = document.getElementById("loginDropdownButton");
//     var overlay = document.getElementById("overlay");
//     var loginContainer = document.getElementById("loginDropdownContainer");

//     // Attach a click event listener to the button
//     loginButton.addEventListener('click', function () {
//         toggleLoginDropdown();
//     });

//     // Attach a click event listener to the overlay to hide the login form
//     overlay.addEventListener('click', function () {
//         hideLoginDropdown();
//     });

//     // Initially hide the login form and overlay
//     loginContainer.style.display = "none";
//     overlay.style.display = "none";
// });

// function toggleLoginDropdown() {
//     var loginContainer = document.getElementById("loginDropdownContainer");
//     var overlay = document.getElementById("overlay");

//     loginContainer.style.display = "inline";
//     overlay.style.display = "block";
// }

// function hideLoginDropdown() {
//     var loginContainer = document.getElementById("loginDropdownContainer");
//     var overlay = document.getElementById("overlay");

//     loginContainer.style.display = "none";
//     overlay.style.display = "none";
// }




document.addEventListener('DOMContentLoaded', function () {
    var loginButton = document.getElementById("loginDropdownButton");
    var overlay = document.getElementById("overlay");
    var loginContainer = document.getElementById("loginDropdownContainer");

    loginButton.addEventListener('click', function (event) {
        event.stopPropagation();
        toggleLoginDropdown();
    });

    overlay.addEventListener('click', function () {
        hideLoginDropdown();
    });

    document.addEventListener('click', function (event) {
        if (!loginContainer.contains(event.target) || isFormElement(event.target)) {
            hideLoginDropdown();
        }
    });

    // Add a click event listener to input elements to stop propagation
    var inputElements = document.querySelectorAll('#loginDropdownContainer input');
    inputElements.forEach(function (inputElement) {
        inputElement.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    function isFormElement(target) {
        return (
            target.tagName.toLowerCase() === "input" ||
            target.tagName.toLowerCase() === "button" ||
            (target.parentNode && isFormElement(target.parentNode))
        );
    }

    loginContainer.style.display = "none";
    overlay.style.display = "none";
});

function toggleLoginDropdown() {
    var loginContainer = document.getElementById("loginDropdownContainer");
    var overlay = document.getElementById("overlay");

    loginContainer.style.display = (loginContainer.style.display === "none" || loginContainer.style.display === "") ? "inline" : "none";
    overlay.style.display = (overlay.style.display === "none" || overlay.style.display === "") ? "block" : "none";
}

function hideLoginDropdown() {
    var loginContainer = document.getElementById("loginDropdownContainer");
    var overlay = document.getElementById("overlay");

    loginContainer.style.display = "none";
    overlay.style.display = "none";
}

