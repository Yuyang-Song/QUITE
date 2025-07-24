# Generating a plain index of dynamic user pages?
[Link to question](https://stackoverflow.com/questions/7792982/generating-a-plain-index-of-dynamic-user-pages)
**Creation Date:** 1318850294
**Score:** 0
**Tags:** asp.net
## Question Body
<p>My site is a business directory. Different businesses on the site have subpages that can be accessed with a URL like <code>http://mysite.com/businessname</code>. Behind the scenes, I'm using url rewriting to point those subpages to a page like <code>http://mysite.com/businesspage.aspx?id=[businessIDGuid]</code>.</p>

<p>I want the business pages to appear in search engines, and to do that I need to create links to them. Users can find businesses using the search tool on my site, but this isn't usable by search engines.</p>

<p>I thought that I should create a flat index page, with the names of every business in my database, and a link to their subpage. However, there are lots of businesses in my database (around 160,000 at the moment) so I can't really put all of them on one page. Also, the obvious way to generate these pages - having an sql query called in the <code>page_load</code> method that pulls back a list of all businesses - would put quite a lot of load on the server. It would make sense to generate a page and cache it for a day or so, but I don't know how to do this while staying within the context of asp.net.</p>

<p>What is the best way to generate an index of user pages in asp.net?</p>

## Answers
### Answer ID: 7793757
<p>In summary, you need to generate a <a href="http://www.sitemaps.org/" rel="nofollow">sitemap</a> and submit it to corresponding search engine. </p>

<p>For large sites, generating and updating a single file sitemap will be tedious task - fortunately, you can break your sitemap into multiple files and search engines like google can take a <a href="http://www.google.com/support/webmasters/bin/answer.py?answer=71453" rel="nofollow">sitemap index</a> which can link to these sitemap files.</p>

<ul>
<li>So essentially, you need find a convenient way to break your
businesses into groups - you can use alphabetical ordering, business
categories, custom tags (or combination) to break them into smaller
groups (say few hundreds to couple of thousands into a single group).</li>
<li>Maintain one sitemap or page per group. Keep a table into your
database tracking each page/sitemap and the last updated date/time
for the same.</li>
<li>You cannot use ASP.NET code to maintain these pages - instead write a small .NET console (or windows forms) program to generate/update sitemaps. Schedule the program using Windows Scheduler (Tasks) to run periodically.</li>
<li>For example, you may run the program say every 15 minutes. The program would first check if there are site-maps that are to be generated (will happen first time). If yes then it will pick-up say 3-4 sitemaps and generated them. Add their entries into the log table.</li>
<li>If all pages are generated then you can start updating them. So again check for last updated pages, pick 3-4 that were updated first and build them again. </li>
<li>You have to adjust your scheduled period and number of pages to be generated/updated to cover entire sitemap in some target time-frame. For example, if you are running the program every 10 minutes from 8PM to 6AM every day and updates 10 site-maps per run then in a day, you will cover 600 sitemaps. If you have total 5000 sitemaps then your entire site-map will get refreshed approx every 8 days.</li>
</ul>

