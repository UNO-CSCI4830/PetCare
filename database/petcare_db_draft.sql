CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pets (
    pet_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(50),
    age INT CHECK (age >= 0),
    weight DECIMAL(5,2),
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Unknown')),
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vaccinations (
    vaccination_id SERIAL PRIMARY KEY,
    pet_id INT REFERENCES pets(pet_id) ON DELETE CASCADE,
    vaccine_name VARCHAR(100) NOT NULL,
    date_given DATE NOT NULL,
    next_due DATE,
    veterinarian VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medications (
    medication_id SERIAL PRIMARY KEY,
    pet_id INT REFERENCES pets(pet_id) ON DELETE CASCADE,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50), -- Example: "Twice a day"
    start_date DATE NOT NULL,
    end_date DATE,
    prescribed_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diet_logs (
    diet_id SERIAL PRIMARY KEY,
    pet_id INT REFERENCES pets(pet_id) ON DELETE CASCADE,
    food_name VARCHAR(100) NOT NULL,
    quantity VARCHAR(50),
    meal_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE TABLE activity_logs (
    activity_id SERIAL PRIMARY KEY,
    pet_id INT REFERENCES pets(pet_id) ON DELETE CASCADE,
    activity_type VARCHAR(50) CHECK (activity_type IN ('Walk', 'Run', 'Play', 'Other')),
    duration_minutes INT CHECK (duration_minutes > 0),
    date_of_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE TABLE contacts (
    contact_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    clinic_name VARCHAR(100),
    address TEXT
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    pet_id INT REFERENCES pets(pet_id) ON DELETE CASCADE,
    contact_id INT REFERENCES contact(contact_id) ON DELETE CASCADE,
    appointment_type VARCHAR(50) CHECK (activity_type IN ('Veterinarian', 'Grooming', 'Training', 'Other')),
    appointment_date DATE,
    appointment_time TIME,
    notes TEXT
);