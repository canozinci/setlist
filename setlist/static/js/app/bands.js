/**
 * Created by canozinci on 5/27/14.
 */


'use strict';

var app = angular.module('example.api', ['ngResource','ngCookies']);

app.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
})

app.factory('User', [
  '$resource', function($resource) {
    return $resource('http://127.0.0.1\\:8000/api/users/:id',
        {id: '@id'}, {format:'json'});
  }
]);

app.factory('Song', [
  '$resource', function($resource) {
    return $resource('http://127.0.0.1\\:8000/api/songs/:id',
       {id: '@id'}, {format:'json'});
  }
]);

app = angular.module('example.app.list', ['example.api']);

app.controller('UserController', [
  '$scope', 'User', function($scope, User) {
    return $scope.users = User.query();
  }
]);

app.controller('SongController', [
  '$scope', 'Song', function($scope, Song) {
    return $scope.songs = Song.query();
  }
]);

/*
$scope.user = User.get({id: 1});
*/


