# Scrapy pipeline queries not all arguments converted during string formatting
[Link to question](https://stackoverflow.com/questions/52812602/scrapy-pipeline-queries-not-all-arguments-converted-during-string-formatting)
**Creation Date:** 1539592211
**Score:** 1
**Tags:** python, scrapy, psycopg2
## Question Body
<p>Hello i'm trying to insert into postgresql using scrapy.</p>

<p>I'm trying to insert data into multiple columns in 1 database with 1 spider</p>

<p>The code for insert into 1 table worked, but when i change my database it required multiple tables to be inserted.</p>

<p>The code for pipeline query i rewrited and now it's returning with "not all arguments converted during string formatting" when i try to run my spider</p>

<p>I know it's something wrong with my query with using "%s" in python but i can't figured how to solve or change the query.</p>

<p><strong>Here is my pipelines.py:</strong></p>

<pre><code>import psycopg2
class TutorialPipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = '123' # your password
        database = 'discount'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into discount(product_name,product_price,product_old_price,product_link,product_image) values(%s,%s,%s,%s,%s)",(item['product_name'],item['product_price'],item['product_old_price'],item['product_link'],item['product_image']))
        self.cur.execute("insert into categories(name) values(%s)",(item['category_name']))
        self.cur.execute("insert into website(site) values(%s)",(item['product_site']))
        self.connection.commit()
        return item
</code></pre>

<p><strong>EDIT: HERE THE TRACEBACK ERRORS</strong></p>

<blockquote>
  <p>self.cur.execute("insert into categories(name)
  values(%s)",(item['category_name'])) TypeError: not all arguments
  converted during string formatting</p>
</blockquote>

## Answers
### Answer ID: 52814656
<p>Use named arguments. Simplified example:</p>
<pre><code>def process_item(self, item, spider):
    self.cur.execute('''
        insert into discount(product_name, product_price) 
        values(%(product_name)s, %(product_price)s)''',
        item)
    self.cur.execute('''
        insert into categories(name) 
        values(%(category_name)s)''',
        item)
    self.cur.execute('''
        insert into website(site) 
        values(%(product_site)s)''',
        item)
    self.connection.commit()
    return item
</code></pre>
<p>Read more on <a href="http://psycopg.org/docs/usage.html#passing-parameters-to-sql-queries" rel="nofollow noreferrer">Passing parameters to SQL queries.</a></p>

