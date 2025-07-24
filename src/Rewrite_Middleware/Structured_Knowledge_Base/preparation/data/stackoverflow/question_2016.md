# error in firing raw query
[Link to question](https://stackoverflow.com/questions/15684453/error-in-firing-raw-query)
**Creation Date:** 1364480876
**Score:** 0
**Tags:** android, illegalstateexception
## Question Body
<p>I am having error saying "IllegalStateException: database is not open" in this statement:</p>

<pre><code>Cursor cursor = database.rawQuery("select rec_field_id, field_value from records_fields_data where cat_field_id = "+get_cat_field_id(category_fields_array_list.get(i))+" AND rec_id = "+rec_id+";", null);
</code></pre>

<p>This is my full java code:</p>

<pre><code>  package com.walletapp;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ContentValues;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

public class AddRecords extends Activity {

    Spinner category_spinner;
    SQLiteDatabase database;
    ArrayList&lt;String&gt; category_spinner_array_list, category_fields_array_list;
    int cat_id;
    int rec_id;
    String[] tags;
    ArrayList&lt;String&gt; tmp_category_fields_array_list;
    ArrayList&lt;String&gt; tags_list;
    private ArrayList&lt;String&gt; selectedTags;
    ArrayList&lt;EditText&gt; edit_text_array_list;
    EditText et_tags;
    int tag_editText_id;
    String cat_name;
    String record_data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_records);

        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        Intent intent = getIntent();
        rec_id = intent.getIntExtra("rec_id", 0);
        record_data = intent.getStringExtra("record_data");
        cat_name = intent.getStringExtra("cat_name");

        category_spinner = (Spinner) findViewById(R.id.spinnerAddRecords);
        build_spinner_list();
        database.close();

        if (rec_id != 0) {
            category_spinner.setSelection(category_spinner_array_list
                    .indexOf(cat_name));
            // generateUI(cat_name);
            category_spinner.setEnabled(false);
        }

        category_spinner
                .setOnItemSelectedListener(new OnItemSelectedListener() {

                    @Override
                    public void onItemSelected(AdapterView&lt;?&gt; arg0, View arg1,
                            int arg2, long arg3) {

                        generateUI(arg0.getItemAtPosition(arg2) + "");
                    }

                    @Override
                    public void onNothingSelected(AdapterView&lt;?&gt; arg0) {

                    }
                });
    }

    protected void generateUI(String string) {

        Log.i("generate UI string passed is : ", string);

        LinearLayout linearLayout_inner = (LinearLayout) findViewById(R.id.linearLayoutAddRecordsScrollViewInner);

        if (string.equals("Category")) {

            linearLayout_inner.removeAllViews();
            Toast.makeText(getBaseContext(),
                    "Select the category to proceed further.",
                    Toast.LENGTH_SHORT).show();
        } else {

            linearLayout_inner.removeAllViewsInLayout();

            tmp_category_fields_array_list = new ArrayList&lt;String&gt;();

            cat_id = getId(string);
            tmp_category_fields_array_list = get_field_names(cat_id);

            category_fields_array_list = new ArrayList&lt;String&gt;();
            category_fields_array_list = get_sorted_fields(tmp_category_fields_array_list);

            edit_text_array_list = new ArrayList&lt;EditText&gt;();

            if (rec_id == 0) {
                for (String s : category_fields_array_list) {
                    TextView tv = new TextView(this);
                    tv.setText(s);
                    linearLayout_inner.addView(tv);

                    EditText et = new EditText(this);
                    et.setHint(s);
                    et.setTag(new Tag(get_cat_field_id(s), s));
                    edit_text_array_list.add(et);

                    linearLayout_inner.addView(et);

                    if (s.equals("Tags")) {
                        tag_editText_id = et.getId();
                        et_tags = et;
                        et.setFocusable(false);
                        et.setFocusableInTouchMode(false);
                        et.setOnClickListener(new OnClickListener() {

                            @Override
                            public void onClick(View v) {

                                showSelectTagsDialog();
                            }
                        });
                    }
                }
            } else {
                Log.i("database is open.", database.isOpen() + "");
                // for(String s : category_fields_array_list)
                for (int i = 0; i &lt; category_fields_array_list.size(); i++) {
                    TextView tv = new TextView(this);
                    tv.setText(category_fields_array_list.get(i));
                    linearLayout_inner.addView(tv);

                    ArrayList&lt;Integer&gt; al_rec_field_id = new ArrayList&lt;Integer&gt;();
                    ArrayList&lt;String&gt; al_field_value = new ArrayList&lt;String&gt;();

                    Cursor cursor = database
                            .rawQuery(
                                    "select rec_field_id, field_value from records_fields_data where cat_field_id = "
                                            + get_cat_field_id(category_fields_array_list
                                                    .get(i))
                                            + " AND rec_id = "
                                            + rec_id + ";", null);
                    while (cursor.moveToNext()) {
                        al_rec_field_id.add(cursor.getInt(0));
                        al_field_value.add(cursor.getString(1));
                    }
                    cursor.close();

                    // ----------------------------------------------------------------------------------------------

                    EditText et = new EditText(this);
                    // et.setHint(category_fields_array_list.get(i));
                    et.setText(al_field_value.get(i));
                    // Tag(int tmp_rec_field_id, int tmp_rec_id, int
                    // tmp_cat_field_id)
                    et.setTag(new Tag(al_rec_field_id.get(i), rec_id,
                            get_cat_field_id(category_fields_array_list.get(i))));
                    edit_text_array_list.add(et);

                    linearLayout_inner.addView(et);

                    if (category_fields_array_list.get(i).equals("Tags")) {
                        tag_editText_id = et.getId();
                        et_tags = et;
                        et.setFocusable(false);
                        et.setFocusableInTouchMode(false);
                        et.setOnClickListener(new OnClickListener() {

                            @Override
                            public void onClick(View v) {

                                showSelectTagsDialog();
                            }
                        });
                    }
                }
            }

            Button btn = new Button(this);
            btn.setText("Save");
            btn.setOnClickListener(new OnClickListener() {

                @Override
                public void onClick(View v) {

                    loadDatabase();
                    ContentValues values = new ContentValues();
                    String currentDate = new SimpleDateFormat("yyyy/MM/dd")
                            .format(Calendar.getInstance().getTime());
                    Tag tag = null;
                    int rec_id = 0;

                    for (int i = 0; i &lt; edit_text_array_list.size(); i++) {
                        if (i == 0) {
                            // --------------first insert into records_data
                            // table------------

                            values.put("cat_id", cat_id);
                            values.put("tag_id", "0");
                            values.put("is_favourite", "0");
                            values.put("rec_name", edit_text_array_list.get(i)
                                    .getText() + "");
                            values.put("is_delete", "0");
                            values.put("create_date", currentDate);
                            values.put("update_date", "0");

                            database.insert("records_data", null, values);
                            values.clear();

                            // -------------then fetch the rec_id for previously
                            // entered record----------

                            Cursor cursor = database
                                    .query("records_data",
                                            new String[] { "rec_id" },
                                            "rec_name=?",
                                            new String[] { edit_text_array_list
                                                    .get(i).getText() + "" },
                                            null, null, null);
                            while (cursor.moveToNext())
                                rec_id = cursor.getInt(0);
                            cursor.close();

                            // -------------use this rec_id for inserting record
                            // into records_fields_data------------

                            values.put("rec_id", rec_id);

                            // ---------get cat_field_id----------

                            tag = (Tag) edit_text_array_list.get(i).getTag();

                            values.put("cat_field_id", tag.get_cat_field_id());
                            values.put("field_value",
                                    edit_text_array_list.get(i).getText() + "");
                            values.put("is_delete", "0");
                            values.put("create_date", currentDate);
                            values.put("update_date", "0");

                            database.insert("records_fields_data", null, values);
                            values.clear();
                        } else if (i &lt; edit_text_array_list.size() - 1) {

                            values.put("rec_id", rec_id);
                            tag = (Tag) edit_text_array_list.get(i).getTag();

                            values.put("cat_field_id", tag.get_cat_field_id());
                            values.put("field_value",
                                    edit_text_array_list.get(i).getText() + "");
                            values.put("is_delete", "0");
                            values.put("create_date", currentDate);
                            values.put("update_date", "0");

                            database.insert("records_fields_data", null, values);
                            values.clear();
                        } else {
                            for (String s : selectedTags) {
                                int tag_id = get_tag_id(s);

                                values.put("rec_id", rec_id);
                                values.put("tag_id", tag_id);

                                database.insert("record_tag_relation", null,
                                        values);
                                values.clear();
                            }
                        }
                    }

                    if (database.isOpen())
                        database.close();

                    finish();
                    startActivity(new Intent(AddRecords.this, AllRecords.class));
                }
            });
            linearLayout_inner.addView(btn);
        }
    }

    protected int get_tag_id(String s) {

        int tag_id = 0;
        Cursor cursor = database.query("tags", new String[] { "tag_id" },
                "tag_name=?", new String[] { s }, null, null, null);
        while (cursor.moveToNext()) {
            tag_id = cursor.getInt(0);
        }
        return tag_id;
    }

    protected void showSelectTagsDialog() {

        build_tags_list();
        selectedTags = new ArrayList&lt;String&gt;();

        boolean[] checkedTags = new boolean[tags.length];
        int count = tags.length;

        for (int i = 0; i &lt; count; i++)
            checkedTags[i] = selectedTags.contains(tags[i]);

        DialogInterface.OnMultiChoiceClickListener tagsDialogListener = new DialogInterface.OnMultiChoiceClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which,
                    boolean isChecked) {
                if (isChecked)
                    selectedTags.add(tags[which]);
                else
                    selectedTags.remove(tags[which]);

                onChangeSelectedTags();
            }
        };

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Select Tag(s)");
        builder.setMultiChoiceItems(tags, checkedTags, tagsDialogListener);
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                dialog.dismiss();
            }
        });

        AlertDialog dialog = builder.create();
        dialog.show();
    }

    protected void onChangeSelectedTags() {

        StringBuilder stringBuilder = new StringBuilder();

        int count = 0;
        for (CharSequence tag : selectedTags) {
            count = count + 1;
            stringBuilder.append(tag);
            if (count &lt; selectedTags.size())
                stringBuilder.append(",");
        }

        for (EditText e : edit_text_array_list) {

            if (e == et_tags) {
                e.setText(stringBuilder.toString());
                break;
            }
        }
    }

    private void build_tags_list() {

        loadDatabase();

        tags_list = new ArrayList&lt;String&gt;();
        Cursor cursor = database.query("tags", new String[] { "tag_name" },
                null, null, null, null, null);
        while (cursor.moveToNext())
            tags_list.add(cursor.getString(0));
        cursor.close();
        database.close();

        tags = tags_list.toArray(new String[tags_list.size()]);
    }

    private int get_cat_field_id(String s) {

        loadDatabase();

        int tmp_cat_field_id = 0;
        Cursor cursor = database.query("category_fields",
                new String[] { "cat_field_id" }, "field_name=?",
                new String[] { s }, null, null, null);
        while (cursor.moveToNext())
            tmp_cat_field_id = cursor.getInt(0);
        cursor.close();
        database.close();

        return tmp_cat_field_id;
    }

    private ArrayList&lt;String&gt; get_sorted_fields(
            ArrayList&lt;String&gt; tmp_category_fields_array_list2) {

        int count = 0;
        ArrayList&lt;String&gt; al_tmp = new ArrayList&lt;String&gt;();
        for (String s : tmp_category_fields_array_list2) {
            if (s.equals("Description")) {
                if (al_tmp.contains(s)) {
                    // ----do nothing
                } else {
                    al_tmp.add(s);
                }
            } else if (s.equals("Notes")) {
                continue;
            } else if (s.equals("Tags")) {
                continue;
            } else {
                if (al_tmp.contains(s)) {
                    // ----do nothing
                } else {
                    al_tmp.add(s);
                }
            }
            count++;
            if (count == tmp_category_fields_array_list.size() - 2) {
                al_tmp.add("Notes");
                al_tmp.add("Tags");
            }
        }
        return al_tmp;
    }

    private ArrayList&lt;String&gt; get_field_names(int cat_id) {

        loadDatabase();

        ArrayList&lt;String&gt; tmp_cat_field_array_list = new ArrayList&lt;String&gt;();

        Cursor cursor = database.query("category_fields",
                new String[] { "field_name" }, "cat_id=?",
                new String[] { cat_id + "" }, null, null, null);
        while (cursor.moveToNext())
            tmp_cat_field_array_list.add(cursor.getString(0));
        cursor.close();

        return tmp_cat_field_array_list;
    }

    protected int getId(String string) {

        loadDatabase();

        int tmp_cat_id = 0;
        Cursor cursor = database.query("category", new String[] { "cat_id" },
                "cat_description=?", new String[] { string }, null, null, null);
        while (cursor.moveToNext())
            tmp_cat_id = cursor.getInt(0);
        cursor.close();
        database.close();

        return tmp_cat_id;
    }

    private void build_spinner_list() {

        loadDatabase();

        category_spinner_array_list = new ArrayList&lt;String&gt;();
        category_spinner_array_list.add("Category");
        Cursor cursor = database.query("category",
                new String[] { "cat_description" }, null, null, null, null,
                null);
        while (cursor.moveToNext())
            category_spinner_array_list.add(cursor.getString(0));
        cursor.close();
        ArrayAdapter&lt;String&gt; dataAdapter = new ArrayAdapter&lt;String&gt;(this,
                android.R.layout.simple_list_item_1,
                category_spinner_array_list);
        dataAdapter
                .setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        category_spinner.setAdapter(dataAdapter);
    }

    private void loadDatabase() {

        database = openOrCreateDatabase("WalletAppDatabase.db",
                SQLiteDatabase.OPEN_READWRITE, null);
    }

    class Tag {
        int cat_field_id;
        String cat_field_name;
        int rec_field_id;
        int rec_id;

        Tag(int id, String name) {
            cat_field_id = id;
            cat_field_name = name;
        }

        Tag(int tmp_rec_field_id, int tmp_rec_id, int tmp_cat_field_id) {
            cat_field_id = tmp_cat_field_id;
            rec_id = tmp_rec_id;
            rec_field_id = tmp_rec_field_id;
        }

        int get_cat_field_id() {
            return cat_field_id;
        }

        String get_cat_field_name() {
            return cat_field_name;
        }

        int get_rec_field_id() {
            return rec_field_id;
        }

        int get_rec_id() {
            return rec_id;
        }
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK &amp;&amp; event.getRepeatCount() == 0) {

            if (database.isOpen())
                database.close();
            finish();

            if (rec_id == 0)
                startActivity(new Intent(AddRecords.this, AllRecords.class));
            else
                startActivity(new Intent(AddRecords.this,
                        RecordsDetailedView.class));
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
}
</code></pre>

