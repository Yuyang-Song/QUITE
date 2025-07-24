# SQLite updating row
[Link to question](https://stackoverflow.com/questions/53219608/sqlite-updating-row)
**Creation Date:** 1541735434
**Score:** 0
**Tags:** sql, sqlite
## Question Body
<p>I am developing a mobile application on cordova with a SQLite database.</p>

<p>The application receives data from an external source via JSONP and writes data to the database.</p>

<p>I need to use the sql query to determine if there is an entry in the table with a specific id, rewriting the row if there is and adding a new one if there is not.</p>

<p>At the moment, the data writing function looks like this:</p>

<pre><code>    addNews: function (id, title, date, content) {
    databaseHandler.db.transaction(
        function (tx) {
            tx.executeSql(
                "insert into news(id, title, date, content) values(?, ?, ?, ?)",
                [id, title, date, content],
                function (tx, results) { },
                function (tx, error) {
                    console.log("add news error: " + error.message);
                }
            );
        },
        function (error) {
        },
        function () {
        }
    );
}

var url = "http://cp35240-wordpress.tw1.ru/wp-content/plugins/plugin/news.js";
var script = document.createElement('script');
script.setAttribute('src', url);
document.getElementsByTagName('head')[0].appendChild(script);

function news(data) {
    var id = data.id;
    var title = data.title;
    var date = data.date;
    var content = data.content;  
    newsHandler.addNews(id, title, date, content);   
}
</code></pre>

## Answers
### Answer ID: 53219669
<p>You can make useof <code>INSERT OR REPLACE</code></p>

<p>Syntax </p>

<pre><code>INSERT OR REPLACE INTO TABLE (column_list) 
VALUES (value_list);
</code></pre>

<p>So here you can use </p>

<pre><code>INSERT OR REPLACE INTO news(id, title, date, content) values(?, ?, ?, ?)
</code></pre>

<p>Or you can use <code>UPSERT</code></p>

<pre><code>INSERT INTO news(id, title, date, content) 
values(?, ?, ?, ?)
ON CONFLICT(Id) DO UPDATE 
    SET tile=?
</code></pre>

<p>Further <a href="https://sqlite.org/lang_UPSERT.html" rel="nofollow noreferrer">Read</a></p>

