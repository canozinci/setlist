/**
 * Created by canozinci on 15/12/14.
 */

'use strict';

// declare modules
angular.module('Authentication', ['ngResource']);
angular.module('Home', ['elasticsearch','ngSanitize','infinite-scroll','ui.sortable']);
angular.module('BasicHttpAuthExample', [
    'Authentication',
    'Home',
    'ngRoute',
    'ngCookies'
])



.factory('AuthInterceptor', function ($rootScope, $q, $window, $location) {
  return {
    request: function (config) {

      //elasticsearche baglanirken auth bilgilerini paste etmesin..
      if( config.url.indexOf("http://canozincimbp.com:9200/")>=0 || config.url.indexOf("http://127.0.0.1:9200/")>=0)
          return config;

        config.headers = config.headers || {};
      if ($window.localStorage.token && $rootScope.userAuthInterceptor) {
        config.headers.Authorization = 'Token ' + $window.localStorage.token;
      }
        return config;
    },

    responseError: function (response) {
      if (response.status === 401) {
       $window.localStorage.removeItem('token');
       $location.path('/');
        return;
      }
      else return $q.reject(response);
    }
  };
})

.config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider){
        // django and angular both support csrf tokens. This tells
        // angular which cookie to add to what header.
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        // bunlardan çok emin değilim
        //$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        //$httpProvider.defaults.withCredentials = true;
        $httpProvider.interceptors.push('AuthInterceptor');
   //     if(window.history && window.history.pushState){
            $locationProvider.html5Mode(true);
            $locationProvider.hashPrefix('!');
     //   }
    }])

.config(['$routeProvider', function ($routeProvider) {

    $routeProvider
        .when('/login', {
            controller: 'authController',
            templateUrl: '/static/modules/authentication/views/login.html',
            hideMenus: true
        })
        .when('/register', {
            controller: 'authController',
            templateUrl: '/static/modules/authentication/views/register.html'
        })
        .when('/', {
            controller: 'HomeController',
            templateUrl: '/static/modules/home/views/home.html'
        })
        .when('/create-band', {
            controller: 'CreateController',
            templateUrl: '/static/modules/home/views/create-band.html'
        })
        .when('/profiles/:userid', {
            controller: 'UserProfileController',
            templateUrl: '/static/modules/home/views/userprofile.html'
        })
        .when('/bands/:bandid', {
            controller: 'BandProfileController',
            templateUrl: '/static/modules/home/views/bandprofile.html'
        })
        .when('/bands/:bandid/create-song', {
            controller: 'SongCreateController',
            templateUrl: '/static/modules/home/views/create-song.html'
        })
        .when('/bands/:bandid/songs/:songid', {
            controller: 'SongDetailController',
            templateUrl: '/static/modules/home/views/song-detail.html'
        })
                .when('/bands/:bandid/create-setlist', {
            controller: 'SetlistCreateController',
            templateUrl: '/static/modules/home/views/create-setlist.html'
        })
        .when('/bands/:bandid/setlists/:setlistid', {
            controller: 'SetlistDetailController',
            templateUrl: '/static/modules/home/views/setlist-detail.html'
        })
        .otherwise({ redirectTo: '/login' });
}])


.run(['$rootScope', '$location', '$cookieStore', '$http','$window','api',
    function ($rootScope, $location, $cookieStore, $http, $window, api) {

         // keep user logged in after page refresh
        try{
            $rootScope.userAuthInterceptor = true;
            $rootScope.authType = 'auth';
            $rootScope.token  = $window.localStorage.token;
            $rootScope.currentuserid  = $window.localStorage.currentuser;

        }

        catch (err){
            console.log(err);
        }

        if ($location.path() !== '/login' && !$window.localStorage.token) {
                $location.path('/login');
            }


        //her url'de login mi diye kontrol ediyor..
        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in
            if ($location.path() !== '/login' && !$window.localStorage.token && $location.path() !== '/register' ) {
                $location.path('/login');
            }
        });
    }]);