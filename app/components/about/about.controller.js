(function () {
    'use strict';
    var controllerId = 'AboutController';
    angular.module('angularstrapControllers', []).controller(controllerId, ["$scope", "$http", "$window", "$q", "asyncService",
/*
        /!**
         * Primary entry point for application
         * @param {array} [scope] The global scope for Angular
         * @param {object} [http] Http object (not in use)
         * @param {object} [q] Queing object
         * @param {object} [asyncService] our async service for http calls
         * @param {string} [APIHOST] constant for pointing to REST server
         *
         /*

          */
          function AboutController($scope, $http, $window, $q, asyncService, APIHOST) {

            var vm = this;

            return vm;
        }

    ]);
})();