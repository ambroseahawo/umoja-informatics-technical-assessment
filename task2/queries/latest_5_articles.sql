SELECT id, title, content, author_id, created_at, updated_at
FROM articles
ORDER BY created_at DESC
LIMIT 5;