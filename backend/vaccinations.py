# Vaccinations API routes

from flask import Blueprint

bp = Blueprint("vaccinations", __name__, url_prefix="/vaccinations")


@bp.get("", strict_slashes=False)
def get_vaccinations():
    # TODO: return list of vaccinations
    return []  # returning a blank list for testing


@bp.post("", strict_slashes=False)
def add_vaccination():
    # TODO: create a vaccination
    return {}


@bp.get("/<int:vaccination_id>", strict_slashes=False)
def get_specific_vaccination(vaccination_id):
    # TODO: return the vaccination that equals the vaccination_id
    return {}


@bp.delete("/<int:vaccination_id>", strict_slashes=False)
def delete_vaccination(vaccination_id):
    # TODO: delete the vaccination that equals the vaccination_id
    return {}


@bp.put("/<int:vaccination_id>", strict_slashes=False)
def update_vaccination(vaccination_id):
    # TODO: read the request body to get what needs to be updated for the vaccination
    return {}
