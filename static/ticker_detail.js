// $(document).ready(function(){
//   // Hide all sections except the first one on page load
//   $('#orders-section').show();
//   $('#positions-section').hide();

//   // Show/hide sections based on clicked tab
//   $('#orders-tab').click(function(){
//       $('#orders-section').show();
//       $('#positions-section').hide();
//   });

//   $('#positions-tab').click(function(){
//       $('#orders-section').hide();
//       $('#positions-section').show();
//   });
// })

// const chartProperties = {
//   width:1500,
//   height:600,
//   timeScale:{
//   timeVisible:true,
//   secondsVisible:false, 
//   }
// }

// document.addEventListener("DOMContentLoaded", function() {
//     const option1 = document.getElementById("orders-tab");
//     const option2 = document.getElementById("positions-tab");
//     const table1 = document.getElementById("orders-section");
//     const table2 = document.getElementById("positions-section");



//     option1.addEventListener("click", function() {
//         table1.style.display = "table";
//         table2.style.display = "none";
//     });

//     option2.addEventListener("click", function() {
//         table1.style.display = "none";
//         table2.style.display = "table";
//     });
// });

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


