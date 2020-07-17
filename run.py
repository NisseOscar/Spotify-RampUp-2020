import time
from flask import Flask, render_template
from Frontend import app

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__=='__main__':
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
