(function () {
    'use strict';

    angular
        .module('app')
        .factory('UserService', UserService);

    UserService.$inject = ['$http', '$rootScope'];
    function UserService($http, $rootScope) {
        var service = {};

        service.GetAll = GetAll;
        service.GetByUsername = GetByUsername;
        service.GetCurrentUsername = GetCurrentUsername;
        service.Create = Create;
        return service;

        function GetAll() {
            var config = {};
            config = {'headers': {"Authorization": "Bearer "+GenAuthorization()}}
            return $http.get('/api/metrics', config).then(handleSuccess, handleError('Error getting metrics'));
        }

        function GetByUsername(username) {
            var config = {};
            if ($rootScope.globals.currentUser.username === username) {
                config.headers = {"Authorization": "Bearer "+GenAuthorization()};
            }
            return $http.get('/api/users/' + username, config).then(handleSuccess, handleError('Error getting user by username'));
        }

        function GetCurrentUsername() {
            return $http.get('/api/usert/' + localStorage.user).then(handleSuccess, handleError('Error getting current username'));
        }

        function Create(user) {
            return $http.post('/api/users', user).then(handleSuccess, handleError('Error creating user'));
        }

        // private functions

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return { success: false, message: error };
            };
        }

        function base64url(source) {
            // Encode in classical base64
            var encodedSource = CryptoJS.enc.Base64.stringify(source);

            // Remove padding equal characters
            encodedSource = encodedSource.replace(/=+$/, '');

            // Replace characters according to base64url specifications
            encodedSource = encodedSource.replace(/\+/g, '-');
            encodedSource = encodedSource.replace(/\//g, '_');

            return encodedSource;
        }


        function GenAuthorization() {

            if (!$rootScope.globals.currentUser || !$rootScope.globals.currentUser.username) {
                return false;
            }

            var header = {
                    "alg": "HS256",
                    "typ": "JWT"
                },
                data = {
                    "username": $rootScope.globals.currentUser.username,
                    "timestamp": Date.now()
                },
                encodedHeader = base64url(CryptoJS.enc.Utf8.parse(JSON.stringify(header))),
                encodedData = base64url(CryptoJS.enc.Utf8.parse(JSON.stringify(data))),
                encodedSig = base64url(CryptoJS.HmacSHA256(encodedHeader + "." + encodedData, localStorage.user)),
                token = encodedHeader+"."+encodedData+"."+encodedSig;

            return token;
        }

    }

})();
