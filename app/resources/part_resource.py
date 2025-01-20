from flask_restful import Resource
from app.models import PartModel
from flask import request

import os
import qrcode

class PartResource(Resource):
    QR_IMAGE_PATH = "app/static/images/qrcodes"  # Path to save QR code images

    def get(self, part_id=None):
        if part_id:
            part = PartModel.query.get(part_id)
            if part:
                return part.json(), 200
            return {"message": "Part not found"}, 404

        parts = PartModel.query.all()
        return [part.json() for part in parts], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("Code") or not data.get("Name") or not data.get("CategoryRef") or not data.get("StorePositionRef"):
            return {"message": "Code, Name, CategoryRef, and StorePositionRef are required"}, 400

        if PartModel.query.filter_by(Code=data["Code"]).first():
            return {"message": "Part with this Code already exists"}, 400

        part = PartModel(
            Code=data["Code"],
            Name=data["Name"],
            UnitRef=data.get("UnitRef"),
            CategoryRef=data["CategoryRef"],
            StorePositionRef=data["StorePositionRef"],
            Quantity=data.get("Quantity", 1),
            Image=data.get("Image")
        )

        try:
            part.save_to_db()

            # Generate QR code
            qr_value = part.PartID
            qr_value = f"https://127.0.0.1:5002/part-details?partId={qr_value}"
            qr = qrcode.make(qr_value)
            qr_file_path = os.path.join(self.QR_IMAGE_PATH, f"part_{part.PartID}.png")
            qr.save(qr_file_path)

            # Update part with QR code data
            part.QRCode = qr_value
            part.QRCodeImage = f"part_{part.PartID}.png"
            part.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return part.json(), 201

    def put(self, part_id):
        data = request.get_json()
        part = PartModel.query.get(part_id)

        if not part:
            return {"message": "Part not found"}, 404

        if "Code" in data:
            part.Code = data["Code"]
        if "Name" in data:
            part.Name = data["Name"]
        if "UnitRef" in data:
            part.UnitRef = data["UnitRef"]
        if "CategoryRef" in data:
            part.CategoryRef = data["CategoryRef"]
        if "StorePositionRef" in data:
            part.StorePositionRef = data["StorePositionRef"]
        if "Quantity" in data:
            part.Quantity = data["Quantity"]
        if "Image" in data:
            part.Image = data["Image"]

        try:
            part.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return part.json(), 200

    def delete(self, part_id):
        part = PartModel.query.get(part_id)

        if not part:
            return {"message": "Part not found"}, 404

        try:
            qr_file_path = os.path.join(self.QR_IMAGE_PATH, part.QRCodeImage)
            # Delete QR code image if it exists
            if qr_file_path and os.path.exists(part.QRCodeImage):
                os.remove(part.QRCodeImage)

            # Delete part from the database
            part.delete_from_db()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Part and associated QR code image deleted"}, 200
