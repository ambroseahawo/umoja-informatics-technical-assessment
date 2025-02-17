# Task 2: Database Design & Management

## Objective: Design an optimized schema for a content management system (CMS).

The schema consists of three tables: users, articles, and comments. Relationships are defined as follows:

- A user can write multiple articles.
- An article can have multiple comments.
- A comment is associated with one user and one article.

## How To Run

1. On a new terminal session, initiate postgres and create a new database.
    ```bash
    psql -U postgres
    CREATE DATABASE your_database_name;
    ```
2. Create table schemas and populate the database.(switch to task2 folder)
    ```bash
    psql -U your_username -d your_database_name -f schema.sql
    ```
3. To run any of the queries:
    ```bash
    psql -U your_username -d your_database_name -f articles.sql
    psql -U your_username -d your_database_name -f comments.sql
    psql -U your_username -d your_database_name -f latest_5_articles.sql
    ```