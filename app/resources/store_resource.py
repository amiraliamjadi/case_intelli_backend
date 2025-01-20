from flask_restful import Resource
from app.models import StoreModel
from flask import request

class StoreResource(Resource):
    def get(self, store_id=None):
        if store_id:
            store = StoreModel.query.get(store_id)
            if store:
                return store.json(), 200
            return {"message": "Store not found"}, 404

        stores = StoreModel.query.all()
        return [store.json() for store in stores], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("Name") or not data.get("Code"):
            return {"message": "Name and Code are required"}, 400

        if StoreModel.query.filter_by(Code=data["Code"]).first():
            return {"message": "Store with this Code already exists"}, 400

        store = StoreModel(
            Name=data["Name"],
            Code=data["Code"]
        )

        try:
            store.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return store.json(), 201

    def put(self, store_id):
        data = request.get_json()
        store = StoreModel.query.get(store_id)

        if not store:
            return {"message": "Store not found"}, 404

        if "Name" in data:
            store.Name = data["Name"]
        if "Code" in data:
            store.Code = data["Code"]

        try:
            store.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return store.json(), 200

    def delete(self, store_id):
        store = StoreModel.query.get(store_id)

        if not store:
            return {"message": "Store not found"}, 404

        try:
            store.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Store deleted"}, 200
