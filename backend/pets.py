# Pets API routes
from flask import Blueprint, jsonify, request, current_app
import MySQLdb.cursors

bp = Blueprint("pets", __name__, url_prefix="/pets")


@bp.get("", strict_slashes=False)
def get_pets():
    try:
        cursor = current_app.extensions['mysql'].connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT pet_id, name, species, breed, age, weight, gender, profile_picture FROM pets")
        pets_list = cursor.fetchall()

        # Convert to dictionary with pet_id as key
        pets = {pet['pet_id']: pet for pet in pets_list}
        return jsonify(pets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("", strict_slashes=False)
def add_pet():
    # Get data from request
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'species', 'breed', 'gender']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        cursor = current_app.extensions['mysql'].connection.cursor()
        cursor.execute(
            "INSERT INTO pets (name, species, breed, age, weight, gender, profile_picture) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (data['name'], data['species'], data['breed'], data.get('age'), data.get('weight'), data['gender'],
             data.get('profile_picture'))
        )
        current_app.extensions['mysql'].connection.commit()

        # Get the new pet ID
        new_pet_id = cursor.lastrowid

        # If owner_id is provided, create the ownership relationship
        if 'owner_id' in data:
            cursor.execute(
                "INSERT INTO pet_ownership (pet_id, user_id, role) VALUES (%s, %s, %s)",
                (new_pet_id, data['owner_id'], data.get('owner_role', 'Primary'))
            )
            current_app.extensions['mysql'].connection.commit()

        return jsonify({"pet_id": new_pet_id, "message": "Pet created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/<int:pet_id>", strict_slashes=False)
def get_specific_pet(pet_id):
    try:
        cursor = current_app.extensions['mysql'].connection.cursor(MySQLdb.cursors.DictCursor)

        # Get pet details
        cursor.execute(
            "SELECT pet_id, name, species, breed, age, weight, gender, profile_picture FROM pets WHERE pet_id = %s",
            (pet_id,))
        pet = cursor.fetchone()

        if not pet:
            return jsonify({"error": "Pet not found"}), 404

        # Get ownership information
        cursor.execute("""
            SELECT po.role, u.user_id, u.first_name, u.last_name, u.email 
            FROM pet_ownership po
            JOIN users u ON po.user_id = u.user_id
            WHERE po.pet_id = %s
        """, (pet_id,))
        owners = cursor.fetchall()

        # Add owners to pet data
        pet['owners'] = owners

        return jsonify(pet)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/<int:pet_id>", strict_slashes=False)
def delete_pet(pet_id):
    try:
        cursor = current_app.extensions['mysql'].connection.cursor()

        # Delete pet (ownership records will be deleted via ON DELETE CASCADE)
        cursor.execute("DELETE FROM pets WHERE pet_id = %s", (pet_id,))
        current_app.extensions['mysql'].connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Pet deleted successfully"})
        else:
            return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/<int:pet_id>", strict_slashes=False)
def update_pet(pet_id):
    # Get data from request
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        cursor = current_app.extensions['mysql'].connection.cursor()

        # Build update query dynamically based on provided fields
        update_fields = []
        values = []

        for field in ['name', 'species', 'breed', 'age', 'weight', 'gender', 'profile_picture']:
            if field in data:
                update_fields.append(f"{field} = %s")
                values.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # Add pet_id to values
        values.append(pet_id)

        # Execute update query
        query = f"UPDATE pets SET {', '.join(update_fields)} WHERE pet_id = %s"
        cursor.execute(query, values)
        current_app.extensions['mysql'].connection.commit()

        # If ownership changes are included
        if 'owner_id' in data and 'owner_role' in data:
            # Check if ownership record exists
            cursor.execute("SELECT * FROM pet_ownership WHERE pet_id = %s AND user_id = %s", (pet_id, data['owner_id']))
            existing = cursor.fetchone()

            if existing:
                # Update existing ownership
                cursor.execute(
                    "UPDATE pet_ownership SET role = %s WHERE pet_id = %s AND user_id = %s",
                    (data['owner_role'], pet_id, data['owner_id'])
                )
            else:
                # Create new ownership
                cursor.execute(
                    "INSERT INTO pet_ownership (pet_id, user_id, role) VALUES (%s, %s, %s)",
                    (pet_id, data['owner_id'], data['owner_role'])
                )

            current_app.extensions['mysql'].connection.commit()

        if cursor.rowcount > 0 or ('owner_id' in data and 'owner_role' in data):
            return jsonify({"message": "Pet updated successfully"})
        else:
            return jsonify({"error": "Pet not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/user/<int:user_id>", strict_slashes=False)
def get_pets_by_owner(user_id):
    try:
        cursor = current_app.extensions['mysql'].connection.cursor(MySQLdb.cursors.DictCursor)

        # Get all pets owned by this user (either primary or secondary)
        cursor.execute("""
            SELECT p.pet_id, p.name, p.species, p.breed, p.age, p.weight, p.gender, 
                   p.profile_picture, po.role AS owner_role
            FROM pets p
            JOIN pet_ownership po ON p.pet_id = po.pet_id
            WHERE po.user_id = %s
        """, (user_id,))

        pets = cursor.fetchall()
        return jsonify(pets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500