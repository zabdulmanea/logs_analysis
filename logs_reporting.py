# !/usr/bin/env python3
# Database code for logs analysis of news DB

import psycopg2

# The questions list should be answered by db queries
questions = [
    "The most popular three articles of all time",
    "The most popular article authors of all time",
    "Days with more than 1% of requests lead to errors",
]

# The queries to answer the questions list
queries = [
    """ SELECT articles.title AS "Popular Articles", COUNT(*) AS Views
      FROM log JOIN articles
      ON articles.slug = SUBSTRING(log.path,10)
      GROUP BY articles.title
      ORDER BY Views DESC LIMIT 3; """,
    """ SELECT authors.name, COUNT(*) AS Views
        FROM log, articles, authors
        WHERE SUBSTRING(log.path,10) = articles.slug
        AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC; """,
    """ WITH logs_status AS(
            SELECT time::date AS date, status, COUNT(*) AS status_num
            FROM log
            GROUP BY date, status )
        SELECT to_char(a.date, 'FMMonth DD, YYYY'),
        Round((b.status_num*1.0/(a.status_num+b.status_num))*100, 2) AS error
        FROM logs_status a JOIN logs_status b
        ON a.date = b.date AND a.status < b.status
        WHERE (b.status_num*1.0/(a.status_num+b.status_num)*100) > 1; """
]


def get_result(query):
    """Return all queries results from 'news database"""
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def view_result():
    """Get queries results and write results into new text file"""

    logs_file = open("logs_results.txt", "w+")
    logs_file.write('-- Log Analysis Reporting Tool Resluts --\r\n')

    i = 0
    while i < len(questions):
        logs_file.write("\r\n* %s:\r\n" % questions[i])
        query_results = get_result(queries[i])

        j = 0
        while j < len(query_results):
            if i == 0:
                logs_file.write('"' + query_results[j][0] + '" - ' +
                                str(query_results[j][1]) + ' views')
            elif i == 1:
                logs_file.write(query_results[j][0] + ' - ' +
                                str(query_results[j][1]) + ' views')
            else:
                logs_file.write(query_results[j][0] + ' - ' +
                                str(query_results[j][1]) + '% errors')
            logs_file.write('\r\n')
            j += 1

        i += 1
    logs_file.close()


if __name__ == '__main__':
    view_result()
