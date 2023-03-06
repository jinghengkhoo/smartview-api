import logging
import os

import config
from flask import Flask, redirect, render_template, request
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.update(
    CORS_HEADERS='Content-Type'
)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_CONNECTION_URI

logger = logging.getLogger()

api = Api(prefix=config.API_PREFIX)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email_address = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(160))
    gender = db.Column(db.String(80))
    fcm_token = db.Column(db.String(80))
    image_url = db.Column(db.String(80))

    def __repr__(self):
        return "<Username: {}>".format(self.username)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        user = User(username=request.form.get("username"))
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    print(users)
    return render_template("home.html", users=users)

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    user = User.query.filter_by(username=oldtitle).first()
    user.title = newtitle
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

class EditUserAPIView(Resource):
    """POST API class"""
    @cross_origin()
    def post(self):
        """
        (POST)
        """
        logger.info('New Edit')
        data = request.form
        if "oldname" in data:
            user = User.query.filter_by(username=data["oldname"]).first()
            user.username = data["username"]
            user.email_address = data["email_address"]
            user.address = data["address"]
            user.gender = data["gender"]
            user.fcm_token = data["fcm_token"]
            user.image_url = data["image_url"]
        else:
            user = User(
                        username=data["username"],
                        email_address=data["email_address"],
                        address=data["address"],
                        gender=data["gender"],
                        fcm_token=data["fcm_token"],
                        image_url=data["image_url"]
                        )
            db.session.add(user)
        db.session.commit()

        return "Ok"

class DeleteUserAPIView(Resource):
    """POST API class"""
    @cross_origin()
    def post(self):
        """
        (POST)
        """
        logger.info('New Delete')
        data = request.form
        username = data["username"]
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()

        return "Ok"


api.add_resource(EditUserAPIView, '/edit')
api.add_resource(DeleteUserAPIView, '/delete')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)