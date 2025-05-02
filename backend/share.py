# Share API routes

from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("share", __name__, url_prefix="/share")

@bp.post("", strict_slashes=False)
def share_pet_profile():
    mysql = current_app.extensions["mysql"]
    data = request.get_json()
    pet_id = data.get("pet_id")
    shared_with_user_id = data.get("shared_with_user_id")
    permission_level = data.get("permission_level", "view")

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO shared_profiles (pet_id, shared_with_user_id, permission_level)
        VALUES (%s, %s, %s)
    """, (pet_id, shared_with_user_id, permission_level))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Pet profile shared successfully"}), 201

@bp.get("/<int:user_id>", strict_slashes=False)
def get_shared_pets(user_id):
    mysql = current_app.extensions["mysql"]
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT pets.id, pets.name, pets.type, pets.breed, pets.age, sp.permission_level
        FROM pets
        JOIN shared_profiles sp ON pets.id = sp.pet_id
        WHERE sp.shared_with_user_id = %s
    """, (user_id,))
    shared_pets = cur.fetchall()
    cur.close()
    return jsonify(shared_pets)
