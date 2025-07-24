# Django MySQL with ElasticSearch
[Link to question](https://stackoverflow.com/questions/40886251/django-mysql-with-elasticsearch)
**Creation Date:** 1480502600
**Score:** 1
**Tags:** django, elasticsearch
## Question Body
<p>I have a django app.</p>

<p>Data is stored in mysql database. There are many tables with many columns (100-200).</p>

<p>How can I use Elasticsearch to make search faster?</p>

<p>Do I need to rewrite all queries?</p>

<p>Links to tutorials will be helpful.</p>

## Answers
### Answer ID: 40886332
<p>Django Haystack is a popular library for integrating search into Django projects.</p>

<p>You can check out their "Getting Started Guide" here: <a href="http://django-haystack.readthedocs.io/en/v2.5.1/tutorial.html" rel="nofollow noreferrer">http://django-haystack.readthedocs.io/en/v2.5.1/tutorial.html</a></p>

<p>Edit: </p>

<p>You probably won't be able to find something that is a plug &amp; play solution and doesn't require you to touch any code. However integrating Haystack for a basic use-case doesn't require very much work.</p>

