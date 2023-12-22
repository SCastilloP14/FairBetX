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
    var currentPage = 1;
    var entriesPerPage = 20; // Set the desired items per page
    var startIndex, endIndex; // Declare global variables for startIndex and endIndex

    updateTable(); // Initial table update

    // Attach event listeners to the next and previous buttons
    document.getElementById("nextButton").addEventListener("click", function (event) {
        showNextEntries(event);
    });

    document.getElementById("prevButton").addEventListener("click", function (event) {
        showPreviousEntries(event);
    });

    function filterOrders(allOrders) {
        var filteredOrders = allOrders.filter(function (order) {
            var statusCell = order.querySelector('[data-class="Status"]');
            var orderStatus = statusCell ? statusCell.innerText.trim() : null;
            return orderStatus === "PARTIAL" || orderStatus === "OPEN";
        });
        return filteredOrders;
    }

    // Function to update the table based on the current page
    function updateTable() {
        var filteredOrders = filterOrders(allOrders);
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
        document.getElementById("currentPage").innerText = "Page " + currentPage;
    }

    // Function to show the next page of entries
    function showNextEntries(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag
        var filteredOrders = filterOrders(allOrders);

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
