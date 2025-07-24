# Is it possible to trick ActiveRecord into understanding it has all the data it needs to create related models in memory?
[Link to question](https://stackoverflow.com/questions/35284066/is-it-possible-to-trick-activerecord-into-understanding-it-has-all-the-data-it-n)
**Creation Date:** 1454993097
**Score:** 1
**Tags:** ruby-on-rails-4, activerecord
## Question Body
<p>For a couple of years, I've worked to make a database that holds the data for an incredibly-complicated engineering process. Right now, it's served by an SQL Server database in Azure, with a WinForms (w/ DevExpress) client, and an Azure worker role for doing a couple of long-running processes which center on our main file format, and a library which operates on it. I've written a data-access library that's essentially a really crappy ORM. I'm tired of this architecture. All along, I've fantasized about rewriting the app in Rails. The app is pretty simple. The model is a nightmare.</p>

<p>I've written about the database schema and the central query of the application over at <a href="https://dba.stackexchange.com/questions/94046/subselect-of-maxversion-takes-many-minutes-though-there-are-only-20k-records">dba.stackexchange.com</a>, and the awesome answer I got there continues to be the strategy I use. It's still performant, even as we've added even more tables to the query.</p>

<p>For the 3rd time now, I'm playing around with trying to encapsulate this model in Rails. The main problem, as I understand how to articulate it, is that the query is essentially a "latest effective date" problem. I need to grab a list of items, by name, up to a certain revision number. For all the discussion I've read on joins and includes, I still don't know if it's even possible to do a "latest effective version number by name" query against my data. I guess it comes down to whether or not ActiveRecord can do this:</p>

<pre><code>SELECT n AS ROW_NUMBER() OVER (PARTITION BY p.Designation ORDER BY o.Version DESC)
</code></pre>

<p>(I also need to marry this versioned information with a separate query that correlates ownership with the various groups of calibrations, but I think I could sort out how to do this second part with AR if the first were possible.)</p>

<p>At this point, I've lifted my current working SQL from .NET and dropped it into my model in Rails, and I can use it to do something like <code>cal = Calibration.find_by_sql()</code>, and the Calibration objects are recognized just fine. My problem is that I need to pull a LOT of other models along with the main query.</p>

<p>I tried making sure that my find_by_sql() included all the foreign key columns for the relations I wanted to preload, and then used includes() for them, but this just doesn't work.</p>

<p>I've discovered <code>ActiveRecord::Associations::Preloader.new.preload(cal, :parameter)</code> (from <a href="http://cha1tanya.com/2013/10/26/preload-associations-with-find-by-sql.html" rel="nofollow noreferrer">here</a>). This is neat, but the initial query takes 1.7 seconds, and then the "preload" takes over 30 seconds, and trips my timeout. And I have 7 other relations to load.</p>

<p>Here's the rub: I've tried returning everything I care about in the find_by_sql(). It just takes a couple seconds, which is perfectly acceptable for this application. But even though I've returned all of the fields of all the models I care about, includes() still can't recognize that all the information is right there in the results of the query, ready to parse into instances of models in memory. Is is possible to "trick" ActiveRecord into doing this for me, or am I just stuck unmarshalling this data into instances of objects myself?</p>

<p>Perhaps there's nothing else for it but to create a PORO class that is the Frankenstein monster of all the munged-together fields I'm interested in, and deal with that as though it were the child of the other 9, database-backed tables, but I wanted to throw this out there in case someone could catch something I'm missing. (Or maybe I should create a <a href="http://railscasts.com/episodes/193-tableless-model?view=asciicast" rel="nofollow noreferrer">tableless model</a> so that I could still traverse the relationships.)</p>

