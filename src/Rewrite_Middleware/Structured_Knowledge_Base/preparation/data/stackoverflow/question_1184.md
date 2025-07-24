# Embed another database on WordPress page &amp; manipulate the database queries using GET method
[Link to question](https://stackoverflow.com/questions/62439975/embed-another-database-on-wordpress-page-manipulate-the-database-queries-using)
**Creation Date:** 1592436563
**Score:** 1
**Tags:** wordpress
## Question Body
<p>I am using WordPress on my website. I have another, separate database on the website filled with data that I wish to query directly on a WordPress page that I created. I've read through forums and still cannot find a method that works.</p>

<p>So far I have done the following:</p>

<p>Installed a PHP Code Snippets plugin that allows me to embed PHP on WordPress pages. Simple code like <code>echo "Hello, World!";</code> works fine when embedded on the page.</p>

<p>The issue seems to be connecting to the database. A sample of my code is below. I will also need to be able to manipulate the database queries using the GET method. Is this possible? I don't want to have to rewrite my database application in order to include it on a WordPress page.</p>

<p>The code below is simply embedded on the WordPress page using the plugin.</p>

<pre><code>// Set the database access information as constants:
DEFINE ('DB_USER', 'admin');
DEFINE ('DB_PASSWORD', '1234');
DEFINE ('DB_HOST', 'localhost');
DEFINE ('DB_NAME', 'example_database_name');

// Make the connection:
$dbc = @mysqli_connect (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) OR die ();

// Set the encoding...
mysqli_set_charset($dbc, 'utf8');

// Process user selection of surface type
if(isset($_GET['surface_type'])) {
    $form_error = false;

    $surface_type = mysqli_real_escape_string($dbc, trim($_GET["surface_type"]));   

    if ($surface_type == "all") {
        // User wants to see all sheets brand
        $sql3 = "SELECT * FROM sheet_brands ORDER BY brand_name ASC";
    } else {
        // User has selected a certain surface type
        $sql3 = "SELECT * FROM sheet_brands WHERE surface_type=$surface_type ORDER BY brand_name ASC";
    }

    // User has selected a sheet brand
    if (isset($_GET['brand_name'])) {
        $brand_name = mysqli_real_escape_string($dbc, trim($_GET["brand_name"]));  
    }
}
</code></pre>

## Answers
### Answer ID: 62440626
<p>You must manually create a new instance of the wpdb class with right settings for your other database.</p>

<p>From the wpdb Codex page:</p>

<blockquote>
  <p>**More Information ** 
  An instantiated wpdb class can talk to any number of tables, but only to one database at >a time. In
  the rare case you need to connect to another database, instantiate
  your own object from the wpdb class with your own database connection
  information.</p>
</blockquote>

