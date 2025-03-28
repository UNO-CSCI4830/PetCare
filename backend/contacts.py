# Contacts API routes

from flask import Blueprint

bp = Blueprint("contacts", __name__, url_prefix="/contacts")


@bp.get("", strict_slashes=False)
def get_contacts():
    # TODO: return list of contacts
    return []  # returning a blank list for testing


@bp.post("", strict_slashes=False)
def add_contact():
    # TODO: create a contact
    return {}


@bp.get("/<int:contact_id>", strict_slashes=False)
def get_specific_contact(contact_id):
    # TODO: return the contact that equals the contact_id
    return {}


@bp.delete("/<int:contact_id>", strict_slashes=False)
def delete_contact(contact_id):
    # TODO: delete the contact that equals the contact_id
    return {}


@bp.put("/<int:contact_id>", strict_slashes=False)
def update_contact(contact_id):
    # TODO: read the request body to get what needs to be updated for the contact
    return {}
