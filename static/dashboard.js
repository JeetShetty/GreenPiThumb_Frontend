var model = {};
var dashboardApp = angular.module('dashboardApp', []).
  directive('lineGraph', function($parse) {
    return {
      restrict: 'E',
      replace: false,
      scope: {data: '=chartData'},
      link: function (scope, element, attrs) {
         //TODO(mtlynch): This code probably doesn't belong here.

        // Set the dimensions of the canvas / graph
        var margin = {top: 30, right: 20, bottom: 30, left: 50},
          width = 600 - margin.left - margin.right,
          height = 270 - margin.top - margin.bottom;

        // Parse the date / time
        var parseDate = d3.utcParse("%Y%m%dT%H:%M:%S.%LZ");

        // Set the ranges
        var x = d3.scaleTime().range([0, width]);
        var y = d3.scaleLinear().range([height, 0]);

        // Define the axes
        var xAxis = d3.axisBottom(x)
          .ticks(5);

        var yAxis = d3.axisLeft(y)
          .ticks(5);

        // Define the line
        var valueline = d3.line()
          .x(function(d) { return x(d.timestamp); })
          .y(function(d) { return y(d.temperature); });

        // Adds the svg canvas
        var svg = d3.select("body")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

        scope.data.forEach(function(d) {
          d.timestamp = parseDate(d.timestamp);
          d.temperature = +d.temperature;
        });

        // Scale the range of the data
        x.domain(d3.extent(scope.data, function(d) { return d.timestamp; }));
        y.domain([0, d3.max(scope.data, function(d) { return d.temperature; })]);

        // Add the valueline path.
        svg.append("path")
          .attr("class", "line")
          .attr("d", valueline(scope.data));

        // Add the X Axis
        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

        // Add the Y Axis
        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);
      }
    };
  });

dashboardApp.run(function($http) {
  $http.get('/temperatureHistory.json').success(function(temperatureHistory) {
    model.temperature = temperatureHistory[temperatureHistory.length - 1].temperature;
  });
  $http.get('/ambientHumidityHistory.json').success(function(humidityHistory) {
    model.humidity = humidityHistory[humidityHistory.length - 1].humidity;
  });
  $http.get('/reservoirHistory.json').success(function(reservoirHistory) {
    model.reservoirLevel = reservoirHistory[reservoirHistory.length - 1].water_ml;
  });
  $http.get('/lightHistory.json').success(function(lightHistory) {
    model.lightLevel = lightHistory[lightHistory.length - 1].light_pct;
  });
  $http.get('/soilMoistureHistory.json').success(function(moistureHistory) {
    model.soilMoisture = moistureHistory[moistureHistory.length - 1].moisture;
  });
});

dashboardApp.controller('DashboardCtrl', function ($scope) {
   $scope.dashboard = model;
   // TODO(mtlynch): Replace synthetic data with data from JSON APIs.
   $scope.dashboard.myData = [
     {"timestamp": "20160710T15:03:24.919Z", "temperature": 10},
     {"timestamp": "20160710T16:03:24.919Z", "temperature": 20},
     {"timestamp": "20160710T17:03:24.919Z", "temperature": 30},
     {"timestamp": "20160710T18:03:24.919Z", "temperature": 40},
     {"timestamp": "20160710T19:03:24.919Z", "temperature": 60},
   ];
});
