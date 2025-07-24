# Integrating multiple system with graphql and postgres
[Link to question](https://stackoverflow.com/questions/76047100/integrating-multiple-system-with-graphql-and-postgres)
**Creation Date:** 1681836075
**Score:** 1
**Tags:** postgresql, graphql, hasura, system-design, multi-database
## Question Body
<p>Application is built using graphql (hasura), postgres and nodejs. The app gets deployed to each clients separately having different DB and so on. Currently, we need to make connection to different clients, so they can access each other DB.</p>
<p>One architecture which makes sense is mesh where multiple clients can connect across each other. So there are basically 3 things which needs to be implemented: <code>Query, Mutation and Subscription</code>.</p>
<p>I am trying to merge the results of the query fetching from all the clients when the request is triggered. This works but, is there any good way so I don't need to rewrite each and every custom query and mutation in hasura to handle multiple requests combing all the results.
Same approach for mutation but redirecting the request to particular client.</p>
<p>Maybe a good way to do in Database itself combining multi DB? Or is there any good high level design which solves this problem?</p>

## Answers
### Answer ID: 76114531
<p>There are a three different approaches for integrating multiple systems:</p>
<ol>
<li><p>Hasura Remote Schemas that allows you to merge multiple GraphQL schemas into one unified schema: <a href="https://hasura.io/docs/latest/remote-schemas/overview/" rel="nofollow noreferrer">https://hasura.io/docs/latest/remote-schemas/overview/</a></p>
</li>
<li><p>GraphQL Federation is an architecture pattern that allows you to build a unified API across multiple services. Apollo Federation, for example, is a popular implementation of this pattern.</p>
</li>
<li><p>Connect multiple PostgreSQL databases to a single Hasura instance.</p>
</li>
</ol>

