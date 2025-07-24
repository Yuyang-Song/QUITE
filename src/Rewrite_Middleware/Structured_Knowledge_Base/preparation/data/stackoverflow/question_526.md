# Multiple Inserted Rows When They Shouldn&#39;t Be
[Link to question](https://stackoverflow.com/questions/29984088/multiple-inserted-rows-when-they-shouldnt-be)
**Creation Date:** 1430470707
**Score:** 0
**Tags:** php, mysql, pdo
## Question Body
<p>I'm working on an assignment from university where I need to create a task management system in PHP (users assign jobs to other users) and I keep getting an annoying bug which I can't quite figure out why it is happening.</p>

<p>First, I tried tracking which functions were being called to see if one of them got called twice and it was inserting the second row. Then I tried inserting a test row into the database without using all the classes who handle it. It still does it, so the problem won't be in the classes.</p>

<p>Here is the code I last used to test (the insert statement is the same as the one from the data mapper I'm using, only the values I've hardcoded for testing purposes):</p>

<pre><code>$sql = "INSERT INTO `jobs` (title, description, estimate, creator, responsible, lastEdit) VALUES ('".uniqid()."', 'some text', 48, 1, 2, NOW());";

// Note: I've already added the needed namespaces at the top of the page

$db = new \PDO('mysql:host=' . Config::get('mysql/host') .
            ';dbname=' . Config::get('mysql/db'),
            Config::get('mysql/username'),
            Config::get('mysql/password')
        );
$db-&gt;setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);

$query = $db-&gt;prepare($sql);

$query-&gt;setFetchMode(\PDO::FETCH_ASSOC);

$query-&gt;execute();
echo '&lt;pre&gt;';
var_dump($query);
echo '&lt;/pre&gt;';
die();
</code></pre>

<p>This code is inserting 2 rows (titles and ids are different) into the database.</p>

<p><strong>The interesting thing</strong> is that the var_dump shows that the query was the <strong>first</strong> entry. If the page is running multiple times, it should show the second entry or both.</p>

<p>I'm testing at the entry point of the app /public/index.php and there aren't any redirects or refreshes. I'm using a .htaccess document which rewrites the url (I'm using MVC for my site):</p>

<pre><code>Options -MultiViews
RewriteEngine On

RewriteBase /

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f

RewriteRule ^(.+) index.php?url=$1 [QSA,L]
</code></pre>

<p>Here is the create code for the jobs table:</p>

<pre><code>CREATE TABLE `jobs` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(50) NOT NULL,
    `description` TEXT NOT NULL,
    `status` ENUM('INPROGRESS','FINISHED') NOT NULL DEFAULT 'INPROGRESS',
    `estimate` INT(11) NOT NULL,
    `creator` INT(11) NOT NULL,
    `responsible` INT(11) NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `lastEdit` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    INDEX `job_creator_key` (`creator`),
    INDEX `job_responsible_key` (`responsible`),
    CONSTRAINT `job_creator_key` FOREIGN KEY (`creator`) REFERENCES `users` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT `job_responsible_key` FOREIGN KEY (`responsible`) REFERENCES `users` (`id`) ON UPDATE CASCADE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
</code></pre>

## Answers
### Answer ID: 29985327
<p>Your script is executed twice and I know why:</p>

<p>your .htaccess is redirecting all missing/404 files to index.php</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f

RewriteRule ^(.+) index.php?url=$1 [QSA,L]
</code></pre>

<p>all files like..... <strong>favicon.ico</strong></p>

<p>when you visit your site, browser is automatically trying to download favicon.ico. but its missing so request is redirected to index.php - that's why you are running index.php twice.</p>

<p>these kinds of bugs can be easily debugged in browser webdeveloper tools like firebug (tab "Network") so you can see all request to website. also you could check web server request log.</p>

