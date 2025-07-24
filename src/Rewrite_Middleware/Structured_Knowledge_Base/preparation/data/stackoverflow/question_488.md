# Laravel orWhereHas not working as expected
[Link to question](https://stackoverflow.com/questions/28241584/laravel-orwherehas-not-working-as-expected)
**Creation Date:** 1422639539
**Score:** 6
**Tags:** php, laravel-4, eloquent
## Question Body
<p>I'm trying to use the <code>orWhereHas</code> method in Laravel with nested relations, but I am not getting the result I expect. Am I misunderstanding how to use this method?</p>

<p>My relationships are set up as follows:</p>

<pre><code>Product
    -&gt; hasOne uniqueItem
        -&gt; hasMany fulfillmentCenterUniqueItems
    -&gt; hasMany skus
        -&gt; hasOne uniqueItem
            -&gt; hasMany fulfillmentCenterUniqueItems
</code></pre>

<p>I'm trying to test out the <code>whereHas</code> and <code>orWhereHas</code> methods by retrieving products from the database that contain <code>uniqueItems</code> that have a <code>uniqueItemFulfillmentCenter</code> with <code>id = 7089</code> OR products that contain a  <code>sku</code>, that contains a <code>uniqueItem</code>, that has a <code>uniqueItemFulfillmentCenter</code> with <code>id = 7412</code>.</p>

<p>Based on the data in my database, the result of this query should be two products. Product IDs 105 and 239.</p>

<p>Here's the Eloquent code I'm using:</p>

<pre><code>$product = Spire_models\Product
    ::whereHas('uniqueItem.fulfillmentCenterUniqueItems', function ($query)
    {
            $query-&gt;where('id', 7089);
    })
    -&gt;orWhereHas('skus.uniqueItem.fulfillmentCenterUniqueItems', function ($query)
    {
            $query-&gt;where('id', 7412);
    })
    -&gt;get()-&gt;toArray();
</code></pre>

<p>For some reason, this is only returning product ID 105, instead of 105 and 239. The generated sql from this function is:</p>

<pre><code>select * from `products` where `products`.`deleted_at` is null and (select count(*) from `unique_items` where `products`.`unique_item_id` = `unique_items`.`id` and (select count(*) from `fulfillment_center_unique_items` where `fulfillment_center_unique_items`.`unique_item_id` = `unique_items`.`id` and `id` = 7089 and `fulfillment_center_unique_items`.`deleted_at` is null) &gt;= 1 and `unique_items`.`deleted_at` is null) &gt;= 1 and (select count(*) from `skus` where `skus`.`product_id` = `products`.`id` and (select count(*) from `unique_items` where `skus`.`unique_item_id` = `unique_items`.`id` or (select count(*) from `fulfillment_center_unique_items` where `fulfillment_center_unique_items`.`unique_item_id` = `unique_items`.`id` and `id` = 7412 and `fulfillment_center_unique_items`.`deleted_at` is null) &gt;= 1 and `unique_items`.`deleted_at` is null) &gt;= 1 and `skus`.`deleted_at` is null) &gt;= 1
</code></pre>

<p>Is this sql being generated incorrectly, or am I misusing the <code>orWhereHas</code> method? To me it does not look like the <code>OR</code> statement is being placed correctly in the sql.</p>

<p>If I remove the <code>orWhereHas</code> method, things works as expected. For example, if I run this:</p>

<pre><code>$product = Spire_models\Product
    ::whereHas('uniqueItem.fulfillmentCenterUniqueItems', function ($query)
    {
            $query-&gt;where('id', 7089);
    })
    -&gt;get()-&gt;toArray();
</code></pre>

<p>I correctly get back product ID 105.  If I run this:</p>

<pre><code>$product = Spire_models\Product
    ::whereHas('skus.uniqueItem.fulfillmentCenterUniqueItems', function ($query)
    {
            $query-&gt;where('id', 7412);
    })
    -&gt;get()-&gt;toArray();
</code></pre>

<p>I correctly get back product ID 239. So the individual pieces of the query work correctly, but it seems when I try to combine these with an <code>orWhereHas</code>, I get unexpected results. Any idea why?</p>

<p><strong>EDIT</strong></p>

<p>As per the comments, it looks like this is a bug. I was able to temporarily work around it by rewriting the code to use <code>where</code> and <code>orWhere</code>.  Here's the temporary solution:</p>

<pre><code>$product = Spire_models\Product
    ::where(function ($query)
    {
            $query-&gt;whereHas('uniqueItem.fulfillmentCenterUniqueItems', function ($query)
            {
                    $query-&gt;where('id', 7089);
            });
    })
    -&gt;orWhere(function ($query)
    {
            $query-&gt;whereHas('skus.uniqueItem.fulfillmentCenterUniqueItems', function ($query)
            {
                    $query-&gt;where('id', 7412);
            });
    })
    -&gt;get()-&gt;toArray();
</code></pre>

## Answers
### Answer ID: 29600198
<p>It was a bug and is fixed by now with this PR <a href="https://github.com/laravel/framework/pull/8171" rel="nofollow">https://github.com/laravel/framework/pull/8171</a></p>

<p>It's been OK since version <strong>5.0.21</strong></p>

