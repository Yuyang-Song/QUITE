# While loop: Works, but also loops over HTML and outputs it twice (once in reverse?)
[Link to question](https://stackoverflow.com/questions/16492702/while-loop-works-but-also-loops-over-html-and-outputs-it-twice-once-in-revers)
**Creation Date:** 1368233576
**Score:** 0
**Tags:** php, html, mysql, loops, while-loop
## Question Body
<p>I have a while loop. It is supposed to loop through the database table and output the results found, which it does fine. However, it also duplicates the HTML in the while loop (outputting it twice, once in reverse??). </p>

<p>SEE: </p>

<blockquote>
  <p>1) Jazzminder Soundscape 2) 3) 1) 2) Jazzminder Dandelion 3)</p>
</blockquote>

<p>SHOULD READ:</p>

<blockquote>
  <p>1) Jazzminder Soundscape 2) Jazzminder Dandelion 3)</p>
</blockquote>

<p>I've tried tweaking and rewriting the code, but I can't isolate the problem. I've not had this problem before. </p>

<p>This is the block of code:  </p>

<pre><code> &lt;p&gt; &lt;a href="promote_next_step.php?promote=&lt;?php echo $_GET['promote']?&gt;"&gt;
&lt;strong&gt;        [More To Next Step]&lt;/strong&gt;&lt;/a&gt;&lt;/p&gt;
&lt;strong&gt;&lt;font color="gray"&gt;Included so far:&lt;/font&gt;&lt;/strong&gt;&lt;br/&gt;

&lt;?php 
  $sql2="SELECT * FROM `promote_track_lists` WHERE `promo_title`='".     $_GET['promote1']."'";
  $result2=mysql_query($sql2);
  while($row2 = mysql_fetch_assoc($result2)){
?&gt;
  1) &lt;font color="orange"&gt;&lt;strong&gt;&lt;?php echo $row2['artist_name1'] ?&gt; &lt;?php echo     $row2['track_title1'] ?&gt;&lt;/strong&gt;&lt;/font&gt;
  2) &lt;font color="orange"&gt;&lt;strong&gt;&lt;?php echo $row2['artist_name2'] ?&gt; &lt;?php echo     $row2['track_title2'] ?&gt;&lt;/strong&gt;&lt;/font&gt;
  3) &lt;font color="orange"&gt;&lt;strong&gt;&lt;?php echo $row2['artist_name3'] ?&gt; &lt;?php echo     $row2['track_title3'] ?&gt;&lt;/strong&gt;&lt;/font&gt;

&lt;?php 
  }
?&gt;
</code></pre>

<p>Thanks for the replies!! The thing is, I have another page which pulls the information from the database just fine:   </p>

<pre><code>  if (isset ($_GET['promote1']) === true) {
  $sql3="SELECT * FROM `promote_track_lists` where `promo_title`    ='".$_GET['promote1']."' "; 
  $result3= mysql_query ($sql3);
 while ($row3 = mysql_fetch_assoc ($result3)) {   
 ?&gt;
              &lt;div id="promotion_files"&gt;
              &lt;!------- track1 -------&gt;
               &lt;?php  if ($row3['iframe1']) {?&gt;
                &lt;div class="promotion_track_name"&gt;&lt;strong&gt;&lt;?php echo     $row3['artist_name1'] ?&gt;-&lt;?php echo $row3['track_title1'] ?&gt;&lt;/strong&gt;&lt;/div&gt;
                &lt;?php echo $row3['iframe1']?&gt;
                &lt;?php
                if (isset ($_POST['submit'])===true &amp;&amp; empty     ($_POST['feedback']) === false) {
                ?&gt;
                &lt;a href="mp3_download.php?promote1=&lt;?php echo     $row['title'] ?&gt;"&gt;&lt;img src='images/design images/iPodDownload.png' /&gt;&lt;/a&gt;
                &lt;?php
                }
                }
            ?&gt;
                           &lt;!------- track2 -------&gt; 
</code></pre>

<p>It does this 20 times without problem, but for some reason on the other page it loops over the HTML and outputs (just the html) twice. I've tried to work the database so that entries are completely unique from one another, but so that everything can be pulled with one query. ...If that makes sense. </p>

## Answers
### Answer ID: 16492821
<p>I'm going to take a stab at this but I could be wrong without the complete code. my guess is the problem is with your MySQL. according to what you are trying to output. one record would look like this</p>

<p>artist_name1 | artist_name2 | artist_name3 | track_title1 | track_title2 | track_title3</p>

<p>but based on what you are stating is the way your output is displaying, more than likely your table looks like this
artist_name | track_title</p>

<p>can you show me what your table looks like?</p>

<p>fyi it's not showing things in reverse, it's showing all 3 line 3 times but your only seeing one set of values each time. so your seeing 1 -data- 2 3 then 1 2 -data- 3 then 1 2 3 -data- I hope that makes sense</p>

<p>so looking at your image and the additional code you posted, I noticed this condition on the second block of code that isn't in your first block of code.</p>

<pre><code>            &lt;?php  if ($row3['iframe1']) {?&gt;
</code></pre>

<p>so my question for you is this. in your database if iframe2 is blank. is artist2 blank? if this is the case and based on what you described in your original email it looks like artist1 title1 and iframe1 all contains values but the rest of the values for that row is blank and in the next record in your table artist2 title2 and iframe2 is filled and the rest of the fields are blank and the same is true for the third.... IF this is the case then you need to do the following to your while loop...</p>

<pre><code>while($row2 = mysql_fetch_assoc($result2)){
     if ($row2['iframe1']) {?&gt;
  1) &lt;font color="orange"&gt;&lt;strong&gt;&lt;?php echo $row2['artist_name1'] ?&gt; &lt;?php echo     $row2['track_title1'] ?&gt;&lt;/strong&gt;&lt;/font&gt;
  &lt;?php  else if ($row2['iframe2']) {?&gt;
  2) &lt;font color="orange"&gt;&lt;strong&gt;&lt;?php echo $row2['artist_name2'] ?&gt; &lt;?php echo     $row2['track_title2'] ?&gt;&lt;/strong&gt;&lt;/font&gt;
  &lt;?php else if ($row2['iframe3']) {?&gt;

  3) &lt;font color="orange"&gt;&lt;strong&gt;&lt;?php echo $row2['artist_name3'] ?&gt; &lt;?php echo     $row2['track_title3'] ?&gt;&lt;/strong&gt;&lt;/font&gt;
  &lt;?php }
</code></pre>

<p>} ?></p>

### Answer ID: 16492872
<pre><code> &lt;p&gt; &lt;a href="promote_next_step.php?promote=&lt;?php echo $_GET['promote']?&gt;"&gt;
&lt;strong&gt;        [More To Next Step]&lt;/strong&gt;&lt;/a&gt;&lt;/p&gt;
&lt;strong&gt;&lt;font color="gray"&gt;Included so far:&lt;/font&gt;&lt;/strong&gt;&lt;br/&gt;

&lt;?php 
  $sql2="SELECT * FROM `promote_track_lists` WHERE `promo_title`='".$_GET['promote1']."'";
  $result2=mysql_query($sql2);

$s=1;

  while($row2 = mysql_fetch_assoc($result2))
  {
      echo $s.') &lt;font color="orange"&gt;&lt;strong&gt;'.$row2['artist_name1'].$row2['track_title1'] .'&lt;/strong&gt;&lt;/font&gt;';
      $s++;
  }
?&gt;
</code></pre>

<p>I think your database structure is messed up. Please post your table structure and which data your are entering to columns whenever you do insertion.</p>

