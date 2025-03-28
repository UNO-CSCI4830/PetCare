# Users API routes
from flask import Blueprint, jsonify, request, current_app
import MySQLdb.cursors

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("", strict_slashes=False)
def get_users():
    # Connect to the database and retrieve users
    cursor = current_app.extensions['mysql'].connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT user_id, first_name, last_name, email, phone FROM users")
    users_list = cursor.fetchall()

    # Convert to dictionary with user_id as key
    users = {user['user_id']: user for user in users_list}
    return jsonify(users)


@bp.get("/test-db-connection", strict_slashes=False)
def test_db_connection():
    try:
        # Try to connect to the database and run a simple query
        cursor = current_app.extensions['mysql'].connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return jsonify({"status": "success", "message": "Connected to AWS RDS database successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.post("", strict_slashes=False)
def add_user():
    # Get data from request
    data = request.get_json()

    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'password_hash']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        cursor = current_app.extensions['mysql'].connection.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash, phone) VALUES (%s, %s, %s, %s, %s)",
            (data['first_name'], data['last_name'], data['email'], data['password_hash'], data.get('phone'))
        )
        current_app.extensions['mysql'].connection.commit()

        # Return the ID of the newly created user
        new_user_id = cursor.lastrowid
        return jsonify({"user_id": new_user_id, "message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/<int:user_id>", strict_slashes=False)
def get_specific_user(user_id):
    try:
        cursor = current_app.extensions['mysql'].connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT user_id, first_name, last_name, email, phone FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/<int:user_id>", strict_slashes=False)
def delete_user(user_id):
    try:
        cursor = current_app.extensions['mysql'].connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        current_app.extensions['mysql'].connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/<int:user_id>", strict_slashes=False)
def update_user(user_id):
    # Get data from request
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        cursor = current_app.extensions['mysql'].connection.cursor()

        # Build update query dynamically based on provided fields
        update_fields = []
        values = []

        for field in ['first_name', 'last_name', 'email', 'phone']:
            if field in data:
                update_fields.append(f"{field} = %s")
                values.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # Add user_id to values
        values.append(user_id)

        # Execute update query
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
        cursor.execute(query, values)
        current_app.extensions['mysql'].connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "User updated successfully"})
        else:
            return jsonify({"error": "User not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500