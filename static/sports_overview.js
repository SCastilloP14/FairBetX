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


// document.getElementById('sportsDropdown').addEventListener('change', function() {
//   var selectedSport = this.value;
//   var tickers = document.querySelectorAll('.ticker');

//   tickers.forEach(function(ticker) {
//       if (selectedSport === '' || ticker.classList.contains(selectedSport)) {
//           ticker.style.display = 'block';
//       } else {
//           ticker.style.display = 'none';
//       }
//   });
// });


document.addEventListener('DOMContentLoaded', function () {
  // Get references to your buttons
  var liveSportsButton = document.getElementById('liveSportsButton');
  var allEventsButton = document.getElementById('allEventsButton');
  var searchBarGames = document.getElementById('searchBarGames');
  var searchBarTeams = document.getElementById('searchBarTeams');
  var sportsDropdown =  document.getElementById('sportsDropdown');
  // All tickers 
  var tickers = document.querySelectorAll('.ticker');

  // Add event listener for liveSportsButton
  liveSportsButton.addEventListener('click', function (event) {
      event.preventDefault();
      filterTickers('LIVE');
  });

  // Add event listener for allEventsButton
  allEventsButton.addEventListener('click', function (event) {
      event.preventDefault();
      // Pass null to the filterTickers function to show all tickers regardless of game status
      filterTickers(null);
  });

  searchBarGames.addEventListener('input', function (event) {
      event.preventDefault();
      // Function to search all games based on any team name
      searchGames();
  });

  searchBarTeams.addEventListener('input', function (event) {
      event.preventDefault();
      // Function to search all games based on any team name
      searchTeams();

  });

  // Function to filter tickers based on game status
  function filterTickers(gameStatus) {
      var tickers = document.querySelectorAll('.ticker');

      // Iterate over each ticker and show/hide based on game status.
      tickers.forEach(function (ticker) {
          // If gameStatus is null, show all tickers; otherwise, show/hide based on game status.
          ticker.style.display = gameStatus === null || ticker.dataset.gameStatus === gameStatus ? 'block' : 'none';
      });
  }

  // Function to filter all tickers by team names
  function searchGames() {
      var searchInput = searchBarGames.value.toLowerCase();
      var tickers = document.querySelectorAll('.ticker');
      console.log("IM here", searchInput);
      tickers.forEach(function (ticker) {
          var tickerText = ticker.textContent.toLowerCase();
          ticker.style.display = tickerText.includes(searchInput) ? 'block' : 'none';
      });
  };

  function searchTeams() {
      var searchInput = searchBarTeams.value.toLowerCase();
      var tickers = document.querySelectorAll('.ticker');

      tickers.forEach(function (ticker) {
          var tickerText = ticker.textContent.toLowerCase();
          ticker.style.display = tickerText.includes(searchInput) ? 'block' : 'none';
      });
  };
});