<p>This is my logcat output:</p>

<pre><code>03-28 19:52:09.060: W/KeyCharacterMap(19142): No keyboard for id 0
03-28 19:52:09.070: W/KeyCharacterMap(19142): Using default keymap: /system/usr/keychars/qwerty.kcm.bin
03-28 19:52:10.480: D/dalvikvm(19142): DexOpt: --- BEGIN 'ads34104.jar' (bootstrap=0) ---
03-28 19:52:10.650: D/dalvikvm(19142): DexOpt: --- END 'ads34104.jar' (success) ---
03-28 19:52:10.650: D/dalvikvm(19142): DEX prep '/data/data/com.walletapp/cache/ads34104.jar': unzip in 1ms, rewrite 167ms
03-28 19:52:10.770: D/dalvikvm(19142): GC_FOR_MALLOC freed 4534 objects / 295152 bytes in 86ms
03-28 19:52:11.140: E/ActivityThread(19142): Failed to find provider info for com.google.plus.platform
03-28 19:52:11.220: W/Ads(19142): loadAd called while the ad is already loading, so aborting.
03-28 19:52:11.350: I/Ads(19142): adRequestUrlHtml: &lt;html&gt;&lt;head&gt;&lt;script src="http://media.admob.com/sdk-core-v40.js"&gt;&lt;/script&gt;&lt;script&gt;AFMA_getSdkConstants();AFMA_buildAdURL({"preqs":0,"session_id":"10699442437020247494","seq_num":"1","slotname":"a1512f50d8c3692","u_w":320,"msid":"com.walletapp","cap":"m,a","adtest":"on","js":"afma-sdk-a-v6.3.0","bas_off":0,"net":"ed","app_name":"1.android.com.walletapp","hl":"en","gnt":3,"carrier":"310260","u_audio":4,"kw":[],"u_sd":1,"simulator":1,"ms":"gHmei5U7VoADe6IEmAL5vLv6CPgwrxTqIxD3RsiiiukAljgNpKCC5wdhfTaJDFudJqp3jlSMt7IQh69rq2tF4dF7mb6cGUjuVtaNrXWv8IlY0shz8dI-iJtcdL05kuErjnIEkpkaKeilFUqY5qSSnF6siTb2kesTfzUM1VS76XkV7IE1q6yulBNFiXmECeZh349c0TjGh_3JdavLTR8MNSo8_c54G3_YkWKGEfhi3Q_lC4lkKWez-_l5_1moHM1MDDMxri5-2E348uKO75YfPB7CvBvFURAd7hD9ijU3Zq5G5dc72VPnnYdq5q819tb0NauVIQ450JDUN5mcbKGHAQ","isu":"B3EEABB8EE11C2BE770B684D95219ECB","format":"320x50_mb","oar":0,"ad_pos":{"height":0,"visible":0,"y":0,"x":0,"width":0},"u_h":480,"pt":1,"bas_on":0,"ptime":0});&lt;/script&gt;&lt;/head&gt;&lt;body&gt;&lt;/body&gt;&lt;/html&gt;
03-28 19:52:11.960: D/webviewglue(19142): nativeDestroy view: 0x293c08
03-28 19:52:11.970: D/dalvikvm(19142): GC_FOR_MALLOC freed 4152 objects / 371416 bytes in 218ms
03-28 19:52:15.091: W/webcore(19142): Can't get the viewWidth after the first layout
03-28 19:52:15.300: I/Ads(19142): Received ad url: &lt;url: "http://googleads.g.doubleclick.net:80/mads/gma?preqs=0&amp;session_id=10699442437020247494&amp;seq_num=1&amp;u_w=320&amp;msid=com.walletapp&amp;cap=m%2Ca&amp;adtest=on&amp;js=afma-sdk-a-v6.3.0&amp;bas_off=0&amp;net=ed&amp;app_name=1.android.com.walletapp&amp;hl=en&amp;gnt=3&amp;carrier=310260&amp;u_audio=4&amp;kw&amp;u_sd=1&amp;ms=gHmei5U7VoADe6IEmAL5vLv6CPgwrxTqIxD3RsiiiukAljgNpKCC5wdhfTaJDFudJqp3jlSMt7IQh69rq2tF4dF7mb6cGUjuVtaNrXWv8IlY0shz8dI-iJtcdL05kuErjnIEkpkaKeilFUqY5qSSnF6siTb2kesTfzUM1VS76XkV7IE1q6yulBNFiXmECeZh349c0TjGh_3JdavLTR8MNSo8_c54G3_YkWKGEfhi3Q_lC4lkKWez-_l5_1moHM1MDDMxri5-2E348uKO75YfPB7CvBvFURAd7hD9ijU3Zq5G5dc72VPnnYdq5q819tb0NauVIQ450JDUN5mcbKGHAQ&amp;isu=B3EEABB8EE11C2BE770B684D95219ECB&amp;format=320x50_mb&amp;oar=0&amp;u_h=480&amp;bas_on=0&amp;ptime=0&amp;u_so=p&amp;output=html&amp;region=mobile_app&amp;u_tz=330&amp;client_sdk=1&amp;ex=1&amp;slotname=a14e8f77524dde8&amp;kw_type=broad&amp;gsb=3g&amp;caps=interactiveVideo_th_autoplay_mediation_sdkAdmobApiForAds_di&amp;jsv=46" type: "admob" afmaNotifyDt: "null" activationOverlayUrl: "null" useWebViewLoadUrl: "false"&gt;
03-28 19:52:15.300: I/Ads(19142): Request scenario: Online server request.
03-28 19:52:16.201: I/generate UI string passed is :(19142): web mail
03-28 19:52:16.300: I/database is open.(19142): true
03-28 19:52:16.390: D/AndroidRuntime(19142): Shutting down VM
03-28 19:52:16.390: W/dalvikvm(19142): threadid=1: thread exiting with uncaught exception (group=0x4001d800)
03-28 19:52:16.480: D/dalvikvm(19142): GC_FOR_MALLOC freed 4094 objects / 277504 bytes in 77ms
03-28 19:52:16.491: W/SQLiteCompiledSql(19142): Releasing statement in a finalizer. Please ensure that you explicitly call close() on your cursor: select rec_field_id, field_value from records_fields_data where cat_field_id = 8 AND rec_id = 1;
03-28 19:52:16.491: W/SQLiteCompiledSql(19142): android.database.sqlite.DatabaseObjectNotClosedException: Application did not close the cursor or database object that was opened here
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteCompiledSql.&lt;init&gt;(SQLiteCompiledSql.java:62)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteProgram.&lt;init&gt;(SQLiteProgram.java:80)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteQuery.&lt;init&gt;(SQLiteQuery.java:46)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDirectCursorDriver.query(SQLiteDirectCursorDriver.java:42)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDatabase.rawQueryWithFactory(SQLiteDatabase.java:1345)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDatabase.rawQuery(SQLiteDatabase.java:1315)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at com.walletapp.AddRecords.generateUI(AddRecords.java:158)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at com.walletapp.AddRecords$1.onItemSelected(AddRecords.java:77)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.widget.AdapterView.fireOnSelected(AdapterView.java:864)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.widget.AdapterView.access$200(AdapterView.java:42)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.widget.AdapterView$SelectionNotifier.run(AdapterView.java:830)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.os.Handler.handleCallback(Handler.java:587)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.os.Handler.dispatchMessage(Handler.java:92)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.os.Looper.loop(Looper.java:123)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at android.app.ActivityThread.main(ActivityThread.java:4627)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at java.lang.reflect.Method.invokeNative(Native Method)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at java.lang.reflect.Method.invoke(Method.java:521)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:868)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:626)
03-28 19:52:16.491: W/SQLiteCompiledSql(19142):     at dalvik.system.NativeStart.main(Native Method)
03-28 19:52:16.500: E/AndroidRuntime(19142): FATAL EXCEPTION: main
03-28 19:52:16.500: E/AndroidRuntime(19142): java.lang.IllegalStateException: database not open
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.database.sqlite.SQLiteDatabase.rawQueryWithFactory(SQLiteDatabase.java:1333)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.database.sqlite.SQLiteDatabase.rawQuery(SQLiteDatabase.java:1315)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at com.walletapp.AddRecords.generateUI(AddRecords.java:158)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at com.walletapp.AddRecords$1.onItemSelected(AddRecords.java:77)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.widget.AdapterView.fireOnSelected(AdapterView.java:864)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.widget.AdapterView.access$200(AdapterView.java:42)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.widget.AdapterView$SelectionNotifier.run(AdapterView.java:830)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.os.Handler.handleCallback(Handler.java:587)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.os.Handler.dispatchMessage(Handler.java:92)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.os.Looper.loop(Looper.java:123)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at android.app.ActivityThread.main(ActivityThread.java:4627)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at java.lang.reflect.Method.invokeNative(Native Method)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at java.lang.reflect.Method.invoke(Method.java:521)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:868)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:626)
03-28 19:52:16.500: E/AndroidRuntime(19142):    at dalvik.system.NativeStart.main(Native Method)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142): Releasing statement in a finalizer. Please ensure that you explicitly call close() on your cursor: SELECT field_name FROM category_fields WHERE cat_id=?
03-28 19:52:16.510: W/SQLiteCompiledSql(19142): android.database.sqlite.DatabaseObjectNotClosedException: Application did not close the cursor or database object that was opened here
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteCompiledSql.&lt;init&gt;(SQLiteCompiledSql.java:62)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteProgram.&lt;init&gt;(SQLiteProgram.java:80)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteQuery.&lt;init&gt;(SQLiteQuery.java:46)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDirectCursorDriver.query(SQLiteDirectCursorDriver.java:42)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDatabase.rawQueryWithFactory(SQLiteDatabase.java:1345)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDatabase.queryWithFactory(SQLiteDatabase.java:1229)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDatabase.query(SQLiteDatabase.java:1184)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.database.sqlite.SQLiteDatabase.query(SQLiteDatabase.java:1264)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at com.walletapp.AddRecords.get_field_names(AddRecords.java:427)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at com.walletapp.AddRecords.generateUI(AddRecords.java:107)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at com.walletapp.AddRecords$1.onItemSelected(AddRecords.java:77)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.widget.AdapterView.fireOnSelected(AdapterView.java:864)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.widget.AdapterView.access$200(AdapterView.java:42)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.widget.AdapterView$SelectionNotifier.run(AdapterView.java:830)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.os.Handler.handleCallback(Handler.java:587)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.os.Handler.dispatchMessage(Handler.java:92)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.os.Looper.loop(Looper.java:123)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at android.app.ActivityThread.main(ActivityThread.java:4627)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at java.lang.reflect.Method.invokeNative(Native Method)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at java.lang.reflect.Method.invoke(Method.java:521)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:868)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:626)
03-28 19:52:16.510: W/SQLiteCompiledSql(19142):     at dalvik.system.NativeStart.main(Native Method)
03-28 19:52:16.550:
</code></pre>

<p>But i logged the database state just before this statement and it showed that database is open. Can anyone help me with this. </p>

## Answers
### Answer ID: 15684800
<p>In <code>get_tag_id(String s)</code> you forget to call <code>cursor.close()</code>. This may not solve the entire issue, but it could be part of it.</p>

