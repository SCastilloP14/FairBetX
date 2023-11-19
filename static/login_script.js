// document.addEventListener('DOMContentLoaded', function () {
//     var loginButton = document.getElementById("loginDropdownButton");
//     var overlay = document.getElementById("overlay");
//     var loginContainer = document.getElementById("loginDropdownContainer");
//     var newUser = document.getElementById("newUser");

//     newUser.addEventListener('click', function () {
//         console.log('Clicked newUser');
//         hideLoginContainer();
//     });

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
//     return (
//         (target && target.tagName && target.tagName.toLowerCase() === "input") ||
//         (target && target.tagName && target.tagName.toLowerCase() === "button") ||
//         (target && target.parentNode && isFormElement(target.parentNode))
//     );
// }

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

// function hideLoginContainer() {
//     console.log('hideLoginContainer invoked');

//     var loginContainer = document.getElementById("loginDropdownContainer");
//     var overlay = document.getElementById("overlay");

//     loginContainer.style.display = "none";
//     overlay.style.display = "block";
// }





document.addEventListener('DOMContentLoaded', function () {
    var loginButton = document.getElementById("loginDropdownButton");
    var overlayDropdown = document.getElementById("overlayDropdown");
    var loginCardContainer = document.getElementById("loginCardContainer");
    var loginCancelButton = document.getElementById("loginCancelButton");

    var beingJourneyButton = document.getElementById("beingJourneyButton");
    var startBettingButton = document.getElementById("startBettingButton");


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

    beingJourneyButton.addEventListener('click', function ()  {
        toggleDropdown();
    });

    startBettingButton.addEventListener('click', function ()  {
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