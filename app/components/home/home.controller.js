(function () {
    'use strict';

    angular.module('angularstrapApp')
        .controller('homeController', homeController);

    homeController.$inject = ["$scope", "$http", "$window", "$q", "asyncService"];

    function homeController($scope, $http, $window, $q, asyncService ) {

            var vm = this;

            //services
            vm.angularstrapService = asyncService;
            vm.Snapshot = [];
            vm.TemperatureNow = "";
            vm.PressureUP = false;
            asyncService.getHeroText();

            // from async service
            vm.HeroHeader = asyncService.retrievedData.HeroHeader;
            vm.HeroText = asyncService.retrievedData.HeroText;

            asyncService.getLatestSnapshot()
            .then(function (resultset) {
                    vm.TemperatureNow = ((resultset[0].TempSensorAvg * 9) / 5) + 32;
                    vm.TempSensor1 = ((resultset[0].TempSensor1 * 9) / 5) + 32;
                    vm.TempSensor2 = ((resultset[0].TempSensor2 * 9) / 5) + 32;
                    vm.TempSensor3 = ((resultset[0].TempSensor3 * 9) / 5) + 32;
                    vm.Humidity = resultset[0].Humidity;
                    vm.Pressure = resultset[0].Pressure;
                    vm.Lux = resultset[0].Lux;


                    if (resultset[0].Pressure > 101325){
                        console.log(vm.Pressure + "its up");
                        vm.PressureUP = true;
                    }else {
                        console.log(vm.Pressure + "its down");
                        vm.PressureUP = false;
                    }
                    console.log(JSON.stringify(resultset));                    
                }, function(error) {
                    deferred.reject(error);
                    console.log("requestService Error: " + JSON.stringify(error));
                });
                
                asyncService.getLastDay()
                .then(function (resultset) {
                    //vm.TemperatureNow = ((resultset[0].TempSensorAvg * 9) / 5) + 32;
                    var tempary = [];
                    var humary = [];

                    angular.forEach(resultset, function(value, key) {
                      //console.log("Key is " + key + ' Value is: ' + value);
                       tempary.push(value.TempSensorAvg);
                       humary.push(value.Humidity);
                    
                    }, resultset);       

                    var finalary = [];
                    finalary.push(tempary);
                    finalary.push(humary);
                    $scope.labels = ["1", "2", "3", "4", "5", "6", "7"];
                    $scope.series = ['Temperature', 'Humidity'];
                    console.log(finalary)
                    $scope.data = finalary;

                  $scope.onClick = function (points, evt) {
                    console.log(points, evt);
                  };

                   
                    console.log(JSON.stringify(resultset));   

                }, function(error) {
                    deferred.reject(error);
                    console.log("requestService Error: " + JSON.stringify(error));
                });

                

            // subsections
            vm.col0heading = "Subsections";
            vm.col0text = "I may populate this with a microservice! Or have this be a separate view. This template uses Angular UI which is better than using the Angular router in my opinion.";

            return vm;
       }
})();