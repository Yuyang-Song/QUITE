# Way to frame an update query with parameters
[Link to question](https://stackoverflow.com/questions/15064618/way-to-frame-an-update-query-with-parameters)
**Creation Date:** 1361787340
**Score:** 1
**Tags:** javascript, sqlite, insert, titanium
## Question Body
<p>I am working on an application in Appcelerator Titanium. The application uses sqlite database. For <strong>inserting into the database</strong>, I have written a <strong>query with parameters</strong> like this:</p>

<pre><code>db.execute("INSERT INTO formData (unique_id,form_xml_id,dateTime_stamp,data,user_id,status) VALUES ('" + Ti.App.mydata._guid + "'," + findex + ",'"+datetime+"','"+fdata1+"'," + Ti.App.information.user_id + ",'" + formstatus + "')");
</code></pre>

<p>I have another <strong>query to update</strong> the database for a different table. But the query is without parameters. Like this:</p>

<pre><code>db.execute("UPDATE formData SET  form_xml_id=" + findex + ",dateTime_stamp='" + datetime + "',data='" + fdata + "',user_id=" + Ti.App.information.user_id + ",status='"+ DataStatus +"' where unique_id='" + Ti.App.mydata._guid + "'");
</code></pre>

<p>I want to <strong>rewrite the update query, like the insert query</strong>. How can I do that?</p>

## Answers
### Answer ID: 15064721
<p>I have a code which update Contacts... you can modify it accordingly:</p>

<pre><code>public int updateContact(Contact contact) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_NAME, contact.getName());
        values.put(KEY_PH_NO, contact.getPhoneNumber());

        // updating row
        return db.update(TABLE_CONTACTS, values, KEY_ID + " = ?",
                new String[] { String.valueOf(contact.getID()) });
    }
</code></pre>

