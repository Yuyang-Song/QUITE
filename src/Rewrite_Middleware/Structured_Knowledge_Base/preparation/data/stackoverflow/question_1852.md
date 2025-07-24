# Retrieve matched properties in Criteria query (like an explanation of the result)
[Link to question](https://stackoverflow.com/questions/10226755/retrieve-matched-properties-in-criteria-query-like-an-explanation-of-the-result)
**Creation Date:** 1334833757
**Score:** 0
**Tags:** hibernate
## Question Body
<p>I'm using Hibernate in a project, and I have to search for Objects in the Database by inserting some constraints.
I want the search procedure to return a row containing the id of the Object, some information on childs entities and, most important, something describing why the row is present in the result, for example a list of pair (matched entity, matched property) including matched child.
I already did it in plain sql, and it's tedious. I think i would be able do do it using hibernate hql too, but it sounds like I'm rewriting the same thing, just in a slighty different language. My question is : There's a way do do it cleanly, using criteria, with as least sql query as possible?
I know that the question is very wide so notice that here I'm searching for advices, tips, best practice, not for complete implementations. Something we can elaborate on later to find a good solution...
Thank you in advance..</p>

## Answers
### Answer ID: 10332130
<p>there is query by example where you can give hibernate an example of the entities it should look for. maybe you could the compare the results with the example.</p>

<pre><code>Example example = Example.create(exampleobj)...; // add configs how to work with the example
Criteria crit = currentSession.createCriteria(Mitarbeiter.class).add(example);
</code></pre>

