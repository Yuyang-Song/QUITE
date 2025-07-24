# Is it possible to use :bind (oracle style) in MYSQL query with Node?
[Link to question](https://stackoverflow.com/questions/44060958/is-it-possible-to-use-bind-oracle-style-in-mysql-query-with-node)
**Creation Date:** 1495164650
**Score:** 0
**Tags:** mysql, node.js
## Question Body
<p>I am migrating the database of my node.js/typescript project from Oracle to MYSQL.
My queries/dml in Oracle are all bind in this style</p>

<pre><code>conn.execute('select date, name from table
              where id = :ID and field = :VAR', 
             {ID: variable1, VAR: variable2});
</code></pre>

<p>When using MYSQL I found this:</p>

<pre><code>connection.query('select date, name from table
                  where id = ? and field = ?',
                  [variable1, variable2]);
</code></pre>

<p>The second approach is worse for me because of following reasons:</p>

<p>i- I would to rewrite a lot of sql calls in my code</p>

<p>ii- I think the first approach is much more reliable, as you are not concerning of having unpredictable results due to changing in SQL</p>

<p>Although I found some mention to the first style <a href="https://github.com/types/npm-mysql/blob/master/test/test.ts" rel="nofollow noreferrer">here</a>, it couldn't make it work</p>

<p>Any tips?</p>

## Answers
### Answer ID: 44081441
<p>As I didn't find anything ready that could solve the issue, I tried to solve the problem. Maybe this could be helpful.</p>

<p>first, this code gets an Oracle bind interface type like <code>{ID: 105, DEPT: 'MKT'}</code> and a query like <code>'select * from emp where id = :ID and deptName = :DEPT'</code> and translates them to <code>[105,'MKT']</code> and <code>'select * from emp where id = ? and deptName = ?'</code></p>

<p>here is the code</p>

<pre><code>const endBindCharacters: string = ' )=';   
function prepareSQL(sql: string, binders: Object = null, valueArray: TBindArray): string {
    let ich: number = 0;
    let bindVariable: string;

    if (! binders) {
        if (sql.indexOf(':') &gt; 0) {
            throw new CustomError(errorCodes.connection.sqlBoundWithNoBinders, 
                                  'No binders {} in a bound SQL ' + sql);
        };
        return sql;
    };

    while ((ich = sql.indexOf(':')) &gt; 0) {
        bindVariable = '';
        while (!endBindCharacters.includes(sql[++ich]) &amp;&amp; ich &lt; sql.length) {
            bindVariable += sql[ich];
        };
        if (binders[bindVariable]) {
            valueArray.push(binders[bindVariable]);  
        } else {
            throw new CustomError(errorCodes.connection.bindVariableNotInBinders, ' Bind variable ' + bindVariable + 
                                  ' não encontradada no binders {} da expressão:\n' + sql)
        };
        sql = sql.replace(':' + bindVariable, ' ? ');
    };
    return sql;
};
</code></pre>

<p>This is the wrapper. It will get a Promise from the callback.</p>

<pre><code>    export async function executeSQL (conn: TConnection, sql: string, 
binders: Object = {}): Promise&lt;TReturn&gt; {  
        let bindArray: TBindArray = [];
        sql = prepareSQL(sql, binders, bindArray);
        console.log(sql, binders, bindArray);
        return new Promise&lt;TReturn&gt;(function(resolve, reject) {
            conn.query(sql, bindArray , function(err: db.IError, results: TReturn) {
                if(err) {reject(err)}
                else {resolve(results)};
            });
        });
    };
</code></pre>

