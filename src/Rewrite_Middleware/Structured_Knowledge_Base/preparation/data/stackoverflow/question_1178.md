# Eloquent Eager Loading in Cursor (Lazy Collection)
[Link to question](https://stackoverflow.com/questions/62220385/eloquent-eager-loading-in-cursor-lazy-collection)
**Creation Date:** 1591375842
**Score:** 4
**Tags:** laravel, eloquent
## Question Body
<p>I'm trying to export a large number of records from my database, but I need relationship data in order to build the export correctly. Ideally I would be able to use <code>cursor()</code> to get a Lazy Collection, but that won't load the relationships. I can't load the relationship within a loop, because that will create N+1 queries, and this could be hundreds of thousands of additional queries, which is unacceptable.</p>

<p>Here's what "works" (but runs out of memory):</p>

<pre><code>Record::with('projects')-&gt;get()-&gt;map(function ($record) {
  dd($record); // Shows the `projects` relationship
});
</code></pre>

<p>But when I use <code>cursor()</code>...</p>

<pre><code>Record::with('projects')-&gt;cursor()-&gt;map(function ($record) {
  dd($record); // Does NOT show the `projects` relationship
});
</code></pre>

<p>Is there a way to get a lazy collection that includes a record's relationship? I have looked in the documentation and it's not clear. Other suggestions have been to use <code>chunk()</code> which is unfortunately not a possibility in this situation.</p>

<p>EDIT: I shouldn't say chunk isn't a possibility, but it's a very expensive re-write. Currently, the data is structured with a lot of variability. So in order to construct the CSV for export, I need (for example) a header for the file. I currently grab that header by looping through all the records (the fields are stored in a JSONB field) and building out an array based on the fields present on those records.</p>

<p>I am also normalizing the data against those headers. So if one record has the field "address-1" but another record doesn't have that, the one that doesn't have it instead shows a blank value in the appropriate column. Otherwise, when inserting the row into the CSV, it doesn't respect the header.</p>

<p>These operations currently grab the entire data set and use a LazyCollection to map the header and normalize the records, and then feed it into the CSV one at a time. It would be ideal if I could grab relationships in a LazyCollection as well rather than having to rewrite the workflow.</p>

## Answers
### Answer ID: 62221100
<p>according to <a href="https://laravel.com/docs/7.x/eloquent#chunking-results" rel="noreferrer">this doc</a></p>

<p>cursor work in db stage, while loading relations come after method 'get' or 'first' ...</p>

<p>so: the code in cursor will work in db row represented as Model instance before the overall result, means that this code will run into db, without loading the relation, again db row (iterate through your database records...)</p>

<p>if you can't use chunk... then i think that you can use mySql to manage your data using <a href="https://laravel.com/docs/7.x/queries#raw-expressions" rel="noreferrer">raw-expressions</a> </p>

