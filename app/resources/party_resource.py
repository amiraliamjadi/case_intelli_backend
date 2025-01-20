from flask_restful import Resource
from app.models import PartyModel
from flask import request

class PartyResource(Resource):
    def get(self, party_id=None):
        if party_id:
            party = PartyModel.query.get(party_id)
            if party:
                return party.json(), 200
            return {"message": "Party not found"}, 404

        parties = PartyModel.query.all()
        return [party.json() for party in parties], 200

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Invalid input"}, 400

        party = PartyModel(
            Title=data.get("Title"),
            FirstName=data.get("FirstName"),
            LastName=data.get("LastName"),
            Gender=data.get("Gender"),
            Mobile=data.get("Mobile"),
            EducationDegree=data.get("EducationDegree")
        )

        try:
            party.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return party.json(), 201

    def put(self, party_id):
        data = request.get_json()
        party = PartyModel.query.get(party_id)

        if not party:
            return {"message": "Party not found"}, 404

        if "Title" in data:
            party.Title = data["Title"]
        if "FirstName" in data:
            party.FirstName = data["FirstName"]
        if "LastName" in data:
            party.LastName = data["LastName"]
        if "Gender" in data:
            party.Gender = data["Gender"]
        if "Mobile" in data:
            party.Mobile = data["Mobile"]
        if "EducationDegree" in data:
            party.EducationDegree = data["EducationDegree"]

        try:
            party.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return party.json(), 200

    def delete(self, party_id):
        party = PartyModel.query.get(party_id)

        if not party:
            return {"message": "Party not found"}, 404

        try:
            party.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Party deleted"}, 200
