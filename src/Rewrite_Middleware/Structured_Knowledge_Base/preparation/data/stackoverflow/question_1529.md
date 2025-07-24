# Listview notifydatachanged() timing concern
[Link to question](https://stackoverflow.com/questions/8619082/listview-notifydatachanged-timing-concern)
**Creation Date:** 1324662357
**Score:** 1
**Tags:** android, android-listview
## Question Body
<p>I have an app that works on the emulator but will intermittently crash when testing on a real device. I am running a modified version of Code Overtones Android Crash report. (http://jyro.blogspot.com/2009/09/crash-report-for-android-app.html) The emailed cause states:</p>

<blockquote>
  <p>The content of the adapter has changed but ListView did not receive a
  notification. Make sure the content of your adapter is not modified
  from a background thread, but only from the UI thread. [in
  ListView(2131296303, class android.widget.ListView) with Adapter(class
  android.widget.SimpleAdapter)]</p>
</blockquote>

<p>The code does not modify the adapter outside of the UI main thread. All access to the adapter is through the onPostExecute of an AsyncTask. The code is:</p>

<pre><code>    @Override
    protected void onPostExecute(String result) {
        MyLog.d(TAG, "onPostExecute");
        foodDescArrayList.clear();
        int entries = holdFoodDescArrayList.size();
        HashMap&lt;String, String&gt; listEntry;
        for (int i = 0; i &lt; entries; i++) {
            listEntry = new HashMap&lt;String, String&gt;();
            listEntry = holdFoodDescArrayList.get(i);
            foodDescArrayList.add(listEntry);
        }
        holdFoodDescArrayList.clear();
        hideProgress();
        foodDescAdapter.notifyDataSetChanged();
        String ents = " entries";
        if (rowsReturned == 1) {
            ents = " entry";
        }
        foodDescHeader.setText("Page " + Integer.toString(currentPage + 1)
                + " of " + Integer.toString(pageCount) + " (" + Integer.toString(rowsReturned) + ents + ")");
        loadActive = false;
    }
</code></pre>

<p>The holdFoodDescArrayList is a stand alone list filled in the background task from an SQLite database. the foodDescArrayList is the array associated with the ListView adapter. (I've found that there is a performance boost when queuing this way. Maybe because the adapter is out of the loop during database access. Less overhead?)</p>

<p>The crash always occurs on first entry (onCreate) after a home key exit and then reentry to the top level activity that calls the list activity. The time between crashes is from 30 minutes to 2 hours during continuous testing. The code that is crashing has been traversed hundreds of times and is linear with no exits. </p>

<p>The only possible hole I can find in reviewing the code is the clear() preceding the array load. Does the clear function act as one change and the group of adds as a second change? Is there a timing consideration? There are from 1 to 24 entries in the list, so the load should take milliseconds and not seconds...</p>

<p>I'm looking for ideas and clues. Please scan the code and see if you see a glaring error or side effect in the code. It is the only place the ListView's associated array data is altered in the app. The background code only alters the hold array.</p>

<p>Please don't enter a full code rewrite in an answer. I'm continuing to try and find the why and which. I don't want to waste more than a few minutes of your time. I will look at this post often for the next few days and answer any questions I find. Thanks for any help...</p>

<p>----------- Update to add code requested ----------</p>

<p>The code in onCreate is:</p>

<pre><code>    setContentView(R.layout.fooddeslist);
    foodDescHeader = (TextView) findViewById(R.id.foodDescHeading);
    foodDescListView = (ListView) findViewById(R.id.foodDescList);
    foodDescArrayList = new ArrayList&lt;HashMap&lt;String, String&gt;&gt;();
    holdFoodDescArrayList = new ArrayList&lt;HashMap&lt;String, String&gt;&gt;();
    foodDescAdapter = new SimpleAdapter(this, foodDescArrayList,
            R.layout.longdescitem, new String[] { GC.FOODDESCLIST_LINE1,
                    GC.FOODDESCLIST_LINE2 },
            new int[] { R.id.longdescListItemLine1,
                    R.id.longdescListItemLine2 });
    foodDescListView.setAdapter(foodDescAdapter);
    registerForContextMenu(foodDescListView);
</code></pre>

<p>The array entries are:</p>

<pre><code>    listEntry = new HashMap&lt;String, String&gt;();
</code></pre>

<p>The hold array is a duplicate of the adapter's array. The hold array is loaded in the doInBackground function in the AsyncTask. I'd show the background code, but it's about 500 lines of code. The end result is that the hold array is loaded with the 2 lines to display and ancillary data that is unique to each entry. Row ids for various bits of data in other tables that is used when an entry is selected. The duplicate tables allow me to take eons (to gigahertz processors) loading the array. The transfer in the UI running post execute just takes a couple of milliseconds.</p>

<p>longdescitem.xml is:</p>

<pre><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;LinearLayout
     xmlns:android="http://schemas.android.com/apk/res/android"
     android:layout_width="match_parent"
     android:layout_height="wrap_content"
     android:orientation="vertical"&gt;

     &lt;TextView android:id="@+id/longdescListItemLine1"
        android:textStyle="italic"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textColor="#ff9900"
        /&gt;
     &lt;TextView android:id="@+id/longdescListItemLine2"
         android:layout_width="match_parent"
         android:layout_height="wrap_content"
         android:textColor="#b89300"

         /&gt;
&lt;/LinearLayout&gt;
</code></pre>

<p>R.layout.fooddesclist is:</p>

<pre><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" &gt;

    &lt;TextView
        android:id="@+id/foodDescHeading"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_alignParentTop="true"
        android:layout_centerHorizontal="true"
        android:layout_marginLeft="2dip"
        android:text="Page 1 of 10 (nnn entries)"
        android:textAppearance="?android:attr/textAppearanceSmall"
        android:textColor="#b89300" /&gt;

    &lt;ImageButton
        android:id="@+id/foodDescForward"
        android:layout_width="50px"
        android:layout_height="50px"
        android:layout_alignParentRight="true"
        android:layout_alignParentTop="true"
        android:layout_marginRight="12dip"
        android:layout_marginTop="5dip"
        android:background="@drawable/forward"
        android:clickable="true"
        android:onClick="foodDescForwardClicked" /&gt;

    &lt;ImageButton
        android:id="@+id/foodDescBack"
        android:layout_width="50px"
        android:layout_height="50px"
        android:layout_alignParentLeft="true"
        android:layout_alignParentTop="true"
        android:layout_marginLeft="12dip"
        android:layout_marginTop="5dip"
        android:background="@drawable/back"
        android:clickable="true"
        android:onClick="foodDescBackClicked" /&gt;

    &lt;View
        android:id="@+id/foodDescSpacer1"
        android:layout_width="match_parent"
        android:layout_height="2dp"
        android:layout_alignParentLeft="true"
        android:layout_below="@id/foodDescForward"
        android:layout_marginBottom="2dip"
        android:layout_marginTop="2dip"
        android:background="@drawable/divider" /&gt;

    &lt;ListView
        android:id="@+id/foodDescList"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_alignParentLeft="true"
        android:layout_below="@id/foodDescSpacer1"
        android:layout_marginLeft="2dip"
        android:layout_marginRight="2dip"
        android:cacheColorHint="#00000000"
        android:divider="#b89300"
        android:dividerHeight="1.0px" /&gt;

&lt;/RelativeLayout&gt;
</code></pre>

<p>-------- Another Update --------------</p>

<p>I've added some code to the opPostExecute function. </p>

<pre><code>    protected void onPostExecute(String result) {
        MyLog.d(TAG, "onPostExecute");
        foodDescArrayList.clear();
        foodDescAdapter.notifyDataSetChanged();
        try {
            Thread.sleep(300);
        } catch (InterruptedException e) {
            MyLog.d(TAG, "Sleep failed: " + e.getMessage());
        }
        int entries = holdFoodDescArrayList.size();
        HashMap&lt;String, String&gt; listEntry;
        for (int i = 0; i &lt; entries; i++) {
            listEntry = new HashMap&lt;String, String&gt;();
            listEntry = holdFoodDescArrayList.get(i);
            foodDescArrayList.add(listEntry);
        }
        holdFoodDescArrayList.clear();
        hideProgress();
        foodDescAdapter.notifyDataSetChanged();
        String ents = " entries";
        if (rowsReturned == 1) {
            ents = " entry";
        }
        foodDescHeader.setText("Page " + Integer.toString(currentPage + 1)
                + " of " + Integer.toString(pageCount) + " (" + Integer.toString(rowsReturned) + ents + ")");
        loadActive = false;
    }
</code></pre>

<p>After two hours of steady testing on the Atrix, it hasn't crashed yet. Before the code, I would get a crash at least once and sometimes twice in 2 hours. I added the notifydatasetchanged after the clear and followed it with a 300 msec sleep. I think the operating system was stepping on its toes because the original notify got lost. Although the database queries can take up to 8 seconds, most of the time it's instant answer. The progress dialog never had a chance to fully set up. The screen would flicker and then the listview would show. The progress display was never identifiable. (The progress dialog is turned on in the preExecute function.) The entire AsyncTask was completing in less than 300 milliseconds. Maybe this is a fix and maybe not.</p>

## Answers
### Answer ID: 8796170
<p>I'm answering this myself to close the post as answered.</p>

