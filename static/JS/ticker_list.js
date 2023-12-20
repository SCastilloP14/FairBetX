document.addEventListener('DOMContentLoaded', function () {
  var dropdowns = document.querySelectorAll('.custom-dropdown');

  dropdowns.forEach(function (dropdown) {
    dropdown.addEventListener('click', function () {
      dropdown.classList.toggle('open');
    });
  });

  var liveSportsButton = document.getElementById('liveSportsButton');
  var filterButtons = document.querySelectorAll('.filterButton');
  var gameCards = document.querySelectorAll('.rightCardContainerMatches');
  // var dateRangeDropdown = document.querySelector('.dateRangeDropdown');
  var tickers = document.querySelectorAll('.ticker');
  var dropdowns = document.querySelectorAll('.custom-dropdown');
  var gameStatus = document.querySelectorAll('.gameStatus');
  var sportsDropdown = document.getElementById('sportsDropdown');
  var searchBarGames = document.getElementById('searchBarGames');
  var searchBarTeams = document.getElementById('searchBarTeams');


  var checkboxes = document.querySelectorAll('.dateRangeDropdown-checkbox');
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
          filterTickers();
        });
    });


    // Add event listener for liveSportsButton
  liveSportsButton.addEventListener('click', function (event) {
        event.preventDefault();
        if (liveSportsButton.classList.contains('active')) {
            liveSportsButton.classList.remove('active');
            filterTickers();
        } else {
            liveSportsButton.classList.add('active');
            filterLiveTickers(gameStatus);
        }
    });

  filterButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var filterValue = button.getAttribute('data-filter');

      gameCards.forEach(function (card) {
        card.style.display = 'none';
      });

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

  sportsDropdown.addEventListener('change', function (event) {
    event.preventDefault();

    var selectedSport = sportsDropdown.value;

    tickers.forEach(function (ticker) {
      if (selectedSport === '' || ticker.classList.contains(selectedSport)) {
        ticker.style.display = 'block';
      } else {
        ticker.style.display = 'none';
      }
    });
  });

  searchBarGames.addEventListener('input', function (event) {
    event.preventDefault();
    searchGames();
  });

  // Search Teams on the left Panel and opening all dropdowns 
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
    };
  });


  // Functions 

  // Search Right Panel Games based on Search Bar Input 
  function searchGames() {
    var searchInput = searchBarGames.value.toLowerCase();

    tickers.forEach(function (ticker) {
      var tickerText = ticker.textContent.toLowerCase();
      ticker.style.display = tickerText.includes(searchInput) ? 'block' : 'none';
    });
  }

  // Search Left Panel Teams based on Search Bar Input 
  function searchTeams() {
      var searchInput = searchBarTeams.value.toLowerCase();
      var teams = document.querySelectorAll('.teams');

      teams.forEach(function (ticker) {
          var tickerText = ticker.textContent.toLowerCase();
          ticker.style.display = tickerText.includes(searchInput) ? 'block' : 'none';
      });
  };

  // Filter Rigth Panel Games based on Date 
  function filterTickers() {
        var selectedDates = getSelectedDates();
        tickers.forEach(function (ticker) {
            var cardDate = ticker.getAttribute('value');

            // Split Date String into components
            var parts = cardDate.split(' ');
            var day = parts[1];
            var month = parts[0];
            var year = parts[2].replace(',', '');
            // Combine the extracted parts into a format you want
            var formattedDate = `${month} ${day} ${year}`;

            if (selectedDates.length === 0 || selectedDates.includes(formattedDate)) {
                ticker.style.display = 'block';
            } else {
                ticker.style.display = 'none';
            }
        });
    }

  function filterLiveTickers(gameStatus) {
        var tickers = document.querySelectorAll('.ticker');
        // Iterate over each ticker and show/hide based on game status.
        tickers.forEach(function (ticker) {
            var status = ticker.querySelector('.gameStatus').getAttribute('value');
            // If gameStatus is null, show all tickers; otherwise, show/hide based on game status.
            ticker.style.display = gameStatus === null || status === "PLAYING" ? 'block' : 'none';
        });
    }


  function getSelectedDates() {
        var selectedDates = [];
        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                selectedDates.push(checkbox.value);
            }
        });
        return selectedDates;
    }

});
