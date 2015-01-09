/**
 * Created by canozinci on 15/12/14.
 */
'use strict';

angular.module('Authentication')

.controller('authController', function($scope, $rootScope,api,$window,$location,$http) {
        // Angular does not detect auto-fill or auto-complete. If the browser
        // autofills "username", Angular will be unaware of this and think
        // the $scope.username is blank. To workaround this we use the
        // autofill-event polyfill [4][5]
        //
        //$('#login-form input').checkAndTriggerAutoFillEvent();
        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password, backend: $rootScope.authType};
        };
        $scope.login = function(){
            $rootScope.authType = 'auth';
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        // on good username and password
                        $rootScope.user = data.username;
                        //browser cookie olarak da yazdık
                        $window.localStorage.token = $scope.token;

                    }).
                    catch(function(data){
                        // on incorrect username and password
                        alert(data.data.detail);
                    });
        };
        $scope.get_token = function(){
            $scope.dataLoading = true;
            api.token.list($scope.getCredentials()).
                $promise.
                    then(function(data){
                        // on good username and password
                        $rootScope.token = data.token;
                        $rootScope.currentuser = data.user;

                        $window.localStorage.token = $rootScope.token;
                        $window.localStorage.currentuser = $rootScope.currentuser;
                        $location.path('/');
                    }).
                    catch(function(data){
                        // on incorrect username and password
                        $scope.error = 'Incorrect Username or Password. Please try again.';
                        $scope.dataLoading = false;
                    });
        };
        $scope.register = function(){
            // create user and immediatly login on success
            api.usergenerate.current($scope.getCredentials()).
                $promise.
                    then(function(){
                        $scope.get_token();
                }).
                    catch(function(data){
                        alert(data.data.username);
                    });
            };
        $scope.facebookConnect = function(){
            $rootScope.authType = 'facebook';
            $rootScope.userAuthInterceptor = false;
            OAuth.initialize('XhsiOw-W2-e4Y_x9hcwngWAsly8');
            OAuth.popup('facebook')
                .done(function (result) {
                    result.me().done(function(data) {
                        var token = result.access_token;
                        $http.defaults.headers.common['authorization'] = 'Token ' + token.toString();
                        api.token.list({backend: $rootScope.authType}).
                            $promise.
                                then(function(data){
                                    $rootScope.token = data.token;
                                    $rootScope.currentuser = data.user;
                                    $window.localStorage.token = data.token;
                                    $window.localStorage.currentuser = data.user;
                                    // normal interceptor'a geri dondugumuz icin bunu kaldırıyoruz
                                    delete $http.defaults.headers.common['authorization'];
                                    $rootScope.userAuthInterceptor = true;
                                    $location.path('/');
                                }).
                                catch(function(data){
                                    // on incorrect username and password
                                    $scope.error = 'Something went wrong';
                                    $rootScope.userAuthInterceptor = true;
                                });

                    })
            })
            .fail(function (error) {
                console.log(error);
            });

        };
    });