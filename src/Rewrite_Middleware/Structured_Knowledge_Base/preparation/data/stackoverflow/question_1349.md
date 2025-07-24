# More concise function to fetch SQL result set in GO Golang
[Link to question](https://stackoverflow.com/questions/71816948/more-concise-function-to-fetch-sql-result-set-in-go-golang)
**Creation Date:** 1649596565
**Score:** 0
**Tags:** mysql, sql, go
## Question Body
<p>I want to retrieve an array of app IDs from a MySQL database. I used <a href="http://go-database-sql.org/retrieving.html" rel="nofollow noreferrer">http://go-database-sql.org</a>'s example code:</p>
<pre class="lang-golang prettyprint-override"><code>func QueryAppList() *[]int64 {
    var (
        appList []int64
        appid   int64
    )
    qry := &quot;SELECT a.appid FROM app a WHERE a.app_status IN (1, 2);&quot;
    // cfg.GetDb() supplies the database connection already established
    rows, err := cfg.GetDb().Query(qry) 
    if err != nil {
        logg.Error(err)
        return &amp;appList
    }
    defer func(rows *sql.Rows) { 
        // simple defer does not catch every error: https://www.joeshaw.org/dont-defer-close-on-writable-files/
        err := rows.Close()
        if err != nil {
            logg.Error(err)
        }
    }(rows)
    for rows.Next() {
        err := rows.Scan(&amp;appid)
        if err != nil {
            logg.Error(err)
            return &amp;appList
        }
        appidList = append(appList, appid)
    }
    err = rows.Err()
    if err != nil {
        logg.Error(err)
        return &amp;appList
    }
    return &amp;appidList
}
</code></pre>
<p>My programm will be littered with queries like this. All the ways of getting the result list and how it to prevent failure make this small query hard to read what is actually going on.</p>
<p><strong>Is there a way to make queries more concise?</strong></p>
<p>These are my thoughts to make the code less verbose:</p>
<ul>
<li>Use functions to handle the errors reducing the error handling to one line.</li>
<li>If it's one column array I want, I could pass the query and column name as parameters and reuse the query function. I rather just rewrite a query function than to deal with complicated abstractions.</li>
<li>Are there packages I missed that help reduce the clutter?</li>
</ul>
<p>Using an ORM like gorm is NOT an option.</p>
<p>I just started Go programming so I am lacking experience with the language.</p>
<p>Below is the same query in Node.js with the same result. It has 9 lines compared to Go's 34 i.e. 65% more concise in terms of length. That's where I ideally would like to get to.</p>
<pre><code>import {query} from &quot;../db/pool&quot;; // connection pool query from https://github.com/sidorares/node-mysql2

export const queryAppList = async () =&gt; {
  try {
    const qry = &quot;SELECT a.appid FROM app a WHERE a.app_status IN (1, 2);&quot;;
    const [appList] = await query(qry);
    return appList; 
  } catch (err) {
    console.error(err)
    return [];
  }
};
</code></pre>

## Answers
### Answer ID: 71817438
<p>You can make a Query struct which has reusable methods for do such things.</p>
<p>Something like this:</p>
<pre><code>type Query struct{
    conn *sql.DB
    rows *sql.Rows
    ...
}

func NewQuery(conn *sql.DB) *Query {
    return &amp;Query{
        conn: conn,
        rows: nil,
    }
}

func (q Query) OpenSQL(sql string) error {
    q.rows, err = q.conn.Query(sql)
    if err != nil {
        log.Error(&quot;SQL error during query (&quot;+sql+&quot;). &quot;+err.Error())
        return err
    }
    return nil
}

func (q Query)Close() (error) {
    err := q.rows.Close()
    if err != nil {
        log.Error(&quot;Error closing rows. &quot;+err.Error())
        return err
    }
    return nil
}

//You can use generic functions to make the code even smaller
func FetchToSlice[T any](q Query) ([]T, error) {
    result := make([]T, 0)
    var value T
    for q.rows.Next() {
        err := q.rows.Scan(&amp;value)
        if err != nil {
           log.Error(&quot;Error during fetching. &quot;+err.Error())
           return nil, err
        }
        result = append(result, value)
    }
    return result, nil
} 
</code></pre>
<p>With this you code will look something like this:</p>
<pre><code>qry := NewQuery(cfg.GetDB())
err := qry.OpenSQL(&quot;SELECT a.appid FROM app a WHERE a.app_status IN (1, 2);&quot;)
if err != nil {
    return err
}
defer qry.Close()
appidList, err := FetchToSlice[int](qry)
if err != nil {
    return err
}
</code></pre>
<p>You can later add more methods to your Query to handle more complex cases, even you can use a <code>sync.Pool</code> to cache your query structs and so on.</p>

