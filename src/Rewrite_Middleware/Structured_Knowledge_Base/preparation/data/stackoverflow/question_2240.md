# mysql encryption at rest
[Link to question](https://stackoverflow.com/questions/25553507/mysql-encryption-at-rest)
**Creation Date:** 1409242747
**Score:** 1
**Tags:** mysql, encryption
## Question Body
<p>I have a mysql database that connects with both a web based php application and a FoxPro application (yes, foxpro).  Working on this after a previous "developer" was fired.</p>

<p>Anyway, I'm familiar with the AES_Encrypt functions, but using this would involve pretty much rewriting all queries in both applications, I'm looking to avoid this if possible.  Just wondering if there are any reasonably priced/open source 3rd party methods/software that will encrypt an entire mysql database at rest on windows server. </p>

<p>I see this <a href="http://www.netlib.com/mysql-encryption.asp" rel="nofollow">http://www.netlib.com/mysql-encryption.asp</a>  but it's a large price tag.  (Yes, it needs to be HIPAA level, non-profit healthcare)</p>

<p>Any suggestions?</p>

## Answers
### Answer ID: 69637242
<p>Consider upgrading to MySql 8 which already comes with Data-At-Rest Encryption. Alternatively, you can upgrade to MaridaDB 10.4.</p>
<p>Won't cost you a penny.</p>
<p>You can encrypt any InnoDB table, and once set up it's entirely transparent. All your queries will work exactly the same as before, except the data is encrypted before save and decrypted after retrieval.</p>
<p>I can not say if it's &quot;HIPAA level&quot; or what not, but it uses AES-256 encryption. We're looking at it now to get SOC2 certification.</p>
<p><a href="https://dev.mysql.com/doc/refman/8.0/en/faqs-tablespace-encryption.html" rel="nofollow noreferrer">https://dev.mysql.com/doc/refman/8.0/en/faqs-tablespace-encryption.html</a></p>

