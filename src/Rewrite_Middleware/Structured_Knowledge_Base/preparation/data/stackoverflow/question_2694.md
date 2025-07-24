# Correct way to update frontend when backend changes
[Link to question](https://stackoverflow.com/questions/47801883/correct-way-to-update-frontend-when-backend-changes)
**Creation Date:** 1513198137
**Score:** 5
**Tags:** node.js, postgresql, reactjs, express, knex.js
## Question Body
<p>I'm currently setting up the following application:</p>

<ul>
<li>Node backend with Express</li>
<li>Postgres DB with Knex as an interface</li>
<li>React frontend</li>
</ul>

<p>Everything is working as intended and I am making good progress, my question is more architectural:</p>

<p><strong>What is the preferred/recommended/best way to notify the frontend when database changes occur?</strong></p>

<p>I saw that Postgres has a <code>LISTEN/NOTIFY</code> feature but that is not currently (ever) supported by Knex (<a href="https://github.com/tgriesser/knex/issues/285" rel="noreferrer">https://github.com/tgriesser/knex/issues/285</a>).</p>

<p>My thoughts:</p>

<ul>
<li>Polling (every x seconds query the DB). This seems wasteful and antiquated but it would be easy to set up.</li>
<li>Sockets. Rewrite all my Express endpoints to use sockets? </li>
<li>?</li>
</ul>

<p>I'm interested to see how others handle this.</p>

<p>Thanks!</p>

## Answers
### Answer ID: 47802556
<p>I've had a similar situation before. I have a front end which connects via web sockets to the API. The API emits a message on successful database commit with the API endpoint matching the update. The front end components listen for these update socket messages and if the updated type is relevant to that component the component will query the API endpoint over https for the new data. Using a web socket only to advertise that an update is available won't necessitate rewriting the entire API.</p>

