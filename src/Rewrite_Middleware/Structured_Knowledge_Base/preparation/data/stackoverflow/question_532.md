# meteor: how to filter local collection by date
[Link to question](https://stackoverflow.com/questions/30192346/meteor-how-to-filter-local-collection-by-date)
**Creation Date:** 1431437301
**Score:** 1
**Tags:** date, meteor, find
## Question Body
<p>I have a subscribed collection <code>entries</code> which consists of entries with a type attribute (e.g. "post" or "article") and two dates for availability (<code>available_from</code> and <code>available_to</code>). These entries are uploaded into the database via a RESTful API and the values for <code>available_from</code> and <code>available_to</code> are stored as <code>ISODates</code> in the form</p>

<p><code>"available_to" : ISODate("2017-06-01T00:00:00Z")</code></p>

<p>The problem is that once I try to do a search (values are fetched from a form and a search hash is created in the following manner) it comes up empty:</p>

<pre><code>"click #search-trigger": -&gt;
  $entry_type = $('#fullsearch-entry-type').val()
  $from = Date.create(moment($('#fullsearch-from').val(), "DD.MM.YYYY").format())
  $to = Date.create(moment($('#fullsearch-to').val(), "DD.MM.YYYY").format())

  searchHash =
    available_from:
      $gte: $from
    available_to:
      $lte: $to
    entry_type: $entry_type

  console.log searchHash
  console.log typeof $from
  console.log typeof $to

  console.log Entry.find(searchHash).fetch()
</code></pre>

<p>The dates are converted to the correct date object (since the value in the input field is in the form of DD.MM.YYYY and would otherwise be just a string if I'm assuming correctly) with SugarJS.</p>

<p>I tried different variants of rewriting the date values, left out one of the two dates or to leave out my search hash and enter the query options by hand into the <code>find()</code> query but to no avail. I hope someone can point me in the right direction because I'm already pulling my hair out over this :)</p>

## Answers
### Answer ID: 31201208
<p>As mwarren stated, the problem was Sugar + moment - once I went a few steps back and stuck to plain JS date, my problems went away.</p>

