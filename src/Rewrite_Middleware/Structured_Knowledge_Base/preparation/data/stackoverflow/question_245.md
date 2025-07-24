# Android: Query to retrive data from db and populate on edittexts
[Link to question](https://stackoverflow.com/questions/17875480/android-query-to-retrive-data-from-db-and-populate-on-edittexts)
**Creation Date:** 1374823919
**Score:** 0
**Tags:** android, sqlite, android-xml
## Question Body
<p>I have a employee table in the database  and have an activity where user inserts the employee details into the table</p>

<p>Now I have to also update the particular employee , so , I used the same xml with different buttons setting the visibility as gone and visible for update and insert buttons respectively</p>

<p>Now when the user clicks on update, I want to display the same xml but with the Edittexts filled with the employee details already and then can be editable </p>

<p>how can I do that ??</p>

<p>this is my xml </p>

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
android:layout_width="wrap_content"
android:layout_height="match_parent"
android:background="@drawable/background"
android:gravity="top" &gt;



&lt;TextView
    android:id="@+id/TV"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content"
    android:layout_alignParentLeft="true"
    android:layout_marginTop="20sp"
    android:gravity="center_horizontal"
    android:text="Employee Entry details"
    android:textColor="#000000"
    android:textSize="35sp"
    android:textStyle="italic" /&gt;

&lt;LinearLayout
    android:id="@+id/mainll"
    android:layout_width="fill_parent"
    android:layout_height="650sp"
    android:layout_alignParentLeft="true"
    android:layout_alignParentRight="true"
    android:layout_below="@+id/TV"
    android:layout_marginTop="10dp"
    android:orientation="vertical" &gt;

    &lt;TableRow
        android:id="@+id/tableRow1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="50sp"&gt;

        &lt;TextView
            android:id="@+id/enametext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee Name:"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp" /&gt;

        &lt;EditText
            android:id="@+id/enameedit"
            android:layout_width="340sp"
            android:layout_height="wrap_content" &gt;

            &lt;requestFocus /&gt;
            &lt;/EditText&gt;
    &lt;/TableRow&gt;

    &lt;TableRow
        android:id="@+id/tableRow2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="20sp"&gt;

        &lt;TextView
            android:id="@+id/edesignationtext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee Designation:"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp"/&gt;

        &lt;EditText
            android:id="@+id/edesignationedit"
            android:layout_width="340sp"
            android:layout_height="wrap_content" &gt;


        &lt;/EditText&gt;




    &lt;/TableRow&gt;

    &lt;TableRow
        android:id="@+id/tableRow3"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="20sp"&gt;

        &lt;TextView
            android:id="@+id/enumbertext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee Phone Number:"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp"/&gt;

        &lt;EditText
            android:id="@+id/enumberedit"
            android:layout_width="340sp"
            android:layout_height="wrap_content"
             &gt;


        &lt;/EditText&gt;

    &lt;/TableRow&gt;

    &lt;TableRow
        android:id="@+id/tableRow4"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="20sp"&gt;

        &lt;TextView
            android:id="@+id/edobtext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee D.O.B :"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp"/&gt;

        &lt;EditText
            android:id="@+id/edobedit"
            android:layout_width="250sp"
            android:layout_height="wrap_content"
            /&gt;

        &lt;Button
            android:id="@+id/dateOfBirth"
            style="?android:attr/buttonStyleSmall"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Date"
            android:textColor="#000000"
            android:textSize="30sp"
            android:background="#ffffff" /&gt;

    &lt;/TableRow&gt;

    &lt;TableRow
        android:id="@+id/tableRow5"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="20sp"&gt;

        &lt;TextView
            android:id="@+id/ebasicpaytext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee Basic Pay :"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp"/&gt;

        &lt;EditText
            android:id="@+id/ebasicpayedit"
            android:layout_width="340sp"
            android:layout_height="wrap_content"
            /&gt;
    &lt;/TableRow&gt;

    &lt;TableRow
        android:id="@+id/tableRow6"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="20sp"&gt;

        &lt;TextView
            android:id="@+id/epftext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee PF deduction :"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp"/&gt;

        &lt;EditText
            android:id="@+id/epfedit"
            android:layout_width="340sp"
            android:layout_height="wrap_content"
            /&gt;
    &lt;/TableRow&gt;


    &lt;TableRow
        android:id="@+id/tableRow6"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="20sp"&gt;

        &lt;TextView
            android:id="@+id/eotherdeductionstext"
            android:layout_width="260sp"
            android:layout_height="wrap_content"
            android:text="Employee Other Deductions :"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#000000"
            android:textSize="30sp"/&gt;

        &lt;EditText
            android:id="@+id/eotherdeductionedit"
            android:layout_width="340sp"
            android:layout_height="wrap_content"
            /&gt;
    &lt;/TableRow&gt;
&lt;/LinearLayout&gt;

&lt;TableRow
    android:id="@+id/inserttablerow"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_alignParentLeft="true"
    android:layout_below="@+id/mainll"
    android:layout_marginTop="61dp"
    android:visibility="visible" &gt;

    &lt;Button
        android:id="@+id/savebutton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginLeft="70sp"
        android:background="#ffffff"
        android:text="Save"
        android:textColor="#000000"
        android:textSize="30sp" /&gt;

    &lt;Button
        android:id="@+id/cancelbutton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginLeft="100sp"
        android:background="#ffffff"
        android:text="Cancel"
        android:textColor="#000000"
        android:textSize="30sp" /&gt;

    &lt;Button
        android:id="@+id/addanotheremployeebutton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:background="#ffffff"
        android:layout_marginLeft="100sp"
        android:text="Add new"
        android:textColor="#000000"
        android:textSize="30sp" /&gt;

&lt;/TableRow&gt;

&lt;TableRow
    android:id="@+id/updatetablerow"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_alignParentLeft="true"
    android:layout_below="@+id/mainll"
    android:layout_marginTop="61dp"
    android:visibility="gone" &gt;

    &lt;Button
        android:id="@+id/updatesavebutton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginLeft="160sp"
        android:background="#ffffff"
        android:text="Update"
        android:textColor="#000000"
        android:textSize="30sp" /&gt;

    &lt;Button
        android:id="@+id/updatecancelbutton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginLeft="100sp"
        android:background="#ffffff"
        android:text="Cancel"
        android:textColor="#000000"
        android:textSize="30sp" /&gt;

&lt;/TableRow&gt;
</code></pre>

<p></p>

<p>and my insert and update methods from datahelper class</p>

<pre><code>//inserting into employeetable

     public void insertDataIntoEmployee(String name_STR, String designation_STR, String phonenumber_STR, String age_STR, 
             String basicpay_STR, String pfdeduction_STR, String otherdeductions_STR) {
           System.out.println(" insertData start ");
           cv = new ContentValues();

           cv.put("ename", name_STR);
           cv.put("edesignation", designation_STR);
           cv.put("ephonenumber", phonenumber_STR);
           cv.put("eage", age_STR);
           cv.put("ebasic", basicpay_STR);
           cv.put("epf", pfdeduction_STR);
           cv.put("eotherdeductions", otherdeductions_STR);
               this.db.insert(EMPLOYEE_TABLE_NAME, null, cv);
               System.out.println(" insertData end ");
     }

     // updating the table

     public void updateDataIntoEmployee(long rowId ,String name_STR, String designation_STR, String phonenumber_STR, String age_STR, 
             String basicpay_STR, String pfdeduction_STR, String otherdeductions_STR) {
           System.out.println(" updateData start ");
           cv = new ContentValues();

           cv.put("ename", name_STR);
           cv.put("edesignation", designation_STR);
           cv.put("ephonenumber", phonenumber_STR);
           cv.put("eage", age_STR);
           cv.put("ebasic", basicpay_STR);
           cv.put("epf", pfdeduction_STR);
           cv.put("eotherdeductions", otherdeductions_STR);
               this.db.update(EMPLOYEE_TABLE_NAME, cv, EMPLOYEE_ID + "=" + rowId, null);
               System.out.println(" updateData end ");
     }
</code></pre>

<p>and my method in class where i have to display the populated edittexts is here</p>

<pre><code>public void onCreate(Bundle savedState) {
EditText editText = (EditText) findViewById(R.id.my_edittext);
String value = // Query your 'last value'.
editText.setText(value);
}
</code></pre>

<p>Now what can be the query which has to be passed  in string value which can be retrieved and also , am I supposed to rewrite this code every time for each edit texts? 
Is there anyway to avoid the redundancy?</p>

<p>Thank you </p>

## Answers
### Answer ID: 17875880
<p>You can try something like</p>

<pre><code>String[] mProjection = {/* All The Columns which you want to retrieve */};
Cursor cursor = this.db.query(EMPLOYEE_TABLE_NAME, mProjection, EMPLOYEE_NAME + "=?", new String[] { name_STR }, null, null, null);
</code></pre>

<p>This will return all the columns names in one shot and you can use whatever you wish. No need to query the db again and again.</p>

<p>After getting the cursor, </p>

<pre><code>if (cursor != null &amp;&amp; cursor.moveToNext()) {
    // you can store all the returned columns in a custom class here and return that class object
}
</code></pre>

