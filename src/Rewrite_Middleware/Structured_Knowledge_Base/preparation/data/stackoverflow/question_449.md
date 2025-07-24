# How to retain information queried from database
[Link to question](https://stackoverflow.com/questions/26783454/how-to-retain-information-queried-from-database)
**Creation Date:** 1415288548
**Score:** 1
**Tags:** sql, vb.net
## Question Body
<p>I am in the process of rewriting some old software. This process has been done before using a indexed collection to store the information that was queried from the database. Then later referenced by way of the indexed value. That's great and all, but the larger portion of this software that needs to be redone queries information from a table that uses two fields as a primary key.</p>

<p>Is there away for a collection to use two fields as an index?</p>

<p>Is there a work around if not?</p>

<p>Is there a better way to achieve the desired results than using a collection?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 26787056
<p>Yes but you will have to override the GetHashCode method of your class to something like this:</p>

<pre><code>Public Overloads Overrides Function GetHashCode() As Integer
    return Key1.ToString.GetHashCode() Xor Key2.ToString.GetHashCode()
End Function
</code></pre>

<p>The above code assumes Key1 and Key2 are your properties you want to makeup your uniqueness.</p>

