# My Dialogflow + Firebase bot does not pull data from Bigquery
[Link to question](https://stackoverflow.com/questions/59646945/my-dialogflow-firebase-bot-does-not-pull-data-from-bigquery)
**Creation Date:** 1578490130
**Score:** 0
**Tags:** node.js, google-bigquery, dialogflow-es
## Question Body
<p>I have built a bot in dialogflow and followed the guidelines for integrating it with a BigQuery database as outlined in <a href="https://medium.com/google-cloud/deconstructing-chatbots-how-to-integrate-dialogflow-with-bigquery-267b68f4e795" rel="nofollow noreferrer">Deconstructing Chatbots</a>, <a href="https://cloud.google.com/bigquery/docs/parameterized-queries" rel="nofollow noreferrer">BigQuery Docs on Parameterized Queries with Node.JS</a> and <a href="https://codelabs.developers.google.com/codelabs/cloud-dialogflow-bqml/index.html?index=..%2F..index#4" rel="nofollow noreferrer">Helpdesk Chatbot  with BigQuery</a></p>

<p>The call to BigQuery is made within an async function '<strong>queryParamsArrays()</strong>' which appears to be the problem based on the Firebase Logs. </p>

<p>I updated the package.json with "engines: 8" and  /* jshint esversion: 8 */  in the index file to override the error. Going off the BigQuery docs, I thought this might work. The desired behavior is that a list of wines is retrieved from the database and presented randomly to the end user. Instead I see the SQL query text generated and the list_wines function (whuch calls the async) completes without substituting any values in. </p>

<p>I am going to try rewriting the async as a promise function. Can anyone tell me if I am on the right track? I'm new to javascript and trying to push through it.</p>

<h3>index.js</h3>

<pre><code>     // See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
     // for Dialogflow fulfillment library docs, samples, and to report issues
    'use strict';

    /* jshint esversion: 8 */


    const functions = require('firebase-functions');
    const {WebhookClient} = require('dialogflow-fulfillment');
    const {Card, Suggestion} = require('dialogflow-fulfillment');
    const {google} = require('googleapis');
    const BIGQUERY = require('@google-cloud/bigquery');

    process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

    exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) =&gt; {
      const agent = new WebhookClient({ request, response });
      console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
      console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
      console.log("Parameters", agent.parameters);

      function getPair(agent) {
        // Return wines that pair well with the food or meet other user specified params

        const results= list_wines(agent);
        agent.add('${results[0].name} is a good choice for ${results[0].food_pairing}. A ${results[1].variety} like ${results[1].name} also works!');
      }

      // Run the proper function handler based on the matched Dialogflow intent name
        let intentMap = new Map();
        intentMap.set('findPair', getPair);
        agent.handleRequest(intentMap);
    });

    function list_wines(agent) {
      // Search the database for parameters 
      // Actual values have been removed for presentation

      const projectId = 'my_project_id';
      const datasetId = "my_dataset_id";
      const tableId = "my_table_id";

      const bigquery = new BIGQUERY({
        projectId: projectId
      });

      const params= agent.parameters;
      const excluded= agent.excluded;

      const name = agent.parameters.label;
      const variety = agent.parameters.variety;
      const food_pairing = agent.parameters.foods;
      const conditions = agent.parameters.conditions;

      // Map param columns to those in the BigQuery database
      const SQL_COLUMN_LABELS={label:'name', variety:'variety', foods:'food_pairing', conditions:'food_pairing'};

      var txt = "SELECT *, RANK() OVER(PARTITION BY food_pairing ORDER BY variety) as cat_count FROM \'my_project_id.my_dataset_id.my_table_id\'";

      var x;
      var filters=[];

      // Loop through params to add search params to the SQL query removing blank arrays and empty text
      // Also handles arrays with a single value or multiple values

      for (x in params) {
        // Correctly checking for Array
        if(!Array.isArray(params[x]) &amp; params[x].length&gt;1 ){
          // If the value is text we can reference it in the query with @
          filters = filters.concat(SQL_COLUMN_LABELS[x] + "= @" + x);
        } else{
          switch(params[x].length) {
              default:
                // Array with more than one value
                filters=filters.concat(SQL_COLUMN_LABELS[x] + " IN UNNEST(@" + x +")");
                break;
              case 1:
                // Array with one value - get the actual value
                filters = filters.concat(SQL_COLUMN_LABELS[x] + "= '" + params[x] +"'");
                break;
              case 0:
                // Empty Array
                break;
          } 
        }
      }

      txt += " WHERE " + filters.join(" AND ");

      // Prints output(the SQL query) to console
      console.log(txt);

      // This async function is supposed to query the database but it doesn't get called. 
      // list_wines completes and returns text without results

      async function queryParamsArrays() {

        console.log('calling queryParamsArrays');

        const sqlQuery = txt +';';

        console.log("SQL Query", sqlQuery);

        const options = {
          query: sqlQuery,
          // Location must match that of the dataset(s) referenced in the query.
          location: 'US',
          params: params,
                };
        try{
           // Run the query returning an array of objects
            const [rows] = await bigquery.query(options);

            console.log('Rows:');
            rows.forEach(row =&gt; {
              console.log(row)
            });


            // Pick ten results at random by shuffling rows
            const shuffled = rows.sort(() =&gt; 0.5 - Math.random());

            // Get sub-array of first 10 elements after shuffled
            let selected = shuffled.slice(0, 10);

            // Return selected 
            return selected;

        } catch(e) {
          console.log(e);
        }
      }
    }
</code></pre>

<h3>package.json</h3>

<pre><code>    {
      "name": "dialogflowFirebaseFulfillment",
      "description": "This is the default fulfillment for a Dialogflow agents using Cloud Functions for Firebase",
      "version": "0.0.1",
      "private": true,
      "license": "Apache Version 2.0",
      "author": "Google Inc.",
      "engines": {
        "node": "8"
      },
      "scripts": {
        "start": "firebase serve --only functions:dialogflowFirebaseFulfillment",
        "deploy": "firebase deploy --only functions:dialogflowFirebaseFulfillment"
      },
      "dependencies": {
        "actions-on-google": "^2.2.0",
        "firebase-admin": "^5.13.1",
        "firebase-functions": "^2.0.2",
        "dialogflow": "^0.6.0",
        "dialogflow-fulfillment": "^0.5.0",
        "@google-cloud/bigquery": "^0.12.0"
      }
    }              
</code></pre>

## Answers
### Answer ID: 59897438
<p>I fixed this issue. Here's where I went wrong:</p>

<ol>
<li>return queryParamsArrays(); within the list_wines function. I forgot a crucial step which was a rookie mistake. You can put this in the code after the async function ends</li>
<li>you cannot pass params as DialogFlow provides it to params as defined within options. You have to clean that up as DF doesn't do a good enough job</li>
<li>string literals - I did not notice that the code I was borrowing from used backticks instead of single quotes. This fixed issues where the codes was to substitute parts of a string with the results from the query. </li>
</ol>

