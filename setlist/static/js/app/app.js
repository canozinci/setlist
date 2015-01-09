

angular.module('authApp', ['ngResource']).
    config(['$httpProvider', function($httpProvider){
        // django and angular both support csrf tokens. This tells
        // angular which cookie to add to what header.
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    }]).
    factory('sharedScope', function($rootScope) {
        var scope = $rootScope.$new(true);
        scope.data = {text: ""};
        return scope;
    }).
    factory('api', function($resource , sharedScope,$window ){
        function add_auth_header(data, headersGetter){
            // as per HTTP authentication spec [1], credentials must be
            // encoded in base64. Lets use window.btoa [2]
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));


        }
        function add_token_auth_header($scope, headersGetter){
            // as per HTTP authentication spec [1], credentials must be
            // encoded in base64. Lets use window.btoa [2]
            var headers = headersGetter();
            headers['Authorization'] = ('Token ' + sharedScope.data.text);
            //console.log($window.localStorage.token);
            //headers['Authorization'] = ('Token ' +  $window.localStorage.token);


        }
        // defining the endpoints. Note we escape url trailing dashes: Angular
        // strips unescaped trailing slashes. Problem as Django redirects urls
        // not ending in slashes to url that ends in slash for SEO reasons, unless
        // we tell Django not to [3]. This is a problem as the POST data cannot
        // be sent with the redirect. So we want Angular to not strip the slashes!
        return {
            auth: $resource('http://127.0.0.1\\:8000/api/auth', {}, {
                login: {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            }),
            users: $resource('http://127.0.0.1\\:8000/api/users', {}, {
                create: {method: 'POST'},
                list: {method: 'GET' , transformRequest: add_token_auth_header}
            }),
            bands: $resource('http://127.0.0.1\\:8000/api/bands', {}, {
                create: {method: 'POST', transformRequest: add_token_auth_header},
                list: {method: 'GET', transformRequest: add_token_auth_header, isArray:true}
            }),
            token: $resource('http://127.0.0.1:8000/api/token-auth', {}, {
                list: {method: 'POST'}
            })
        };
    }).

    controller('authController', function($scope, sharedScope,api,$window) {
        // Angular does not detect auto-fill or auto-complete. If the browser
        // autofills "username", Angular will be unaware of this and think
        // the $scope.username is blank. To workaround this we use the
        // autofill-event polyfill [4][5]
        $('#id_auth_form input').checkAndTriggerAutoFillEvent();
        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };
        $scope.login = function(){
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        // on good username and password
                        $scope.user = data.username;
                        //browser cookie olarak da yazdık
                        $window.localStorage.token = $scope.token;

                    }).
                    catch(function(data){
                        // on incorrect username and password
                        alert(data.data.detail);
                    });
        };
        $scope.get_token = function(){
            api.token.list($scope.getCredentials()).
                $promise.
                    then(function(data){
                        // on good username and password
                        $scope.token = data.token;
                        $window.localStorage.token = $scope.token;
                        sharedScope.data.text = $scope.token;
                    }).
                    catch(function(data){
                        // on incorrect username and password
                        alert('WRONGGG');
                    });
        };

        $scope.logout = function(){
            api.auth.logout(function(){
                $window.localStorage.token ='';
                $scope.user = undefined;
            });
        };
        $scope.register = function($event){
            // prevent login form from firing
            $event.preventDefault();
            // create user and immediatly login on success
            api.users.create($scope.getCredentials()).
                $promise.
                    then($scope.login).
                    catch(function(data){
                        alert(data.data.username);
                    });
            };
    }).
    controller('bandController', function($scope, sharedScope, api) {
        //$scope.token = sharedScope.data;
        //return $scope.bands = api.bands.list();
        //console.log($scope.bands);
        //$scope.bands = api.bands.list();
        $scope.showBands = function(){
            return $scope.bands = api.bands.list();

        };
        $scope.showUsers = function(){

            return $scope.test2="Users";
        };

    })
;



