from flask import Blueprint, render_template
from .extensions import db
from flask_restful import Api
from app.resources import *


# Define a Blueprint
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


def register_routes(app):
    api = Api(app)
    api.add_resource(CategoryResource, "/categories", "/categories/<int:category_id>")