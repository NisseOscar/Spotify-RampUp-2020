import numpy as np
from flask import Flask, render_template, redirect, url_for, jsonify, make_response, request
from Frontend import application
# Imports application details from a private file
from details import client_id, client_secret
import requests
from Backend.RequestError import RequestError
from Backend.SptfyApiHndler import SptfyApiHndler

application.config.from_object('configurations.ProductionConfig')

@application.route('/getPlaylists', methods = ['GET'])
def getPlaylists():
    try:
        assert request.path == '/getPlaylists'
        assert request.method == 'GET'

        tkn = request.args.get('tkn')
        ## Get user_id
        req = requests.get( "https://api.spotify.com/v1/me",
                                headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            print('An error occured getting user id occured, error code: '+str(req.status_code))
            raise RequestError('An Error has occured')
        req_Json = req.json()
        usr_id = req_Json['id']
        ## Get user Playlists
        playlists = []
        i = 0
        while(len(playlists)==i):
            req = requests.get("https://api.spotify.com/v1/users/"+usr_id+"/playlists?limit="+str(50)+"&offset="+str(i), headers={ 'authorization': "Bearer " + tkn })
            if req.status_code != 200:
                print('An error occured getting user playlists, error code: '+str(req.status_code))
                raise RequestError('An Error has occured')
            req_Json = req.json()
            for lst in req_Json['items']:
                images = lst['images']
                if(len(images)==0):
                    continue
                if(len(images)>=2):
                    image_url = images[1]['url']
                else:
                    image_url = images[0]['url']
                playlists.append({'id':lst['id'], 'isActive':False,'image_url':image_url, 'name':lst['name'], 'tracks':lst['tracks']['total']})
            i = i+50

        return jsonify({'ok':True, 'playlists':playlists})
    except RequestError:
        return jsonify({'ok':False, 'message':"A requesterror has occured"})
    except AssertionError:
        return jsonify({'ok':False, 'message':"An invalid request has been made"})
    except Exception:
        return jsonify({'ok':False, 'message':"An unexpected error has occured"})

@application.route('/CheckMood', methods = ['GET'])
def checkMood():
    try:
        assert request.path == '/CheckMood'
        assert request.method == 'GET'
        tkn = request.args.get('tkn')
        mood = request.args.get('mood')

        ## Get playlists on mood
        req = requests.get( "https://api.spotify.com/v1/search?q="+mood+"&type=playlist&limit=5",
                                headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            raise RequestError('An Error has occured')
        req_Json = req.json()
        playlists = req_Json['playlists']['items']
        if(len(playlists)<5):
            return jsonify({'ok':True, 'valid':False})
        else:
            return jsonify({'ok':True, 'valid':True})
    except RequestError as e:
        return jsonify({'ok':False, 'message':"A requesterror has occured"})
    except AssertionError as e:
        return jsonify({'ok':False, 'message':"An invalid type of request has been made"})
    except Exception as e:
        return jsonify({'ok':False, 'message':"An unexpected error has occured"})

@application.route('/createPlaylist', methods = ['GET'])
def createPlaylist():
    try:
        assert request.path == '/createPlaylist'
        assert request.method == 'GET'
        tkn = request.args.get('tkn')
        mood = request.args.get('mood')
        playlists = request.args.get('playlistIDs').split(',')
        ####### PUT BACKEND CODE METHOD HERE #################
        sptfyApi = SptfyApiHndler()
        newPlaylistID = sptfyApi.filterPlaylists(client_id,tkn,mood,playlists)
        ########################
        # newPlaylistID = 'https://open.spotify.com/embed/playlist/7xB5RIoWhp2RHVCT43GwWg?si=9XxgO-g9QIS0v4GcIaCH9Q'
        return jsonify({'ok':True, 'newPlaylistID':newPlaylistID})
    except RequestError as e:
        print(e)
        return jsonify({'ok':False, 'message':"A requesterror has occured"})
    except AssertionError as e:
        return jsonify({'ok':False, 'message':"An invalid type of request has been made"})
    except Exception as e:
        print(e)
        return jsonify({'ok':False, 'message':"An unexpected error has occured"})

@application.route('/')
def login():
    scopes = ['user-read-private','user-read-email','playlist-read-private','playlist-read-collaborative','playlist-modify-public']
    scope = '%20'.join(scopes)
    redirect_url = url_for('index')
    redirect_url = 'http://127.0.0.1:5000'+redirect_url
    url = 'https://accounts.spotify.com/authorize?client_id='+client_id+'&redirect_uri='+redirect_url+'&scope='+scope+'&response_type=token&state=123'
    return redirect(url)

@application.route('/welcome')
def index():
    resp = make_response(render_template("index.html"))
    resp.set_cookie('cross-site-cookie', 'spotify1', domain='.spotify.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'spotify2', domain='.accounts.spotify.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'spotify3', domain='.community.spotify.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'spotify4', domain='.www.spotify.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'goadjust', domain='go.adjust.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'applicationadjust', domain='application.adjust.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'general', samesite=None, secure=True);
    resp.headers.add('Set-Cookie','cross-site-cookie=spotify; SameSite=None; Secure')
    return resp

if __name__=='__main__':
    application.run()
