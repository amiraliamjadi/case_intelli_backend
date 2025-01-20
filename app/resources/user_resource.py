from flask_restful import Resource
from app.models import UserModel
from flask import request

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = UserModel.query.get(user_id)
            if user:
                return user.json(), 200
            return {"message": "User not found"}, 404

        users = UserModel.query.all()
        return [user.json() for user in users], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("Email") or not data.get("Password") or not data.get("PartyRef"):
            return {"message": "Email, Password, and PartyRef are required"}, 400

        if UserModel.query.filter_by(Email=data["Email"]).first():
            return {"message": "User with this Email already exists"}, 400

        user = UserModel(
            email=data["Email"],
            partyref=data["PartyRef"],
            password=data["Password"],
            isadministrator=data.get("IsAdministrator", False)
        )

        try:
            user.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return user.json(), 201

    def put(self, user_id):
        data = request.get_json()
        user = UserModel.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        if "Email" in data:
            user.Email = data["Email"]
        if "PartyRef" in data:
            user.PartyRef = data["PartyRef"]
        if "Password" in data:
            user.password_hash = UserModel.generate_hash(data["Password"])
        if "IsAdministrator" in data:
            user.IsAdministrator = data["IsAdministrator"]

        try:
            user.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return user.json(), 200

    def delete(self, user_id):
        user = UserModel.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        try:
            user.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "User deleted"}, 200
