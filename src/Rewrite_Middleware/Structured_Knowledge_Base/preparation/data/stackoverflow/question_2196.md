# Trying to run 3 SQL statements on Node.js + SQLite getting abysmal performance
[Link to question](https://stackoverflow.com/questions/23073030/trying-to-run-3-sql-statements-on-node-js-sqlite-getting-abysmal-performance)
**Creation Date:** 1397524552
**Score:** 1
**Tags:** sql, node.js, sqlite
## Question Body
<p>I have a 127MB SQLite database, very simple just one table and 8 columns, it looks like this:</p>

<pre><code>CREATE TABLE stocks (Ticker text, Date text,  Open real, High real, Low real, Close real, Volume integer, Change real);
</code></pre>

<p>Using Node.js I am trying to execute these 3 SQL statements on my database:</p>

<pre><code>SELECT DISTINCT ticker FROM stocks
SELECT close,date from stocks where ticker=? order by date asc
UPDATE stocks set change=? where ticker=? and date=?
</code></pre>

<p>They are all nested in foreach (i.e. for each result of the first statement I execute the second and for each result in the second I execute the third).</p>

<p>I have tried using two modules: (<strong>dblite</strong> &amp; <strong>node-sqlite3</strong>). With dblite I get <strong>100% CPU load on sqlite</strong>, left it running for 24 hours and the DB file is untouched. With <strong>node-sqlite3 I get 100% CPU load on Node.js</strong> and no results.</p>

<p>Source with <strong>dblite</strong>:</p>

<pre><code>var dblite = require('dblite'),
    db = dblite('asx.db');

db.query(
  'SELECT DISTINCT ticker FROM stocks',  function (err, tickers) {
    if(err) console.log(err);
    console.log('Got '+tickers.length+' tickers.');
    tickers.forEach(function(ticker) {
        db.query('SELECT close,date from stocks where ticker=? order by date asc',ticker, function(err, rows) {
                if(err) console.log(err);
                var count = 0;
                var previousClose = 0;
                rows.forEach(function(row) {
                        if (count&gt;0) {
                                var change = ((((row[0]-previousClose)/previousClose))*100).toFixed(2);
                                db.query('UPDATE stocks set change=? where ticker=? and date=?',[change,ticker,row[1]], function(err) {
                                        if(err) console.log(err);
                                });

                        }
                        previousClose = row[0];
                        count++;
                });
        });
    });
  }
);
</code></pre>

<p>Source with <strong>node-sqlite3</strong>:</p>

<pre><code>var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('asx.db');

db.each(
  'SELECT DISTINCT ticker FROM stocks',  function (err, tickers) {
    if(err) console.log(err);
        var count = 0;
        var previousClose = 0;
        db.each('SELECT close,date from stocks where ticker=? order by date asc',tickers.Ticker, function(err, row) {
                if(err) console.log(err);
                        if (count&gt;0) {
                                var change = ((((row.Close-previousClose)/previousClose))*100).toFixed(2);
                                db.run('UPDATE stocks set change=? where ticker=? and date=?',[change,tickers.Ticker,row.Date], function(err) {
                                        if(err) console.log(err);
                                });
                        }
                        previousClose = row.Close;
                        count++;
                });
        });
</code></pre>

<p>I know my nested queries are causing exponential complexity, still I don't think it should be taking this long to execute. I think I am doing something wrong. How can I solve this problem? Should I rewrite my code in a sync fashion with Perl or should I switch from SQLite to MySQL?</p>

<p>Thanks.</p>

## Answers
### Answer ID: 23082906
<p>Lookup and sorting operations can be sped up with indexes.</p>

<p>For these particular statements, the following index would be useful:</p>

<pre class="lang-sql prettyprint-override"><code>CREATE INDEX stocks_ticker_date_idx ON stocks(ticker, date);
</code></pre>

### Answer ID: 23074588
<p>I was able to get it working ( I think, still 100% CPU load but at least the DB file is being updated ). I followed Dan Bracuk's idea and changed all dates to integer, then I combined my first two SQL statements into one. <strong>I tried using sqlite3 but it was always running out of memory</strong>. Then I switched to dblite and that's what I am using right now. This is the working code:</p>

<pre><code>var dblite = require('dblite'),
db = dblite('asx.db');
var count = 0;
var previousClose = 0;
var previousTicker = '';
db.query('SELECT ticker,close,date from stocks order by ticker, date asc',function(err, rows) {
     if(err) console.log(err);
     rows.forEach(function(row) {
          if (previousTicker !== row[0]) {
               count = 0;
               previousClose = 0;
               previousTicker = row[0];
          }
          if (count&gt;0) {
               var change = ((((row[1]-previousClose)/previousClose))*100).toFixed(2);
               db.query('UPDATE stocks set change=? where ticker=? and date=?',[change,row[0],row[2]], function(err) {
                     if(err) console.log(err);
               });
          }
          previousClose = row[1];
          count++;
     });
});
</code></pre>

