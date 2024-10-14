CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL
);

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(150) NOT NULL UNIQUE,
        password_hash VARCHAR(128) NOT NULL
    );

ALTER TABLE todos ADD COLUMN user_id INTEGER REFERENCES users(id);
