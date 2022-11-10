from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


class UserLists(Resource):
    def get(self):
        users = UserModel.query.all()
        return { "status": 200, "users": [user.json() for user in users ]}

class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="username cannot be empty."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="username cannot be empty."
    )
   
    def post(self):
        data = CreateUser.parser.parse_args()

        old_user = UserModel.find_user_by_username(data["username"])
        if old_user is not None:
            return {
                "status": 409,
                "message": "usename already exists."
            }

        new_user = UserModel(data["username"], data["password"])

        try:
            new_user.save_to_db()
        except BaseException as error:
            print(error)
            return {"status": 500, "message": "an error occured while creating user."} , 500
        return { "status": 201, "message": "user created successfully."} , 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="username cannot be empty."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="username cannot be empty."
    )

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_user_by_username(username=data["username"])
        if user is None:
            return { "status": 401, "message": "Invalid credential." }
        match_password = check_password_hash(user.password, data["password"])
        if not match_password:
            return { "status": 401, "message": "Invalid Credential."}, 401
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {
            "status": 200,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return { 'access_token': new_token }, 200