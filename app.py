from flask import Flask
from flask_restful import Api
from flask_uuid import FlaskUUID
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

from resources.user import CreateUser, UserLists, UserLogin, TokenRefresh
from resources.note import NoteLists, CreateNote, GetNoteByUserId, UpdateNote, DeleteNote

load_dotenv()

app = Flask(__name__)
CORS(app)
uuid = FlaskUUID(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:adan3433;@localhost:5432/note"
app.config['JWT_SECRET_KEY']=os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api = Api(app)
jwt = JWTManager(app)


@app.route("/")
def index():
    return "server running"

api.add_resource(UserLists, "/users/getAll")
api.add_resource(CreateUser, '/users/create')
api.add_resource(UserLogin, "/auth/login")
api.add_resource(TokenRefresh, "/auth/refresh")

api.add_resource(NoteLists, "/notes/getAll")
api.add_resource(CreateNote, '/notes/create')
api.add_resource(GetNoteByUserId, '/notes/getByUserId')
api.add_resource(UpdateNote, '/notes/update')
api.add_resource(DeleteNote, '/notes/delete')
