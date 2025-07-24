# Kmeans implementation in Shiny
[Link to question](https://stackoverflow.com/questions/56946542/kmeans-implementation-in-shiny)
**Creation Date:** 1562654055
**Score:** 0
**Tags:** r, shiny
## Question Body
<p>I have a code that do kmeans on text data. It has about 160 lines of code. My main goal is to query a database with the data provided by the user and then conduct on these text kmeans. </p>

<p>The table output of the data queried by the user is working. Now I would like to rewrite the code to shiny. </p>

<pre><code># Here is the data that is provided by the query
query &lt;- reactive({
    query &lt;- get_sql_query(input$key)
    query_data &lt;- dbGetQuery(con, query)
  })

  word_extract &lt;- function(x) unlist(strsplit(x, "[[:space:]]|(?=[.!?*-])", perl = TRUE))

eng.reviews &lt;- reactive({
      data &lt;- query()
      data &lt;- as.data.frame(data)
      eng.reviews &lt;- data[,3]
    })

eng.reviews.list &lt;- reactive({
    eng.reviews &lt;- eng.reviews()
    eng.reviews.list &lt;- list()
    for (i in 1:nrow(eng.reviews)) {
      z &lt;- word_extract(tolower(as.character(eng.reviews[i,1])))
      eng.reviews.list[[i]] &lt;- z
    }
  })
</code></pre>

<p>Can I use in this case reactive? Next I create VectorSource, Corpus, tm_map, DocumentTermMatrix, dist.matrix.jaccard but I do this in one code snippet which not works in Shiny.</p>

