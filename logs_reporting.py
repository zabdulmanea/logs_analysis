#!/usr/bin/env python3
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
        SELECT to_char(a.date, 'FMMonth DD, YYYY') AS Date,
        Round((b.status_num*1.0/(a.status_num+b.status_num))*100, 2) AS error
        FROM logs_status a JOIN logs_status b
        ON a.date = b.date AND a.status < b.status
        WHERE (b.status_num*1.0/(a.status_num+b.status_num)*100) > 1; """
]


def connect_db(db_name):
    """Connect to the PostgreSQL database then return the connection"""
    try:
        db = psycopg2.connect("dbname=" + db_name)
        cursor = db.cursor()
        return db, cursor
    except psycopg2.Error as e:
        print("Unable to connect to '" + db_name + "' database")
        # throw an error
        raise e


def get_result(query):
    """Execute the PostgreSQL query then return the results"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def popular_articles():
    """Get popular articales results"""
    articles = "\r\n1. %s:\r\n" % questions[0]
    result = get_result(queries[0])
    for article in result:
        articles += '"' + article[0] + '" - ' + str(article[1]) + ' views\r\n'
    return articles


def popular_authors():
    """Get popular authors results"""
    authors = "\r\n2. %s:\r\n" % questions[1]
    result = get_result(queries[1])
    for author in result:
        authors += author[0] + ' - ' + str(author[1]) + ' views\r\n'
    return authors


def top_errors_days():
    """Get days with error more than 1%"""
    days = "\r\n3. %s:\r\n" % questions[2]
    result = get_result(queries[2])
    for day in result:
        days += day[0] + ' - ' + str(day[1]) + '% errors\r\n'
    return days


def print_results():
    """Write results into new text file and terminal"""
    summary_title = "-- Log Analysis Reporting Tool Resluts --\r\n"
    # print results into a file
    logs_file = open("logs_results.txt", "w+")
    logs_file.write(summary_title + top_articles + top_authors + error_days)
    logs_file.close()
    # print results into terminal
    print(summary_title + top_articles + top_authors + error_days)


if __name__ == '__main__':
    # connect to news database
    db, cursor = connect_db("news")
    # get results of top three articles
    top_articles = popular_articles()
    # get results of top authors
    top_authors = popular_authors()
    # get results of days with more than 1% errors
    error_days = top_errors_days()
    # close db connection
    db.close()
    # print log analysis summary
    print_results()
