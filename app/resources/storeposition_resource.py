from flask_restful import Resource
from app.models import StorePositionModel
from flask import request

class StorePositionResource(Resource):
    def get(self, position_id=None):
        if position_id:
            position = StorePositionModel.query.get(position_id)
            if position:
                return position.json(), 200
            return {"message": "Store position not found"}, 404

        positions = StorePositionModel.query.all()
        return [position.json() for position in positions], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("Code") or not data.get("Name") or not data.get("StoreID"):
            return {"message": "Code, Name, and StoreID are required"}, 400

        if StorePositionModel.query.filter_by(Code=data["Code"]).first():
            return {"message": "Store position with this Code already exists"}, 400

        position = StorePositionModel(
            Code=data["Code"],
            Name=data["Name"],
            StoreID=data["StoreID"]
        )

        try:
            position.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return position.json(), 201

    def put(self, position_id):
        data = request.get_json()
        position = StorePositionModel.query.get(position_id)

        if not position:
            return {"message": "Store position not found"}, 404

        if "Code" in data:
            position.Code = data["Code"]
        if "Name" in data:
            position.Name = data["Name"]
        if "StoreID" in data:
            position.StoreID = data["StoreID"]

        try:
            position.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return position.json(), 200

    def delete(self, position_id):
        position = StorePositionModel.query.get(position_id)

        if not position:
            return {"message": "Store position not found"}, 404

        try:
            position.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Store position deleted"}, 200
