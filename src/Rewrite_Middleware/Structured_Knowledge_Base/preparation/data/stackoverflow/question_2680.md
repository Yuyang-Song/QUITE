# Elasticsearch - how to apply sort on nested field
[Link to question](https://stackoverflow.com/questions/46938766/elasticsearch-how-to-apply-sort-on-nested-field)
**Creation Date:** 1508953105
**Score:** 1
**Tags:** elasticsearch, elasticsearch-query
## Question Body
<p>I'm rewriting the nested field in the documents and failing to get the query right to sort on the nested fields.</p>

<p>Previously I had the nested field like this:</p>

<pre><code>"my_nested_obj": {
        "project-type": [
          {
            "name": "Table",
            "value": "159841"
          }
        ],
        "cost": [
          {
            "name": "Under $50",
            "value": "426503"
          }
        ],
        "skill-level": [
          {
            "name": "Intermediate",
            "value": "63897"
          }
        ],
        "room": [
          {
            "name": "Outdoor",
            "value": "19246"
          }
        ]
      }....
</code></pre>

<p>And I was able to write queries like these where I can boost and also sort on the 'my_nested_obj' for example:</p>

<pre><code>    {
      "from": 0,
      "size": 50,
      "query": {
      "filtered": {
      "query": {
        "multi_match": {
            "query": "something",
            "fields": [
                "content",
                "name",
                "my_nested_obj.skill-level.name^3"
            ]
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "match_all": [

              ]
            },
            {
              "term": {
                "retired": false
              }
            }
          ]
        }
      }
    }
  },
      "sort": {
       "my_nested_obj.skill-level.name": "desc"
      },
      "timeout": "1800ms"
      }
</code></pre>

<p>Now, I need to reformat the nested field like:</p>

<pre><code> "my_nested_obj": [
        {
          "name": "Table",
          "type": "project-type",
          "value": "159841"
        },
        {
          "name": "Under $50",
          "type": "cost",
          "value": "426503"
        },
        {
          "name": "Intermediate",
          "type": "skill-level",
          "value": "63897"
        },
        {
          "name": "Outdoor",
          "type": "room",
          "value": "19246"
        }
      ]....
</code></pre>

<p>I can do a generic sort on my_nested_obj.name like:</p>

<pre><code>....
"sort": {
    "my_nested_obj.name": "desc"
 },
 ...
</code></pre>

<p>How do I go about adding for example sort specifically skill-level name and not all the <code>my_nested_obj.name</code>? Also is there some way to specify the boost?</p>

<p>Thanks!</p>

