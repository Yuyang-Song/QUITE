# Exclude a portfolio category from being displayed
[Link to question](https://stackoverflow.com/questions/18758863/exclude-a-portfolio-category-from-being-displayed)
**Creation Date:** 1378973458
**Score:** 0
**Tags:** php, wordpress, categories, portfolio
## Question Body
<p>I want to ask the Portfolio Page Template to exclude one portfolio category from being displayed in the portfolio. So when it shows the categories: All | Travel | Macro | Archive, etc. I need to exclude Archive (slug archive) from both the top filter and from the All feed, because I want to place that on a separate page called Archive.</p>

<p>How do I do that?</p>

<pre><code>&lt;?php
/*
Template Name: Portfolio number 1
*/
?&gt;
&lt;?php get_header(); ?&gt;

&lt;div class="container"&gt;

        &lt;div id="homecontent"&gt;

            &lt;ul id="portfolio-filter" class="filter clearfix"&gt;
                      &lt;li class="active"&gt;&lt;a href="javascript:void(0)" class="all"&gt;All&lt;/a&gt;&lt;/li&gt;

                      &lt;?php
                          // Get the taxonomy
                          $terms = get_terms('categories');
                                  $term_list = '';

                          // set a count to the amount of categories in our taxonomy
                          $count = count($terms); 

                          // set a count value to 0
                          $i=0;

                          // test if the count has any categories
                          if ($count &gt; 0) {

                              // break each of the categories into individual elements
                              foreach ($terms as $term) {

                                  // increase the count by 1
                                  $i++;

                                  // rewrite the output for each category
                                  $term_list .= '&lt;li&gt;&lt;a href="javascript:void(0)" class="'. $term-&gt;slug .'"&gt;' . $term-&gt;name . '&lt;/a&gt;&lt;/li&gt;';

                                  // if count is equal to i then output blank
                                  if ($count != $i)
                                  {
                                      $term_list .= '';
                                  }
                                  else 
                                  {
                                      $term_list .= '';
                                  }
                              }

                              // print out each of the categories in our new format
                              echo $term_list;
                          }
                      ?&gt;
                  &lt;/ul&gt;

                  &lt;div style="clear: both;"&gt;&lt;/div&gt;




                  &lt;ul id="portfolio-list" class="filterable-grid clearfix centerrow filter-posts"&gt;

                        &lt;?php 
                          // Set the page to be pagination
                          $paged = get_query_var('paged') ? get_query_var('paged') : 1;

                          // Query Out Database
                          $wpbp = new WP_Query(array( 'post_type' =&gt; 'myportfoliotype', 'posts_per_page' =&gt;'99', 'paged' =&gt; $paged ) ); 
                        ?&gt;

                        &lt;?php
                          // Begin The Loop
                          if ($wpbp-&gt;have_posts()) : while ($wpbp-&gt;have_posts()) : $wpbp-&gt;the_post(); 
                        ?&gt;

                        &lt;?php 
                          // Get The Taxonomy 'Filter' Categories "categories"
                          $terms = get_the_terms( get_the_ID(), 'categories' ); 
                        ?&gt;

                        &lt;?php 
                        $large_image =  wp_get_attachment_image_src( get_post_thumbnail_id(get_the_ID()), 'fullsize', false, '' ); 
                        $large_image = $large_image[0]; 
                        $another_image_1 = get_post_meta($post-&gt;ID, 'themnific_image_1_url', true);
                        $video_input = get_post_meta($post-&gt;ID, 'themnific_video_url', true);
                        $price = get_post_meta($post-&gt;ID, 'themnific_item_price', true);
                        $ribbon = get_post_meta($post-&gt;ID, 'themnific_class', true);
                        ?&gt;

                        &lt;li class="centerfourcol filter" data-id="id-&lt;?php echo $count; ?&gt;" data-type="&lt;?php foreach ($terms as $term) { echo strtolower(preg_replace('/\s+/', '-', $term-&gt;slug)). ' '; } ?&gt;"&gt;

                            &lt;?php get_template_part('/includes/folio-types/home_carousel'); ?&gt;

                        &lt;/li&gt;


                      &lt;?php $count++; // Increase the count by 1 ?&gt;     
                      &lt;?php endwhile; endif; // END the Wordpress Loop ?&gt;
                      &lt;?php wp_reset_query(); // Reset the Query Loop?&gt;

                  &lt;/ul&gt;
                  &lt;?php
                      /* 
                       * Download WP_PageNavi Plugin at: http://wordpress.org/extend/plugins/wp-pagenavi/
                       * Page Navigation Will Appear If Plugin Installed or Fall Back To Default Pagination
                      */        
                      if(function_exists('wp_pagenavi'))
                      {              
                          wp_pagenavi(array( 'query' =&gt; $wpbp ) );
                          wp_reset_postdata();  // avoid errors further down the page
                      }
                  ?&gt;
                  &lt;div style="clear: both;"&gt;&lt;/div&gt;

        &lt;/div&gt;&lt;!-- #homecontent --&gt;

&lt;/div&gt;

&lt;?php get_footer(); ?&gt;
</code></pre>

## Answers
### Answer ID: 18830070
<p>I found the answer, the code below only allows one categorie to be displayed in the portfolio.</p>

<pre><code>‘tax_query’ =&gt; array( array( ‘taxonomy’ =&gt; ‘categories’, ‘field’ =&gt; ‘slug’, ‘terms’ =&gt; ‘archive’, ‘operator’ =&gt; ‘IN’) ),
</code></pre>

