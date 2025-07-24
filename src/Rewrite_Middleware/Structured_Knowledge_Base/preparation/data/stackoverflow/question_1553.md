# Is it a good idea to modify fields in Model instances returned in a QuerySet? Will it kill performance?
[Link to question](https://stackoverflow.com/questions/9453245/is-it-a-good-idea-to-modify-fields-in-model-instances-returned-in-a-queryset-wi)
**Creation Date:** 1330260945
**Score:** 0
**Tags:** django, django-templates, django-views
## Question Body
<p>So, my problem is this. I have a legacy MySQL database that I'm building a shiny new Django application over. For whatever reason, some fairly daft design decisions were made—such as all fields, no matter what they contain, being stored as varchars—but because since other systems that I'm not rewriting depend on that same data I can't destructively change that schema at all.</p>

<p>I want to treat a certain field—the stock quantity on hand—as an integer, so that in my template I can check its amount and display a relevant value (basically, if there are more than 100 items available, I want to just display "100+ Available").</p>

<p>The existing value for stock quantity is stored as, oddly, a varchar holding a float (as if it's possible to have fractional amounts of an item in stock):</p>

<pre><code>item.qty: u"72.0"
</code></pre>

<p>Now, I figure as a worst case I can use QuerySet.values(), and iterate over the results, replacing each stock quantity with an int() parsed version of itself. Something like ...</p>

<pre><code>item_list = items.values()
for item in item_list:
    item['qty'] = int(float(item['qty']))
</code></pre>

<p>... but won't that cause my QuerySet to evaluate itself completely? I confess to being fairly ignorant of the process by which Django handles lazy execution of queries, but it seems like working with actual values would mean evaluating the query before it needs to.</p>

<p>So, am I complaining about nothing (I mean, it's definitely evaluating these values in the template anyway), or is there a better way to do what I need to do?</p>

## Answers
### Answer ID: 9453588
<p>Yes, iterating through in the view would evaluate the entire queryset. That may or not be what you want - for example, if you're paginating, the paginator limits the query automatically, so you don't want to evaluate the whole thing separately.</p>

<p>I would approach this in a different way, by calling a function in the template to format the data. You can either do this with a method on the model, if there's just one field you want to format:</p>

<pre><code>class Item(models.Model):
    ...
    def get_formatted_qty(self):
        return int(float(self.qty))
</code></pre>

<p>and call it:</p>

<pre><code>{{ item.get_formatted_qty }}
</code></pre>

<p>Or, to make it more general, you can define a custom filter in your templatetags:</p>

<pre><code>@register.filter
def format_value(value):
    return int(float(value))


{{ item.qty|format }}
</code></pre>

