# Activities API routes


from flask import Blueprint

bp = Blueprint("activities", __name__, url_prefix="/activities")


@bp.get("", strict_slashes=False)
def get_activities():
    # TODO: return list of activities
    return []  # returning a blank list for testing


@bp.post("", strict_slashes=False)
def add_activity():
    # TODO: create a activity
    return {}


@bp.get("/<int:activity_id>", strict_slashes=False)
def get_specific_activity(activity_id):
    # TODO: return the activity that equals the activity_id
    return {}


@bp.delete("/<int:activity_id>", strict_slashes=False)
def delete_activity(activity_id):
    # TODO: delete the activity that equals the activity_id
    return {}


@bp.put("/<int:activity_id>", strict_slashes=False)
def update_activity(activity_id):
    # TODO: read the request body to get what needs to be updated for the activity
    return {}
