from flask_restful import Resource
from app.models import UnitModel
from flask import request

class UnitResource(Resource):
    def get(self, unit_id=None):
        if unit_id:
            unit = UnitModel.query.get(unit_id)
            if unit:
                return unit.json(), 200
            return {"message": "Unit not found"}, 404

        units = UnitModel.query.all()
        return [unit.json() for unit in units], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("Name"):
            return {"message": "Name is required"}, 400

        if UnitModel.query.filter_by(Name=data["Name"]).first():
            return {"message": "Unit with this Name already exists"}, 400

        unit = UnitModel(
            Name=data["Name"],
            AbbreviatedName=data.get("AbbreviatedName")
        )

        try:
            unit.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return unit.json(), 201

    def put(self, unit_id):
        data = request.get_json()
        unit = UnitModel.query.get(unit_id)

        if not unit:
            return {"message": "Unit not found"}, 404

        if "Name" in data:
            unit.Name = data["Name"]
        if "AbbreviatedName" in data:
            unit.AbbreviatedName = data["AbbreviatedName"]

        try:
            unit.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return unit.json(), 200

    def delete(self, unit_id):
        unit = UnitModel.query.get(unit_id)

        if not unit:
            return {"message": "Unit not found"}, 404

        try:
            unit.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Unit deleted"}, 200
