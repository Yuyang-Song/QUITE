# React Apollo - Strange Effect When Making Mutation?
[Link to question](https://stackoverflow.com/questions/52789125/react-apollo-strange-effect-when-making-mutation)
**Creation Date:** 1539399389
**Score:** 1
**Tags:** reactjs, promise, graphql, apollo, react-apollo
## Question Body
<p>I've set up a React application with React-Apollo and can successfully query my API.</p>

<p>However, when I make a mutation, a strange effect occurs. I get all the data back successfully (as seen in the Network tab of the Chrome Dev Tools), but when trying to <code>console.log</code> the data, it says that it is <code>null</code>.</p>

<p>Here's the relevant code:</p>

<pre><code>// mutation file

import gql from "graphql-tag";
export default gql`
  mutation CreateReservation($name: String!, $time: String!, $persons: String, $specialMessage: String, $email: String!) {
    createReservation(input: {
        name: $name,
        time: $time,
        persons: $persons,
        specialMessage: $specialMessage,
        email: $email
    }) {
        __typename
        error
        data
    }
  }
`;

// component file

import React from "react";
import {graphql, compose} from "react-apollo";
import CreateReservationMutation from "../../graphql/mutations/api/CreateReservation";

class Reservations extends React.Component {
testGraphQL = ({ reservationName, reservationTime, reservationEmail, reservationPartySize, reservationMessage}) =&gt; {

    const variables = {
        name: reservationName,
        time: reservationTime,
        persons: reservationPartySize,
        specialMessage: reservationMessage,
        email: reservationEmail
    };

    this.props.createReservation(variables)
    .then(({data}) =&gt; {
        console.log("Data received: ", data); // Here is the problem
    }).catch((err) =&gt; {
        console.log("Error sending data: ", err);
    })
}
render() {
    return (
        &lt;div&gt;
            ...
            &lt;div&gt;
                &lt;Form 
                    ...
                    submitFunc={this.testGraphQL}
                /&gt;
            &lt;/div&gt;
            ...
            &lt;/div&gt;
        &lt;/div&gt;
    )
  }
}

export default compose(
    graphql(CreateReservationMutation, {
        props: ({mutate}) =&gt; ({
            createReservation: (variables) =&gt; mutate({variables})
        })
    })
)(Reservations);
</code></pre>

<p>So when I call the <code>testGraphQL</code> function, I receive the following in the console: </p>

<pre><code>Data received:  {createReservation: null}
</code></pre>

<p>But when looking in the Network tab, I see that the data is actually there after all and is exactly what I am looking for. Furthermore, my database is correctly updated with all the reservation details, so I know with certainty that the mutation is being executed. </p>

<p>This is what I see from the Network tab:</p>

<pre><code>{"data":{"createReservation":{"__typename":"ReservationResponse","error":null,"data":"Success"}}}
</code></pre>

<p>That is what I expect to see when I call <code>console.log</code> in <code>testGraphQL</code>.</p>

<p>So I know that I don't have any errors with my schema, my Apollo Client, or my mutation file.</p>

<p>Instead, the problem has to lie with how I'm setting up my <code>compose</code> statement or with how I'm calling the mutation itself.</p>

<p>Please let me know if you spot the error here. Thank you</p>

<p><strong>UPDATE</strong></p>

<p>I should mention that I am using AWS AppSync as my GraphQL provider.</p>

<p>The mutation calls a lambda function which does the following:</p>

<pre><code>...
Promise.all([dynamodbPromise, snsPromise, sesPromise])
    .then((data) =&gt; {
        callback(null, {data: "Success"});
    })
    .catch((err) =&gt; {
        callback(null, {error: err});
    });
</code></pre>

<p>Here is my resolver for this mutation:</p>

<pre><code>// request mapping template

{
  "version" : "2017-02-28",
  "operation": "Invoke",
  "payload": $util.toJson($ctx.args.input)
}

//  response mapping template

$util.toJson($context.result)
</code></pre>

<p><strong>UPDATE 2</strong></p>

<p>Configuring an <code>optimisticResonse</code> and rewriting my mutation like this:</p>

<pre><code>this.props.createReservation({
        variables,
        optimisticResponse: {
            createReservation: {
                __typename: "ReservationResponse",
                errorMessage: null,
                responseMessage: "_TEST_"
            }
        }
    })
    .then(res =&gt; {
        console.log("Apllo Data: ", res);
    })
</code></pre>

<p>Leads me to get only the data from the optimistic response, which is this:</p>

<pre><code>{data:
  createReservation: {
    __typename: "ReservationResponse", 
    errorMessage: null, 
    responseMessage: "Optimistic Success"
}
</code></pre>

<p>So the data returned must not be updated with the actual response from the API.</p>

<p>How can I now force Apollo to update the response after returning the optimistic response?</p>

## Answers
### Answer ID: 58142139
<p>you can access the returned properties just by useing <strong>res.data</strong></p>

<pre><code>this.props.createReservation({
    variables,
    optimisticResponse: {
        createReservation: {
            __typename: "ReservationResponse",
            errorMessage: null,
            responseMessage: "_TEST_"
        }
    }
})
.then(res =&gt; {
    console.log("Apllo Data: ", res.data);
})
</code></pre>

### Answer ID: 52796888
<p>I finally solved it, though the solution is less than ideal.</p>

<p>I had to write an update function for my mutation. This is a barebones implementation that eventually gives me the actual data from the API:</p>

<pre><code>this.props.createReservation({
        variables,
        optimisticResponse: {
            createReservation: {
                __typename: "ReservationResponse",
                errorMessage: null,
                responseMessage: "Optimistic Success"
            }
        },
        update: (proxy, {data: {createReservation}}) =&gt; {
            console.log("Update: ", createReservation);
        }
    })
    .then(res =&gt; {
        console.log("Apllo Data: ", res);
    })
</code></pre>

<p>The update function gets called three times. The first two fire before the promise is resolved and include the data from the <code>optimisticResponse</code> as shown in my "Update 2" section. The third call finally returns the actual data from the API.</p>

<p>While this will work for now, please let me know if there is a more direct method here. In this case, I don't want the <code>optimisticResponse</code> returned at all. I only want the actual data from my API to be returned. This way I can give my users proper error handling in the event something goes wrong.</p>

<p>Thank you, and I hope that we can help other people that have this issue.</p>

### Answer ID: 52792328
<p>You have two options to get the data response from a mutation:</p>

<p>In the Mutation component:</p>

<pre><code>&lt;Mutation&gt;{mutation, {data}}&lt;/Mutation&gt;
</code></pre>

<p>Or in the mutation function:</p>

<pre><code>mutate().then(data =&gt; ...)
</code></pre>

<p>You are getting in the mutate promise response, but you are expecting the state object that apollo pass to the Mutation component.</p>

<p>It doesn't make sense for apollo to pass the state object, because if the mutation resolved it was successful, any error will make the promise to be rejected and no loading state is provided during the mutate call.</p>

<p>So to fix your code, you just need to change this</p>

<pre><code>this.props.createReservation(variables)
    .then(data =&gt; {
</code></pre>

