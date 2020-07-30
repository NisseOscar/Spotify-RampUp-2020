import time
from flask import Flask, render_template, redirect, url_for, jsonify
from Frontend import app
# Imports app details from a private file
from details import client_id, client_secret
from flask import request
import requests
from Backend import RequestError

@app.route('/getPlaylists', methods = ['GET'])
def getPlaylists():
    assert request.path == '/getPlaylists'
    assert request.method == 'GET'

    tkn = request.args.get('tkn')


    ## Get user_id
    req = requests.get( "https://api.spotify.com/v1/me",
                            headers={ 'authorization': "Bearer " + tkn })
    if req.status_code != 200:
        raise RequestError(req.status_code)
    req_Json = req.json()
    usr_id = req_Json['id']
    ## Get user Playlists
    playlists = []
    i = 0
    while(len(playlists)==i):
        req = requests.get("https://api.spotify.com/v1/users/"+usr_id+"/playlists?limit="+str(50)+"&offset="+str(i), headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            raise RequestError(req.status_code)
        req_Json = req.json()
        tmpPlaylists = [{'id':item['id'], 'isActive':False,'image_ref':item['images'][0]['url'], 'name':item['name']} for item in req_Json['items']]
        playlists = playlists+tmpPlaylists
        i = i+50

    return jsonify({'code':200, 'playlists':playlists})

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
    return render_template("index.html")

if __name__=='__main__':
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
