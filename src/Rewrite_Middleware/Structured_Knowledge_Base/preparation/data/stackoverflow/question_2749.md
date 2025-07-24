# Autosuggestion and ajax calls
[Link to question](https://stackoverflow.com/questions/50782634/autosuggestion-and-ajax-calls)
**Creation Date:** 1528625540
**Score:** 0
**Tags:** jquery, ajax
## Question Body
<p>I am working with the autosuggestion search. The problem is I have a "keyup" event that sends an ajax request to the database on the change of the search query term.
From time to time it happens that user quickly changes those search query terms. 
What I mean by that: </p>

<p>1) User enters "123" -> an ajax request to the database is sent.
2) Right after that, very rapidly, he decides to drop '3' from "123" -> a new ajax request with "12" as a new search query is sent to the database. 
The second request fetches the data faster than the first one. And this leads to the situation when the search query remains correct, but the list of found products is not as first request with its fetched data rewrites the second one. 
It should be vice verse. </p>

<p>Please, help me come up with some ideas on how I can, like, synchronize those two request</p>

<p>Kind regards! </p>

