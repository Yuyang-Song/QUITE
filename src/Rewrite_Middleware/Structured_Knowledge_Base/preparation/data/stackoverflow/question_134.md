# NullPointerException on Matcher.appendEvaluated()?
[Link to question](https://stackoverflow.com/questions/14045354/nullpointerexception-on-matcher-appendevaluated)
**Creation Date:** 1356550735
**Score:** 0
**Tags:** java, android, optimization, nullpointerexception, matcher
## Question Body
<p>Here is the stack trace..........you will see "<em>removed</em>" a few times as well as in the code because I wish to keep my package private.</p>

<pre><code>java.lang.RuntimeException: Unable to start activity ComponentInfo{com.*removed*.*removed*/com.*removed*.*removed*.List}: java.lang.NullPointerException
at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:1768)
at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:1784)
at android.app.ActivityThread.access$1500(ActivityThread.java:123)
at android.app.ActivityThread$H.handleMessage(ActivityThread.java:939)
at android.os.Handler.dispatchMessage(Handler.java:99)
at android.os.Looper.loop(Looper.java:130)
at android.app.ActivityThread.main(ActivityThread.java:3835)
at java.lang.reflect.Method.invokeNative(Native Method)
at java.lang.reflect.Method.invoke(Method.java:507)
at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:864)
at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:622)
at dalvik.system.NativeStart.main(Native Method)
Caused by: java.lang.NullPointerException
at java.util.regex.Matcher.appendEvaluated(Matcher.java:135)
at java.util.regex.Matcher.appendReplacement(Matcher.java:115)
at java.util.regex.Matcher.replaceAll(Matcher.java:322)
at java.lang.String.replaceAll(String.java:1963)
at com.*removed*.*removed*.List.fillData(NoteList.java:100)
at com.*removed*.*removed*.List.onCreate(NoteList.java:31)
at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1047)
at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:1722)
... 11 more
</code></pre>

<p>......and here is the relevant code. When the user starts the List activity, I want them to see results based on the item they clicked from the previous list.  The home page is a list, so the List activity is basically a query where I search the database for all entries where the book column name matches the name they clicked on in the home page.  This method "fills" the List listview with the results of the query.</p>

<pre><code>@SuppressWarnings("deprecation")
private void fillData() {

String[] args = {"woo"};

    for(int i = 0; i &lt; args.length ; i++){
        args[i] = args[i].replaceAll("woo", getBook());}

    String[] projection = ............removed


    Cursor cursor = managedQuery(Provider.CONTENT_URI, projection,
            Database.COLUMN_BOOK + "=" + "?",
            args, null);

    String[] from = ............removed     
    int[] to = ...........removed


    adapter = new SimpleCursorAdapter(List.this, R.layout.note_row, cursor, from,
            to);

    setListAdapter(adapter); }

static String book;
public static String getBook() {return book;}
public static void setBook(String book) {List.book = book;}
</code></pre>

<p>Adn here is the code from the home page</p>

<pre><code>public void onItemClick(AdapterView&lt;?&gt; adapter, View v,
        int position, long id) {
    final String[] choice = getResources().getStringArray(R.array.booknames);
       String book = choice[position];
       List.setBook(book);
   Intent x = new Intent(Home.this, List.class);
   Home.this.startActivity(x);

}
</code></pre>

<p>This app is already on the market, and about 3% of devices are getting this Null pointer exception.  So this way of doing it is not quite 100% effective as I had hoped.  </p>

<p>My first guess is that I'm not initializing the variable args correctly, which is causing the ReplaceAll method to glitch in rare cases.
My second guess is that I should be avoiding getters and setters and using bundles.</p>

<p>How do I rewrite this query for 100% success?</p>

## Answers
### Answer ID: 14045698
<p>Looking at the stack trace, it seems <em>much</em> more likely that <code>getBook()</code> is returning null in the problem situation. </p>

<p>You use a static variable to pass information to your List activity, which is <em>not</em> a very good idea in general. That is what passing extras (a bundle) is for.</p>

<p>In rare situation, all of your application might be killed and recreated. Any extras get get passed to the Activity again, but your <code>book</code> remains null in that case.</p>

