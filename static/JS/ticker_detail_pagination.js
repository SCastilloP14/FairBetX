// ======================================================================


//                            TABLE PAGINATION 

// ======================================================================

// Execute the initial setup when the page loads
// document.addEventListener("DOMContentLoaded", function () {
//     var allOrders = Array.from(document.getElementsByClassName("order-row"));
//     var currentPage = 1;
//     var entriesPerPage = 1; // Set the desired items per page
    
//     updateTable(currentPage, entriesPerPage, allOrders);

//     // Attach event listeners to the next and previous buttons
//     document.getElementById("nextButton").addEventListener("click", function (event) {
//         showNextEntries(event, currentPage, entriesPerPage);
//     });

//     document.getElementById("prevButton").addEventListener("click", function (event) {
//         showPreviousEntries(event, currentPage);
//     });

//     function filterOrders(allOrders) {
//         console.log("All Orders", allOrders);

//         var filteredOrders = allOrders.filter(function (order) {
//             var statusCell = order.querySelector('[data-class="Status"]');
//             var orderStatus = statusCell ? statusCell.innerText.trim() : null;
//             return orderStatus === "PARTIAL" || orderStatus === "OPEN";
//         });
//         return filteredOrders;
//     }

//     // Function to update the table based on the current page
//     function updateTable(currentPage, entriesPerPage, allOrders) {
//         var filteredOrders = filterOrders(allOrders);
//         var startIndex = (currentPage - 1) * entriesPerPage;
//         var endIndex = startIndex + entriesPerPage;
//         var totalPages = Math.ceil(filteredOrders.length / entriesPerPage);

//         console.log("All Orders", allOrders.length);

//         for (var i = 0; i < allOrders.length; i++) {
//             var order = allOrders[i];
//             order.style.display = "none";
//         }

//         // Show only Filtered Orders depending on Page
//         for (var i = startIndex; i < endIndex && i < filteredOrders.length; i++) {
//             var order = filteredOrders[i];
//             order.style.display = "";
//         }

//         document.getElementById("currentPage").innerText = "Page " + currentPage + " of " + totalPages;
//     }

//     // Function to show the next page of entries
//     function showNextEntries(event, currentPage, entriesPerPage) {
//         event.preventDefault(); // Prevent the default behavior of the anchor tag
//         var filteredOrders = filterOrders(allOrders);

//         if (currentPage < Math.ceil(filteredOrders.length / entriesPerPage)) {
//             currentPage++;
//             updateTable(currentPage, entriesPerPage, allOrders);
//         }
//     }

//     // Function to show the previous page of entries
//     function showPreviousEntries(event, currentPage) {
//         event.preventDefault(); // Prevent the default behavior of the anchor tag

//         if (currentPage > 1) {
//             currentPage--;
//             updateTable(currentPage, entriesPerPage, allOrders);
//         }
//     }

// });








document.addEventListener("DOMContentLoaded", function () {
    var allOrders = Array.from(document.getElementsByClassName("order-row"));
    var allFillsOrders = Array.from(document.getElementsByClassName("fills-row"));
    var allPositionsOrders = Array.from(document.getElementsByClassName("positions-row"));
    var allHistoricOrders = Array.from(document.getElementsByClassName("historic-row"));

    const ordersSection = document.getElementById("orders-section");
    const positionsSection = document.getElementById("positions-section");
    const fillsSection = document.getElementById("fills-section");
    const historicordersSection = document.getElementById("historic-orders-section");

    var currentPage = 1;
    var entriesPerPage = 20; // Set the desired items per page
    var startIndex, endIndex; // Declare global variables for startIndex and endIndex

    var tableType = "orders"; //Initial Value 
    updateTable(); // Initial table update

    document.getElementById("orders-tab").addEventListener("click", function (event) {
        if (ordersSection.style.display == "block") {
            tableType = "orders";
            updateTable();
            }
    });
    document.getElementById("fills-tab").addEventListener("click", function (event) {
        if (fillsSection.style.display == "block") {
            tableType = "fills";
            updateTable();
            }
    });
    document.getElementById("positions-tab").addEventListener("click", function (event) {
        if (positionsSection.style.display == "block") {
            tableType = "positions";
            updateTable();
            }
    });
    document.getElementById("historic-orders-tab").addEventListener("click", function (event) {
        if (historicordersSection.style.display == "block") {
            tableType = "historic";
            updateTable();
            }
    });

    // Attach event listeners to the next and previous buttons
        // Orders 
    document.getElementById("nextButtonOrders").addEventListener("click", function (event) {
        showNextEntries(event);
    });

    document.getElementById("prevButtonOrders").addEventListener("click", function (event) {
        showPreviousEntries(event);
    });
        // Fills 
    document.getElementById("nextButtonFills").addEventListener("click", function (event) {
        showNextEntries(event);
    });

    document.getElementById("prevButtonFills").addEventListener("click", function (event) {
        showPreviousEntries(event);
    });
        // Positions 
    document.getElementById("nextButtonPositions").addEventListener("click", function (event) {
        showNextEntries(event);
    });

    document.getElementById("prevButtonPositions").addEventListener("click", function (event) {
        showPreviousEntries(event);
    });
        // Historic 
    document.getElementById("nextButtonHistoric").addEventListener("click", function (event) {
        showNextEntries(event);
    });

    document.getElementById("prevButtonHistoric").addEventListener("click", function (event) {
        showPreviousEntries(event);
    });



    function filterOrders(orderType) {

        // Check for which Table is in focus 
        if (orderType == "orders") {
            var filteredOrders = allOrders.filter(function (order) {
                var statusCell = order.querySelector('[data-class="Status"]');
                var orderStatus = statusCell ? statusCell.innerText.trim() : null;
                return orderStatus === "PARTIAL" || orderStatus === "OPEN";
            });   
        } 
        else if (orderType == "fills") {
            var filteredOrders = allFillsOrders; 
        }
        else if (orderType == "positions") {
            var filteredOrders = allPositionsOrders ;
        }
        else if (orderType == "historic") {
            var filteredOrders = allHistoricOrders;
        }

        return filteredOrders;
    }

    // Function to update the table based on the current page
    function updateTable() {
        console.log("inside Table", tableType);
        var filteredOrders = filterOrders(tableType);
        startIndex = (currentPage - 1) * entriesPerPage;
        endIndex = startIndex + entriesPerPage;
        
        for (var i = 0; i < allOrders.length; i++) {
            var order = allOrders[i];
            order.style.display = "none";
        }

        for (var i = 0; i < filteredOrders.length; i++) {
            var order = filteredOrders[i];
            if (i >= startIndex && i < endIndex) {
                order.style.display = "";
            } else {
                order.style.display = "none";
            }
        }
        document.getElementById("currentPage" + tableType.charAt(0).toUpperCase()+tableType.slice(1)).innerText = "Page " + currentPage;
    }

    // Function to show the next page of entries
    function showNextEntries(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag
        var filteredOrders = filterOrders(tableType);

        if (currentPage < Math.ceil(filteredOrders.length / entriesPerPage)) {
            currentPage++;
            updateTable();
        }
    }

    // Function to show the previous page of entries
    function showPreviousEntries(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag

        if (currentPage > 1) {
            currentPage--;
            updateTable();
        }
    }
});



