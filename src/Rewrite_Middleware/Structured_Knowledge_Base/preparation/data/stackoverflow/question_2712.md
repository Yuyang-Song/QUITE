# MySQL: Move data from one table to another with different schema
[Link to question](https://stackoverflow.com/questions/48593654/mysql-move-data-from-one-table-to-another-with-different-schema)
**Creation Date:** 1517628616
**Score:** 0
**Tags:** mysql, sql, database
## Question Body
<p>I have a table with a bad design:</p>

<pre><code>CREATE TABLE token (
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT(10) UNSIGNED NOT NULL,

    token VARCHAR(191) NOT NULL,
    expiration TIMESTAMP NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);
</code></pre>

<p>The reason I see it as bad now even though it worked well before is because now I cannot reuse that <code>token</code> table if I want a token related to an email or something else. I could just add <code>email_id</code> column but then I would need ugly logic to determine if the token is meant for a user or an email, respectively.</p>

<p>I want to normalize this design such that I can have a single <code>token</code> table that isn't coupled to any <code>user_id</code> or <code>email_id</code>, and have <code>user_token</code> and <code>email_token</code> pivot tables for the relations.</p>

<p>But I am also using migrations so I can't just rewrite my schema. I need to modify this on the fly with data present in the database.</p>

<p>I need to do the following:</p>

<ol>
<li>Create new <code>user_token</code> and <code>email_token</code> tables <strong>(COMPLETE)</strong></li>
<li>Copy <code>token.id</code> to <code>user_token.token_id</code> column, and copy <code>token.user_id</code> value to <code>user_token.user_id</code> column. The copying needs to be done in an <code>INSERT</code> statement since the <code>user_token</code> table will be brand new with no data <strong>(TODO)</strong></li>
<li>Remove <code>token.user_id</code> column <strong>(COMPLETE)</strong></li>
</ol>

<p>Step 2 is the part I need help on. Any help would be appreciated to write that query.</p>

<p>This is what the new schema will look like if it helps to create a query for step 2:</p>

<pre><code>CREATE TABLE token (
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,

    token VARCHAR(191) NOT NULL,
    expiration TIMESTAMP NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE user_token (
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT(10) UNSIGNED NOT NULL,
    token_id INT(10) UNSIGNED NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (token_id) REFERENCES token (id) ON DELETE CASCADE
);

CREATE TABLE email_token (
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    email_id INT(10) UNSIGNED NOT NULL,
    token_id INT(10) UNSIGNED NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (email_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (token_id) REFERENCES token (id) ON DELETE CASCADE
);
</code></pre>

## Answers
### Answer ID: 48593846
<p>IF you haven't delete token.user_id and token.email_id columns from token table, then you can copy them by using a simple INSERT:</p>

<pre><code>INSERT INTO user_token (user_id, token_id)
SELECT user_id, id
FROM token

INSERT INTO email_token (email_id, token_id)
SELECT email_id, id
FROM token
</code></pre>

<p>if you want to copy created_at, updated_at, and deleted_at columns along with them, you could just add them into the query:</p>

<pre><code>INSERT INTO user_token (user_id, token_id, created_at, updated_at, deleted_at)
SELECT user_id, id, created_at, updated_at, deleted_at
FROM token

INSERT INTO email_token (email_id, token_id, created_at, updated_at, deleted_at)
SELECT email_id, id, created_at, updated_at, deleted_at
FROM token
</code></pre>

<p>this will copy them into the new tables. Then, you only need to delete user_id and email_id columns from token table by a simple ALTER :</p>

<p>FIRST DELETE FOREIGN KEY: </p>

<pre><code>ALTER TABLE token DROP FOREIGN KEY user_id
</code></pre>

<p>THEN DELETE THE COLUMNS: </p>

<pre><code>ALTER TABLE token DROP COLUMN user_id;
ALTER TABLE token DROP COLUMN email_id;
</code></pre>

