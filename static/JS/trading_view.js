  document.addEventListener("DOMContentLoaded", function () {
  var container = document.getElementById("chart-container");
  container.style.height = "440px"; // Set the desired height

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
          minValue: 0,
        },
        rightOffset: 0,
          // Ensure the right-most candlestick stays on scroll
        rightBarStaysOnScroll: true,
  });


chart.applyOptions({
  timeScale: {
      barSpacing: 5,
      borderVisible: false,
      borderColor: 'red',
      visible: true,
      timeVisible: true,
      secondsVisible: true,   
    },
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

    var timeframe ="5"; //Default Value

    function updateChartData() {
    var ticker_id = document.getElementById("chart-container").getAttribute('value') ;

    console.log("ticker", ticker_id);
    console.log("Time", timeframe);

    var url = '/api/trades/?ticker_id=' + ticker_id + '&timeframe=' + timeframe;
    console.log(url);
    // Make an AJAX request to get the JSON data
    fetch(url)  // Update with the correct URL
      .then(response => response.json())
      .then(data => {
        console.log(data)
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
    console.log("60 Minutes");
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

  // Set up an interval to update data periodically (adjust the interval time as needed)
  setInterval(updateChartData, 60000); // Update every 60 seconds (1 minute)
});

