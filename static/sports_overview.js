document.addEventListener('DOMContentLoaded', function () {
  // Get all elements with the class 'custom-dropdown'
  var dropdowns = document.querySelectorAll('.custom-dropdown');

  // Add click event listener to each dropdown
  dropdowns.forEach(function (dropdown) {
    dropdown.addEventListener('click', function () {
      // Toggle the 'open' class for the clicked dropdown
      dropdown.classList.toggle('open');
    });
  });
});
