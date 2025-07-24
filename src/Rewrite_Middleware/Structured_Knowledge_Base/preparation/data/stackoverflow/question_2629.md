# Azure Search Index - manage indexer for when database is erase/replace every 24 hours?
[Link to question](https://stackoverflow.com/questions/43600576/azure-search-index-manage-indexer-for-when-database-is-erase-replace-every-24)
**Creation Date:** 1493087235
**Score:** 1
**Tags:** azure, azure-cognitive-search
## Question Body
<p>We've set up an Azure Search Index on our Azure SQL Database of ~2.7 million records all contained in one Capture table.  Every night, our data scrapers grab the latest data, truncate the Capture table, then rewrite all the latest data - most of which will be duplicates of what was just truncated, but with a small amount of new data.  We don't have any feasible way of only writing new records each day, due to the large amounts of unstructured data in a couple fields of each record.</p>

<p>How should we best manage our index in this scenario?  Running the indexer on a schedule requires you to indicate this "high watermark column."  Because of the nature of our database (erase/replace once a day) we don't have any column that would apply here.  Further, what really needs to happen for our Azure Search Index is either it also needs to go through a full daily erase/replace, or some other approach so that we don't keep adding 2.7 million duplicate records every day to the index.  The former likely won't work for us because it takes 4 hours minimum to index our whole database.  That's 4 hours where clients (worldwide) may not have a full dataset to query on.  </p>

<p>Can someone from Azure Search make a suggestion here?</p>

## Answers
### Answer ID: 43600641
<p>What's the proportion of the data that actually changes every day? If that proportion is small, then you don't need to recreate the search index. Simply <code>reset</code> the indexer after the SQL table has been recreated, and trigger reindexing (resetting an indexer clears its high water mark state, but doesn't change the target index). Even though it may take several hours, your index is still there with the mostly full dataset. Presumably if you update the dataset once a day, your clients can tolerate hours of latency for picking up latest data. </p>

