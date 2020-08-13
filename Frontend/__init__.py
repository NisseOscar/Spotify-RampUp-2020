from flask import Flask

application = Flask(__name__,
 static_folder = './public',
 template_folder="./static")
