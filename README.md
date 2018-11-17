# Log Analysis
An internal reporting tool uses information from the database of newspaper articles and web servers log. This reporting tool aims to build an informative summary of most articles people like to read, most authors people like thier article and the days when more than 1% request errors has occured. The project is guided by [Udacity’s Full Stack Developer Nanodegree Program](https://sa.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Description
This is a python module uses information from logs in a large database and build an informative summary from that information. The database of this project is from a newspaper database and it includes three tables:
* `Authors`: includes information about articles authors.
* `Articles`: includes information of articles.
* `Log`: includes logs of every article request to the web server.

#### The project aims to solve these question:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Instructions

### PreRequests
* [Python 3](https://www.python.org/).
* [VirtualBox](https://www.virtualbox.org/).
* [Vagrant](https://www.vagrantup.com/).

### Setup
**1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)**

**2. Download the VM configuration**
* Open terminal.
* Clone the VM configuration repository:
`git clone https://github.com/udacity/fullstack-nanodegree-vm` 
* Change the directory to vagrant directory.
* Run `vagrant up` - to download and install the Linux operating system.
* Run `vagrant ssh` - to log into your Linux VM!

**3. Load the database into your local database**
*  Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). - newspaper data file `newsdata.sql`
* Unzip the file and put it inside vagrant directory.
* Run `psql -d news -f newsdata.sql`

**4. Clone the project repository to vagrant directory**  
`git clone https://github.com/zabdulmanea/logs_analysis.git`

**5. Run Python Module**
* Change directory to the project directory:  
`cd /vagranat/logs_analysis`
* Run `python3 logs_reporting.py`

**6. View Results Summary**  
You can see the logs Analysis results inside `logs_results.txt`


### Creating Views
1. Open terminal and satrt the VM.

2. Run `psql -d news` - to connect to the database.

3. Create **Popular Articles** View
```
CREATE OR REPLACE VIEW popular_articles AS
    SELECT articles.title AS "Popular Articles", COUNT(*) AS Views
    FROM log JOIN articles
    ON articles.slug = SUBSTRING(log.path,10)
    GROUP BY articles.title
    ORDER BY Views DESC LIMIT 3;
```
|     Column      |  Type  | 
------------------|--------|
 Popular Articles | text   | 
 views            | bigint | 

4. Create **Popular Authors** View
```
CREATE OR REPLACE VIEW popular_authors AS
    SELECT authors.name, COUNT(*) AS Views
    FROM log, articles, authors
    WHERE SUBSTRING(log.path,10) = articles.slug
        AND articles.author = authors.id
    GROUP BY authors.name
    ORDER BY views DESC;
```
| Column |  Type  |
---------|--------|
 name    | text   | 
 views   | bigint | 

5. Create **Request Errors** View
```
CREATE OR REPLACE VIEW log_errors AS
    WITH logs_status AS(
        SELECT time::date AS date, status, COUNT(*) AS status_num
        FROM log
        GROUP BY date, status )
    SELECT to_char(a.date, 'FMMonth DD, YYYY') AS Date,
        Round((b.status_num*1.0/(a.status_num+b.status_num))*100, 2) AS error
    FROM logs_status a JOIN logs_status b
    ON a.date = b.date AND a.status < b.status
    WHERE (b.status_num*1.0/(a.status_num+b.status_num)*100) > 1;
```
| Column |  Type   |
---------|---------|
 date    | text    | 
 error   | numeric | 