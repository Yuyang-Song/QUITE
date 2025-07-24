# Calculate intersection of two Django queries: one aggregate, another - simple
[Link to question](https://stackoverflow.com/questions/59940633/calculate-intersection-of-two-django-queries-one-aggregate-another-simple)
**Creation Date:** 1580169985
**Score:** 0
**Tags:** django, django-orm, python-2.x
## Question Body
<p>I have a model <code>VariantTag</code> that stores the <code>ids</code> of another model called <code>SavedVariant</code>. The former has another <code>variant_tag_type_id</code> that is pointing to its relative model type <code>VariantTagType</code>. Now I am trying to get all <code>SavedVariant</code> <code>ids</code> which have <code>only one</code> <code>variant_tag_type.name = 'Review'</code> tag. To make things clearer here is what I am trying to do in Django:</p>

<pre><code>    # Variants with just only one tag present                                                                          
    single_variant_ids = VariantTag.objects.values_list('saved_variant_id', flat=True) \                               
            .annotate(id_count=Count('saved_variant_id')).filter(id_count=1)                                           
    # All variants that have 'Review' tag                                                                              
    review_all_variant_ids = VariantTag.objects.filter(variant_tag_type__name='Review') \                              
            .values_list('saved_variant_id', flat=True)                                                                
    # Intersection of the previous two queries                                                                         
    review_variant_ids = single_variant_ids.intersection(review_all_variant_ids)
</code></pre>

<p>And this is not working giving me an error:</p>

<blockquote>
  <p>ProgrammingError: each INTERSECT query must have the same number of columns
  LINE 1: ...nttag"."saved_variant_id") = 1) INTERSECT (SELECT "seqr_vari...</p>
</blockquote>

<p>How could I write such a query in <code>Django</code>?</p>

<blockquote>
  <p>Update</p>
</blockquote>

<p>I used the advice of <code>Omar</code> and was able to eliminate the error by rewriting the second query like that:</p>

<pre><code>review_all_variant_ids = VariantTag.objects.filter(variant_tag_type__name='Review') \                              
                .values_list('saved_variant_id', flat=True).annotate(val=Value(0, output_field=IntegerField()))  
</code></pre>

<p>However, the <code>intersection</code> does not calculate intersection correctly instead just returning the empty <code>QuerySet</code>. I checked both <code>QuerySets</code> converting them to python <code>lists</code> and printing them out and here is what I see:</p>

<pre><code>single_variant_ids: [46, 28, 38, 30, 33, 29, 47, 31, 44]
review_all_variant_ids: [22, 36, 46, 47]
review_variant_ids: []
</code></pre>

<p>As you can see the intersection result should not be empty but should be a <code>QuerySet</code> with the values: <code>46</code> and <code>47</code>. I also tried to just write intersection like that:</p>

<pre><code>single_variant_ids &amp; review_all_variant_ids 
</code></pre>

<p>But it is giving an error:</p>

<blockquote>
  <p>TypeError: Merging 'QuerySet' classes must involve the same values in each case.</p>
  
  <p>Update</p>
</blockquote>

<p>I changed the name of the empty column of the second <code>QuerySet</code>:</p>

<pre><code>review_all_variant_ids = VariantTag.objects.filter(variant_tag_type__name='Review') \                              
                .values_list('saved_variant_id', flat=True).annotate(id_count=Value(0, output_field=IntegerField()))
</code></pre>

<p>After which the following worked:</p>

<pre><code>review_variant_ids = single_variant_ids &amp; review_all_variant_ids
</code></pre>

<p>But the result is wrong:</p>

<pre><code>[22, 36, 46, 47]
</code></pre>

<p>So, the intersection is performed in the wrong way here, not like I need. Of course, the easiest is just to convert both <code>QuerySets</code> to python <code>sets</code> and calculate their intersection but I want to avoid querying the database until the very last point.</p>

## Answers
### Answer ID: 60023856
<p>Initially, you had annotated the first query with <code>id_count</code> which means it will be a column in the result of the query, this column doesn't exist in the second query, you might just want to annotate it there as Value(0) to keep the columns consistent when intersecting.</p>

<p>Once you've done that, you can now try your initial attempt at intersection or you can try this filter: </p>

<pre><code>single_variant_ids.filter(saved_variant_id__in=review_all_variant_ids.values_list('saved_variant_id'))
</code></pre>

<p>All the best</p>

