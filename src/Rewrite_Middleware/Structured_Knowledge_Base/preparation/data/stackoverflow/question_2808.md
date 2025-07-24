# Working SQL produces type and syntax errors with Node and pg-promise
[Link to question](https://stackoverflow.com/questions/53471546/working-sql-produces-type-and-syntax-errors-with-node-and-pg-promise)
**Creation Date:** 1543177212
**Score:** 0
**Tags:** node.js, postgresql, express, pg-promise
## Question Body
<p>I'm working with Node and Express, and using the pg-promise library to interact with my Postgres database. I have many queries set up and they all work fine. I have written a query no different than the rest that works when tested out in the Postgres command line. All it does is get a list of filenames from each entry in the "awards" table belonging to a particular user. However, when my server tries to execute the code, it throws multiple exceptions:</p>

<blockquote>
  <p>TypeError: path must be a string or Buffer</p>
  
  <p>syntax error at or near \"JOIN\"</p>
</blockquote>

<p>The relevant code is:</p>

<pre><code>const GET_ALL_PDFS = PS('getAllPDFs', `SELECT pdf_filename AS filenames
                                   FROM awards
                                   JOIN users ON users.id = awards.award_giver
                                   WHERE users.id = $1;`);

UserManagementDAO.getAllPDFs = (userId, cb) =&gt; {
db.any(GET_ALL_PDFS, userId)
    .then(result =&gt; {
        cb(null, result);
    })
    .catch(err =&gt; {
        winston.error(`Error fetching all PDF filenames for user ${userId}: ${err}`);
        cb(err);
    });
};
</code></pre>

<p>I've tried using '' instead of ``, putting the SQL statement on one line, rewriting the entire SQL statement, using db.manyOrNone instead of db.any, putting the SQL statement in directly instead of using a prepared statement, explicitly using INNER JOIN instead of JOIN, and so far nothing has worked. I always get the same errors.</p>

