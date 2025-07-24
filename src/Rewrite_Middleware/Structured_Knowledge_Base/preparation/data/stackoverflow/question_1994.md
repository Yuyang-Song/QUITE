# IllegalStateException &quot;attempt to re-open an already-closed object&quot; in SimpleCursorAdapter from ContentProvider
[Link to question](https://stackoverflow.com/questions/14956608/illegalstateexception-attempt-to-re-open-an-already-closed-object-in-simplecur)
**Creation Date:** 1361274062
**Score:** 4
**Tags:** android, android-contentprovider, android-cursoradapter, android-loadermanager, android-loader
## Question Body
<p>I have a series of <code>ListView</code> objects in <code>Fragment</code>s that are being populated by a <code>CursorAdapter</code> which gets a <code>Cursor</code> from the <code>LoaderManager</code> for the activity.  As I understand it, all database and <code>Cursor</code> close actions are completely handled by the <code>LoaderManager</code> and the <code>ContentProvider</code>, so at no point in any of the code am I calling <code>.close()</code> on anything.</p>

<p>Sometimes, however, I get this exception:</p>

<pre><code>02-19 11:07:12.308 E/AndroidRuntime(18777): java.lang.IllegalStateException: attempt to re-open an already-closed object: android.database.sqlite.SQLiteQuery (mSql = SELECT * FROM privileges WHERE uuid!=?) 
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.database.sqlite.SQLiteClosable.acquireReference(SQLiteClosable.java:33)
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.database.sqlite.SQLiteQuery.fillWindow(SQLiteQuery.java:82)
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.database.sqlite.SQLiteCursor.fillWindow(SQLiteCursor.java:164)
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.database.sqlite.SQLiteCursor.onMove(SQLiteCursor.java:147)
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.database.AbstractCursor.moveToPosition(AbstractCursor.java:178)
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.database.CursorWrapper.moveToPosition(CursorWrapper.java:162)
02-19 11:07:12.308 E/AndroidRuntime(18777): at android.widget.CursorAdapter.getView(CursorAdapter.java:241)
</code></pre>

<p>I put some log code into my <code>CursorAdapter</code> that tells me when <code>getView(...)</code>, <code>getItem(...)</code> or <code>getItemId(...)</code> are being called and it seems as though this is happening on the first <code>getView(...)</code> for a given adapter after a lot of <code>getView(...)</code>s for another adapter.  It also happens after a user has navigated around the app a lot.</p>

<p>This makes me wonder if the <code>Cursor</code> for an adapter is being retained in the <code>CursorAdapter</code>, but being closed in error by the <code>ContentProvider</code> or the <code>Loader</code>.  Is this possible?  Should I be doing any housekeeping on the <code>CursorAdapter</code> based on app/activity/fragment lifecycle events?</p>

<p><code>ContentProvider</code> query method:</p>

<pre><code>class MyContentProvider extends ContentProvider {
//...

    @Override
    public Cursor query(Uri uri, String[] projection, String selection,
            String[] selectionArgs, String sortOrder) {
        SQLiteDatabase db = mOpenHelper.getReadableDatabase();
        Cursor query = db.query(getTableName(uri), projection, selection, selectionArgs, null, null, sortOrder);
        query.setNotificationUri(getContext().getContentResolver(), uri);
        return query;
    }

//...
}
</code></pre>

<p>Typical <code>LoaderCallbacks</code>:</p>

<pre><code>LoaderCallbacks&lt;Cursor&gt; mCallbacks = new LoaderCallbacks&lt;Cursor&gt;() {

    @Override
    public void onLoaderReset(Loader&lt;Cursor&gt; loader) {
        mArticleAdapter.swapCursor(null);
    }

    @Override
    public void onLoadFinished(Loader&lt;Cursor&gt; loader, Cursor cursor) {
        if(cursor.isClosed()) {
            Log.d(TAG, "CURSOR RETURNED CLOSED");
            Activity activity = getActivity();
            if(activity!=null) {
                activity.getLoaderManager().restartLoader(mFragmentId, null, mCallbacks);
            }
            return;
        }
        mArticleAdapter.swapCursor(cursor);
    }

    @Override
    public Loader&lt;Cursor&gt; onCreateLoader(int id, Bundle args) {
        triggerArticleFeed();
        CursorLoader cursorLoader = null;

        if(id == mFragmentId) {
            cursorLoader = new CursorLoader(getActivity(),
                                            MyContentProvider.ARTICLES_URI,
                                            null,
                                            ArticlesContentHelper.ARTICLES_WHERE,
                                            ArticlesContentHelper.ARTICLES_WHEREARGS,
                                            null);
        }
        return(cursorLoader);
    }
};
</code></pre>

<p><code>CursorAdapter</code> constructor:</p>

<pre><code>public ArticlesCursorAdapter(Context context, Cursor c) {
    super(context, c, 0);
    mImageloader = new ImageLoader(context);
}
</code></pre>

<p>I have read this question but unfortunately it hasn't got the answer to my problem as it simply suggests using a <code>ContentProvider</code>, which I am.</p>

<p><a href="https://stackoverflow.com/questions/12358864/illegalstateexception-attempt-to-re-open-an-already-closed-object-simplecursor">IllegalStateException: attempt to re-open an already-closed object. SimpleCursorAdapter problems</a></p>

<p><strong>IMPORTANT NEW INFORMATION THAT HAS JUST COME TO LIGHT</strong></p>

<p>I discovered some other code elsewhere in the project that was NOT using <code>Loader</code>s and NOT managing its <code>Cursor</code>s properly.  I've just switched this code over to use the same pattern as above; however, if this fixes things, it would suggest that an unmanaged <code>Cursor</code> in one part of a project can kill a properly managed one elsewhere.</p>

<p>Stick around.</p>

<p><strong>OUTCOME OF NEW INFORMATION</strong></p>

<p>That did not fix it.</p>

<p><strong>NEW IDEA</strong></p>

<pre><code>@Override
onDestroyView() {
    getActivity().getLoaderManager().destroyLoader(mFragmentId);
    //any other destroy-time code
    super.onDestroyView()
}
</code></pre>

<p>ie possibly yes, I <em>should</em> be doing housekeeping on the <code>CursorAdapter</code> (or rather the <code>CursorLoader</code> in line with lifecycle events).</p>

<p><strong>OUTCOME OF NEW IDEA</strong></p>

<p>Nope.</p>

<p><strong>PREVIOUS IDEA</strong></p>

<p>Turned out to work once I added in a minor tweak!  However it's so complex that I should probably rewrite the entire question.</p>

## Answers
### Answer ID: 31700183
<p>You can try to path null instead cursor into adapter constructor. Then owerride SwapCursor(Cursor c) in adapter, move initialization of cursor data there and call it in OnLoadFinished(Loader loader, Cursor data) method of your data loader.</p>

<pre><code>enter code here
    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
    // ... building your query here
       mSimpleCursorAdapter = new mSimpleCursorAdapter(getActivity().getApplicationContext(),
           layout, null, from, to, flags);
    }

    @Override
    public void onLoadFinished(Loader&lt;Cursor&gt; loader, Cursor data) {
       contentAdapter.swapCursor(data);
    }
</code></pre>

### Answer ID: 14956705
<p>Have you updated your data set? It could be the case that the cursor has been re-loaded due notifying a change in the content resolver:</p>

<pre><code>getContentResolver().notifyChange(URI, null);
</code></pre>

<p>If you have set a notification URI, this would trigger your current cursor to close and a new cursor to be returned by the cursor loader. You can then grab the new cursor if you have registered a onLoadCompleteListener:            </p>

<pre><code>mCursorLoader.registerListener(0, new OnLoadCompleteListener&lt;Cursor&gt;() {
    @Override
    public void onLoadComplete(Loader&lt;Cursor&gt; loader, Cursor cursor) {
        // Set your listview's CursorAdapter
    }
});
</code></pre>

