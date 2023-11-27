document.addEventListener('DOMContentLoaded', function () {
    // Login 
    var loginButton = document.getElementById("loginDropdownButton");
    var overlayDropdown = document.getElementById("overlayDropdown");
    var loginCardContainer = document.getElementById("loginCardContainer");
    var loginCancelButton = document.getElementById("loginCancelButton");

    var beingJourneyButton = document.getElementById("beingJourneyButton");
    var startBettingButton = document.getElementById("startBettingButton");

    // Signup 
    var newUserButton = document.getElementById("newUserButton");
    var signUpOverlay = document.getElementById("signUpOverlay");
    var signUpCardContainer = document.getElementById("signUpCardContainer");
    var existingUserButton = document.getElementById("existingUserButton");

    var registrationCancelButton = document.getElementById("registrationCancelButton");


    // Initially hide the loginDropdownContainer
    loginCardContainer.style.display = "none";
    overlayDropdown.style.display = "none";

    signUpCardContainer.style.display = "none";
    signUpOverlay.style.display = "none";
    


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

    // Registration 
    newUserButton.addEventListener('click', function ()  {
        
        closingDropdown();
        toggleRegistrationDropdown();
    });

    existingUserButton.addEventListener('click', function () {
        closeRegistrationDropdown();
        toggleDropdown();
    });

    registrationCancelButton.addEventListener('click', function ()  {
        closeRegistrationDropdown();
        console.log("Clicked Registration Cancel");
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
    console.log("Closing Login Page");

    var loginCardContainer = document.getElementById("loginCardContainer");
    var overlayDropdown = document.getElementById("overlayDropdown");

    loginCardContainer.style.display = "none";
    overlayDropdown.style.display = "none";

}

function toggleRegistrationDropdown() {
    console.log("Opening Registration Page");

    var signUpCardContainer = document.getElementById("signUpCardContainer");
    var signUpOverlay = document.getElementById("signUpOverlay");

    signUpCardContainer.style.display = "block";
    signUpOverlay.style.display = "flex";  
}

function closeRegistrationDropdown() {
    console.log("Closing Registration Page");

    var signUpCardContainer = document.getElementById("signUpCardContainer");
    var signUpOverlay = document.getElementById("signUpOverlay");

    signUpCardContainer.style.display = "none";
    signUpOverlay.style.display = "none";  
}