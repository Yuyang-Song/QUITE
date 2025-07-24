# Convert array of paths into UL list
[Link to question](https://stackoverflow.com/questions/4903668/convert-array-of-paths-into-ul-list)
**Creation Date:** 1296859541
**Score:** 10
**Tags:** php, recursion, path, tree
## Question Body
<p>I have a table in a database that contains a variety of paths to pages of my website. Each path is listed only one time. I currently have a very long and convoluted series of queries and PHP to pull all these and rewrite the data into an unordered list (to create a menu for my website). It seems that there is probably a relatively simple looping approach that would work MUCH more efficiently, but I cannot seem to get anything working.  I have found TONS of PHP scripts that create UL lists from file trees, but all of them either don't work or can't handle the inherently not recursive nature of my query results (some require multi-dimensional arrays of my paths, which would be fine except for my trouble with creating those). I did find a script that works pretty close, but it formats the <code>&lt;ul&gt;</code> portion incorrectly by placing sub-lists outside of the <code>&lt;li&gt;</code> section (I will explain below)</p>

<p>Here is a sample:</p>

<p>DB returns the following in results array:</p>

<pre><code>about/contact/
about/contact/form/
about/history/
about/staff/
about/staff/bobjones/
about/staff/sallymae/
products/
products/gifts/
products/widgets/
</code></pre>

<p>and I want to create the following output:</p>

<pre><code>&lt;ul&gt;
  &lt;li&gt;about/
  &lt;ul&gt;
    &lt;li&gt;about/contact/
    &lt;ul&gt;
      &lt;li&gt;about/contact/form/&lt;/li&gt;
    &lt;/ul&gt;
    &lt;/li&gt;
    &lt;li&gt;about/history/&lt;/li&gt;
    &lt;li&gt;about/staff/
    &lt;ul&gt;
      &lt;li&gt;about/staff/bobjones/&lt;/li&gt;
      &lt;li&gt;about/staff/sallymae/&lt;/li&gt;
    &lt;/ul&gt;
    &lt;/li&gt;
  &lt;/ul&gt;
  &lt;/li&gt;
  &lt;li&gt;products/
  &lt;ul&gt;
    &lt;li&gt;products/gifts/&lt;/li&gt;
    &lt;li&gt;products/widgets/&lt;/li&gt;
  &lt;/ul&gt;
  &lt;/li&gt;
&lt;/ul&gt;
</code></pre>

<p>So I got very close with a script found here:  <a href="http://www.daniweb.com/forums/thread285916.html" rel="nofollow">http://www.daniweb.com/forums/thread285916.html</a>  but I have run into a problem. It turns out that the script that I found creates improperly formatted UL lists. In a CORRECT situation, a sub-list is contained within the <code>&lt;li&gt;</code> of the parent element. In this scripting, the parent <code>&lt;li&gt;</code> is closed and then a <code>&lt;ul&gt;</code> block is inserted. The overall script is actually fairly elegant in the way that it keeps up with the levels and such, but I cannot wrap my head around it enough to figure out how to fix it. I have the whole thing in a function here:</p>

<pre><code>function generateMainMenu()
{
  global $db;

  $MenuListOutput = '';
  $PathsArray = array();

  $sql = "SELECT PageUrlName FROM `table`";
  $result = mysql_query($sql, $db) or die('MySQL error: ' . mysql_error());
  while ($PageDataArray = mysql_fetch_array($result))
  {
    $PathsArray[] = rtrim($PageDataArray['PageUrlName'],"/"); //this function does not like paths to end in a slash, so remove trailing slash before saving to array
  }

  sort($PathsArray);// These need to be sorted.
  $MenuListOutput .= '&lt;ul id="nav"&gt;'."\n";//get things started off right
  $directories=array ();
  $topmark=0;
  $submenu=0;
  foreach ($PathsArray as $value) {
    // break up each path into it's constituent directories
    $limb=explode("/",$value);
    for($i=0;$i&lt;count($limb);$i++) {
      if ($i+1==count($limb)){
        // It's the 'Leaf' of the tree, so it needs a link
        if ($topmark&gt;$i){
          // the previous path had more directories, therefore more Unordered Lists.
          $MenuListOutput .= str_repeat("&lt;/ul&gt;",$topmark-$i); // Close off the Unordered Lists
          $MenuListOutput .= "\n";// For neatness
        }
        $MenuListOutput .= '&lt;li&gt;&lt;a href="/'.$value.'"&gt;'.$limb[$i]."&lt;/a&gt;&lt;/li&gt;\n";// Print the Leaf link
        $topmark=$i;// Establish the number of directories in this path
      }else{
        // It's a directory
        if($directories[$i]!=$limb[$i]){
          // If the directory is the same as the previous path we are not interested.
          if ($topmark&gt;$i){// the previous path had more directories, therefore more Unordered Lists.
            $MenuListOutput .= str_repeat("&lt;/ul&gt;",$topmark-$i);// Close off the Unordered Lists
            $MenuListOutput .= "\n";// For neatness
          }

          // (next line replaced to avoid duplicate listing of each parent)
          //$MenuListOutput .= "&lt;li&gt;".$limb[$i]."&lt;/li&gt;\n&lt;ul&gt;\n";
          $MenuListOutput .= "&lt;ul&gt;\n";
          $submenu++;// Increment the dropdown.
          $directories[$i]=$limb[$i];// Mark it so that if the next path's directory in a similar position is the same, it won't be processed.
        }
      }
    }
  }
  $MenuListOutput .= str_repeat("&lt;/ul&gt;",$topmark+1);// Close off the Unordered Lists

  return $MenuListOutput."\n\n\n";
}
</code></pre>

<p>and it returns something like this:</p>

<pre><code>&lt;ul id="nav"&gt;
&lt;li&gt;&lt;a href="/about"&gt;about&lt;/a&gt;&lt;/li&gt;
&lt;ul&gt;
&lt;li&gt;&lt;a href="/about/history"&gt;history&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="/about/job-opportunities"&gt;job-opportunities&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="/about/mission"&gt;mission&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="/about/privacy-policy"&gt;privacy-policy&lt;/a&gt;&lt;/li&gt;
&lt;/ul&gt;
&lt;li&gt;&lt;a href="/giftcards"&gt;giftcards&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="/locations"&gt;locations&lt;/a&gt;&lt;/li&gt;
&lt;ul&gt;
&lt;li&gt;&lt;a href="/locations/main-office"&gt;main-office&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="/locations/branch-office"&gt;branch-office&lt;/a&gt;&lt;/li&gt;
&lt;/ul&gt;
&lt;li&gt;&lt;a href="/packages"&gt;packages&lt;/a&gt;&lt;/li&gt;
&lt;/ul&gt;
</code></pre>

<p>Anyone have an idea of where I need to add in some additional logic and how I can accomplish this? Other ideas on a better way to do this?  It seems like this is such a common issue that there would be a simple/standard method of handling something like this.  Maybe if I could figure out how to create a multi-dimensional array from my paths then those could be iterated to make this work?</p>

<hr />

<p><strong>EDIT: More Complex :-(</strong></p>

<p>I tried casablanca's response and it worked perfectly...except I then realized that now I have a follow-up to make things more difficult. In order to display the "name" of the page, I need to also have that info in the array, thus the path probably works better as the array key and the name in the value. Any thoughts on changing like this:</p>

<pre><code>$paths = array(
    "about/contact/ " =&gt; "Contact Us", 
    "about/contact/form/ " =&gt; "Contact Form",
    "about/history/ " =&gt; "Our History",
    "about/staff/ " =&gt; "Our Staff",
    "about/staff/bobjones/ " =&gt; "Bob",
    "about/staff/sallymae/ " =&gt; "Sally",
    "products/ " =&gt; "All Products",
    "products/gifts/ " =&gt; "Gift Ideas!",
    "products/widgets/ " =&gt; "Widgets"
);
</code></pre>

<p>and then using something like this line within the <code>buildUL</code> function:</p>

<pre><code>echo '&lt;a href="'.$prefix.$key.'/"&gt;'.$paths[$prefix.$key].'&lt;/a&gt;';
</code></pre>

## Answers
### Answer ID: 4904365
<p><strong>Edit:</strong></p>

<p>Changed to cater for updated question.</p>

<p>I'm using an array index of <code>__title</code> to hold the page title. As long as you never have a directory in your tree called <code>__title</code> this should be fine. You're free to change this sentinel value to anything you wish however.</p>

<p>I have also changed it so the list building function returns a string, so that you can store the value for use later in your page. (You can of course just do <code>echo build_list(build_tree($paths))</code> to output the list directly.</p>

<pre><code>&lt;?php

$paths = array(
    'about/contact/' =&gt; 'Contact Us', 
    'about/contact/form/' =&gt; 'Contact Form',
    'about/history/' =&gt; 'Our History',
    'about/staff/' =&gt; 'Our Staff',
    'about/staff/bobjones/' =&gt; 'Bob',
    'about/staff/sallymae/' =&gt; 'Sally',
    'products/' =&gt; 'All Products',
    'products/gifts/' =&gt; 'Gift Ideas!',
    'products/widgets/' =&gt; 'Widgets'
);

function build_tree($path_list) {
    $path_tree = array();
    foreach ($path_list as $path =&gt; $title) {
        $list = explode('/', trim($path, '/'));
        $last_dir = &amp;$path_tree;
        foreach ($list as $dir) {
            $last_dir =&amp; $last_dir[$dir];
        }
        $last_dir['__title'] = $title;
    }
    return $path_tree;
}

function build_list($tree, $prefix = '') {
    $ul = '';
    foreach ($tree as $key =&gt; $value) {
        $li = '';
        if (is_array($value)) {
            if (array_key_exists('__title', $value)) {
                $li .= "$prefix$key/ &lt;a href=\"/$prefix$key/\"&gt;${value['__title']}&lt;/a&gt;";
            } else {
                $li .= "$prefix$key/";
            }
            $li .= build_list($value, "$prefix$key/");
            $ul .= strlen($li) ? "&lt;li&gt;$li&lt;/li&gt;" : '';
        }
    }
    return strlen($ul) ? "&lt;ul&gt;$ul&lt;/ul&gt;" : '';
}

$tree = build_tree($paths);
$list = build_list($tree);
echo $list;

?&gt;
</code></pre>

### Answer ID: 4903871
<p>Indeed a multi-dimensional would help here. You can build one by splitting each path into components and using those to index into the array. Assuming <code>$paths</code> is your initial array, the code below will build a multi-dimensional array <code>$array</code> with keys corresponding to the path components:</p>

<pre><code>$array = array();
foreach ($paths as $path) {
  $path = trim($path, '/');
  $list = explode('/', $path);
  $n = count($list);

  $arrayRef = &amp;$array; // start from the root
  for ($i = 0; $i &lt; $n; $i++) {
    $key = $list[$i];
    $arrayRef = &amp;$arrayRef[$key]; // index into the next level
  }
}
</code></pre>

<p>You can then iterate over this array using a recursive function, which you can use to naturally build a recursive UL list as in your example. In each recursive call, <code>$array</code> is a sub-array of the entire array this is being currently processed and <code>$prefix</code> is the path from the root to the current sub-array:</p>

<pre><code>function buildUL($array, $prefix) {
  echo "\n&lt;ul&gt;\n";
  foreach ($array as $key =&gt; $value) {
    echo "&lt;li&gt;";
    echo "$prefix$key/";
    // if the value is another array, recursively build the list
    if (is_array($value))
      buildUL($value, "$prefix$key/");
    echo "&lt;/li&gt;\n";
  }
  echo "&lt;/ul&gt;\n";
}
</code></pre>

<p>The initial call would simply be <code>buildUL($array, '')</code>.</p>

