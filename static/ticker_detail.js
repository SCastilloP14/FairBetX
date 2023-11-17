document.addEventListener("DOMContentLoaded", function () {
  const ordersTab = document.getElementById("orders-tab");
  const positionsTab = document.getElementById("positions-tab");
  const fillsTab = document.getElementById("fills-tab");

  const ordersSection = document.getElementById("orders-section");
  const positionsSection = document.getElementById("positions-section");
  const fillsSection = document.getElementById("fills-section");

  // Show orders-section by default and hide positions-section
  ordersSection.style.display = "block";
  positionsSection.style.display = "none";
  fillsSection.style.display = "none";

  // Add event listener to orders-tab
  ordersTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Show orders-section and hide positions-section
    ordersSection.style.display = "block";
    positionsSection.style.display = "none";
    fillsSection.style.display = "none";

  });

  // Add event listener to positions-tab
  positionsTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and show positions-section
    ordersSection.style.display = "none";
    positionsSection.style.display = "block";
    fillsSection.style.display = "none";

  });

    fillsTab.addEventListener("click",function (event) {
    event.preventDefault();
    ordersSection.style.display = "none";
    positionsSection.style.display = "none";
    fillsSection.style.display = "block";
  });
  
});


