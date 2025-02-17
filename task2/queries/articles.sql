SELECT a.id, a.title, a.content, u.name AS author_name, a.created_at, a.updated_at
FROM articles a
JOIN users u ON a.author_id = u.id;