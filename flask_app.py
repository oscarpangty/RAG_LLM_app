from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    
@app.route("/oscar")
def hello_worldo():
    return "<p>Hello, World oscar!</p>"