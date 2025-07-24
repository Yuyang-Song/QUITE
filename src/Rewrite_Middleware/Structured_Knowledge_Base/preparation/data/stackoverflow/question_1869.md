# In Android,how is a string or other variable type parsed?
[Link to question](https://stackoverflow.com/questions/10421036/in-android-how-is-a-string-or-other-variable-type-parsed)
**Creation Date:** 1335989944
**Score:** 0
**Tags:** java, android, parsing
## Question Body
<p>I'm querying my database to display the row based on the date column. I've got the method to function correctly, but I'm having to change the format of my date values in the database. Previously, I had the dates as yyyyMd which would get 201252 for today for example. Then I parsed the date into a Long and passed it into my method</p>

<pre><code>        String sd = hiddenDate.getText().toString();
    long aLong = Long.parseLong(sd);
    dba.open();
    String[] rScr = dba.getTodayMethod(aLong);
</code></pre>

<p>But I'm having to rewrite the date format into yyyy-M-y. Then the dashes in the date are breaking the "parseLong" I think. And it appears that just passing the sd variable into the getTodayMethod, like <code>String[] rScr = dba.getTodayMethod(sd);</code> doesn't work either. So what should I parse the String sd into to accomodate the dashes in the date? and how would that parse code be written?</p>

## Answers
### Answer ID: 10421096
<p>Fundamentally, you're doing the wrong thing by trying to parse it as a long to start with. It's not the textual representation of a 64-bit integer - it's the textual representation of a <em>date</em>. So use types that are to do with date/time.</p>

<p>Personally I like using <a href="http://joda-time.sf.net" rel="nofollow">Joda Time</a>, but if you're on Android that <em>may</em> be too big for you - in which case you'll have to use <a href="http://docs.oracle.com/javase/7/docs/api/java/util/Date.html" rel="nofollow"><code>java.util.Date</code></a> and <a href="http://docs.oracle.com/javase/7/docs/api/java/util/Calendar.html" rel="nofollow"><code>java.util.Calendar</code></a>, horrible though they are, and then use <a href="http://docs.oracle.com/javase/7/docs/api/java/text/SimpleDateFormat.html" rel="nofollow"><code>java.text.SimpleDateFormat</code></a> for the parsing. (Don't forget to set the locale and time zone appropriately...)</p>

