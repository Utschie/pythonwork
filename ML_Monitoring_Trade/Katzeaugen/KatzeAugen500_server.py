from flask import Flask
app = Flask(__name__)

@aqq.route('/')
def hello_world():
    return 'Hello, World!'
