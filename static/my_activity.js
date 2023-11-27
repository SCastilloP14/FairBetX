document.addEventListener("DOMContentLoaded", function () {
  const activityOrdersTab = document.getElementById("activity-orders-tab");
  const activityPositionsTab = document.getElementById("activity-positions-tab");
  const activityFillsTab = document.getElementById("activity-fills-tab");
  const activityHistoricOrdersTab = document.getElementById("activity-historic-orders-tab");


  const activityOrdersSection = document.getElementById("activity-orders-section");
  const activityPositionsSection = document.getElementById("activity-positions-section");
  const activityFillsSection = document.getElementById("activity-fills-section");
  const activityHistoricOrdersSection = document.getElementById("activity-historic-orders-section");


  // Function to remove "active" class from all tabs
  function resetTabs() {
    activityOrdersTab.classList.remove("active");
    activityPositionsTab.classList.remove("active");
    activityFillsTab.classList.remove("active");
    activityHistoricOrdersTab.classList.remove("active");
  }

  // Show orders-section by default and hide positions-section
  activityOrdersSection.style.display = "block";
  activityPositionsSection.style.display = "none";
  activityFillsSection.style.display = "none";
  activityHistoricOrdersSection.style.display = "none";


  // Add event listener to orders-tab
  activityOrdersTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Show orders-section and hide positions-section
    activityOrdersSection.style.display = "block";
    activityPositionsSection.style.display = "none";
    activityFillsSection.style.display = "none";
    activityHistoricOrdersSection.style.display = "none";

    // Highlight the clicked tab
    resetTabs();
    activityOrdersTab.classList.add("active");
  });

  // Add event listener to positions-tab
  activityPositionsTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and show positions-section
    activityOrdersSection.style.display = "none";
    activityPositionsSection.style.display = "block";
    activityFillsSection.style.display = "none";
    activityHistoricOrdersSection.style.display = "none";

    // Highlight the clicked tab
    resetTabs();
    activityPositionsTab.classList.add("active");
  });

  // Add event listener to fills-tab
  activityFillsTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    activityOrdersSection.style.display = "none";
    activityPositionsSection.style.display = "none";
    activityFillsSection.style.display = "block";
    activityHistoricOrdersSection.style.display = "none";


    // Highlight the clicked tab
    resetTabs();
    activityFillsTab.classList.add("active");
  });

  activityHistoricOrdersTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    activityOrdersSection.style.display = "none";
    activityPositionsSection.style.display = "none";
    activityFillsSection.style.display = "none";
    activityHistoricOrdersSection.style.display = "block";


    // Highlight the clicked tab
    resetTabs();
    activityHistoricOrdersTab.classList.add("active");
  });
});
