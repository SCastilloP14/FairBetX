// document.addEventListener('DOMContentLoaded', function () {
//     var loginButton = document.getElementById("startBettingDropdownButton");
//     var overlay = document.getElementById("startBettingOverlay");
//     var loginContainer = document.getElementById("startBettingDropdownContainer");

//     loginButton.addEventListener('click', function (event) {
//         event.stopPropagation();
//         toggleLoginDropdown();
//     });

//     overlay.addEventListener('click', function () {
//         hideLoginDropdown();
//     });

//     document.addEventListener('click', function (event) {
//         if (!loginContainer.contains(event.target) || isFormElement(event.target)) {
//             hideLoginDropdown();
//         }
//     });

//     // Add a click event listener to input elements to stop propagation
//     var inputElements = document.querySelectorAll('#loginDropdownContainer input');
//     inputElements.forEach(function (inputElement) {
//         inputElement.addEventListener('click', function (event) {
//             event.stopPropagation();
//         });
//     });

//     function isFormElement(target) {
//         return (
//             target.tagName.toLowerCase() === "input" ||
//             target.tagName.toLowerCase() === "button" ||
//             (target.parentNode && isFormElement(target.parentNode))
//         );
//     }

//     loginContainer.style.display = "none";
//     overlay.style.display = "none";
// });

// function toggleLoginDropdown() {
//     var loginContainer = document.getElementById("loginDropdownContainer");
//     var overlay = document.getElementById("overlay");

//     loginContainer.style.display = (loginContainer.style.display === "none" || loginContainer.style.display === "") ? "inline" : "none";
//     overlay.style.display = (overlay.style.display === "none" || overlay.style.display === "") ? "block" : "none";
// }

// function hideLoginDropdown() {
//     var loginContainer = document.getElementById("loginDropdownContainer");
//     var overlay = document.getElementById("overlay");

//     loginContainer.style.display = "none";
//     overlay.style.display = "none";
// }



document.addEventListener('DOMContentLoaded', function () {
    var loginButton = document.getElementById("loginDropdownButton");
    var overlayDropdown = document.getElementById("overlayDropdown");
    var loginCardContainer = document.getElementById("loginCardContainer");
    var loginCancelButton = document.getElementById("loginCancelButton");


    // Initially hide the loginDropdownContainer
    loginCardContainer.style.display = "none";
    overlayDropdown.style.display = "none";

    loginCancelButton.addEventListener('click', function ()  {
        closingDropdown();
        console.log("Clicked Cancel");
    });

    loginButton.addEventListener('click', function () {
        toggleDropdown();
    });

    

});

function toggleDropdown() {
    console.log("Clicked Button");

    var loginCardContainer = document.getElementById("loginCardContainer");
    var overlayDropdown = document.getElementById("overlayDropdown");

    loginCardContainer.style.display = "block";
    overlayDropdown.style.display = "flex";


}

function closingDropdown() {
    console.log("You pressed the overlay");
    var loginCardContainer = document.getElementById("loginCardContainer");
    var overlayDropdown = document.getElementById("overlayDropdown");

    loginCardContainer.style.display = "none";
    overlayDropdown.style.display = "none";

}