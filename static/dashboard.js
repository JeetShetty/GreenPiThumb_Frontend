var model = {};
var dashboardApp = angular.module('dashboardApp', []);

dashboardApp.run(function($http) {
  $http.get('/temperatureHistory.json').success(function(temperatureHistory) {
    model.temperature = temperatureHistory[temperatureHistory.length - 1].temperature;
  });
});

dashboardApp.controller('DashboardCtrl', function ($scope) {
   $scope.dashboard = model;
});
