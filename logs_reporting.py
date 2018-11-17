# !/usr/bin/env python3
# Database code for logs analysis of news DB

import psycopg2

questions = [
    "The most popular three articles of all time",
    "The most popular article authors of all time",
    "Days with more than 1% of requests lead to errors",
]

queries = [
    """ SELECT articles.title AS "Popular Articles", COUNT(*) AS Views
      FROM log JOIN articles
      ON articles.slug = SUBSTRING(log.path,10)
      GROUP BY articles.title
      ORDER BY Views DESC LIMIT 3;
    """, """ SELECT authors.name, COUNT(*) AS Views
        FROM log, articles, authors
        WHERE SUBSTRING(log.path,10) = articles.slug
        AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;
    """, """ WITH logs_status AS(
            SELECT time::date AS date, status, COUNT(*) AS status_num
            FROM log
            GROUP BY time::date, status ) 
        SELECT to_char(a.date, 'FMMonth DD, YYYY'), 
        Round((b.status_num*1.0/(a.status_num+b.status_num))*100, 2) AS error
        FROM logs_status a JOIN logs_status b
        ON a.date = b.date AND a.status < b.status
        WHERE (b.status_num*1.0/(a.status_num+b.status_num)*100) > 1;
    """
]


def get_result(query):
    """Return all results from 'news database"""
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def view_result():
    print('-- Log Analysist Reporting Tool Resluts --')
    i = 0
    while i < len(questions):
        print('\n' + questions[i] + ':')
        query_results = get_result(queries[i])
        j = 0
        while j < len(query_results):
            if i != 2:
                print('"' + query_results[j][0] + '" — ' +
                      str(query_results[j][1]) + ' views')
            else:
                print(query_results[j][0] + ' — ' + str(query_results[j][1]) +
                      '% errors')
            j += 1
        i += 1


if __name__ == '__main__':
    view_result()
