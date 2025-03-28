# Medications API routes

from flask import Blueprint

bp = Blueprint("medications", __name__, url_prefix="/medications")


@bp.get("", strict_slashes=False)
def get_medications():
    # TODO: return list of medications
    return []  # returning a blank list for testing


@bp.post("", strict_slashes=False)
def add_medication():
    # TODO: create a medication
    return {}


@bp.get("/<int:medication_id>", strict_slashes=False)
def get_specific_medication(medication_id):
    # TODO: return the medication that equals the medication_id
    return {}


@bp.delete("/<int:medication_id>", strict_slashes=False)
def delete_medication(medication_id):
    # TODO: delete the medication that equals the medication_id
    return {}


@bp.put("/<int:medication_id>", strict_slashes=False)
def update_medication(medication_id):
    # TODO: read the request body to get what needs to be updated for the medication
    return {}
