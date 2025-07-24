# How do I rewrite URLs with Nginx admin / Apache / Wordpress
[Link to question](https://stackoverflow.com/questions/9626486/how-do-i-rewrite-urls-with-nginx-admin-apache-wordpress)
**Creation Date:** 1331248067
**Score:** 0
**Tags:** apache, wordpress, url-rewriting, nginx
## Question Body
<p>I have the following URL format:</p>

<pre><code>www.example.com/members/admin/projects/?projectid=41
</code></pre>

<p>And I would like to rewrite them to the following format:</p>

<pre><code>www.example.com/avits/projectname/
</code></pre>

<p>Project names do not have to be unique when a user creates them therefore I will be checking for an existing name and appending an integer to the end of the project name if a project of the same name already exists. e.g. example.project, example.project1, example.project2 etc.</p>

<p>I am happy setting up the GET request to query the database by project name however I am having huge problems setting up these pretty url's.</p>

<p>I am using Apache with Nginx Admin installed which mens that all static content is served via Nginx without the overhead of apache.</p>

<p>I am totally confused as to whether I should be employing an nginx rewrite rule in my nginx.conf file or standard rewrites in my .htaccess file.</p>

<p>To confuse matters further although this is a rather large custom appliction it is build on top of a wordpress backbone for easy blogging functionality meaning that I also have the built in wordpress rewrite module at my disposal.</p>

<p>I have tried all three methods with absolutely no success.  I have read a lot on the matter but simply cannot seem to get anything to work.  I am certain this is purely down to a complete lack of understanding on with regards to URL rewriting.  Combined with the fact that I don't know which type of rewriting should be applicable in my case means that I am doing nothing more than going round in circles.</p>

<p>Can anyone clear up this matter for me and explain how to rewrite my URLs in the manner described above?</p>

<p>Many thanks.</p>

## Answers
### Answer ID: 9681900
<p>If you are proxying all the non static file requests to Apache, do the rewrites there - you don't need to do anything on nginx as it will just pass the requests to the back end.</p>

<p>The problem with what you are proposing is that it's not actually a rewrite, a rewrite is taking the first URL and just changing it around or moving the user to another location.</p>

<p>What you need actually takes logic to extrapolate the project name from the project ID.</p>

<p>For example you can rewrite:</p>

<pre><code>www.example.com/members/admin/projects/?projectid=41
</code></pre>

<p>To:</p>

<pre><code>www.example.com/avits/41/
</code></pre>

<p>Fairly easily, but can you map that /41/ in your app code to change it to /projectname/ - because a URL rewrite can't do that.</p>

