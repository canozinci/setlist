/**
 * Created by canozinci on 15/12/14.
 */
'use strict';

angular.module('Authentication')

.factory('api', function($resource , $rootScope, $window ){

    //patch yaparken gereksiz datalari siliyorum
    var dropUnchangedFields = function(data, headerGetter) {
        var newData = data;
        delete newData['bandid'] ;
        delete newData['setlist'] ;
        delete newData['section'] ;
        delete newData['song'] ;


        return JSON.stringify(newData);

}



        function add_auth_header(data, headersGetter){
            // as per HTTP authentication spec [1], credentials must be
            // encoded in base64. Lets use window.btoa [2]
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }
        //function add_token_auth_header($scope, headersGetter){
            // as per HTTP authentication spec [1], credentials must be
            // encoded in base64. Lets use window.btoa [2]
         //   var headers = headersGetter();
         //   headers['Authorization'] = ('Token ' + $rootScope.token);
            //console.log($window.localStorage.token);
            //headers['Authorization'] = ('Token ' +  $window.localStorage.token);
        //}
        // defining the endpoints. Note we escape url trailing dashes: Angular
        // strips unescaped trailing slashes. Problem as Django redirects urls
        // not ending in slashes to url that ends in slash for SEO reasons, unless
        // we tell Django not to [3]. This is a problem as the POST data cannot
        // be sent with the redirect. So we want Angular to not strip the slashes!

        //transformRequest: add_token_auth_header
        return {
            auth: $resource('http://127.0.0.1\\:8000/api/auth', {}, {
                login: {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            }),
            users: $resource('http://127.0.0.1\\:8000/api/users\\/', {}, {
                list: {method: 'GET', isArray:true}
            }),
            currentuser: $resource('http://127.0.0.1\\:8000/api/users/:id', {id :"@id"}, {
                list: {method: 'GET'}
            }),
            usergenerate: $resource('http://127.0.0.1\\:8000/api/users/usergenerate\\/', {}, {
                create: {method: 'POST'}
            }),
            bands: $resource('http://127.0.0.1\\:8000/api/bands\\/', {}, {
                create: {method: 'POST'},
                list: {method: 'GET', isArray:true}
            }),
            bandprofile: $resource('http://127.0.0.1\\:8000/api/bands/:id', {id :"@id"}, {
                create: {method: 'POST'},
                list: {method: 'GET'}
            }),
            bandsongs: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/songs\\/:songid', {bandid :"@band", songid:"@songid"}, {
                create: {method: 'POST'},
                list: {method: 'GET'}
            }),
            songdetail: $resource('http://127.0.0.1\\:8000/api/songs/:songid', { songid:"@songid"}, {
                list: {method: 'GET'}
            }),
            songedit: $resource('http://127.0.0.1\\:8000/api/songs/:songid/songedit\\/', { songid:"@songid"}, {
                update: {method: 'PATCH'}
            }),
            songpart: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/songs/:songid/parts/:partid\\/', {bandid :"@bandid", songid:"@songid", partid:"@partid"}, {
                list: {method: 'GET'},
                delete: {method: 'DELETE'}

            }),
            songpartcreate: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/songs/:song/parts\\/', {bandid :"@bandid", song:"@song"}, {
                create: {method: 'POST'}

            }),
            bandmembers: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/members\\/', { bandid:"@bandid"}, {
                list: {method: 'GET', isArray:true}
            }),
            bandactions: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/actions\\/', { bandid:"@bandid"}, {
                list: {method: 'GET', isArray:true}
            }),
            songcommentcreate: $resource('http://127.0.0.1\\:8000/api/bands/:band/songs/:song/createcomments\\/', {band :"@band", song:"@song"}, {
                create: {method: 'POST'}

            }),
            songmediacreate: $resource('http://127.0.0.1\\:8000/api/bands/:band/songs/:song/createmedia\\/', {band :"@band", song:"@song"}, {
                create: {method: 'POST'}

            }),

            bandsetlist: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/nested\\/', { bandid:"@bandid", setlistid:"@setlistid"}, {
                list: {method: 'GET'}
            }),

            setlistncreate: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists\\/', { bandid:"@band", setlistid:"@setlistid"}, {
                create: {method: 'POST'}
            }),
            setlistdelete: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid\\/', { bandid:"@bandid", setlistid:"@setlistid"}, {
                delete: {method: 'DELETE'}
            }),
            setlistcommentcreate: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/createcomments\\/', {bandid:"@bandid", setlistid:"@setlist"}, {
                create: {method: 'POST'}

            }),
            setlistsectioncreate: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/sections\\/', { bandid:"@bandid", setlistid:"@setlist"}, {
                create: {method: 'POST'}
            }),
            setlistsectiondelete: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/sections/:sectionid\\/', { bandid:"@bandid", setlistid:"@setlistid", sectionid:"@sectionid"}, {
                delete: {method: 'DELETE'}
            }),

            setlistsectionsongcreate: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/sections/:sectionid/songs\\/', { bandid:"@bandid", setlistid:"@setlist",sectionid:"@section"}, {
                create: {method: 'POST'}
            }),

            setlistsectionsongdelete: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/sections/:sectionid/songs/:songid\\/', { bandid:"@bandid", setlistid:"@setlistid",sectionid:"@sectionid",songid:"@songid"}, {
                delete: {method: 'DELETE'}
            }),
            setlistsectionsongupdate: $resource('http://127.0.0.1\\:8000/api/bands/:bandid/setlists/:setlistid/sections/:sectionid/songs/:songid\\/', { bandid:"@bandid", setlistid:"@setlist",sectionid:"@section",songid:"@song"}, {
                update: {method: 'PATCH',
                transformRequest: dropUnchangedFields
                }
            }),

            token: $resource('http://127.0.0.1:8000/api/token-auth/:backend', {backend :"@backend"}, {
                list: {method: 'POST'}
            })
        };
    })

