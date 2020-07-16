import time
from flask import Flask, render_template

application = app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/alla')
def index():
    return render_template('index.html')

if __name__=='__main__':

    app.debug = True
    app.run()
