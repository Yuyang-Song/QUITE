# MSSQL leaking connections
[Link to question](https://stackoverflow.com/questions/42988169/mssql-leaking-connections)
**Creation Date:** 1490308220
**Score:** 1
**Tags:** sql-server, go
## Question Body
<p>I have strange issue with golang sql and probably denisenkom/go-mssqldb.</p>

<p>My code part:
</p>

<pre><code>func Auth(username string, password string, remote_ip string, user_agent string) (string, User, error) {
var token string
var user = User{}

query := `exec dbo.sp_get_user ?,?`

rows, err := DB.Query(query, username, password)
if err != nil {
    return token, user, err
}
defer rows.Close()

rows.Next()
if err = rows.Scan(&amp;user.Id, &amp;user.Username, &amp;user.Description); err != nil {
    log.Printf("SQL SCAN: Failed scan User in Auth. %v \n", err)
    return token, user, err
}

hashFunc := md5.New()
hashFunc.Write([]byte(username + time.Now().String()))

token = hex.EncodeToString(hashFunc.Sum(nil))

query = `exec dbo.sp_set_session ?,?,?,?`

_, err = DB.Exec(query, user.Id, token, remote_ip, user_agent)
if err != nil {
    return token, user, err
}

return token, user, nil
}
</code></pre>

<p>Problem: <code>defer rows.Close()</code> - not working properly</p>

<p>After this with <code>DB.Connection.Stats().OpenConnections</code> I always have 2 connection opened (also after repeat User login is still 2 connection for whole app lifecycle)</p>

<p>But if I rewrite func as:</p>

<pre><code>...
    query := `exec dbo.sp_get_user ?,?`

    rows, err := DB.Query(query, username, password)
    if err != nil {
        return token, user, err
    }
    defer rows.Close()

    rows.Next()
    if err = rows.Scan(&amp;user.Id, &amp;user.Username, &amp;user.Description); err != nil {
        log.Printf("SQL SCAN: Failed scan User in Auth. %v \n", err)
        return token, user, err
    }

    rows.Close()
...
</code></pre>

<p>Then rows underline stmt is closed and next <code>DB.Connection.Stats().OpenConnections</code> always will be 1 connection open.</p>

<p><code>DB</code> in my app is simply return underlying connection from <code>sql.Open</code></p>

<p>Problem is only in this part where two query executions with <code>Query</code> and <code>Exec</code> in one functions.</p>

<p>Maybe <code>Query</code> and <code>Exec</code> defines different connections, but i don't find this in driver source or database/sql source.</p>

<p>Thank you! (sorry for english if it's so bad)</p>

<p>PS:</p>

<p><code>exec dbo.sp_get_user ?,?</code> - is simple select from user table, not more.</p>

<p><code>exec dbo.sp_set_session ?,?,?,?</code> - is simple insert to user table, not more</p>

<p>In MSSQL - <code>DBCC INPUTBUFFER</code> shows me query = <code>'cast(@@identity as bigint)'</code> which executes in denisenkom/go-mssqldb mssql.go on line 593</p>

