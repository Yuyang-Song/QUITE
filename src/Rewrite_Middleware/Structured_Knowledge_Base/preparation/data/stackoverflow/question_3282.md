# How to delete duplicate rows from a table using Django ORM?
[Link to question](https://stackoverflow.com/questions/75059549/how-to-delete-duplicate-rows-from-a-table-using-django-orm)
**Creation Date:** 1673278447
**Score:** 0
**Tags:** django, postgresql, orm, duplicates
## Question Body
<p>I have a database table <code>bad_reviews</code> and a corresponding Django model <code>BadReviews</code>. I want to delete duplicate records based on the fields <code>client_id</code>, <code>survey_id</code>, <code>text</code>, <code>rating</code>, <code>privacy_agreement</code>. I've come up with this query which works:</p>
<pre><code>SELECT br.*
FROM bad_reviews br
JOIN (
    SELECT client_id, survey_id, text, rating, privacy_agreement, COUNT(*)
    FROM bad_reviews
    GROUP BY client_id, survey_id, text, rating, privacy_agreement
    HAVING count(*) &gt; 1
) dupes
ON br.client_id = dupes.client_id
AND br.survey_id = dupes.survey_id
AND br.text = dupes.text
AND br.rating = dupes.rating
AND br.privacy_agreement = dupes.privacy_agreement
ORDER BY br.client_id, br.survey_id, br.text, br.rating, br.privacy_agreement, br.id
</code></pre>
<p>How to rewrite it using Django ORM?</p>

## Answers
### Answer ID: 75060002
<p>I hope this will work.</p>
<pre class="lang-py prettyprint-override"><code>from django.db.models import Count, Subquery


#  Equivalent of this query in with Django ORM: SELECT client_id, survey_id, text, rating, privacy_agreement, COUNT(*)
#     FROM bad_reviews
#     GROUP BY client_id, survey_id, text, rating, privacy_agreement
#     HAVING count(*) &gt; 1
subquery = BadReviews.objects \
        .values('client_id', 'survey_id', 'text', 'rating', 'privacy_agreement') \
        .annotate(count=Count('id')).filter(count__gt=1)

# use the subquery as a filter in the main query
bad_reviews = BadReviews.objects.filter(
    client_id=Subquery(subquery.values('client_id')),
    survey_id=Subquery(subquery.values('survey_id')),
    text=Subquery(subquery.values('text')),
    rating=Subquery(subquery.values('rating')),
    privacy_agreement=Subquery(subquery.values('privacy_agreement')),
).order_by('client_id', 'survey_id', 'text', 'rating', 'privacy_agreement', 'id')


</code></pre>

