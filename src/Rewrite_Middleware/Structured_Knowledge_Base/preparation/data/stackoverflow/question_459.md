# Fatal Exception AsyncTask #2 what did I do wrong?
[Link to question](https://stackoverflow.com/questions/27071700/fatal-exception-asynctask-2-what-did-i-do-wrong)
**Creation Date:** 1416610301
**Score:** 0
**Tags:** java, android
## Question Body
<p>I have a php/mysql query working that looks up the VIN, if the VIN is in the database it returns "VIN already exists"  Where did I screw up in this:  Error report say <code>Fatal Exception : AsyncTask #2</code> (I have code that actually works above this, problem started when I tried to rewrite this to run the php checkVin before launching the Sell page)</p>

<pre><code>11-21 16:34:43.736: E/AndroidRuntime(725): FATAL EXCEPTION: AsyncTask #2
11-21 16:34:43.736: E/AndroidRuntime(725): java.lang.RuntimeException: An error occured while executing doInBackground()
11-21 16:34:43.736: E/AndroidRuntime(725):  at android.os.AsyncTask$3.done(AsyncTask.java:299)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.FutureTask$Sync.innerSetException(FutureTask.java:273)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.FutureTask.setException(FutureTask.java:124)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.FutureTask$Sync.innerRun(FutureTask.java:307)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.FutureTask.run(FutureTask.java:137)
11-21 16:34:43.736: E/AndroidRuntime(725):  at android.os.AsyncTask$SerialExecutor$1.run(AsyncTask.java:230)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1076)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:569)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.lang.Thread.run(Thread.java:856)
11-21 16:34:43.736: E/AndroidRuntime(725): Caused by: java.lang.IllegalArgumentException: Host name may not be null
11-21 16:34:43.736: E/AndroidRuntime(725):  at org.apache.http.HttpHost.&lt;init&gt;(HttpHost.java:83)
11-21 16:34:43.736: E/AndroidRuntime(725):  at org.apache.http.impl.client.AbstractHttpClient.determineTarget(AbstractHttpClient.java:497)
11-21 16:34:43.736: E/AndroidRuntime(725):  at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:626)
11-21 16:34:43.736: E/AndroidRuntime(725):  at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:616)
11-21 16:34:43.736: E/AndroidRuntime(725):  at com.mobile.donswholesale.Scan.getServerResopnse(Scan.java:272)
11-21 16:34:43.736: E/AndroidRuntime(725):  at com.mobile.donswholesale.Scan.access$1(Scan.java:260)
11-21 16:34:43.736: E/AndroidRuntime(725):  at com.mobile.donswholesale.Scan$4.doInBackground(Scan.java:240)
11-21 16:34:43.736: E/AndroidRuntime(725):  at com.mobile.donswholesale.Scan$4.doInBackground(Scan.java:1)
11-21 16:34:43.736: E/AndroidRuntime(725):  at android.os.AsyncTask$2.call(AsyncTask.java:287)
11-21 16:34:43.736: E/AndroidRuntime(725):  at java.util.concurrent.FutureTask$Sync.innerRun(FutureTask.java:305)
11-21 16:34:43.736: E/AndroidRuntime(725):  ... 5 more
</code></pre>

<hr>

<pre><code>private void addSellButtonListener() {
    Button sell = (Button) findViewById(R.id.sell_button);
    sell.setOnClickListener(new OnClickListener() {
        public void onClick(View v) {
            sendDatatoServer();
        }
    });
}
private String formatDataAsJASON() {
    JSONObject root = new JSONObject();
    try {
        root.put("User", userId.getText().toString());
        root.put("Pword", userPass.getText().toString());
        root.put("VIN", VINID.getText().toString());
        return root.toString();
    } catch (JSONException e) {
        Log.d("JWP", "Can't format JSON");
    }
    return null;
}
private void sendDatatoServer() {
    final String json = formatDataAsJASON();
    new AsyncTask&lt;Void, Void, String&gt;() {
        @Override
        protected String doInBackground(Void... params) {
            return getServerResopnse(json);
        }
        @Override
        protected void onPostExecute(String result) {
            if (result == "VIN already exists") {
                Toast.makeText(Scan.this,
                        getString(R.string.vin_exists), Toast.LENGTH_LONG)
                        .show();
                final Intent i = new Intent(Scan.this, Scan.class);
                startActivity(i);
            } else {
                StartSell();
            }
        }
    }.execute();
}
private String getServerResopnse(String json) {
    HttpPost post = new HttpPost("http://" + serverIp.getText().toString()
            + "/chekVIN.php");
    try {
        StringEntity entity = new StringEntity(json);
        post.setEntity(entity);
        post.setHeader("Content-type", "application/json");
        DefaultHttpClient client = new DefaultHttpClient();
        BasicResponseHandler handler = new BasicResponseHandler();
        String response = client.execute(post, handler);
        return response;
    } catch (UnsupportedEncodingException e) {
        Log.d("JWP", e.toString());

    } catch (ClientProtocolException e) {
        Log.d("JWP", e.toString());
    } catch (IOException e) {
        Log.d("JWP", e.toString());
    }
    return null;
}
private void StartSell() {
    final Intent i = new Intent(Scan.this, Sell.class);
    EditText editText = (EditText) findViewById(R.id.VIN);
    String text = editText.getText().toString();
    EditText editText2 = (EditText) findViewById(R.id.Make);
    String text2 = editText2.getText().toString();
    EditText editText3 = (EditText) findViewById(R.id.Model);
    String text3 = editText3.getText().toString();
    EditText editText4 = (EditText) findViewById(R.id.Color);
    String text4 = editText4.getText().toString();
    EditText editText5 = (EditText) findViewById(R.id.Year);
    String text5 = editText5.getText().toString();
    try {
        FileOutputStream fos = openFileOutput(VinHolder,
                Context.MODE_PRIVATE);
        fos.write(text.getBytes());
        fos.close();
        FileOutputStream fos2 = openFileOutput(MakeHolder,
                Context.MODE_PRIVATE);
        fos2.write(text2.getBytes());
        fos2.close();
        FileOutputStream fos3 = openFileOutput(ModelHolder,
                Context.MODE_PRIVATE);
        fos3.write(text3.getBytes());
        fos3.close();
        FileOutputStream fos4 = openFileOutput(ColorHolder,
                Context.MODE_PRIVATE);
        fos4.write(text4.getBytes());
        fos4.close();
        FileOutputStream fos5 = openFileOutput(YearHolder,
                Context.MODE_PRIVATE);
        fos5.write(text5.getBytes());
        fos5.close();
    }
    catch (Exception e) {
        Log.d("DEBUGTAG", "File Not Saved" + text);
        e.printStackTrace();
    }
    startActivity(i);
}
</code></pre>

## Answers
### Answer ID: 29655932
<p>Because I use a Text file from another page of the app to hold a manually entered ip address, I needed to carry that info over so that the the HttpPost("http://" +serverIp.getText().toString() + "chechvin.php"); would actually have the ip address in it. 
After adding: </p>

<p>public static final String SERVERIP= "sinfo.txt"; </p>

<p>everything worked just fine.</p>

