# What is the best practise for using a service in java threads?
[Link to question](https://stackoverflow.com/questions/54048224/what-is-the-best-practise-for-using-a-service-in-java-threads)
**Creation Date:** 1546652367
**Score:** 0
**Tags:** java, mongodb-java, java-threads
## Question Body
<p>I'm writing an application that will launch several threads - the amount varies per execution, but in general more than 5 and less than 100 - each of which will repeatedly read from a Mongo database. </p>

<pre><code>public class MyThread implements Runnable {
    private MyMongoClient myMongoClient = MyMongoClient.getInstance();

    public MyThread() {
    }

    @Override
    public void run() {
        Document myDocument = myMongoClient.getDocumentById("id");
        Document newDocument = new Document("id": "newId");
        myMongoClient.writeDocument(newDocument);
    }
}
</code></pre>

<p>I have an existing singleton service class to query and update Mongo, and would like any advice on patterns to follow for using it in the threads?</p>

<pre><code>public class MyMongoClient {
    private static MyMongoClient INSTANCE = new MyMongoClient();
    private myCollection; 

    private MyMongoClient() {
        try (MongoClient mongoClient = new MongoClient(host)) {
            MongoDatabase db = mongoClient.getDatabase("myDatabase");
            myCollection = db.getCollection("myCollection");
        } 
    }

    public static MyMongoClient getInstance() {
        return INSTANCE;
    }

    private Document getObjectById(String id) {
        // Implementation
    }

    private write writeDocument(Document document) {
        // Implementation
    }    
}
</code></pre>

<p>As shown, each thread will read from existing entries, but not update any of them, and will write new entries using the same service</p>

<p>Should each thread use the same instance of the service, or should I rewrite the service so that each thread has its own instance?</p>

## Answers
### Answer ID: 54048745
<p>You can use <code>ThreadPoolExecutor</code>. It handles everything, you just submit task to the pool.</p>

<p>In my sample, <code>keepAliveTime=10</code> secs, its value depends on your requirements.</p>

<pre><code>ExecutorService threadPoolExecutor = new ThreadPoolExecutor(
            5,
            100,
            10,
            TimeUnit.SECONDS,
            new LinkedBlockingQueue&lt;Runnable&gt;()
    );
</code></pre>

<p>See the Oracle <a href="https://docs.oracle.com/javase/tutorial/essential/concurrency/executors.html" rel="nofollow noreferrer">Tutorial on the Executors</a> framework. </p>

### Answer ID: 54048340
<p>You're going to get an error because you close your <code>MongoClient</code> in that constructor.  <code>MongoClient</code> has a built in connection pool so there's no reason to create more than one.  Create just the one and share it amongst your threads.</p>

