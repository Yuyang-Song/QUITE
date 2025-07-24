# Temp views are disabled on Cloudant
[Link to question](https://stackoverflow.com/questions/38453210/temp-views-are-disabled-on-cloudant)
**Creation Date:** 1468916960
**Score:** 0
**Tags:** couchdb, pouchdb, cloudant
## Question Body
<p>I get a <code>403 forbidden</code> when querying my database on Cloudant, with the following error: &quot;temp views are disabled on Cloudant&quot;.</p>
<p>How can I rewrite the query to avoid this?</p>
<pre><code>.factory('usersDatabaseRemote', [
    'pouchDB',
    function (pouchDB) {
        'use strict';

        var usersDatabaseRemote = pouchDB('https://id:pwd@louis.cloudant.com/board_users');
           
        return usersDatabaseRemote;
    }
])
</code></pre>
<p>and :</p>
<pre><code>           usersDatabaseRemote.query(mapByEmail, {
                key: email,
                include_docs: true
            }).then(function (result) {

                if (!result.rows.length) { //email doesn't exist in DB
                    return callback(false);
                }
                if (result.rows.length === 1) {
                    return callback(result);
                }
                console.log(&quot;problem : several docs in the DB with same email, run a duplicate check on the DB&quot;);
                return callback(result);
            });
</code></pre>

## Answers
### Answer ID: 38662498
<p>Temporary views were dropped in CouchDB 2.0 and in Cloudant because they were determined to be too big of a source of user error and therefore not worth maintaining. They are slow and people tended to abuse them to create slow indexes.</p>

