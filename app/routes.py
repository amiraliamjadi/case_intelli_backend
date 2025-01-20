from flask import Blueprint, render_template
from .extensions import db
from flask_restful import Api
from app.resources import *


# Define a Blueprint
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/search")
def search():
    return render_template("search.html")

@main.route("/parts/<int:part_id>")
def part(part_id):
    return render_template("part.html")



@main.route("/crud/categories")
def categories():
    return render_template("category_crud.html")

@main.route("/crud/units")
def units():
    return render_template("unit_crud.html")

@main.route("/crud/stores")
def stores():
    return render_template("store_crud.html")

@main.route("/crud/storepositions")
def store_positions():
    return render_template("storeposition_crud.html")

@main.route("/crud/parties")
def parties():
    return render_template("party_crud.html")

@main.route("/crud/users")
def users():
    return render_template("user_crud.html")

@main.route("/crud/parts")
def parts():
    return render_template("part_crud.html")



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