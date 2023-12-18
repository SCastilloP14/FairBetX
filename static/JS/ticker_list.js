document.addEventListener('DOMContentLoaded', function () {
  // Get all elements with the class 'custom-dropdown'
  var dropdowns = document.querySelectorAll('.custom-dropdown');

  // Add click event listener to each dropdown
  dropdowns.forEach(function (dropdown) {
    dropdown.addEventListener('click', function () {
        console.log("Clicked Teams", dropdown)

      // Toggle the 'open' class for the clicked dropdown
      dropdown.classList.toggle('open');
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  // Get all elements with the class 'league-dropdown'
  var leagueDropdowns = document.querySelectorAll('.league-dropdown');

  // Add 'open' class to each league dropdown by default
  leagueDropdowns.forEach(function (leagueDropdown) {
    leagueDropdown.classList.add('open');
  });

  // Add click event listener to each league dropdown
  leagueDropdowns.forEach(function (leagueDropdown) {
    // Add a click event listener to each league dropdown
    leagueDropdown.addEventListener('click', function (event) {
      // Check if the click target is not part of the dropdown content
      if (!leagueDropdown.contains(event.target.closest('.league-dropdown-content'))) {
        // Toggle the 'open' class for the clicked league dropdown
        leagueDropdown.classList.toggle('open');
      }
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

document.addEventListener('DOMContentLoaded', function () {
  // Get references to your buttons
  var liveSportsButton = document.getElementById('liveSportsButton');
  var allEventsButton = document.getElementById('allEventsButton');
  var searchBarGames = document.getElementById('searchBarGames');
  var searchBarTeams = document.getElementById('searchBarTeams');
  // var sportsDropdown =  document.getElementById('sportsDropdown');
  var leagueDropdown = document.getElementById('leagueDropdown');
  // All tickers 
  var tickers = document.querySelectorAll('.ticker');
  var dropdowns = document.querySelectorAll('.custom-dropdown');
  var gameStatus = document.querySelectorAll('.gameStatus');
  var leagueDropdowns = document.querySelectorAll('.league-dropdown');

  //Add event listener for sportsDropdown
  // sportsDropdown.addEventListener('change', function (event) {
  //   event.preventDefault();

  //   var selectedSport = sportsDropdown.value;

  //   tickers.forEach(function(ticker) {
  //       if (selectedSport === '' || ticker.classList.contains(selectedSport)) {
  //           ticker.style.display = 'block';
  //       } else {
  //           ticker.style.display = 'none';
  //       }
  //   });
  // })


  // Add event listener for allEventsButton
  allEventsButton.addEventListener('click', function (event) {
      event.preventDefault();
      // Pass null to the filterTickers function to show all tickers regardless of game status
      filterTickers(null);
  });

  // Add event listener for liveSportsButton
  liveSportsButton.addEventListener('click', function (event) {
      event.preventDefault();
      console.log("Pressedn live button");
      filterLiveTickers(gameStatus);
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

      if (searchBarTeams.value.trim() !== '') {
      dropdowns.forEach(function (dropdown) {
        dropdown.classList.add('open');
      });
    } else {
      dropdowns.forEach(function (dropdown) {
        dropdown.classList.remove('open');
      });
    }
 

  });

  // Function to filter tickers based on game status
  function filterTickers(gameStatus) {
      var tickers = document.querySelectorAll('.ticker');
      // Iterate over each ticker and show/hide based on game status.
      tickers.forEach(function (ticker) {
            var status = ticker.querySelector('.gameStatus').getAttribute('value');

          // If gameStatus is null, show all tickers; otherwise, show/hide based on game status.
          ticker.style.display = gameStatus === null || status === "PLAYING" ? 'block' : 'none';
      });
  }

  function filterLiveTickers() {
    var tickers = document.querySelectorAll('.ticker');
    
    tickers.forEach(function (ticker) {
      var status = ticker.querySelector('.gameStatus').getAttribute('value');
      var leagueDropdown = ticker.closest('.league-dropdown');

      // Check if the league dropdown is open and the game is live
      var showTicker = leagueDropdown.classList.contains('open') && status === "PLAYING";
      ticker.style.display = showTicker ? 'block' : 'none';
    });
  }

  // Function to filter all tickers by team names
  function searchGames() {
      var searchInput = searchBarGames.value.toLowerCase();
      var tickers = document.querySelectorAll('.ticker');

      tickers.forEach(function (ticker) {
          var tickerText = ticker.textContent.toLowerCase();
          ticker.style.display = tickerText.includes(searchInput) ? 'block' : 'none';
      });
  };

  function searchTeams() {
      var searchInput = searchBarTeams.value.toLowerCase();
      var teams = document.querySelectorAll('.teams');

      teams.forEach(function (ticker) {
          var tickerText = ticker.textContent.toLowerCase();
          ticker.style.display = tickerText.includes(searchInput) ? 'block' : 'none';
      });
  };
});