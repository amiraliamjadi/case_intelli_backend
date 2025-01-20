from flask_restful import Resource
from app.models import CategoryModel
from flask import request


class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id:
            category = CategoryModel.query.get(category_id)
            if category:
                return category.json(), 200
            return {"message": "Category not found"}, 404
        
        categories = CategoryModel.query.all()
        return [category.json() for category in categories], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("Code") or not data.get("Name"):
            return {"message": "Code and Name are required"}, 400

        if CategoryModel.query.filter_by(Code=data["Code"]).first():
            return {"message": "Category with this Code already exists"}, 400

        category = CategoryModel(
            Code=data["Code"],
            Name=data["Name"],
            PricingMethod=data.get("PricingMethod")
        )
        
        try:
            category.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return category.json(), 201

    def put(self, category_id):
        data = request.get_json()
        category = CategoryModel.query.get(category_id)

        if not category:
            return {"message": "Category not found"}, 404

        if "Code" in data:
            category.Code = data["Code"]
        if "Name" in data:
            category.Name = data["Name"]
        if "PricingMethod" in data:
            category.PricingMethod = data.get("PricingMethod")

        try:
            category.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return category.json(), 200

    def delete(self, category_id):
        category = CategoryModel.query.get(category_id)

        if not category:
            return {"message": "Category not found"}, 404

        try:
            category.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Category deleted"}, 200