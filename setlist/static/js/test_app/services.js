/**
 * Created by canozinci on 5/29/14.
 */


app.factory('AuthService', ['$resource','$window', function($resource,$window){

    function add_token_auth_header(data, headersGetter){

            var headers = headersGetter();
            headers['Authorization'] = ('Token ' + $window.localStorage.token);
            alert('im here');
    }

    return {
        users: $resource('http://127.0.0.1\\:8000/api/users/1', {}, {
                create: {method: 'POST'},
                list: {method: 'GET' , transformRequest: add_token_auth_header}
            }),
        token: $resource('http://127.0.0.1:\\8000/api/token-auth', {}, {
               get_token: {method: 'POST'}
                })
           };
  }]);