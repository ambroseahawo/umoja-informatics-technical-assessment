-- Enable the uuid-ossp extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY, -- Auto-generated UUID
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Create articles table
CREATE TABLE articles (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY, -- Auto-generated UUID
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create comments table
CREATE TABLE comments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY, -- Auto-generated UUID
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO users (name, email, role) VALUES
('Peter Oax', 'peter.oax@example.com', 'admin'),
('Mary Anne', 'maryanne@example.com', 'author'),
('Alice Johnson', 'alice.johnson@example.com', 'reader');

-- Insert sample articles
INSERT INTO articles (title, content, author_id) VALUES
('Introduction to PostgreSQL', 'PostgreSQL is a powerful open-source relational database system.', (SELECT id FROM users WHERE email = 'peter.oax@example.com')),
('Advanced SQL Techniques', 'Learn advanced SQL queries and optimization techniques.', (SELECT id FROM users WHERE email = 'maryanne@example.com')),
('Database Design Best Practices', 'Key principles for designing efficient databases.', (SELECT id FROM users WHERE email = 'peter.oax@example.com'));

-- Insert sample comments
INSERT INTO comments (article_id, user_id, comment_text) VALUES
((SELECT id FROM articles WHERE title = 'Introduction to PostgreSQL'), (SELECT id FROM users WHERE email = 'alice.johnson@example.com'), 'Great article! Very helpful.'),
((SELECT id FROM articles WHERE title = 'Introduction to PostgreSQL'), (SELECT id FROM users WHERE email = 'maryanne@example.com'), 'I learned a lot from this.'),
((SELECT id FROM articles WHERE title = 'Advanced SQL Techniques'), (SELECT id FROM users WHERE email = 'alice.johnson@example.com'), 'Looking forward to more advanced topics.'),
((SELECT id FROM articles WHERE title = 'Database Design Best Practices'), (SELECT id FROM users WHERE email = 'maryanne@example.com'), 'Excellent guide for database design.');