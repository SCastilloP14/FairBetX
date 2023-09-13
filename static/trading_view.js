// // custom-lightweight-chart.js
// document.addEventListener("DOMContentLoaded", function () {
//   // Fetch custom data from Django backend
//   fetch("/custom-data/")
//     .then((response) => response.json())
//     .then((data) => {
//       // Parse data for use in the chart
//       const chartData = data.map((point) => ({
//         time: point.time,
//         open: point.open,
//         high: point.high,
//         low: point.low,
//         close: point.close,
//       }));

//       // Create a new TradingView Lightweight Chart
//       const chart = LightweightCharts.createChart(
//         document.getElementById("chart-container"),
//         {
//           width: document.getElementById("chart-container").offsetWidth,
//           layout: {
//             background: { color: '#00171f' },
//             textColor: '#DDD',
//         },
//         grid: {
//             vertLines: { color: 'white' },
//             horzLines: { color: 'white' },
//         },
//         }
//       );
        
//       // Add a candlestick series with the custom data
//       const candlestickSeries = chart.addCandlestickSeries();
    
//       // Apply the custom data to the series
//       candlestickSeries.setData(chartData);
//     })
//     .catch((error) => console.error("Error fetching custom data:", error));
// });

//  document.addEventListener("DOMContentLoaded", function () {
//     // Fetch custom data from Django backend
//     fetch('/custom-data/')
//         .then(response => response.json())
//         .then(data => {
//             // Sort data by timestamp in ascending order
//             data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

//             // Convert datetime strings to timestamps in milliseconds
//             const candlestickData = [];
//             let currentCandle = null;

//             data.forEach(item => {
//                 const timestamp = new Date(item.timestamp).getTime(); // Convert to milliseconds
//                 const price = item.price;

//                 // Define the desired interval (e.g., 1 minute in milliseconds)
//                 const interval = 60 * 1000; // 1 minute

//                 // Initialize a new candle if needed
//                 if (!currentCandle || timestamp - currentCandle.time >= interval) {
//                     if (currentCandle) {
//                         candlestickData.push(currentCandle);
//                     }
//                     // Calculate the start time of the new candle
//                     const startTime = Math.floor(timestamp / interval) * interval;
//                     currentCandle = {
//                         time: startTime,
//                         open: price,
//                         high: price,
//                         low: price,
//                         close: price,
//                     };
//                 } else {
//                     // Update the existing candle
//                     currentCandle.high = Math.max(currentCandle.high, price);
//                     currentCandle.low = Math.min(currentCandle.low, price);
//                     currentCandle.close = price;
//                 }
//             });

//             // Push the last candle to the candlestick data
//             if (currentCandle) {
//                 candlestickData.push(currentCandle);
//             }

//             // Create a new TradingView Lightweight Chart
//             const chart = LightweightCharts.createChart(document.getElementById('chart-container'), {
//             width: document.getElementById("chart-container").offsetWidth,
//             layout: {
//                 background: { color: '#00171f' },
//                 textColor: '#DDD',
//             },
//             grid: {
//                 vertLines: { color: 'white' },
//                 horzLines: { color: 'white' },
//             },
//             });

//             // Add a candlestick series with the converted data
//             const candlestickSeries = chart.addCandlestickSeries();

//             // Apply the candlestick data to the series
//             candlestickSeries.setData(candlestickData);
//         })
//         .catch(error => console.error("Error fetching custom data:", error));
// });


// document.addEventListener("DOMContentLoaded", function () {
//     // Make an AJAX request to get the JSON data
//     fetch('/custom-data/')  // Update with the correct URL
//       .then(response => response.json())
//       .then(data => {
//         // Create the TradingView lightweight chart
        
//         // Split the date and time parts
//                var container = document.getElementById("chart-container");
//         var chart = LightweightCharts.createChart(container, 
//              {
//             width: document.getElementById("chart-container").offsetWidth,
//             layout: {
//                 background: { color: '#00171f' },
//                 textColor: '#DDD',
//             },
//             grid: {
//                 vertLines: { color: 'white' },
//                 horzLines: { color: 'white' },
//             },
//             timeScale: {
//             timeVisible: true, // Show the time
//             borderColor: '#485c7b',
//             timeBorderColor: '#485c7b',
//             timeBackgroundColor: '#00171f',
//             secondsVisible: true,
//           },
//             }
//             );
//         var candlestickSeries = chart.addCandlestickSeries();

//         // Map the fetched JSON data to the required format (open, high, low, close)
//         var formattedData = data.map(item => ({
//           time: item.time,// Assuming "Time" is a string timestamp
//           open: item.open,
//           high: item.high,
//           low: item.low,
//           close: item.close,
//         }));

//         // Add the formatted data to the candlestick series
//         candlestickSeries.setData(formattedData);
//         chart.timeScale().fitContent();

//         // update the most recent bar
//         areaSeries.update({ time: '2023-09-12', value: 25 });
//         candlestickSeries.update({ time: '2023-09-12', open: 109.87, high: 114.69, low: 85.66, close: 112 });

//         // creating the new bar
//         areaSeries.update({ time: '2023-09-12-01', value: 20 });
//         candlestickSeries.update({ time: '2023-09-12', open: 112, high: 112, low: 100, close: 101 });
//       })
//       .catch(error => {
//         console.error('Error fetching chart data:', error);
//       });

//        updateChartData();

//         // Set up an interval to update data periodically (adjust the interval time as needed)
//         setInterval(updateChartData, 60000); 
//   });


  document.addEventListener("DOMContentLoaded", function () {
  // Create the TradingView lightweight chart
  var container = document.getElementById("chart-container");
  var chart = LightweightCharts.createChart(container, {
    width: document.getElementById("chart-container").offsetWidth,
    layout: {
      background: { color: '#00171f' },
      textColor: '#DDD',
    },
    grid: {
      vertLines: { color: 'white' },
      horzLines: { color: 'white' },
    },
    timeScale: {
          timeVisible: true,
          borderColor: '#485c7b',
          timeBorderColor: '#485c7b',
          timeBackgroundColor: '#00171f',
          secondsVisible: true,
          // Specify the format for displaying time
          timeFormat: ['%Y-%m-%d %H:%M'],
          },
        priceScale: {
          minValue: 0,
        },
        rightOffset: 0,
          // Ensure the right-most candlestick stays on scroll
        rightBarStaysOnScroll: true,
 
        
  });

chart.applyOptions({
    timeScale: {
        barSpacing: 5,
        // fixLeftEdge: true,
        // rightOffset: 80,
        rightBarStaysOnScroll: false,
        borderVisible: false,
        borderColor: '#fff000',
        visible: true,
        timeVisible: true,
        secondsVisible: true        }
    }
);

chart.timeScale().fitContent();


  var candlestickSeries = chart.addCandlestickSeries();
chart.priceScale('right').applyOptions({
    scaleMargins: {
        top: 0.6,
        bottom: 0,
    },
});
  function updateChartData() {
    // Make an AJAX request to get the JSON data
    fetch('/custom-data/')  // Update with the correct URL
      .then(response => response.json())
      .then(data => {
        // Map the fetched JSON data to the required format (open, high, low, close)
        var formattedData = data.map(item => ({
          time: item.time , 
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
        }));

        // Set the new data on the candlestick series
        candlestickSeries.setData(formattedData);
      })
      .catch(error => {
        console.error('Error fetching chart data:', error);
      });
  }

  // Call the updateChartData function to initially load data
  updateChartData();

  // Set up an interval to update data periodically (adjust the interval time as needed)
  setInterval(updateChartData, 60000); // Update every 60 seconds (1 minute)
});