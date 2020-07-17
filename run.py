import time
from flask import Flask, render_template, redirect, url_for
from Frontend import app
# Imports app details from a private file
from details import client_id, client_secret

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/')
def login():
    scope = 'user-read-private'
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
