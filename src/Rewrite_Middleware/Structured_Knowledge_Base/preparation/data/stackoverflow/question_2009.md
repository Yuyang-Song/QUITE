# Mysql - associative table - Unknown column in on clause
[Link to question](https://stackoverflow.com/questions/15494109/mysql-associative-table-unknown-column-in-on-clause)
**Creation Date:** 1363679599
**Score:** 0
**Tags:** php, mysql, sql, join
## Question Body
<p>The following query always returns #1054 - Unknown column 'T_RELATIF_SESS.REL_COM_ID' in 'on clause'</p>

<pre><code>SELECT
`T_FORMATIONS`.`FOR_ID`, 
`T_FORMATIONS`.`FOR_TITRE`, 
`T_FORMATIONS`.`FOR_NIVEAU`, 
`T_FORMATIONS`.`FOR_MAX_PART`, 
`T_RELATIF_SESS`.`REL_COM_ID`, 
`T_RELATIF_SESS`.`REL_SES_ID`,
`T_SESSIONS`.`SES_ID`, 
`T_SESSIONS`.`SES_TITRE`, 
`T_SESSIONS`.`SES_TYPE`, 
`T_SESSIONS`.`SES_ADRESSE`, 
`T_SESSIONS`.`SES_NPA`, 
`T_SESSIONS`.`SES_LIEU`, 
`T_SESSIONS`.`SES_PRIX_SPECIAL`, 
`T_SESSIONS`.`SES_VAL_PRIX_SPECIAL`, 
`T_SESSIONS`.`SES_PRIX_SPEC_EXP`, 
`T_SESSIONS`.`SES_SUPP_COURS_INCL`, 
`T_SESSIONS`.`SES_SUPP_COURS_ADD`, 
`T_SESSIONS`.`SES_PRIX_SUPP_COURS_ADD`, 
`T_SESSIONS`.`SES_HORAIRE_SPECIAL`, 
`T_SESSIONS`.`SES_REMARQUES`, 
`T_SESSIONS`.`SES_REC_ID`, 
`T_COURS`.`COU_ID`, 
`T_COURS`.`COU_DATE`, 
    (SELECT `COU_DATE` FROM `T_COURS` WHERE `T_COURS`.`COU_SES_ID` = `T_SESSIONS`.`SES_ID` ORDER BY `COU_DATE` ASC LIMIT 1) AS `PREMIERCOURS`, 
    (SELECT `COU_DATE` FROM `T_COURS` WHERE `T_COURS`.`COU_SES_ID` = `T_SESSIONS`.`SES_ID` ORDER BY `COU_DATE` DESC LIMIT 1) AS `DERNIERCOURS` 
FROM `T_COURS` 
INNER JOIN `T_COMMANDES` ON `T_RELATIF_SESS`.`REL_COM_ID` = `T_COMMANDES`.`COM_ID` 
INNER JOIN `T_RELATIF_SESS` ON `T_SESSIONS`.`SES_ID` = `T_RELATIF_SESS`.`REL_SES_ID` 
INNER JOIN `T_SESSIONS` ON `T_COURS`.`COU_SES_ID` = `T_SESSIONS`.`SES_ID` 
INNER JOIN `T_FORMATIONS` ON `T_SESSIONS`.`SES_FOR_ID` = `T_FORMATIONS`.`FOR_ID` 
WHERE `T_COMMANDES`.`COM_ID`=19
</code></pre>

<p>This query worked fine before I add </p>

<pre><code>INNER JOIN `T_COMMANDES` ON `T_RELATIF_SESS`.`REL_COM_ID` = `T_COMMANDES`.`COM_ID` 
INNER JOIN `T_RELATIF_SESS` ON `T_SESSIONS`.`SES_ID` = `T_RELATIF_SESS`.`REL_SES_ID` 
</code></pre>

<p>And</p>

<pre><code>WHERE `T_COMMANDES`.`COM_ID`=19
</code></pre>

<p><code>T_RELATIF_SESS</code> is juste an associative table between the tables called "T_SESSIONS" and "T_COMMANDES".
I've tried to rewrite the query many times but I still get this error and I really don't understand why. Every field exists in my database.</p>

<p>I know it may be simple but it really gives me headache. Can someone can give me a hand or just explain to me what I do wrong? It would be much apprecietaded!
Thank you very much!</p>

## Answers
### Answer ID: 15494234
<p>You try to access <code>T_RELATIF_SESS</code> before you have joined the table. You must join <code>T_COMMANDES</code> after <code>T_RELATIF_SESS</code> and <code>T_RELATIF_SESS</code> after <code>T_SESSIONS</code> </p>

<pre><code>SELECT
`T_FORMATIONS`.`FOR_ID`, 
...
FROM `T_COURS` 
INNER JOIN `T_SESSIONS` ON `T_COURS`.`COU_SES_ID` = `T_SESSIONS`.`SES_ID` 
INNER JOIN `T_FORMATIONS` ON `T_SESSIONS`.`SES_FOR_ID` = `T_FORMATIONS`.`FOR_ID` 
INNER JOIN `T_RELATIF_SESS` ON `T_SESSIONS`.`SES_ID` = `T_RELATIF_SESS`.`REL_SES_ID` 
INNER JOIN `T_COMMANDES` ON `T_RELATIF_SESS`.`REL_COM_ID` = `T_COMMANDES`.`COM_ID` 
WHERE `T_COMMANDES`.`COM_ID`=19
</code></pre>

### Answer ID: 15494202
<p>your order of table are messed up after you add your join, since you are using <code>INNER JOIN</code>, you can declare the table anywhere you like as long as the fields are visible on the joins. It will still yield the same result.</p>

<p>To solve the problem, put those new join on the lower part of your joins:</p>

<pre><code>FROM    T_COURS 
        INNER JOIN T_SESSIONS 
            ON T_COURS.COU_SES_ID = T_SESSIONS.SES_ID 
        INNER JOIN T_FORMATIONS 
            ON T_SESSIONS.SES_FOR_ID = T_FORMATIONS.FOR_ID
        INNER JOIN T_RELATIF_SESS 
            ON T_SESSIONS.SES_ID = T_RELATIF_SESS.REL_SES_ID 
        INNER JOIN T_COMMANDES 
            ON T_RELATIF_SESS.REL_COM_ID = T_COMMANDES.COM_ID 
</code></pre>

<p>The reason why an error message: <code>Unknown column 'T_RELATIF_SESS.REL_COM_ID' in 'on clause'</code> was thrown is because when joining <code>T_COURS</code> with <code>T_COMMANDES</code>, column <code>T_RELATIF_SESS</code>.<code>REL_COM_ID</code> isn't visible yet since you have declared table <code>T_RELATIF_SESS</code> on the lower part of the join.</p>

### Answer ID: 15494192
<p>So from your description you try to run the script without </p>

<pre><code>INNER JOIN `T_COMMANDES` ON `T_RELATIF_SESS`.`REL_COM_ID` = `T_COMMANDES`.`COM_ID` 
INNER JOIN `T_RELATIF_SESS` ON `T_SESSIONS`.`SES_ID` = `T_RELATIF_SESS`.`REL_SES_ID` 
</code></pre>

<p>and it is working, but not with that script? Try to make it in order, since on your first inner join, you are trying to join the table (T_COMMANDES) with the table that you will join next (T_RELATIF_SESS).</p>

<p>So try:</p>

<pre><code>INNER JOIN `T_SESSIONS` ON `T_COURS`.`COU_SES_ID` = `T_SESSIONS`.`SES_ID` 
INNER JOIN `T_FORMATIONS` ON `T_SESSIONS`.`SES_FOR_ID` = `T_FORMATIONS`.`FOR_ID` 
INNER JOIN `T_RELATIF_SESS` ON `T_SESSIONS`.`SES_ID` = `T_RELATIF_SESS`.`REL_SES_ID` 
INNER JOIN `T_COMMANDES` ON `T_RELATIF_SESS`.`REL_COM_ID` = `T_COMMANDES`.`COM_ID`
</code></pre>

