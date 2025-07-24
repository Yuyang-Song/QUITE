# Wordpress portfolio page display only images from certain filter
[Link to question](https://stackoverflow.com/questions/17582080/wordpress-portfolio-page-display-only-images-from-certain-filter)
**Creation Date:** 1373495496
**Score:** 0
**Tags:** php, wordpress
## Question Body
<p>I have been following many tutorials on a portfolio which uses quicksand.js to do a filter animation. In the function i can create filters (categories) with slugs. I can't, after endless hour of reading, figure out how to only display the thumbnails from a certain filter. </p>

<p>I've included the parts of the portfolio from my <code>functions.php</code></p>

<p>I know this is a lot of code, but this is a last resort. I can't get it working so i am hoping some php / wordpress guru might point out something i've missed. </p>

<p>Through reading up on it, i did managed to pull out JUST the featured images posted in 'featured' by using:</p>

<pre><code>&lt;?php
$args = array(
    'post_type' =&gt; 'portfolio',
    'tax_query' =&gt; array(
        array(
            'taxonomy' =&gt; 'filter',
            'field' =&gt; 'slug',
            'terms' =&gt; 'featured'
        )
    )
);
$query = new WP_Query( $args );
?&gt;
</code></pre>

<p>However, this just pulls out the image and it's title, without the formatted HTML i need. But applying this to what i already use is where i get completely lost.</p>

<p>Thanks in advance. </p>

<p><strong>My Index.php</strong></p>

<pre><code>h2&gt;Featured Work&lt;/h2&gt;



&lt;ul id="image_gallery" class="group index_gallery filterable-grid"&gt;
&lt;?php 

    // Query Out Database
    $wpbp = new WP_Query(array( 'post_type' =&gt; 'portfolio', 'posts_per_page' =&gt;'9' ) ); 
?&gt;

&lt;?php 

 $terms = get_terms("filter");
 $count = count($terms);
 if ( $count &gt; 0 ){
     echo "&lt;ul&gt;";
     foreach ( $terms as $term ) {
       echo "&lt;li&gt;" . $term-&gt;name . "&lt;/li&gt;";

     }
     echo "&lt;/ul&gt;";
 }
?&gt;

&lt;?php
    // Begin The Loop
    if ($wpbp-&gt;have_posts()) : while ($wpbp-&gt;have_posts()) : $wpbp-&gt;the_post(); 
?&gt;

&lt;?php 
    // Get The Taxonomy 'Filter' Categories
    $terms = get_the_terms( get_the_ID(), 'filter' ); 
?&gt;

&lt;?php 
$large_image =  wp_get_attachment_image_src( get_post_thumbnail_id(get_the_ID()), 'fullsize', false, '' ); 
$large_image = $large_image[0]; 
?&gt;

        &lt;?php
            //Apply a data-id for unique indentity, 
            //and loop through the taxonomy and assign the terms to the portfolio item to a data-type,
            // which will be referenced when writing our Quicksand Script
        ?&gt;
&lt;li class="gallery_image" data-id="id-&lt;?php echo $count; ?&gt;" data-type="&lt;?php foreach ($terms as $term) { echo strtolower(preg_replace('/\s+/', '-', $term-&gt;name)). ' '; } ?&gt;"&gt;
        &lt;?php 
            // Check if wordpress supports featured images, and if so output the thumbnail
            if ( (function_exists('has_post_thumbnail')) &amp;&amp; (has_post_thumbnail()) ) : 
        ?&gt;
            &lt;?php // Output the featured image ?&gt;
            &lt;a rel="prettyPhoto[gallery]" class="zoom" href="&lt;?php echo $large_image ?&gt;"&gt;
                &lt;img class="mag" src="&lt;?php bloginfo('template_url'); ?&gt;/imgs/mag.png"/&gt;&lt;div class="thumb_bg"&gt;&lt;/div&gt;&lt;?php the_post_thumbnail('portfolio'); ?&gt;
            &lt;/a&gt;                                    

        &lt;?php endif; ?&gt; 
        &lt;!--&lt;?php // Output the title of each portfolio item ?&gt;
        &lt;p&gt;&lt;a href="&lt;?php the_permalink(); ?&gt;"&gt;&lt;?php echo get_the_title(); ?&gt;&lt;/a&gt;&lt;/p&gt;--&gt;
&lt;/li&gt;
&lt;?php $count++; // Increase the count by 1 ?&gt;       
&lt;?php endwhile; endif; // END the Wordpress Loop ?&gt;
&lt;?php wp_reset_query(); // Reset the Query Loop?&gt;
&lt;/ul&gt;

&lt;div class="gallery_control"&gt;
    &lt;a href="&lt;?php echo home_url(); ?&gt;/portfolio/" class="gallery-btn artwork"&gt;&lt;span class="icon-search"&gt;&lt;/span&gt;View more&lt;/a&gt;
&lt;/div&gt;
&lt;?php
$taxonomy = 'filter';
  $terms = get_terms( $taxonomy, '' );
  if ($terms) {
    foreach($terms as $term) {
        echo '&lt;p&gt;' . '&lt;a href="' . esc_attr(get_term_link($term, $taxonomy)) . '" title="' . sprintf( __( "View all posts in %s" ), $term-&gt;name ) . '" ' . '&gt;' . $term-&gt;name.'&lt;/a&gt; has ' . $term-&gt;count . ' post(s). &lt;/p&gt; ';
    }
  }
?&gt;
</code></pre>

<p><strong>Portfolio workings:</strong></p>

<pre><code>// function: post_type BEGIN  
        function post_type()  
        {  
        $labels = array(  
            'name' =&gt; __( 'Portfolio'),   
            'singular_name' =&gt; __('Portfolio'),  
            'rewrite' =&gt; array(  
                'slug' =&gt; __( 'portfolio' )   
            ),  
            'add_new' =&gt; _x('Add Item', 'portfolio'),   
            'edit_item' =&gt; __('Edit Portfolio Item'),  
            'new_item' =&gt; __('New Portfolio Item'),   
            'view_item' =&gt; __('View Portfolio'),  
            'search_items' =&gt; __('Search Portfolio'),   
            'not_found' =&gt;  __('No Portfolio Items Found'),  
            'not_found_in_trash' =&gt; __('No Portfolio Items Found In Trash'),  
            'parent_item_colon' =&gt; ''  
        );  
            $args = array(  
            'labels' =&gt; $labels,  
            'public' =&gt; true,  
            'publicly_queryable' =&gt; true,  
            'show_ui' =&gt; true,  
            'query_var' =&gt; true,  
            'rewrite' =&gt; true,  
            'capability_type' =&gt; 'post',  
            'hierarchical' =&gt; false,  
            'menu_position' =&gt; null,  
            'supports' =&gt; array(  
                'title',  
                'editor',  
                'thumbnail'  
            )  
        ); 

        register_post_type(__( 'portfolio' ), $args);  

    } // function: post_type END  

    // function: portfolio_messages BEGIN  
    function portfolio_messages($messages)  
    {  
        $messages[__( 'portfolio' )] =   
            array(  
                0 =&gt; '',   
                1 =&gt; sprintf(('Portfolio Updated. &lt;a href="%s"&gt;View portfolio&lt;/a&gt;'), esc_url(get_permalink($post_ID))),  
                2 =&gt; __('Custom Field Updated.'),  
                3 =&gt; __('Custom Field Deleted.'),  
                4 =&gt; __('Portfolio Updated.'),  
                5 =&gt; isset($_GET['revision']) ? sprintf( __('Portfolio Restored To Revision From %s'), wp_post_revision_title((int)$_GET['revision'], false)) : false,  
                6 =&gt; sprintf(__('Portfolio Published. &lt;a href="%s"&gt;View Portfolio&lt;/a&gt;'), esc_url(get_permalink($post_ID))),  
                7 =&gt; __('Portfolio Saved.'),  
                8 =&gt; sprintf(__('Portfolio Submitted. &lt;a target="_blank" href="%s"&gt;Preview Portfolio&lt;/a&gt;'), esc_url( add_query_arg('preview', 'true', get_permalink($post_ID)))),  
                9 =&gt; sprintf(__('Portfolio Scheduled For: &lt;strong&gt;%1$s&lt;/strong&gt;. &lt;a target="_blank" href="%2$s"&gt;Preview Portfolio&lt;/a&gt;'), date_i18n( __( 'M j, Y @ G:i' ), strtotime($post-&gt;post_date)), esc_url(get_permalink($post_ID))),  
                10 =&gt; sprintf(__('Portfolio Draft Updated. &lt;a target="_blank" href="%s"&gt;Preview Portfolio&lt;/a&gt;'), esc_url( add_query_arg('preview', 'true', get_permalink($post_ID)))),  
            );  
        return $messages;  

    } // function: portfolio_messages END  

    // function: portfolio_filter BEGIN  
    function portfolio_filter()  
    {  
        register_taxonomy(  
            __( "filter" ),  
            array(__( "portfolio" )),  
            array(  
                "hierarchical" =&gt; true,  
                "label" =&gt; __( "Filter" ),  
                "singular_label" =&gt; __( "Filter" ),  
                "rewrite" =&gt; array(  
                    'slug' =&gt; 'filter',  
                    'hierarchical' =&gt; true  
                )  
            )  
        );  
    } // function: portfolio_filter END  

    add_action( 'init', 'post_type' );  
    add_action( 'init', 'portfolio_filter', 0 );  
    add_filter( 'post_updated_messages', 'portfolio_messages' ); 
</code></pre>

## Answers
### Answer ID: 17625208
<p>This is the code I use to get full image and thumb of attached images:</p>

<pre><code>  $args = array(
    'order' =&gt; 'ASC',
    'post_mime_type' =&gt; 'image',
    'post_parent' =&gt; $post-&gt;ID,
    'post_status' =&gt; null,
    'post_type' =&gt; 'attachment',

  );

  $upload_dir = wp_upload_dir();
  $upload_url = $upload_dir['baseurl'];


  // Get img data
  $attachments    = get_children( $args );
  $images = array();

  // Loop through attached images and get thumb + large img url
  foreach($attachments as $attachment) {
    $image_attributes = wp_get_attachment_image_src( $attachment-&gt;ID, 'thumbnail' );
    $img['thumb'] = $image_attributes[0];
    $image_attributes = wp_get_attachment_image_src( $attachment-&gt;ID, 'large' );
    $img['large'] = $image_attributes[0];
    array_push($images,$img);
  }

  // Get the image that you have set as the featured image in the post
  $featured_img = wp_get_attachment_url(get_post_thumbnail_id($post-&gt;ID));
  $featured_img_thumb = wp_get_attachment_image_src( get_post_thumbnail_id($post-&gt;ID), 'thumbnail' );
</code></pre>

### Answer ID: 17625199
<p>I found a solution:</p>

<pre><code>&lt;?php
$args = array(
    'post_type' =&gt; 'project',
    'tax_query' =&gt; array(
        array(
            'taxonomy' =&gt; 'filter',
            'field' =&gt; 'slug',
            'terms' =&gt; 'featured'
        )
    )
);
$query = new WP_Query( $args );
?&gt;
</code></pre>

<p>Only displays my filtered item with a name of featured. </p>

### Answer ID: 17582482
<p>I am not sure what you are doing here but change this</p>

<pre><code>&lt;?php 
$large_image =  wp_get_attachment_image_src( get_post_thumbnail_id(get_the_ID()), 'fullsize', false, '' ); 
$large_image = $large_image[0]; 
?&gt;
</code></pre>

<p>to this</p>

<pre><code>&lt;?php 
$large_images[] =  wp_get_attachment_image_src( get_post_thumbnail_id(get_the_ID()), 'fullsize', false, '' ); 
$large_image = $large_images[0]; 
?&gt;
</code></pre>

