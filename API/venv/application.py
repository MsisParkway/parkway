from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return "Hello world"

if _name__= '__main__':
	app.run()