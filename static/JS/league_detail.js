// Function to show/hide select elements based on the league
    function updateSelectVisibility() {
        // Get the selected league name
        var selectedLeague = document.getElementById("league-name").textContent ;
        // Hide all select elements
        var allSelects = document.querySelectorAll('.leagueOverviewConferenceSelection');
        allSelects.forEach(function (select) {
            select.style.display = 'none';
        });

        // Show the select element corresponding to the selected league
        var selectedSelect = document.getElementById(selectedLeague + '-Conferences');
        if (selectedSelect) {
            selectedSelect.style.display = 'block';
        }
    }

    // Call the function initially and whenever the league changes
    document.addEventListener("DOMContentLoaded", updateSelectVisibility);