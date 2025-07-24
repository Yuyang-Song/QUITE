# How does an api compare to directly querying your database
[Link to question](https://stackoverflow.com/questions/58833714/how-does-an-api-compare-to-directly-querying-your-database)
**Creation Date:** 1573636479
**Score:** 6
**Tags:** node.js, api, express, backend
## Question Body
<p>I am kind of confused about when an API is needed. I have recently created a mobile app with flutter and cloud firestore as the database where i simply queried and wrote to the database when needed. Now i am learning full stack web development and I recently watched a tutorial where he built like an Express API with GET, POST, and DELETE functionality for a simple item in the database. </p>

<p>Coming from a background where i just directly accessed the database i am not sure why an API in this case is necessary, is it so I wouldnt have to rewrite the queries every time? This is a very simple project so he's definitely not making a 3rd party api for other developers to use. Am i misunderstanding what an API does exactly? </p>

<p>It was really simple, there was one collection in a MongoDB database and he was using postman to read and write to and from the database to check if it works.</p>

## Answers
### Answer ID: 58871249
<p>Another most important factor is coupling. To add to @Dijkstra API provides a way to decouple the logic from each other, thus allowing for more application reliability, maintainability, fault-tolerance and if required scalability.</p>

<p>Thus there is no right or wrong here, or the comparison of API vs DB call is in itself not justified for the fact that <strong>fetching the data from Database is the ultimate aim</strong>. Even if you use a REST API or Query a database.</p>

<p>The means to achieve the same can differ based on specific requirements. For example, fetching water from the well. </p>

<ul>
<li>You can always climb down the well and fetch a bucket of water if you need 1 bucket per day and you are the only user.</li>
<li>But if there are many users you would want to install a pull and wheel where people use it to pour fetched water into their bucket, yet again this will depend if there are 100 users per day using or more than that. As this will not work in the case of more than 100 users.</li>
<li>IF the case is that an entire community of say 1000 user are going to need the water you would go with a more complex solution of installing a motorized water pump to pump out the water and supply it to the user's home via a pipeline. This solution has many benefits like fast supply, easy to use, filtered water, scheduled, etc. But the cost and effort to achieve the solution is higher as well.</li>
</ul>

<p>All in all, It comes down to the <strong>cost-vs-benefit ratio</strong> which you and only you can chart out, for different solutions vs the particular problem, as you are the best judge of scale and future user flow. </p>

<hr>

<p>While doing that you can ask the following question about the solution to help decide :</p>

<ul>
<li>Is the solution satisfying the primary requirement of the problem?</li>
<li>How much time is it going to take to build it?</li>
<li>For the time we spend to build a solution, is it going to working at more than 75% or more of its capacity?</li>
<li>If not is there a simpler solution that I can use to satisfy the problem and scale it as the requirement increases?</li>
</ul>

<p>HTH.</p>

### Answer ID: 58835718
<p>In your case, you are using a pre-written SDK which knows how to connect to Firestore, does caching and updates application data when needed, and provides a standard method of reading, writing and deleting data in Firestore (with associated documentation and example data from google).</p>

<p>Therefore, using an API (as described for the mongoDB) is not required and is undesirable.</p>

<p>There are some cases where you might want to have no read or write access to a firestore collection or document, and in this case, you could write a cloud function which your app calls with parameters, that receives the data that you want to write and does some sort of checking or manipulation beyond the capabilities of cloud firestore rules (although these can get pretty sophisticated). See <a href="https://firebase.google.com/docs/firestore/security/get-started" rel="nofollow noreferrer">https://firebase.google.com/docs/firestore/security/get-started</a> </p>

<p>Todd (in the video contained in this link) does a few good videos on this subject.</p>

<p>However, this is not really working in the same was as the API you mentioned in your question.</p>

<p>So in the case of using Firestore, you should use the SDK and not re-invent the wheel by creating your own API.</p>

<p>If you want to share photos for example, you can also store them in firebase storage and then provide a URL for other devices to access them without your app being installed.</p>

<p>If you want to write something to firestore which is then sent to all other users then you can use listeners on each app, and the data will be sent to the apps after it arrives at Firestore.</p>

<p><a href="https://firebase.google.com/docs/firestore/query-data/listen" rel="nofollow noreferrer">https://firebase.google.com/docs/firestore/query-data/listen</a> gives an overview of this.</p>

<p>One thing to always look at with firebase is the cost of doing anything. Cloud functions cost more than doing a read of a firestore document.</p>

<p>This gives an overview of pricing for different capabilities within the firebase set of capabilities.</p>

<p><a href="https://firebase.google.com/pricing" rel="nofollow noreferrer">https://firebase.google.com/pricing</a></p>

### Answer ID: 58833976
<p>May be for you, an API is not necessary. But, the use-cases of an API is a lot.</p>

<p>For example:</p>

<ul>
<li>You don't have to write business logic for every platform. (iOS, Android, Web, Whatever)</li>
<li>Your app will be lightweight since some computation would be offloaded to server. </li>
<li>Your app can be reverse engineered to get secret informations. (or, Your secret algorithm may be?)</li>
<li>What if you need to store something in filesystem that you want share with others?</li>
</ul>

<p>Also a good read: <a href="https://stackoverflow.com/questions/5320003/why-we-should-use-rest">Why we should use REST?</a></p>

### Answer ID: 58833885
<p>API is a standard way with which your front-end (web/mobile) stores/gets information for your application. Your front-end can/should not directly access database ever. Understand the purpose of front-end which is to just display the interface and should do minimal processing. All the application logic should be at your backend (API server) which is exposed to your frontend via API (GET, POST etc) calls. So to store an item in your database, you will write data storing logic in your backend, and expose an API end-point which when triggered will perform the storing operation. That API call should be used by your front-end to trigger the storing process. In this way your logic of storing/database or any other thing is not exposed, only the API URL is. The purpose of front-end is to be exposed whereas backend/database should never be exposed and used from front-end</p>

