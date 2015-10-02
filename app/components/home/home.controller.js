(function () {
    'use strict';

    angular.module('angularstrapApp')
        .controller('homeController', homeController);

    homeController.$inject = ["$scope", "$http", "$window", "$q", "asyncService"];

    function homeController($scope, $http, $window, $q, asyncService ) {

            var vm = this;

            // guage settings
            vm.options = {
                width: 500, height: 200,
                min: 0,
                max: 120,
                greenFrom: 0,
                greenTo: 32,
                yellowFrom: 32,
                yellowTo: 80,
                redFrom: 80,
                redTo: 120,
                greenColor: '#B8EEFC',
                yellowColor: '#FCCF80',
                redColor: '#F25337',
                minorTicks: 4
            };

            //services
            vm.angularstrapService = asyncService;
            vm.Snapshot = [];
            vm.TemperatureNow = "";
            vm.PressureUP = false;
            asyncService.getHeroText();

            // from async service
            vm.HeroHeader = asyncService.retrievedData.HeroHeader;
            vm.HeroText = asyncService.retrievedData.HeroText;

            function drawGuages(){
                 vm.guage1data = google.visualization.arrayToDataTable([
                      ['Label', 'Value'],
                      ['', vm.TempSensor1],
                    ]);
                 vm.guage2data = google.visualization.arrayToDataTable([
                      ['Label', 'Value'],
                      ['', vm.TempSensor2],
                    ]);
                 vm.guage3data = google.visualization.arrayToDataTable([
                      ['Label', 'Value'],
                      ['', vm.TempSensor3],
                    ]);

                    var chart1 = new google.visualization.Gauge(document.getElementById('chart_div1'));
                    var chart2 = new google.visualization.Gauge(document.getElementById('chart_div2'));
                    var chart3 = new google.visualization.Gauge(document.getElementById('chart_div3'));

                    chart1.draw(vm.guage1data, vm.options);
                    chart2.draw(vm.guage2data, vm.options);
                    chart3.draw(vm.guage3data, vm.options);
            }

            asyncService.getLatestSnapshot()
            .then(function (resultset) {
                    vm.TemperatureNow = ((resultset[0].TempSensorAvg * 9) / 5) + 32;
                    vm.TempSensor1 = ((resultset[0].TempSensor1 * 9) / 5) + 32;
                    vm.TempSensor2 = ((resultset[0].TempSensor2 * 9) / 5) + 32;
                    vm.TempSensor3 = ((resultset[0].TempSensor3 * 9) / 5) + 32;
                    vm.Humidity = resultset[0].Humidity;
                    vm.Pressure = resultset[0].Pressure;
                    vm.Lux = resultset[0].Lux;

                    drawGuages();

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
          
                       tempary.push(((value.TempSensorAvg * 9) / 5) + 32);
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