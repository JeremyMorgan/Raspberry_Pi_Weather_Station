(function () {
    'use strict';

    angular.module('angularstrapServices', [])
        .service('asyncService', asyncService);

    asyncService.$inject = ['$http', '$q'];

        function asyncService($http, $q) {
            
            var factory = {
                //properties
                retrievedData: [],
                getHeroText : getHeroText,
                getLatestSnapshot : getLatestSnapshot,
                getLastDay : getLastDay
            };

            function getLatestSnapshot(){
                var deferred = $q.defer();

                $http.get("http://weathercenter.azurewebsites.net/api/Reading/1").
                then(function(response) {
                    deferred.resolve(response.data);
                }, function(error) {
                    deferred.reject(error);
                    console.log("Error: " + JSON.stringify(error));
                });

                return deferred.promise;
            }

            function getLastDay(){
                var deferred = $q.defer();

                $http.get("http://weathercenter.azurewebsites.net/api/Reading/60").
                then(function(response) {
                    deferred.resolve(response.data);
                }, function(error) {
                    deferred.reject(error);
                    console.log("Error: " + JSON.stringify(error));
                });

                return deferred.promise;
            }

            function getHeroText() {

                // this is where we'd put some ajax calls

                factory.retrievedData = {
                    HeroHeader: "Hello AngularStrap!",
                    HeroText: "This is the AngularStrap home page. This text is being pulled from a service, and can be populated by hand coding the property in the controller, dynamically or via services."
                };

                //factory.retrievedData.HeroHeader = "Hello World!";
                //factory.retrievedData.HeroText = "This is the AngularStrap home page. This text is being pulled from a service, and can be populated by hand coding the property in the controller, dynamically or via services.";


            }
            return factory;
        }
})();