# More efficient way of accessing/rewriting uploaded images
[Link to question](https://stackoverflow.com/questions/37943930/more-efficient-way-of-accessing-rewriting-uploaded-images)
**Creation Date:** 1466510660
**Score:** 0
**Tags:** php, mysql, .htaccess, mod-rewrite
## Question Body
<p>At the moment we currently store image uploads in the following directory and format:</p>

<p><code>/uploads/products/{product_id}.jpg</code></p>

<p>However, we don't want this <code>uploads</code> directory to be shown publicly, and nor do we want to expose a product's unique ID, so we rewrite the requested image URLs as follows (using .htaccess and PHP):</p>

<p><code>/images/products/{product_url}.jpg</code></p>

<p>For reference, this corresponds to the product in question, such as:</p>

<p><code>/products/{product_url}</code></p>

<p>This has advantages of hiding the original upload folder as well as the unique ID of each product, by rewriting the ID to the corresponding URL of that product (which is obviously public knowledge).</p>

<p>The rewriting part of this works great; we process each request via .htaccess and then use PHP to query the database based on the ID given and retrieve the product's URL. However, as this process can be called numerous times per page, the amount of connections to the database can be ridiculous and slow. On certain pages, we end up re-connecting to the database 20+ times, once for each product image requested, which feels completely wrong and probably isn't very efficient at all.</p>

<p>Is there a better way to manage this process? We'd still like to keep rewriting the images to show the URL of the product rather than expose the product's ID or indeed <code>uploads</code> folder, if possible.</p>

<p>I've thought of generating a JSON file with a list of ID => URL pairs and then parse this upon image request instead of re-connecting and querying the database, but I'm not sure if this would be a valid, faster alternative?</p>

<p>(I've also contemplated persistent database connections but I'd rather not go down that route for now, if any other viable solutions exist instead.)</p>

<p><strong>EDIT:</strong></p>

<p>Some more information might help. We currently use .htaccess to rewrite the above image requests to a single file, <code>image.php</code>:</p>

<p><code>RewriteRule ^images/products/(.*)$ image.php?url=$1 [L,QSA]</code></p>

<p>Every time an image is requested, this file is called, checking that the URL is valid, and if so displays the real file located under <code>/uploads/products/{product_id}.jpg</code>.</p>

<p>So every time a browser encounters an <code>&lt;img&gt;</code> tag pointing to <code>/images/products/...</code> it starts the rewrite/database process each time the image is loaded, which is what I'm questioning the efficiency of really (and hence a new database connection each time too).</p>

