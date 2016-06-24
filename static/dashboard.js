var model = {};
var dashboardApp = angular.module('dashboardApp', []);

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
});
