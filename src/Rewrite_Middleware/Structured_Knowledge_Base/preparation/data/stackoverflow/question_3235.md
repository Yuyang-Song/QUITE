# How can I query all products with their variation attributes?
[Link to question](https://stackoverflow.com/questions/72670990/how-can-i-query-all-products-with-their-variation-attributes)
**Creation Date:** 1655570297
**Score:** 0
**Tags:** django, django-orm
## Question Body
<p>I have following database schema:</p>
<p><a href="https://i.sstatic.net/7HdHm.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/7HdHm.png" alt="database schema" /></a></p>
<p>Django models:</p>
<pre><code>class Product(models.Model):
    name = models.CharField(max_length=150)
    # price and so on

class Size(models.Model):
    value = models.CharField(max_length=20)
    
class Color(models.Model):
    value = models.CharField(max_length=20)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name=&quot;variations&quot;)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
</code></pre>
<p>So I can write:</p>
<pre><code>product.variations
</code></pre>
<p>But I also want to be able to write</p>
<pre><code>product.sizes

product.colors
</code></pre>
<p>to get all sizes or colors that this product has in variation table</p>
<p>The problem that I'm trying to solve: I have product card list. And each card has options of sizes and colors to choose and to add to user's cart. I want to show the user sizes and colors that this particular product has in database to not list all the sizes and colors from database.</p>
<p><a href="https://i.sstatic.net/ARjnN.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/ARjnN.png" alt="enter image description here" /></a></p>
<p>But variations can have duplicates, for example, consider these combinations for some random product:</p>
<p>size - 40, color - red</p>
<p>size - 42, color - green</p>
<p>size - 44, color - red (again)</p>
<p>size - 42 (again), color - gray</p>
<p>I want to show the user
sizes: 40, 42, 44</p>
<p>colors: red, green, gray</p>
<p>At the moment I'm showing all of them with duplicates like</p>
<p>sizes: 40, 42, 44, 42</p>
<p>colors: red, green, red, gray</p>
<p>It is produced by this code and I don't know how to rewrite it:</p>
<pre><code>products: QuerySet[Product] = (
    Product.objects
        .prefetch_related(&quot;variations__size&quot;)
        .prefetch_related(&quot;variations__color&quot;)
        .all()[:15]
)
</code></pre>
<p>Then I iterate over products in my template without producing extra queries like</p>
<pre><code>{% for variation in product.variations.all %}
    variation.size.value
{% endfor %}
</code></pre>

## Answers
### Answer ID: 72674715
<p>It seems I've found a solution:</p>
<p>I used Prefetch object and its 3rd argument to_attr:</p>
<p><a href="https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.Prefetch" rel="nofollow noreferrer">https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.Prefetch</a></p>
<pre><code>products: QuerySet[Product] = (
    Product.objects
        .prefetch_related(Prefetch(
            &quot;variations&quot;,
            queryset=Variation.objects
                .select_related(&quot;size&quot;)
                .select_related(&quot;color&quot;)
                .distinct(&quot;color&quot;),
            to_attr=&quot;color_variations&quot;,
        ))
        .prefetch_related(Prefetch(
            &quot;variations&quot;,
            queryset=Variation.objects
                .select_related(&quot;size&quot;)
                .select_related(&quot;color&quot;)
                .distinct(&quot;size&quot;),
            to_attr=&quot;size_variations&quot;,
        ))
        .all()[:15]
)
</code></pre>

