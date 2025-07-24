# Spring Boot - Pass parameter into REST API via Request Body (Post) that is not in the data model class (@Entity)
[Link to question](https://stackoverflow.com/questions/71469357/spring-boot-pass-parameter-into-rest-api-via-request-body-post-that-is-not-i)
**Creation Date:** 1647268052
**Score:** 0
**Tags:** java, spring, spring-boot, api, rest
## Question Body
<p>Would something like this be possible?  With previous REST API calls, I was able to use ObjectNode to accomplish this - I pass in my parameters via RequestBody, and just pull them out using objectNode.get (Not basing it on an Entity.)  But with my current situation, the Entity is already so large, I'd rather not rewrite it if I can help it.</p>
<p>It's sensitive information, so I don't want to use @RequestParams and pass it via URL.  One other idea may be to just add this new item to the Entity.  Then the problem is I have a native query that uses this Entity also...Would it be bad practice to add this new item to the query, and just set it to null since it's not actually in that database?</p>
<p>Hope that all makes sense, looking for any tips/best practices/options I'm missing.  Thanks!</p>

