/**
 * Created by canozinci on 5/29/14.
 */

app.controller('authController', function($scope, AuthService,$window) {
    $('#id_auth_form input').checkAndTriggerAutoFillEvent();
    $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };
     $scope.get_my_token = function(){
            AuthService.token.get_token($scope.getCredentials()).
                $promise.
                    then(function(data){
                        $scope.token = data.token;
                        $window.localStorage.token = $scope.token;
                    }).
                    catch(function(data){
                        alert(data.data);
                        alert(data.data.detail);
                    });
        };
    $scope.get_user = function(){
            var users = AuthService.users.list();
            console.log(users.id);
        };
});
