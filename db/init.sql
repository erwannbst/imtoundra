-- Create a table for animal observations
CREATE TABLE observations (
     id SERIAL PRIMARY KEY,
     date TIMESTAMP NOT NULL,
     animal_name VARCHAR(255) NOT NULL,
     temp DECIMAL(5, 2) NOT NULL,
     air_quality VARCHAR(50) NOT NULL
);

-- Insert some sample data
INSERT INTO observations (date, animal_name, temp, air_quality) VALUES
    ('2024-01-14 08:00:00', 'wolf', 35.5, 80.0),
    ('2024-01-14 09:30:00', 'fox', 32.0, 75.5),
    ('2024-01-14 11:15:00', 'caribou', 30.8, 78.2);
