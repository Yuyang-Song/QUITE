# Java Array Of Record Solution
[Link to question](https://stackoverflow.com/questions/29079661/java-array-of-record-solution)
**Creation Date:** 1426516984
**Score:** 0
**Tags:** java, arrays, storage
## Question Body
<p>I'm busy rewriting an Informix-4GL program in Java and I'm having some trouble with retrieving data from the database.</p>

<p>At the moment I am using SQLite3 for testing purposes and I am compiling and executing my code from the windows command line (not using any IDE at this point).</p>

<p>The problem I am having is that I am so used to using the Informix-4GL dynamic array of record such as below:</p>

<pre><code>dataArray dynamic array of record
   data_id     integer,
   data_name   char(15),
   data_desc   char(15)
end record
</code></pre>

<p>which I am able to populate as I please and then retrieve data (example the third row inserted) using</p>

<pre><code>display dataArray[3].data_id
</code></pre>

<p>I would like to know the recommended way of doing something similair in Java, is it possible to store data in a Java equivalent of the dynamic array of record and then select data from it using some form of identifier?</p>

<p>Here's how I did it in Informix-4GL to make it more clear</p>

<pre><code>main

   define

      lv_string string,                   # general variables
      lv_cnt integer,
      lr_table record like table.*,

      dataArray dynamic array of record   # the values I am storing in array
         data_id     integer,
         data_name   char(15),
         data_desc   char(15)
      end record

   let lv_string = "select * from table ",   # prepared statement 01
                   "where 1=1"
   prepare data_prep from lv_string
   declare data_curs cursor for data_prep

   let lv_string = "select * from table02 ",   # prepared statement 01
                   "where id = ?"
   prepare data02_prep from lv_string

   let lv_cnt = 0

   foreach data_curs into lr_table.*   # loop through sql return results

      let lv_cnt =  lv_cnt + 1

      let dataArray[lv_cnt].data_id = lr_table.id       # store variables
      let dataArray[lv_cnt].data_name = lr_table.name

      execute data02_prep using lr_table.id             # store variables from
         into dataArray[lv_cnt].data_desc               # different table

   end foreach

   if dataArray.getLength() = 5 then         # use the data I have stored
      display "there are 5 rows in here"
   end if

   if dataArray.getLength() = 17 then        # very flexible
      display dataArray[5].data_id,
              dataArray[9].data_name
              dataArray[14].data_desc
   end if

end main
</code></pre>

<p>This is not the actual program but I just took the features I would like to recreate in java.</p>

<p>What's great about this is that I can query the database once and close the connection, I won't need to query the database again for the entire duration of the program.</p>

## Answers
### Answer ID: 29081892
<p>I think in your case, using an ArrayList is far more easier. example</p>

<pre><code>public class Sample {
    List&lt;Data&gt; datas = new ArrayList&lt;Data&gt;();

    datas.add(new Data("1", "2" ,"3"));
    datas.add(new Data("4", "5" ,"6"));

    datas.get(0); // should give you the first data
}

class Data {
    Object id,name,desc;
    Data(Object id, Object name, Object desc) {
        this.id = id;
        this.name = name;
        this.desc = desc;
    }
}
</code></pre>

<p>by the way, i think the problem you have with HashMap (the one that you say got overridden) is because you didn't override equal and hashcode method as these two methods is used to place the object in HashMap.</p>

<p>Hope this is help you :D</p>

<p>=============</p>

<p>Assuming that your row variable is referring to ResultSet, then you could do this.</p>

<pre><code>public void doFill(ResultSet row) {
    while(row.next()) {
        datas.add(new Data(row.getObject("id"), row.getObject("name"), row.getObject("desc")));
    }
}
</code></pre>

### Answer ID: 29079855
<p>Use <code>HashMap</code>. It's basically a dictionary, array by key, ... whatever you want to call it, it's a key-value store where you can choose your key. HashMap has O(1) operations (theoretically) and forbids duplicate keys. Enjoy.</p>

