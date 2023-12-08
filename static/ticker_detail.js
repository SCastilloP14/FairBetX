// document.addEventListener("DOMContentLoaded", function () {
//   const ordersTab = document.getElementById("orders-tab");
//   const positionsTab = document.getElementById("positions-tab");
//   const fillsTab = document.getElementById("fills-tab");

//   const ordersSection = document.getElementById("orders-section");
//   const positionsSection = document.getElementById("positions-section");
//   const fillsSection = document.getElementById("fills-section");

//   // Show orders-section by default and hide positions-section
//   ordersSection.style.display = "block";
//   positionsSection.style.display = "none";
//   fillsSection.style.display = "none";

//   // Add event listener to orders-tab
//   ordersTab.addEventListener("click", function (event) {
//     event.preventDefault();

//     // Show orders-section and hide positions-section
//     ordersSection.style.display = "block";
//     positionsSection.style.display = "none";
//     fillsSection.style.display = "none";

//   });

//   // Add event listener to positions-tab
//   positionsTab.addEventListener("click", function (event) {
//     event.preventDefault();

//     // Hide orders-section and show positions-section
//     ordersSection.style.display = "none";
//     positionsSection.style.display = "block";
//     fillsSection.style.display = "none";

//   });

//     fillsTab.addEventListener("click",function (event) {
//     event.preventDefault();
//     ordersSection.style.display = "none";
//     positionsSection.style.display = "none";
//     fillsSection.style.display = "block";
//   });
  
// });

document.addEventListener("DOMContentLoaded", function () {
  const ordersTab = document.getElementById("orders-tab");
  const positionsTab = document.getElementById("positions-tab");
  const fillsTab = document.getElementById("fills-tab");
  const historicordersTab = document.getElementById("historic-orders-tab");


  const ordersSection = document.getElementById("orders-section");
  const positionsSection = document.getElementById("positions-section");
  const fillsSection = document.getElementById("fills-section");
  const historicordersSection = document.getElementById("historic-orders-section");


  // Function to remove "active" class from all tabs
  function resetTabs() {
    ordersTab.classList.remove("active");
    positionsTab.classList.remove("active");
    fillsTab.classList.remove("active");
    historicordersTab.classList.remove("active");
  }

  // Show orders-section by default and hide positions-section
  ordersSection.style.display = "block";
  positionsSection.style.display = "none";
  fillsSection.style.display = "none";
  historicordersSection.style.display = "none";


  // Add event listener to orders-tab
  ordersTab.addEventListener("click", function (event) {
    console.log("We are inside");

    event.preventDefault();

    // Show orders-section and hide positions-section
    ordersSection.style.display = "block";
    positionsSection.style.display = "none";
    fillsSection.style.display = "none";
    historicordersSection.style.display = "none";

    // Highlight the clicked tab
    resetTabs();
    ordersTab.classList.add("active");
  });

  // Add event listener to positions-tab
  positionsTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and show positions-section
    ordersSection.style.display = "none";
    positionsSection.style.display = "block";
    fillsSection.style.display = "none";
    historicordersSection.style.display = "none";

    // Highlight the clicked tab
    resetTabs();
    positionsTab.classList.add("active");
  });

  // Add event listener to fills-tab
  fillsTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    ordersSection.style.display = "none";
    positionsSection.style.display = "none";
    fillsSection.style.display = "block";
    historicordersSection.style.display = "none";


    // Highlight the clicked tab
    resetTabs();
    fillsTab.classList.add("active");
  });

  historicordersTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    ordersSection.style.display = "none";
    positionsSection.style.display = "none";
    fillsSection.style.display = "none";
    historicordersSection.style.display = "block";


    // Highlight the clicked tab
    resetTabs();
    historicordersTab.classList.add("active");
  });
});

