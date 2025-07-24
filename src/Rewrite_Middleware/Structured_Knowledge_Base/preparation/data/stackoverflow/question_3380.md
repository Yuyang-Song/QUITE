# WooCommerce: Product permalink base mishandled by theme if matches slug for custom shop Page
[Link to question](https://stackoverflow.com/questions/77887759/woocommerce-product-permalink-base-mishandled-by-theme-if-matches-slug-for-cust)
**Creation Date:** 1706287154
**Score:** 0
**Tags:** wordpress, woocommerce, url-rewriting, permalinks, taxonomy-terms
## Question Body
<p><strong>Background:</strong> I have published a web site with a custom shop storefront Page, and erroneously left the WooCommerce &quot;shop page&quot; setting empty.  While this produced the expected results on our local development environment, after pushing the files and database to our web hosting environment I encountered inconsistencies with handling of rewrite_rules.
I had to correct this problem as per the directives provided in this previous Question/Answer:
<a href="https://stackoverflow.com/q/77886695/4087434">WooCommerce Permalinks: Rewrite Rules not generating as expected</a></p>
<p><strong>Zain's answer worked, however</strong> the custom shop page I designed is now mishandling the product permalink custom base.  This page was created using our (Avada) theme's &quot;Fusion builder&quot; (a WYSIWYG interface) which provides various &quot;Elements&quot; to choose and configure when designing a page.</p>
<p>In this case, I chose a design Element (named &quot;Post Cards&quot;) which I configured to display the products in a grid.  This was achieved by using the WYSIWYG interface to build a query whereby the post type selected is &quot;Products&quot; and the taxonomy selected is &quot;Product Categories&quot;, with several categories selected for inclusion.</p>
<p>The interface also allows me to specify how many products will appear before the user is offered a &quot;load more&quot; button.  When pressed, this button is supposed to render additional rows below what was displayed when the page was loaded.</p>
<p>For whatever reason, this &quot;Element&quot; of our page builder is now telling WordPress to run a query which only returns a number of products equal to the number of grid slots (rows / columns) visible when the page is loaded.  Pressing &quot;Load more Products&quot; yields the error message &quot;No additional items found.&quot;</p>
<p>Yet, if I increase the number of products to be initially displayed from 6 to 60, the Element renders all 35 of our products on the first page load.</p>
<p><strong>I tried changing the product Permalink base</strong> to /product/ instead of /shop/, suspecting a conflict because the page which contains this custom storefront code also has a slug of /shop/.  Using /shop/ as both a Page slug and as the product permalink base <em>did not</em> create problems on our local environment.</p>
<p>However, when I try changing the product permalink base from /shop/ to /product/ (the default), the Page I built at /shop/ begins to correctly load all of our products without any of the problems I mentioned.</p>
<p>But, changing the product permalink back to /shop/ again returns the storefront Page I designed with a slug of /shop/ to the broken state I described.</p>
<p>What could be responsible for this?</p>

