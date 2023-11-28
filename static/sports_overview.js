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


document.addEventListener('DOMContentLoaded', function () {
  var filterButtons = document.querySelectorAll('.filterButton');
  var gameCards = document.querySelectorAll('.rightCardContainerMatches');

  filterButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var filterValue = button.getAttribute('data-filter');

      // Hide all cards
      gameCards.forEach(function (card) {
        card.style.display = 'none';
      });

      // Show only cards that match the selected filter
      if (filterValue === 'all') {
        gameCards.forEach(function (card) {
          card.style.display = 'block';
        });
      } else {
        var filteredCards = document.querySelectorAll('.' + filterValue);
        filteredCards.forEach(function (card) {
          card.style.display = 'block';
        });
      }
    });
  });
});


document.getElementById('sportsDropdown').addEventListener('change', function() {
  var selectedSport = this.value;
  var tickers = document.querySelectorAll('.ticker');

  tickers.forEach(function(ticker) {
      if (selectedSport === '' || ticker.classList.contains(selectedSport)) {
          ticker.style.display = 'block';
      } else {
          ticker.style.display = 'none';
      }
  });
});