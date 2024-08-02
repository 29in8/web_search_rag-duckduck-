from flask import Flask
from flask_cors import CORS

from routes.tools import tools

app = Flask(__name__)
CORS(app)

app.register_blueprint(tools)

if __name__ == '__main__':
    app.run(port=8080)