# TYPO3 12.1.3 - getting 503 code after attempt login by LoginForm on frontend
[Link to question](https://stackoverflow.com/questions/75039641/typo3-12-1-3-getting-503-code-after-attempt-login-by-loginform-on-frontend)
**Creation Date:** 1673087830
**Score:** 0
**Tags:** mariadb, typo3
## Question Body
<p>Backend works correct. Problem is only on frontend with additionally Login Form on custom login site.
I getting 503 error after trying login by &quot;Login Panel&quot;. It doesn't matter right or wrong login data.</p>
<p><img src="https://i.sstatic.net/IergI.png" alt="1" /></p>
<p>I turned off the redirect on backend but I still get this same error with log below:</p>
<p>Core: Exception handler (WEB): Uncaught TYPO3 Exception: #1064: An exception occurred while executing a query: You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ')))) AND (<code>fe_users</code>.<code>deleted</code> = 0)' at line 1 | Doctrine\DBAL\Exception\SyntaxErrorException thrown in file /public/my_site_name/vendor/doctrine/dbal/src/Driver/API/MySQL/ExceptionConverter.php in line 86. Requested URL: <a href="https://my-domain-name.pl/login?tx_felogin_login%5Baction%5D=login&amp;tx_felogin_login%5Bcontroller%5D=Login&amp;cHash=9238b3d3ba4dbeb2c75d778a5cd1f17b" rel="nofollow noreferrer">https://my-domain-name.pl/login?tx_felogin_login%5Baction%5D=login&amp;tx_felogin_login%5Bcontroller%5D=Login&amp;cHash=9238b3d3ba4dbeb2c75d778a5cd1f17b</a></p>
<p>I know it is probably cause by third party extension like bootstrap (bk2k). But I don't believe I need to rewrite manual syntax in my mariadb. it's ridiculous.</p>
<p>Im checked requirements for this version of TYPO3. And my requirements are ok. Im checked my database (MariaDB) by mysqlcheck and all is ok. Checked version of MariaDB and its ok.</p>
<p>Im beginner in TYPO3 so please be understanding.</p>

## Answers
### Answer ID: 75048871
<pre><code>root@database-deb:/home/marlon# mysql -V
mysql  Ver 15.1 Distrib 10.7.3-MariaDB, for debian-linux-gnu (x86_64) using readline EditLine wrapper
</code></pre>
<p>I looked in wrong places. On TYPO3 site you can see:</p>
<blockquote>
<p>System requirements PHP 8.1 MariaDB 10.3+ / MySQL 8.0+ / PostgreSQL
10.0+ / SQLite 3.8.3+</p>
</blockquote>
<p>but if you see details:
<a href="https://i.sstatic.net/PTvZX.png" rel="nofollow noreferrer">Requirements on TYPO3 site</a></p>
<p>MariaDB &gt;= 10.3.0 &lt;= 10.6.99 <strong>is not the same</strong> MariaDB 10.3+</p>
<p>I guess, due to incompatible version of mariadb...</p>
<p>A few hours later... I create new one VM with older MariaDB.</p>
<pre><code>root@mariadb-10-6:/home/marlon# mysql -V
mysql  Ver 15.1 Distrib 10.6.11-MariaDB, for debian-linux-gnu (x86_64) using readline EditLine wrapper
</code></pre>
<p>Nothing changed. Still same error.</p>

