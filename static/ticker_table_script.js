// <!-- Include jQuery -->
// <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>


//     $(document).ready(function () {
//         // Your data (assuming user_orders is an array of orders)
//         var userOrders = {{ user_orders|tojson|safe }};
//         var itemsPerPage = 20;
//         var currentPage = 1;
//         var totalPages = Math.ceil(userOrders.length / itemsPerPage);

//         function updateTable() {
//             var startIndex = (currentPage - 1) * itemsPerPage;
//             var endIndex = startIndex + itemsPerPage;
//             var slicedOrders = userOrders.slice(startIndex, endIndex);

//             // Clear existing rows
//             $('#table-body').empty();

//             // Append new rows
//             $.each(slicedOrders, function (index, order) {
//                 // Create and append your table rows here
//                 var row = '<tr><td>' + order.ticker_id + '</td><td>' + order.creation_timestamp + '</td><!-- ... (other cells) ... --></tr>';
//                 $('#table-body').append(row);
//             });

//             // Update pagination info
//             $('#pagination-info').text('Page ' + currentPage + ' of ' + totalPages);
//         }

//         // Initial table update
//         updateTable();

//         // Event listener for left arrow
//         $('.tickerPageArrowLeft').on('click', function (e) {
//             e.preventDefault();
//             if (currentPage > 1) {
//                 currentPage--;
//                 updateTable();
//             }
//         });

//         // Event listener for right arrow
//         $('.tickerPageArrowRight').on('click', function (e) {
//             e.preventDefault();
//             if (currentPage < totalPages) {
//                 currentPage++;
//                 updateTable();
//             }
//         });
//     });

