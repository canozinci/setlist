/**
 * Created by canozinci on 5/29/14.
 */

var app = angular.module('SetList',['ngResource']);

app.config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
