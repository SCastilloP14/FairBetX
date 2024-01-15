  document.addEventListener("DOMContentLoaded", function () {
  var container = document.getElementById("chart-container");
  container.style.height = container.offsetHeight; // Set the desired height

  var chart = LightweightCharts.createChart(container, {
    width: document.getElementById("chart-container").offsetWidth,
    height: container.offsetHeight, // Set the height dynamically
    layout: {
      background: { color: '#f7f7f7' },
      textColor: '#white',
    },
    grid: {
      vertLines: { color: 'rgba(0, 0, 0, 0)'},
      horzLines: { color: 'white' },
    },
    timeScale: {
          timeVisible: true,
          borderColor: 'red',
          timeBorderColor: 'red',
          timeBackgroundColor: 'red',
          secondsVisible: true,
          // Specify the format for displaying time
          timeFormat: ['%Y-%m-%d %H:%M'],
          },
        priceScale: {
          mode: 0,  // Use '0' for "normal" scale (not logarithmic)
          autoScale: false,  // Disable auto scaling
          invertScale: false,  // Set to 'true' if you want the y-axis inverted
          minValue: 0,
          maxValue: 10,
        },
        rightOffset: 0,
          // Ensure the right-most candlestick stays on scroll
        rightBarStaysOnScroll: true,
  });

// Function to update the chart height
function updateChartHeight() {
  chart.applyOptions({
    height: container.offsetHeight,
  });
}

chart.applyOptions({
  timeScale: {
      barSpacing: 5,
      borderVisible: false,
      borderColor: 'red',
      visible: true,
      timeVisible: true,
      secondsVisible: true, 
    },
  priceScale: {
      scaleMargins: {
        top: 0.6,
        bottom: 0,
      },
      borderColor: 'black',  // Set color for y-axis
      borderWidth: 2,  // Set thickness for y-axis
    },
  }
);

// chart.timeScale().fitContent();
chart.timeScale().applyOptions({
  borderColor:'red',
  barSpacing:10,
})



chart.priceScale('left').applyOptions({
  mode: 0,  // Use '0' for "normal" scale (not logarithmic)
  autoScale: false,  // Disable auto scaling
  invertScale: false,  // Set to 'true' if you want the y-axis inverted
  minValue: 0,
  maxValue: 10,
});

var candlestickSeries = chart.addCandlestickSeries();

chart.priceScale('right').applyOptions({
    
    mode: 0,
    // autoScale: 0,  
  // invertScale: false,  // Set to 'true' if you want the y-axis inverted
  minValue: 0,
  maxValue: 10,
    
});

    var timeframe ="5"; //Default Value

    function updateChartData() {
    var ticker_id = document.getElementById("chart-container").getAttribute('value') ;

    var url = '/api/trades/?ticker_id=' + ticker_id + '&timeframe=' + timeframe;

    // Make an AJAX request to get the JSON data
    fetch(url)  // Update with the correct URL
      .then(response => response.json())
      .then(data => {

        // Map the fetched JSON data to the required format (open, high, low, close)
        var formattedData = data.map(item => ({
          time: new Date(item.timestamp).getTime()/1000 , 
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

  // Event listeners for interval buttons
  document.getElementById("btn-1m").addEventListener("click", function () {
    timeframe = '1';
    updateChartData(timeframe);
  });

  document.getElementById("btn-5m").addEventListener("click", function () {
    timeframe = '5';
    updateChartData(timeframe);
  });

  document.getElementById("btn-1h").addEventListener("click", function () {
    timeframe = '60';
    updateChartData(timeframe);
  });

    document.getElementById("btn-6h").addEventListener("click", function () {
    timeframe = '300';
    updateChartData(timeframe);
  });

    document.getElementById("btn-1d").addEventListener("click", function () {
    timeframe = '1440';
    updateChartData(timeframe);
  });

   

  // Call the updateChartData function to initially load data
  updateChartData();
  window.addEventListener('resize', updateChartHeight);


  // Set up an interval to update data periodically (adjust the interval time as needed)
  setInterval(updateChartData, 60000); // Update every 60 seconds (1 minute)
});

