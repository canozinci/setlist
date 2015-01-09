/**
 * Created by canozinci on 15/12/14.
 */
'use strict';

angular.module('Home')

// ago kullanabilmek icin filtre
 .filter('moment', [
    function () {
      return function (date, method) {
        var momented = moment(date);
        return momented[method].apply(momented, Array.prototype.slice.call(arguments, 2));
      };
    }
  ])

//orderBy array icin calisiyor..obcjetler icin ayri filter yazdik
.filter('orderObjectBy', function() {
  return function(items, field, reverse) {
    var filtered = [];
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    filtered.sort(function (a, b) {
      return (a[field] > b[field] ? 1 : -1);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
})

// elasticsearch servisi
.service('esService', function (esFactory) {

    return esFactory({
        host: 'http://canozincimbp.com:9200',
        sniffOnStart: true,
        sniffInterval: 300000 // clusterdaki nodeları check ediyor
    });
})
.controller('SearchServerHealthController', function($scope, esService) {

    esService.cluster.health(function (err, resp) {
        if (err) {
            $scope.error = err.message;
        } else {
            $scope.data = resp;
        }
    });
})



.controller('HomeController',
    function ($scope,$window,$location,$rootScope, api) {
        $scope.bandButtonClicked = false;


        $scope.logout = function(){
            localStorage.removeItem('token');
            localStorage.removeItem('currentuser');
            delete $rootScope.token;
            delete $rootScope.currentuser;
            $rootScope.token = '';
            //$window.localStorage.token ='';
            //$window.localStorage.currentuser ='';
            $location.path('/login');
        };
        $scope.showBands = function(){
            if(!$scope.bandButtonClicked){
                $scope.bandButtonClicked = true;
                return $scope.bands = api.bands.list();
            }
            else {
                $scope.bandButtonClicked = false;
                return $scope.bands= '';
            }
        };
        $scope.showUsers = function(){
            return $scope.users = api.users.list();

        };
        $scope.createBands = function(){
            return $location.path('/create-band');

        };

        if ($rootScope.token){
            $rootScope.currentuserid  = $window.localStorage.currentuser;
            api.currentuser.list({id : $rootScope.currentuserid }).
            $promise.
                then(function(data){
                    $rootScope.currentuser = data;


                })
                .catch(function(data){
                    });
        }
    })
.controller('CreateController',
    function ($scope,$window,$location,$rootScope, api) {

    $scope.getBandName = function(){

        return {name: $scope.bandname}
    };
    $scope.createBand = function(){
        console.log($scope.getBandName());
        api.bands.create($scope.getBandName()).
                $promise.
                    then(function(data){
                        console.log("misssion accomplised")
                }).
                    catch(function(data){
                       console.log("misssion not accomplised")
                    });
            };

    })
.controller('UserProfileController',
    function ($scope,$window,$location,$rootScope, api, $routeParams) {

        api.currentuser.list({id: $routeParams.userid}).
              $promise.
                    then(function(data){

                    $scope.userprofile =data;

                }).
                    catch(function(data){
                       console.log("misssion not accomplised")
                    });

    })
.controller('BandProfileController',
    function ($scope,$window,$location,$rootScope, api, $routeParams) {

        $scope.addSetlistBox = false;

        api.bandprofile.list({id: $routeParams.bandid}).
              $promise.
                    then(function(data){

                    $scope.band =data;
                    $scope.members = [];
                    $scope.songs = [];
                    $scope.setlists = [];
                    $scope.events = [];


                    $.each(data.band_member, function(index, element){
                        api.currentuser.list({id: element.user}).
                            $promise.
                                then(function(data){
                                    $scope.members.push(data);
                                 }).
                    catch(function(data){
                       console.log("misssion not accomplised");
                    });
                    });
                    $.each(data.songs, function(index, element){
                        $scope.songs.push(element);

                    });
                    $.each(data.setlists, function(index, element){
                        $scope.setlists.push(element);

                    });
                    $.each(data.events, function(index, element){
                        $scope.events.push(element);

                    });
                    attendance_count();
                }).
                    catch(function(data){
                       console.log("misssion not accomplised")
                    });
        var attendance_count = function(){

            for(var i =0; i< $scope.events.length; i++){
                $scope.events[i].attends = [];
                $scope.events[i].notattends = [];
                $scope.events[i].notreplies = [];

                for (var y=0; y<$scope.events[i].attending.length;y++ ){

                    if($scope.events[i].attending[y].status == true){
                        $scope.events[i].attends.push($scope.events[i].attending[y].bandmember);
                    }
                    else if($scope.events[i].attending[y].status == false){
                        $scope.events[i].notattends.push($scope.events[i].attending[y].bandmember);
                    }
                    if($scope.events[i].attending[y].status == null){
                        $scope.events[i].notreplies.push($scope.events[i].attending[y].bandmember);
                    }
                }

            }
        }


        api.bandactions.list({bandid: $routeParams.bandid}).
                $promise.
                then(function(data){
                    $scope.actions = data;
                }).
                catch (function(data){
                    console.log(data.data);
                });
    $scope.addSong = function(){
        console.log($scope.band.id);
        $location.path('/bands/'+ $scope.band.id+'/create-song');
    }
    $scope.createSetlist =function(name){
                console.log("here");

                api.setlistncreate.create({band: $routeParams.bandid, name: name}).
              $promise.
                    then(function(data){
                         $location.path('/bands/'+ $routeParams.bandid+'/setlists/'+data.id);
                    }).
                    catch(function(data){
                       console.log("NOOO");
                        $scope.error = data;
                    });


    }
    })

.controller('SongCreateController',
    function ($scope,$window,$location,$rootScope, api, $routeParams) {

   $scope.is_original_indicator =true;

   $scope.setOriginalValue = function(value){

       console.log(value);
       $scope.is_original_indicator = value;
   };

   $scope.getSongData = function(){

            return {name: $scope.songname, band: $routeParams.bandid, length:$scope.length, is_original: $scope.is_original, original_album_name:$scope.original_album_name, original_artist:$scope.original_artist}
       };


    $scope.createSong = function(){
        api.bandsongs.create($scope.getSongData()).
                $promise.
                    then(function(data){
                        //$location.path('/bands/'+ $routeParams.bandid);
                        $location.path('/bands/'+ $routeParams.bandid+'/songs/'+data.id);
                }).
                    catch(function(data){
                        $scope.error = data.data;
                       console.log("misssion not accomplised")
                    });
            };

    })

.controller('SongDetailController' ,
    function ($scope,$window,$location,$rootScope, api, $routeParams, $timeout, $sce){
        $scope.addSongPartBoxVisible = false;
        $scope.lyricsBoxVisible = false;
        $scope.addlyricsBoxVisible = false;
        $scope.addCommentBoxVisible = false;
        $scope.addMediaBoxVisible = false;
        $scope.songid =$routeParams.songid;
        $scope.bandid =$routeParams.bandid;

        $scope.getSongData = function(){

            return {songid: $scope.songid}
       };

        //api call to load song data, refreshes itself every 15 seconds
        $scope.loadData = function(){api.songdetail.list($scope.getSongData()).
                $promise.
                    then(function(data){
                        //$timeout($scope.loadData, 15000);
                       $scope.song = data;

                       $scope.songparts =$scope.song.song_parts;
                        $scope.getExistingUserInstruments();
                        }).
                    catch(function(data){
            console.log(data);
        })};

        //initial function call
        $scope.loadData();
        //api call to delete a songpart
        $scope.removeSongPart = function(Bandid, Songid,SongPartid){
            $scope.getSongPartData = function(){
                return {bandid: Bandid, songid: Songid, partid:SongPartid }
            };

            api.songpart.delete($scope.getSongPartData()).
                $promise.
                then (function(data){
                $scope.loadData();
                }).
                catch(function(data){
                    $scope.error= data.data.detail;
            })

        };
        //api call to create the songpart
        $scope.createSongPart = function(user_instrument,bandid,song){

            var getParams = function(){
                console.log(user_instrument,song,bandid);
                return {user_instrument:user_instrument,song: song,bandid: bandid }

            }

            api.songpartcreate.create(getParams()).
                $promise.
                    then(function(data){
                    $scope.loadData();
                }).
                    catch(function(data){});

        }
        //main function for this subview(div), loads band member data with their instruments
        $scope.addSongPart = function(bandid){

            $scope.getBandId = function(){
            return {bandid:bandid}

        }

            api.bandmembers.list($scope.getBandId()).
                $promise.
                    then(function(data){
                        $scope.addSongPartBoxVisible = true;
                        $scope.members =data;
                }).
                    catch(function(data){
                        $scope.error = data.data;
                       console.log("misssion not accomplised")
                    });





        }

        //read exisiting userinstruments for this song into an array
        $scope.getExistingUserInstruments = function(){

            $scope.UserInstrumentContainer =[];


            for (var loopindex = 0; loopindex<$scope.song.song_parts.length; loopindex++){


                $scope.UserInstrumentContainer.push($scope.song.song_parts[loopindex].user_instrument.id);
            }

        }
        //checks if the listed UserPart is already included in this Song
        $scope.checkExisting = function(a){
            return $scope.UserInstrumentContainer.indexOf(a) > -1;
        }

        $scope.addSongComment = function(song,band, body){

            var getParams = function(){

                console.log(band, song, body);
                return {band:band, song:song, body:body}

            }

            api.songcommentcreate.create(getParams()).
                $promise.
                 then(function(data){
                    $scope.addCommentBoxVisible =false;
                    $scope.loadData();
                }).
                 catch(function(data){
                    console.log("not done");
                });
        }

        $scope.addSongMedia = function(song,band, link, description){

            var getParams = function(){


                return {band:band, song:song, description:description, link: link}

            }

            api.songmediacreate.create(getParams()).
                $promise.
                 then(function(data){
                    console.log("done");
                    $scope.addMediaBoxVisible =false;
                    $scope.loadData();
                }).
                 catch(function(data){
                    console.log("not done");
                });
        }

        $scope.getIframeSource = function(domain,link){
            var long_link;
            var long_link_temp;

           if(domain =="youtube"){
                long_link_temp = "http://www.youtube.com/embed/"+link+ "?rel=0&amp;showinfo=0";

            }
           else if(domain =="vimeo"){
               long_link_temp = "http://player.vimeo.com/video"+link;
           }
            long_link = $sce.trustAsResourceUrl(long_link_temp);
            return long_link;
        }

        $scope.addSongLyrics = function(lyrics){

            console.log(lyrics);

            api.songedit.update({songid: $scope.song.id,lyrics:lyrics}).
                $promise.
                 then(function(data){
                    $scope.loadData();
                }).
                 catch(function(data){
                    $scope.error =data;
                });
            $scope.addlyricsBoxVisible =!$scope.addlyricsBoxVisible;
        }

    })


.controller('SetlistDetailController' ,
    function ($scope,$window,$location,$rootScope, api, $routeParams, $timeout, $sce, esService,$filter){
        $scope.addCommentBoxVisible = false;
        $scope.queryTerm = [];
        $scope.hits = [];
        $scope.per_page = 20;
        $scope.page = 0;
        $scope.bandid =$routeParams.bandid;
        $scope.setlistid =$routeParams.setlistid;
        $scope.setlist = [];
        $scope.setlist.sections = [];
        $scope.addSetlistBoxVisible =false;
        var songArray =[];
        var updateArray = function (array, old_index, new_index) {
            if (new_index >= array.length) {
                var k = new_index - array.length;
                while ((k--) + 1) {
                    array.push(undefined);
                }
            }
            array.splice(new_index, 0, array.splice(old_index, 1)[0]);
        };
        $scope.sortableOptions = {
            cursor : "move",
            start: function(event, ui) {
                    ui.item.startPos = ui.item.index();
                    songArray =[];
                    for (var i = 1; i <= ui.item.scope().section.section_songs.length;i++){
                        songArray.push(ui.item.scope().section.section_songs[i-1].id);
                    }
                    },
            stop: function(e,ui) {
                var y = 0;
                var startposition = ui.item.startPos;
                var finishposition = ui.item.index();
                updateArray(songArray,startposition,finishposition);
              for (var i = 1; i <= ui.item.scope().section.section_songs.length;i++){
                    var section_id= ui.item.scope().section.id;

                    api.setlistsectionsongupdate.update({bandid:$routeParams.bandid, setlist :$routeParams.setlistid,section:section_id,song:songArray[i-1],song_number:i}).
                        $promise.
                            then(function(data){

                                if( y == ui.item.scope().section.section_songs.length){
                                    $scope.loadData();
                                }
                         }).
                            catch(function(data){
                        $scope.error =data
                    });
                    y= y+1;

                }



            }

        };
        var sortSongs = function(ary){
            var length = ary['sections'].length;
            for (var i = 0; i<length;i++){
               ary['sections'][i]['section_songs'] = $filter('orderBy')(ary['sections'][i]['section_songs'], 'song_number');
            }
        }

        $scope.getSetlistData = function(){

            return {bandid: $scope.bandid, setlistid : $scope.setlistid}
       };
        //api call to load song data, refreshes itself every 15 seconds
        $scope.loadData = function(){api.bandsetlist.list($scope.getSetlistData()).
                $promise.
                    then(function(data){
                        //$timeout($scope.loadData, 15000);
                        var newData = data;
                        sortSongs(newData);
                        $scope.setlist = newData;
                       $scope.sections =$scope.setlist.sections;
                        }).
                    catch(function(data){
                $scope.error =data.data;
        })};
        $scope.loadData();
        $scope.songs=[];
        $scope.getSongDetails = function(songid){

            api.songdetail.list({songid:songid}).
                $promise.
                then (function(data){
                    var i;
                    for (i = 0; i < $scope.songs.length; i++) {
                        // gelen song elimizdeki arrayde varmı diye kontrol ediyoruz
                        if (angular.equals($scope.songs[i], data)) {
                             return;
                            }
                        }
                    $scope.songs.push(data);

                }).
                catch (function(data){
                $scope.error =data.data;
            })
        };
        $scope.deleteSetlist = function(){
            if ($window.confirm('The setlist will be deleted permanently. Are you sure?')){


                api.setlistdelete.delete({bandid:$routeParams.bandid, setlistid :$routeParams.setlistid}).
                    $promise.
                        then(function(data){
                            console.log(data);
                            $location.path('/bands/'+$routeParams.bandid);
                        }).
                        catch(function(data){
                        $scope.error =data
                    }
                    )
            };


        }
        $scope.deleteSong = function(sectionid, songid, parentindex){

            var update_song_numbers = function(){
                var song_counter = 1;
                for (var i = 0; i < $scope.setlist.sections[parentindex].section_songs.length;i++){

                    // sildigimiz song ise loopta pass geciyoruz ve song_number icin i yerine ayri bir index tutuyoruz
                    if(songid !=$scope.setlist.sections[parentindex].section_songs[i].id ){
                    api.setlistsectionsongupdate.update({bandid:$routeParams.bandid, setlist :$routeParams.setlistid,section:$scope.setlist.sections[parentindex].id,song:$scope.setlist.sections[parentindex].section_songs[i].id,song_number:song_counter}).
                        $promise.
                            then(function(data){

                            $scope.loadData();
                         }).
                            catch(function(data){
                                $scope.error =data
                            })
                    song_counter = song_counter +1;
                    }
                    else { $scope.loadData();}
               }
        };
            api.setlistsectionsongdelete.delete({bandid:$routeParams.bandid, setlistid :$routeParams.setlistid,sectionid:sectionid,songid:songid}).
                    $promise.
                        then(function(data){
                               update_song_numbers();

                        }).
                        catch(function(data){
                        $scope.error =data
                    }
                    )

        };
        $scope.showSectionBox = function(){
            $scope.addSetlistBoxVisible =!$scope.addSetlistBoxVisible;
        }
        $scope.addSetlistSection = function(setlistname){
            console.log(setlistname);
            api.setlistsectioncreate.create({bandid:$scope.bandid,setlist:$scope.setlistid,name:setlistname }).
                $promise.
                 then(function(data){
                     $scope.addSetlistBoxVisible =false;
                     $scope.loadData();
                }).
                catch(function(data){
                    $scope.error=data;
                })

        }
        $scope.deleteSection = function(sectionid){
                api.setlistsectiondelete.delete({bandid:$routeParams.bandid, setlistid :$routeParams.setlistid,sectionid:sectionid}).
                    $promise.
                        then(function(data){
                            $scope.loadData();

                        }).
                        catch(function(data){
                        $scope.error =data
                    }
                    )



        }
        //pagination ve infite scroll daha patlak
        $scope.show_more = function () {
            if($scope.total_results > ($scope.page+$scope.per_page)){
                $scope.page = $scope.page+$scope.per_page;
            }

        };
        $scope.searchSong = function(index){
        esService.search({
            index: 'setlist_index',
            size: $scope.per_page,
            from: $scope.page,
            body: {
            "query":
                {
                    "match": {
                        _all: {
                            "query": $scope.queryTerm[index],
                            "operator": "and"
                        }
                    }
                }
            }
            })
            .then(function (response) {
              $scope.hits[index] = response.hits.hits;
              $scope.total_results = response.hits.total;
            });
        }
        $scope.searchSongAdd = function(sectionid,parentindex, index){

            api.setlistsectionsongcreate.create({bandid:$routeParams.bandid, setlist :$routeParams.setlistid,section:sectionid,song: $scope.hits[parentindex][index]._id,song_number:$scope.setlist.sections[parentindex].section_songs.length +1}).
                    $promise.
                        then(function(data){
                            $scope.loadData();
                        }).
                        catch(function(data){
                        $scope.error =data
                    }
                    )

        }

        $scope.addSetlistComment = function(body){

            var getParams = function(){

                return {bandid:$routeParams.bandid, setlist:$routeParams.setlistid, body:body}

            }

            api.setlistcommentcreate.create(getParams()).
                $promise.
                 then(function(data){
                    $scope.addCommentBoxVisible =false;
                    $scope.loadData();
                }).
                 catch(function(data){
                    console.log("not done");
                });
        }
    })



;