from flask import Flask, jsonify
from flask_mysqldb import MySQL
import pets, users, contacts, vaccinations, activities, appointments, diets, medications

app = Flask(__name__)

# Configure database
app.config['MYSQL_HOST'] = 'petcare-db.cbyc0go6qmwd.us-east-2.rds.amazonaws.com'  # AWS endpoint
app.config['MYSQL_USER'] = 'admin'  # Master username
app.config['MYSQL_PASSWORD'] = 'csci4830db!'  # Master password
app.config['MYSQL_DB'] = 'petcare_database'
mysql = MySQL(app)
app.extensions['mysql'] = mysql

app.register_blueprint(pets.bp)
app.register_blueprint(users.bp)
app.register_blueprint(contacts.bp)
app.register_blueprint(vaccinations.bp)
app.register_blueprint(activities.bp)
app.register_blueprint(appointments.bp)
app.register_blueprint(diets.bp)
app.register_blueprint(medications.bp)


if __name__ == "__main__":
    app.run(port=5001)
