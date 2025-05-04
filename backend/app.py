from flask import Flask, jsonify, send_from_directory
from flask_mysqldb import MySQL
import os # For pet images
import pets, users, contacts, vaccinations, activities, share, appointments, diets, medications, resources, notifications
from flask_cors import CORS
app = Flask(__name__)

CORS(app)



# Configure database
app.config['MYSQL_HOST'] = 'petcare-db.cbyc0go6qmwd.us-east-2.rds.amazonaws.com'  # AWS endpoint
app.config['MYSQL_USER'] = 'admin'  # Master username
app.config['MYSQL_PASSWORD'] = 'csci4830db!'  # Master password
app.config['MYSQL_DB'] = 'petcare_database'
mysql = MySQL(app)
app.extensions['mysql'] = mysql

# Add route to serve pet images
@app.route('/pet_images/<filename>')
def get_pet_image(filename):
    return send_from_directory(
        os.path.join(os.getcwd(), 'static', 'pet_images'),
        filename
    )

app.register_blueprint(pets.bp)
app.register_blueprint(users.bp)
app.register_blueprint(contacts.bp)
app.register_blueprint(vaccinations.bp)
app.register_blueprint(activities.bp)
app.register_blueprint(appointments.bp)
app.register_blueprint(diets.bp)
app.register_blueprint(medications.bp)
app.register_blueprint(notifications.bp)
app.register_blueprint(share.bp)
app.register_blueprint(resources.bp)


if __name__ == "__main__":
    app.run(port=5001)
