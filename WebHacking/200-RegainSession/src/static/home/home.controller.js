(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['UserService', 'AuthenticationService', '$rootScope', '$location', 'FlashService'];
    function HomeController(UserService, AuthenticationService, $rootScope, $location, FlashService) {
        var vm = this;

        vm.user = null;
        vm.allUsers = [];

        initController();

        function initController() {
            loadCurrentUser();
            loadMetrics();
        }

        function loadCurrentUser() {

            if (!$rootScope.globals.currentUser) {
                if (localStorage.user) {
                    UserService.GetCurrentUsername()
                        .then(function(username) {
                            if (username.success === false) {
                                $location.path('/login');
                                return;
                            }
                            $rootScope.globals.currentUser = username;
                            _loadCurrentUser();
                        })
                } else {
                    $location.path('/login');
                    return;
                }
            } else {
                _loadCurrentUser();
            }
        }

        function _loadCurrentUser() {
            UserService.GetByUsername($rootScope.globals.currentUser.username)
                .then(function (user) {
                    AuthenticationService.SetLoginData(user);
                    vm.user = $rootScope.globals.currentUser;
                });
        }

        function loadMetrics() {
            UserService.GetAll()
                .then(function (metrics) {
                    if (metrics.success === false) {
                        FlashService.Error(metrics.message, true);
                        $location.path('/login');
                        return;
                    }
                    console.log(metrics);

                    vm.metrics = metrics.metrics;

                    setTimeout(function() {
                        loadMetrics();
                    }, 5000);

                }, function(response) {
                    console.log(response);
                });

        }
    }

})();