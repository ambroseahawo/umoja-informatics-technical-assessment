SELECT a.id AS article_id, a.title, COUNT(c.id) AS comment_count
FROM articles a
LEFT JOIN comments c ON a.id = c.article_id
GROUP BY a.id, a.title;