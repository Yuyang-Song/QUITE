# How to wrap pool.query function for error handling in node/mysql2 using typescript
[Link to question](https://stackoverflow.com/questions/61837507/how-to-wrap-pool-query-function-for-error-handling-in-node-mysql2-using-typescri)
**Creation Date:** 1589635601
**Score:** 0
**Tags:** node.js, typescript, types, mysql2
## Question Body
<p>I'm currently rewriting a modularized node application to use async/await, inlcuding the database connection. I am using <a href="https://github.com/sidorares/node-mysql2" rel="nofollow noreferrer">https://github.com/sidorares/node-mysql2</a> and also installed <a href="https://github.com/types/mysql2" rel="nofollow noreferrer">https://github.com/types/mysql2</a>.</p>
<p>I want to write a wrapper function that takes the SQL statement and additional data, and returns either <strong>(1)</strong> a result set (for <code>SELECT</code>), <strong>(2)</strong> some kind of success message (for <code>INSERT</code>, <code>UPDATE</code>...) or <strong>(3)</strong> an error message (duplicate entry, no connection ...).</p>
<p>My approach so far:</p>
<p><em>database.wrapper.ts</em></p>
<pre class="lang-js prettyprint-override"><code>const pool = createPool(config.db).promise();

const query = async (sql, data, DEBUG_INFO) =&gt; {
    data = escapeSql(data);
    try {
        const [result] = await pool.query(sql, data);
        return result;
    } catch (e) {
        const errorMessage = logDbErrors(e, DEBUG_INFO);
        return {
            message: errorMessage,
        } as ApiResponse;
    }
};

export { query };
</code></pre>
<p><em>log-db-errors.ts</em> (logging works as it should be)</p>
<pre class="lang-js prettyprint-override"><code>export const logDbErrors = (err: MysqlError, DEBUG_INFO = { }): string =&gt; {

    DEBUG_INFO = {
        logtype: LogTypes.MySQL,    // Set LogType to MySQL to apply proper format
        err,    // Add the MysqlError for the log files
        ...DEBUG_INFO,  // Append additionally provided information (like filename)
    };

    let message = '';

    if (err) {
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            message = 'Database connection was closed';
        } else if (err.code === 'ER_CON_COUNT_ERROR') {
            message = 'Database has too many connections';
        } else if (err.code === 'ECONNREFUSED') {
            message = 'Database connection was refused';
        } else {
            message = `Database error: ${ err.message }`;
        }
    }

    logger.error(message, DEBUG_INFO);
    return message;
};
</code></pre>
<p>You can ignore the DEBUG_INFO stuff. My problem is to return the proper type in the query function. In my services, I want to be able to query something from the database and return either multiple rows, a success info or an error:</p>
<p><em>foo.service.ts</em> (as example)</p>
<pre class="lang-js prettyprint-override"><code>const createUser = async (firstName, lastName) =&gt; {
    const sql = 'INSERT INTO users SET ?';
    const sqlData = { id: null, first_name: firstName, last_name: lastName };
    const result = await query(sql, sqlData, DEBUG_INFO);
    // return either resultset, success info or error
};
</code></pre>
<p>In this example though I'm not able to distinguish this when calling <code>query(...)</code>. I know there are RowDataPacket, OkPacket and QueryError interfaces in types/mysql2, but I cannot tell which result I get in my service.</p>
<p>Any tips for handling this situation? Do I need multiple functions (<code>querySelect()</code>, <code>queryInsert()</code> ...) for this? How can I return an api response using the <code>result</code> in <em>foo.service.ts</em>?</p>
<p>EDIT: Also came across this 'sure thing', a wrapper for promises where you define if it's okay or not (in my case result set, success or error): <a href="https://medium.com/@jesterxl/easier-error-handling-using-async-await-b9ab0cb938e#ac60" rel="nofollow noreferrer">https://medium.com/@jesterxl/easier-error-handling-using-async-await-b9ab0cb938e#ac60</a>
Would this be the only workaround to my problem?</p>

