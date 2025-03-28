# Appointments API routes

from flask import Blueprint

bp = Blueprint("appointments", __name__, url_prefix="/appointments")


@bp.get("", strict_slashes=False)
def get_appointments():
    # TODO: return list of appointments
    return []  # returning a blank list for testing


@bp.post("", strict_slashes=False)
def add_appointment():
    # TODO: create a appointment
    return {}


@bp.get("/<int:appointment_id>", strict_slashes=False)
def get_specific_appointment(appointment_id):
    # TODO: return the appointment that equals the appointment_id
    return {}


@bp.delete("/<int:appointment_id>", strict_slashes=False)
def delete_appointment(appointment_id):
    # TODO: delete the appointment that equals the appointment_id
    return {}


@bp.put("/<int:appointment_id>", strict_slashes=False)
def update_appointment(appointment_id):
    # TODO: read the request body to get what needs to be updated for the appointment
    return {}
