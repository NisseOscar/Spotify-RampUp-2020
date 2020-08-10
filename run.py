import time
from flask import Flask, render_template, redirect, url_for, jsonify, make_response
from Frontend import app
# Imports app details from a private file
from details import client_id, client_secret
from flask import request
import requests
from Backend.RequestError import RequestError

@app.route('/getPlaylists', methods = ['GET'])
def getPlaylists():
    try:
        assert request.path == '/getPlaylists'
        assert request.method == 'GET'

        tkn = request.args.get('tkn')
        ## Get user_id
        req = requests.get( "https://api.spotify.com/v1/me",
                                headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            raise RequestError()
        req_Json = req.json()
        usr_id = req_Json['id']
        ## Get user Playlists
        playlists = []
        i = 0
        while(len(playlists)==i):
            req = requests.get("https://api.spotify.com/v1/users/"+usr_id+"/playlists?limit="+str(50)+"&offset="+str(i), headers={ 'authorization': "Bearer " + tkn })
            if req.status_code != 200:
                raise RequestError()
            req_Json = req.json()
            tmpPlaylists = [{'id':lst['id'], 'isActive':False,'image_ref':lst['images'][0]['url'], 'name':lst['name'], 'tracks':lst['tracks']['total']} for lst in req_Json['items']]
            playlists = playlists+tmpPlaylists
            i = i+50

        return jsonify({'code':200, 'playlists':playlists})
    except RequestError:
        return jsonify({'ok':False, 'message':"A requesterror has occured"})
    except AssertionError:
        return jsonify({'ok':False, 'message':"An invalid request has been made"})
    except Exception:
        return jsonify({'ok':False, 'message':"An unexpected error has occured"})

@app.route('/CheckMood', methods = ['GET'])
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
            raise RequestError()
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

@app.route('/createPlaylist', methods = ['GET'])
def createPlaylist():
    try:
        assert request.path == '/createPlaylist'
        assert request.method == 'GET'
        tkn = request.args.get('tkn')
        mood = request.args.get('mood')
        playlists = request.args.get('playlists')
        ####### PUT BACKEND CODE METHOD HERE #################

        ########################
        newPlaylistID = 'https://open.spotify.com/playlist/7xB5RIoWhp2RHVCT43GwWg?si=rmjmqajXQEuuyHhZYfT6eg'
        return jsonify({'ok':True, 'newPlaylistID':newPlaylistID})
    except RequestError as e:
        return jsonify({'ok':False, 'message':"A requesterror has occured"})
    except AssertionError as e:
        return jsonify({'ok':False, 'message':"An invalid type of request has been made"})
    except Exception as e:
        print(e)
        return jsonify({'ok':False, 'message':"An unexpected error has occured"})

@app.route('/')
def login():
    scope = 'user-read-private%20playlist-read-private%20playlist-read-collaborative%20user-read-email'
    redirect_url = url_for('index')
    redirect_url = 'http://127.0.0.1:5000'+redirect_url
    print(redirect_url)
    url = 'https://accounts.spotify.com/authorize?client_id='+client_id+'&redirect_uri='+redirect_url+'&scope='+scope+'&response_type=token&state=123'
    print(url)
    return redirect(url)

@app.route('/welcome')
def index():
    resp = make_response(render_template("index.html"))
    resp.set_cookie('same-site-cookie', 'foo', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'bar', domain='.spotify.com', samesite=None, secure=True);
    resp.set_cookie('cross-site-cookie', 'bar', domain='.adjust.com', samesite=None, secure=True);
    # resp.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')
    return resp
    # return render_template("index.html")

if __name__=='__main__':
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
