document.addEventListener("DOMContentLoaded", function () {
  const ordersTab = document.getElementById("orders-tab");
  const positionsTab = document.getElementById("positions-tab");
  const fillsTab = document.getElementById("fills-tab");
  const historicordersTab = document.getElementById("historic-orders-tab");

  const ordersSection = document.getElementById("orders-section");
  const positionsSection = document.getElementById("positions-section");
  const fillsSection = document.getElementById("fills-section");
  const historicordersSection = document.getElementById("historic-orders-section");

  // Order Submission Field 
  const orderType = document.getElementById("order-type");
  const orderPrice = document.getElementById("order-price");


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

orderType.addEventListener("change", function (event) {
  
  console.log("Im in here");
  if (orderType.value=="MARKET") {
    orderPrice.disabled = true;
    orderPrice.placeholder = "MARKET";
  };
  
  if (orderType.value=="LIMIT") {
    orderPrice.disabled = false;
    orderPrice.placeholder = "$0.00";

  };
})




function showConfirmationPopup() {
        // Get form data
        var orderType = document.getElementById("order-type").value;
        var orderSide = document.querySelector(".tickerDetailSideSelect").value;
        var orderPrice = document.getElementById("order-price").value;
        var orderQuantity = document.getElementById("order-quantity").value;

        var maxProfit;
        var maxLoss;
        var alternativeMessage;

        // var buyOrdersTable = document.getElementById('buy-orders');

        // Read sell orders data attribute
        // var sellOrdersTable = document.getElementById('sell-orders');


        if (orderType === "MARKET") {
            if (orderSide === "BUY") {
                // Calculate maximum loss and profit based on the highest sell order
                var highestSellOrder = getHighestSellOrder(orderQuantity);
                if (highestSellOrder == null) {
                    alternativeMessage = "Your Market Order Quantity exceeds the total Volume the Market is currently offering. If you submit the order it might get filled, but there is no guarantee"
                }
                else {
                    console.log("HighestSellOrders", highestSellOrder);

                    // Calculate maxProfit considering the expected price to the HighestSellOrder.order_price
                    var maxProfit = highestSellOrder ? (10- highestSellOrder.order_price) * orderQuantity : 0;

                    // Calculate maxLoss based on the orderPrice and orderQuantity
                    var maxLoss = highestSellOrder.order_price * orderQuantity;
                    var totalPrice = maxLoss;
                }
            } else if (orderSide === "SELL") {
                // Calculate maximum loss and profit based on the highest buy order
                var highestBuyOrder = getHighestBuyOrder(orderQuantity);
                if (highestBuyOrder == null) {
                    alternativeMessage = "Your Market Order Quantity exceeds the total Volume the Market is currently offering. If you submit the order it might get filled, but there is no guarantee"
                }
                else {
                    var maxProfit = highestBuyOrder.order_price * orderQuantity;
                    var maxLoss = (10 - highestBuyOrder.order_price) * orderQuantity; // Assuming the user sells at the highest buy price
                    var totalPrice = maxProfit;
                }
                
            }
            if (alternativeMessage != null) {
                confirmationMessage = alternativeMessage;
            }
            else {
                confirmationMessage =
                    "You are submitting a MARKET ORDER to " + orderSide + " " + 
                    orderQuantity + " Contracts at the best available price for a TOTAL EXPECTED PRICE of $" + 
                    totalPrice + "<br>" +
                    "Maximum Profit: $" + maxProfit + "<br>" +
                    "Maximum Loss:  $" + maxLoss;
            }
        } else {
            // Logic for other order types
            confirmationMessage = 
                "You are submitting a "+ "LIMIT ORDER to " + orderSide + " " + 
                orderQuantity + " Contracts at $" + orderPrice + " for a TOTAL Price of $" + 
                (orderPrice * orderQuantity) + "<br>" + "<br>" +
                "Maximum Profit: $" + (orderSide === 'BUY' ? (10 - orderPrice) * orderQuantity : orderPrice * orderQuantity) + "<br>" +
                "Maximum Loss:   $" + (orderSide === 'BUY' ? orderPrice * orderQuantity : (10 - orderPrice) * orderQuantity);
            ;
        }
        // Display the confirmation pop-up
        document.getElementById("confirmation-message").innerHTML = confirmationMessage;
        document.getElementById("confirmation-overlay").style.display = "flex";
    }

    function hideConfirmationPopup(event) {
        event.preventDefault();

        // Hide the confirmation pop-up
        document.getElementById("confirmation-overlay").style.display = "none";
    }

    function submitOrder() {
        // Submit the form
        document.getElementById("order-form").submit();
    }

    function parseSellOrdersContent(content) {
        try {
            // Replace Decimal with Number in the content
            const cleanedContent = content.replace(/Decimal\(/g, "Number(");
            // Use eval to convert the content into a JavaScript array
            const parsedArray = eval(`[${cleanedContent}]`);
            // Check if parsedArray is an array
            if (Array.isArray(parsedArray)) {
                return parsedArray;
            }
        } catch (error) {
            console.error("Error parsing sell-orders content:", error);
        }

        return null;
    }

    function getHighestSellOrder(quantity) {
        try {
            // Get the text content of the sell-orders div
            const sellOrdersText = $("#sell-orders").text();

            // Use a regular expression to extract the array portion within brackets
            const arrayMatch = sellOrdersText.match(/\[([^[\]]*)\]/);
            if (arrayMatch && arrayMatch.length > 1) {
                // Extract the content within brackets
                const arrayContent = arrayMatch[1];
                // Parse the content using the custom parser
                const ordersData = parseSellOrdersContent(arrayContent);
                // Check if ordersData is an array and has elements
                if (Array.isArray(ordersData) && ordersData.length > 0) {
                    // Sort sellOrders by order price in ascending order
                    ordersData.sort((a, b) => a.order_price - b.order_price);
                    // Find the highest sell order with enough quantity
                    for (let i = ordersData.length - 1; i >= 0; i--) {
                        if (ordersData[i].total_quantity >= quantity) {
                            return ordersData[i];
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Error extracting sell-orders:", error);
        }
        return null; // No suitable sell order found
    }


    // Function to get all buy orders and determine likelihood of getting filled 
    function getHighestBuyOrder(quantity) {
        try {
            // Use a regular expression to extract the array portion within brackets
            const buyOrdersText = $("#buy-orders").text();
            const arrayMatch = buyOrdersText.match(/\[([^[\]]*)\]/);


            if (arrayMatch && arrayMatch.length > 1) {
                // Extract the content within brackets
                const arrayContent = arrayMatch[1];

                // Parse the content using the custom parser
                const ordersData = parseSellOrdersContent(arrayContent);

                // Check if ordersData is an array and has elements
                if (Array.isArray(ordersData) && ordersData.length > 0) {
                    // Sort buyOrders by order price in descending order
                    ordersData.sort((a, b) => b.order_price - a.order_price);

                    // Find the highest buy order with enough quantity
                    for (let i = 0; i < ordersData.length; i++) {
                        if (ordersData[i].total_quantity >= quantity) {
                            return ordersData[i];
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Error extracting buy-orders:", error);
        }
        return null; // No suitable buy order found
    }


});



    
