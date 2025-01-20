from flask import Blueprint, render_template
from .extensions import db
from flask_restful import Api
from app.resources import *


# Define a Blueprint
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


# Register routes for APIs using Flask-RESTful
def register_routes(app):
    api = Api(app)
    api.add_resource(CategoryResource, "/categories", "/categories/<int:category_id>")
    api.add_resource(UnitResource, '/units', '/units/<int:unit_id>')
    api.add_resource(StoreResource, '/stores', '/stores/<int:store_id>')
    api.add_resource(StorePositionResource, '/store-positions', '/store-positions/<position_id>')
    api.add_resource(PartyResource, '/parties', '/parties/<int:party_id>')
    api.add_resource(UserResource, '/users', '/users/<int:user_id>')
    api.add_resource(PartResource, '/parts', '/parts/<int:part_id>')