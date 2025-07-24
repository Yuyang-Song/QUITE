# Create function from a mysql query
[Link to question](https://stackoverflow.com/questions/48460548/create-function-from-a-mysql-query)
**Creation Date:** 1516966372
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>I have a specific query which is reading the 5 latest articles out of my database for category (mysql column) "sport"</p>

<p>I would like to run mulitiple queries, one for sport, one for cars, one for books, etc. Instead of rewriting the full query multiple times and replace the category sport by cars/books etc I would like to know if it possible to rebuild it to a function in which I input the category (like sports in line 2) and it outputs a string $sports (like in line 10/11) with all retrieves from the database as defined in the query.</p>

<pre><code>// Build feed source for the latest News of Sport
$sqlCommand = "SELECT * FROM feeds where category like 'Sport' ORDER BY id DESC LIMIT 5"; 
$query = mysqli_query($myConnection, $sqlCommand) or die (mysqli_error()); 

$sport = '';
while ($row = mysqli_fetch_array($query)) { 
    $fid1 = $row["id"];
    $title1 = $row["title"];
    $description1 = $row["description"];
    $sport .= '&lt;h2&gt;&lt;b&gt;&lt;a href="detail/' . $fid1 . '/' . $title1 . '" title="' . $title1 . '"&gt;' . $title1 . '&lt;/a&gt;&lt;/b&gt;&lt;/h2&gt;';
    $sport .= '&lt;a href="detail/' . $fid1 . '/' . $title1 . '" title="' . $title1 . '"&gt;' . $description1 . '&lt;/a&gt;&lt;br/&gt;';

} 
mysqli_free_result($query);
</code></pre>

## Answers
### Answer ID: 48585943
<p>This is how I finally resolved it:</p>

<pre><code>function nieuws ($category,$color) {

    global $myConnection;
    $sqlCommand = "SELECT * FROM feeds where category like '$category' ORDER BY id DESC LIMIT 1"; 
    $query = mysqli_query($myConnection, $sqlCommand) or die (mysqli_error()); 
    $output = '';
    $output = "&lt;div class=headlines style=background:$color&gt;&lt;a class=newslink href='$category'&gt;$category&lt;/a&gt;&lt;/div&gt;";
    while ($row = mysqli_fetch_array($query)) { 
        $fid1 = $row["id"];
        $title1 = $row["title"];
        $titleseo1 = seofy($title1);
        $description1 = $row["description"];
        $photo1 = $row["photo"];
        if ('' == $photo1) {$photo1='images/pic1.jpg';};
        $output .= "&lt;div class=news2 style=background:#F0F8FF&gt;&lt;img src='$photo1' alt='photo' style='width:200px;height:150px;object-fit:cover;border:0;margin:0px 5px 0px 0px;float:left'&gt;"; //object-fit: cover zorgt dat het origineel het plaatje vult zonder distortion, is in principe cropping
        $output .= '&lt;b&gt;&lt;a href="detail/' . $fid1 . '/' . $titleseo1 . '" title="' . $title1 . '"&gt;' . $title1 . '&lt;/a&gt;&lt;/b&gt;&lt;/br&gt;';
        $output .= '&lt;a href="detail/' . $fid1 . '/' . $titleseo1 . '" title="' . $title1 . '"&gt;' . $description1 . '&lt;/a&gt;&lt;br/&gt;';
        $output .= "&lt;/div&gt;";
        } 
        mysqli_free_result($query);
}
</code></pre>

