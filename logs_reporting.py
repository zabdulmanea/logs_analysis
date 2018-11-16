# Database code for logs analysis of news DB

import psycopg2

db = psycopg2.connect("dbname=news")

# 1. What are the most popular three articles of all time?
'''
SELECT articles.title AS "Popular Articles", COUNT(*) AS Views
FROM log JOIN articles
ON articles.slug = SUBSTRING(log.path,10)
GROUP BY articles.title
ORDER BY Views DESC LIMIT 3;
'''

# 2. Who are the most popular article authors of all time?
'''
SELECT authors.name, COUNT(*) AS Views
FROM log, articles, authors
WHERE SUBSTRING(log.path,10) = articles.slug
AND articles.author = authors.id
GROUP BY authors.name
ORDER BY views DESC;
'''

# 3. On which days did more than 1% of requests lead to errors?
'''
WITH logs_status AS(
	SELECT time::date AS date, status, COUNT(*) AS status_num
	FROM log
	GROUP BY time::date, status
) 
SELECT a.date, Round((b.status_num*1.0/(a.status_num+b.status_num))*100, 2) AS error
FROM logs_status a JOIN logs_status b
ON a.date = b.date AND a.status < b.status
WHERE (b.status_num*1.0/(a.status_num+b.status_num)*100) > 1;
'''