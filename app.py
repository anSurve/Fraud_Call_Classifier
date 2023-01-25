from flask import Flask
from api.routes import api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = './profile_pics'
app.register_blueprint(api, url_prefix='/api')


@app.route("/")
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run()

