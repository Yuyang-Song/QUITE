# DRF multiple update with reduced database hits
[Link to question](https://stackoverflow.com/questions/74155522/drf-multiple-update-with-reduced-database-hits)
**Creation Date:** 1666364107
**Score:** 0
**Tags:** python, django, django-rest-framework
## Question Body
<p>I'm using DRF's example of multiple updates which works fine except every <code>self.child.update</code> is a separate update query to the database.</p>
<p>Is there a way I can rewrite this to call the updates as one query as a bulk update?</p>
<pre><code>class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            ret.append(self.child.update(book, data))

        return ret

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        list_serializer_class = BookListSerializer
</code></pre>

## Answers
### Answer ID: 74177444
<pre><code>A few suggestions:

 - Use ModelSerializer, as mentioned. It will handle updates/creates automatically and more efficiently.
 - Use model validation (clean methods) instead of serializer validation for database-level validation.
 - Use bulk_create for the creation case (instead of a loop).
 - Use select_related/prefetch_related to reduce queries when fetching the instance.
 - Use .update() or F-expressions to update fields, instead of re-getting the instance from the DB.
 - Use partial=True on the serializer if you expect partial updates.
</code></pre>

### Answer ID: 74155741
<p>Django has a command <code>bulk_update</code><br />
Docs: <a href="https://docs.djangoproject.com/en/4.1/ref/models/querysets/#bulk-update" rel="nofollow noreferrer">https://docs.djangoproject.com/en/4.1/ref/models/querysets/#bulk-update</a></p>
<p>I'd write up a full example but I'm not sure what <code>validated_data</code> looks like</p>

