# How to pull in custom post type categories?
[Link to question](https://stackoverflow.com/questions/23666573/how-to-pull-in-custom-post-type-categories)
**Creation Date:** 1400108510
**Score:** 0
**Tags:** wordpress, categories, custom-post-type, taxonomy
## Question Body
<p>Having the hardest time with my custom post types and retriving categories...</p>

<p>I have two custom post types that are registered and working so far:  RV Rentals, and RV Sales. </p>

<p>I just need a template page that pulls in all the categories for RV sales, but I can't get this to work... the code seems to just be pulling in categories for RV Rentals, even though it should just be displaying ALL CPT categories for RV Rentals and RV Sales. Going insane trying to figure out how to have it ONLY pull in RV sales... can someone please help?  I realize this is a lot of code I've posted but really don't know what is wrong here... losing my mind. </p>

<p>This is the functions file I have that registers my RV sales custom post type:</p>

<pre><code>/* ------------------------------
CPT RV SALES  
------------------------------*/

add_action('init','create_rvsales_post_type'); 

function create_rvsales_post_type() {
$labels = array(
    'name' =&gt; 'RV Sales',
    'singular_name' =&gt; 'RV Sales',
);
$args = array(
    'labels' =&gt; $labels,
    'public' =&gt; true,
    'exclude_from_search' =&gt; false,
    'publicly_queryable' =&gt; true,
    'show_ui' =&gt; true, 
    'show_in_nav_menus' =&gt; false, 
    'show_in_menu' =&gt; true,
    'show_in_admin_bar' =&gt; true,
    'menu_position' =&gt; 20,
    'menu_icon' =&gt; null,
    'capability_type' =&gt; 'post',
    'hierarchical' =&gt; false,
    'supports' =&gt; array('title','thumbnail','editor'),
    'has_archive' =&gt; 'motorhomes-for-sale',
    'rewrite' =&gt; array('slug' =&gt; 'motorhomes-for-sale/%rvsales_cats%'),
    'query_var' =&gt; true,
    'can_export' =&gt; true,
); 
register_post_type('rv_sales',$args);
}

 //setup tax
 add_action( 'init', 'create_rvsales_taxonomies', 0 ); 


 function create_rvsales_taxonomies() 
 {
 $labels = array(
 'name' =&gt; _x( 'RV Sales Categories', 'taxonomy general name' ),
 'singular_name' =&gt; _x( 'RV Sales Category', 'taxonomy singular name' ),
  );

   register_taxonomy('rvsales_cats',array('rv_sales'), array(
  'hierarchical' =&gt; true,
  'labels' =&gt; $labels,
  'show_ui' =&gt; true,
  'query_var' =&gt; true,
  'rewrite' =&gt; array( 'slug' =&gt; 'motorhomes-for-sale' ),
    ));

 }

 register_taxonomy_for_object_type('category', 'rv_sales');

 //get that nice url structure
 function filter_post_type_link2($link, $post) {
 if (!in_array($post -&gt; post_type, array(
         'rv_sales',
     )))
     return $link;


 if ($catsegors = get_the_terms($post -&gt; ID, 'rvsales_cats')) {
    $link = str_replace('%rvsales_cats%', array_pop($catsegors) -&gt; slug, $link); 
}

 return $link;
}

 add_filter('post_type_link2', 'filter_post_type_link2', 10, 2); 
</code></pre>

<p>Here's the template I have, that should be calling in ALL CPT categories (From RV SALES and RV Rentals), but it still just pulls in the categories from RV Rentals even when there's a bogus parameter in the 'rv_salesblah' for get_categories:</p>

<pre><code>&lt;?php 
                // get all the categories from the database
                    $cats = get_categories('rv_salesblah'); 
                    // loop through the categries
                    foreach ($cats as $cat) {

                    // setup the cateogory ID
                    $cat_id= $cat-&gt;term_id;

                    // Make a header for the category
                    echo "&lt;h2&gt;".$cat-&gt;name."&lt;/h2&gt;";

                    // create a custom wordpress query
                    query_posts("cat=$cat_id&amp;posts_per_page=100");

                    // start the wordpress loop!
                    if (have_posts()) : while (have_posts()) :     the_post();     ?&gt;

                    &lt;?php // create our link now that the post is setup ?&gt;
                    &lt;a href="&lt;?php the_permalink();?&gt;"&gt;&lt;?php the_title(); ?&gt;&lt;/a&gt;
                    &lt;?php echo '&lt;hr/&gt;'; ?&gt;

                &lt;?php endwhile; endif; // done our wordpress loop. Will start again for    each         category ?&gt;
                &lt;?php } // done the foreach statement ?&gt;
</code></pre>

<p>EDIT: Fixed this, if some sorry soul comes across this same issue, this is the code I used to get me on the right track:</p>

<pre><code> &lt;?php
 //for a given post type, return all
  $post_type = 'rv_sales';
$tax = 'rvsales_cats';
$tax_terms = get_terms($tax);
if ($tax_terms) {
foreach ($tax_terms  as $tax_term) {
 $args=array(
  'post_type' =&gt; $post_type,
  "$tax" =&gt; $tax_term-&gt;slug,
  'post_status' =&gt; 'publish',
  'posts_per_page' =&gt; -1,
  'caller_get_posts'=&gt; 1
);

$my_query = null;
$my_query = new WP_Query($args);
if( $my_query-&gt;have_posts() ) {
  echo 'List of  '. $tax_term-&gt;name;
  while ($my_query-&gt;have_posts()) : $my_query-&gt;the_post(); ?&gt;
    &lt;p&gt;&lt;a href="&lt;?php the_permalink() ?&gt;" rel="bookmark" title="Permanent Link to &lt;?php     the_title_attribute(); ?&gt;"&gt;&lt;?php the_title(); ?&gt;&lt;/a&gt;&lt;/p&gt;
    &lt;?php
   endwhile;
}
 wp_reset_query();
}
}
?&gt;
</code></pre>

## Answers
### Answer ID: 25073172
<p>EDIT: Fixed this, if some sorry soul comes across this same issue, this is the code I used to get me on the right track:</p>

<pre><code> ?php
 //for a given post type, return all
 $post_type = 'rv_sales';
$tax = 'rvsales_cats';
$tax_terms = get_terms($tax);
if ($tax_terms) {
foreach ($tax_terms  as $tax_term) {
 $args=array(
 'post_type' =&gt; $post_type,
  "$tax" =&gt; $tax_term-&gt;slug,
   'post_status' =&gt; 'publish',
  'posts_per_page' =&gt; -1,
   'caller_get_posts'=&gt; 1
);

 $my_query = null;
$my_query = new WP_Query($args);
if( $my_query-&gt;have_posts() ) {
 echo 'List of  '. $tax_term-&gt;name;
 while ($my_query-&gt;have_posts()) : $my_query-&gt;the_post(); ?&gt;
&lt;p&gt;&lt;a href="&lt;?php the_permalink() ?&gt;" rel="bookmark" title="Permanent Link to &lt;?php          the_title_attribute(); ?&gt;"&gt;&lt;?php the_title(); ?&gt;&lt;/a&gt;&lt;/p&gt;
   &lt;?php
  endwhile;
}
wp_reset_query();
}
}
?&gt;
</code></pre>

