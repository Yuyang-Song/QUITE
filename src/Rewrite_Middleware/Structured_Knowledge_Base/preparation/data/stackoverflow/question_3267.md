# How do I add a default vote value to every user for every post in SQL?
[Link to question](https://stackoverflow.com/questions/74389762/how-do-i-add-a-default-vote-value-to-every-user-for-every-post-in-sql)
**Creation Date:** 1668086680
**Score:** 0
**Tags:** mysql, sql, express
## Question Body
<p>real newbie in programming here. I started learning SQL a few days ago and now I am building a really simple backend in Express JS for a simple database that looks a little bit like the schema.</p>
<p><a href="https://i.sstatic.net/ckfIn.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/ckfIn.png" alt="schema" /></a></p>
<p>There are users who can post posts and who can either upvote (+1) a post or downvote it (-1). With each vote, a record is added to the votes table. If the same user votes again on the same post, the vote will not be added, regardless if it is an upvote or a downvote. This is the query I am using for upvote, for example:</p>
<p><code>INSERT INTO votes (username, post_id, vote) SELECT 'jackie' , 4, 1 WHERE NOT EXISTS  (SELECT * FROM votes WHERE username = 'jackie' AND post_id = 4);</code></p>
<p>However, this is not really what I want because a user should be able to change their mind and downvote/upvote in case they voted differently. Therefore, I think it would be better if all the users had a default vote of 0 for each post, so I could rewrite the code for upvoting and downvoting as an UPDATE query instead.</p>
<p>Unfortunately, I am still not very good at SQL and I am not sure if it is even possible or how I would go about it. In my mind, it would look something like this even though it is obviously wrong and silly:</p>
<p><code>INSERT INTO votes (username, post_id, vote) VALUES ('jackie', (SELECT id FROM posts), 0);</code></p>
<p>Can anyone please help?</p>

