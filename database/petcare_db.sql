CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pets (
    pet_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(50) NOT NULL, -- Pets should have a breed (Mix/Unknown if needed)
    age INT,
    weight DECIMAL(5,2),
    gender ENUM('Male', 'Female', 'Unknown') NOT NULL,
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pet_ownership (
    ownership_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    user_id INT NULL, -- MUST allow NULL for ON DELETE SET NULL
    role ENUM('Primary', 'Secondary') NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    contact_type ENUM('Veterinarian', 'Groomer', 'Trainer', 'Pet-Sitter', 'Other') NOT NULL,
    other_contact_type VARCHAR(100), -- Allows custom input for "Other"
    name VARCHAR(100),  -- Not required; May be business only, not individual
    company_name VARCHAR(100), -- Not required; May be individual only, not business
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address TEXT
);

CREATE TABLE pet_sharing (
    share_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    shared_with_user_id INT, -- Sharing with another pet owner
    shared_with_contact_id INT, -- Sharing with an external provider
    access_level ENUM('View', 'Limited Edit') NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with_contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE
);

CREATE TABLE vaccinations (
    vaccination_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    veterinarian_id INT, -- Optional reference to contacts
    veterinarian_name VARCHAR(100), -- Free-text entry
    vaccine_name VARCHAR(100) NOT NULL,
    date_given DATE NOT NULL,
    next_due DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (veterinarian_id) REFERENCES contacts(contact_id) ON DELETE SET NULL
);

CREATE TABLE medications (
    medication_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE, -- Open-ended, allowing ongoing meds
    prescribed_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
);

CREATE TABLE diet_logs (
    diet_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    food_name VARCHAR(100) NOT NULL,
    quantity VARCHAR(50),
    meal_time DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
);

CREATE TABLE activity_logs (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    activity_type ENUM('Walk', 'Run', 'Play', 'Other') NOT NULL,
    other_activity_type VARCHAR(100), -- Allows custom input for "Other"
    duration_minutes INT CHECK (duration_minutes > 0),    
    activity_date DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
);

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    contact_id INT NOT NULL,
    appointment_type ENUM('Veterinarian', 'Grooming', 'Training', 'Other') NOT NULL,
    other_appt_type VARCHAR(100), -- Allows custom input for "Other"
    appointment_date DATE,
    appointment_time TIME,
    notes TEXT,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE
);

-- Add indexes on foreign keys for better performance
-- USE pet_care;  -- this line is not needed when working on Railway
CREATE INDEX idx_pet_ownership_pet_id ON pet_ownership(pet_id);
CREATE INDEX idx_pet_ownership_user_id ON pet_ownership(user_id);
CREATE INDEX idx_pet_sharing_pet_id ON pet_sharing(pet_id);
CREATE INDEX idx_pet_sharing_user_id ON pet_sharing(shared_with_user_id);
CREATE INDEX idx_pet_sharing_contact_id ON pet_sharing(shared_with_contact_id);
CREATE INDEX idx_activity_logs_pet_id ON activity_logs(pet_id);
CREATE INDEX idx_diet_logs_pet_id ON diet_logs(pet_id);
CREATE INDEX idx_medications_pet_id ON medications(pet_id);
CREATE INDEX idx_vaccinations_pet_id ON vaccinations(pet_id);
CREATE INDEX idx_appointments_pet_id ON appointments(pet_id);
CREATE INDEX idx_appointments_contact_id ON appointments(contact_id);