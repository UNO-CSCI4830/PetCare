# Diets API routes

from flask import Blueprint

bp = Blueprint("diets", __name__, url_prefix="/diets")


@bp.get("", strict_slashes=False)
def get_diets():
    # TODO: return list of diets
    return []  # returning a blank list for testing


@bp.post("", strict_slashes=False)
def add_diet():
    # TODO: create a diet
    return {}


@bp.get("/<int:diet_id>", strict_slashes=False)
def get_specific_diet(diet_id):
    # TODO: return the diet that equals the diet_id
    return {}


@bp.delete("/<int:diet_id>", strict_slashes=False)
def delete_diet(diet_id):
    # TODO: delete the diet that equals the diet_id
    return {}


@bp.put("/<int:diet_id>", strict_slashes=False)
def update_diet(diet_id):
    # TODO: read the request body to get what needs to be updated for the diet
    return {}
