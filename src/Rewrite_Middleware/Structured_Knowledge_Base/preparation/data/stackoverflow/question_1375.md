# Druid query in Power BI shows errors
[Link to question](https://stackoverflow.com/questions/73417703/druid-query-in-power-bi-shows-errors)
**Creation Date:** 1660916458
**Score:** 0
**Tags:** powerbi, m, druid
## Question Body
<p>I've got a problem connecting my report with a Druid database, based on a query that runs perfectly in Postman.</p>
<p>So the original Druid query is this:</p>
<pre><code>curl -L -X POST 'https://api.xxxxxxxxxxxxxxxx' -H 'Content-Type: application/json' -H 'Authorization: Bearer xxxxxxx' --data-raw '{ &quot;query&quot;:{
&quot;metrics&quot;: [
    {
        &quot;type&quot;: &quot;count&quot;,
        &quot;filter&quot;: {
            &quot;type&quot;: &quot;and&quot;,
            &quot;children&quot;: [
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;event.type&quot;,
                    &quot;value&quot;: &quot;check-point&quot;
                },
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;check_point.name&quot;,
                    &quot;value&quot;: &quot;Start of article&quot;
                }
            ]
        },
        &quot;values&quot;: {
            &quot;main&quot;: &quot;value&quot;
        },
        &quot;name&quot;: &quot;Początek strony artykułowej&quot;,
        &quot;clicked&quot;: false,
        &quot;id&quot;: 2,
        &quot;enabled&quot;: true
    },
    {
        &quot;type&quot;: &quot;count&quot;,
        &quot;filter&quot;: {
            &quot;type&quot;: &quot;and&quot;,
            &quot;children&quot;: [
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;event.type&quot;,
                    &quot;value&quot;: &quot;check-point&quot;
                },
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;check_point.name&quot;,
                    &quot;value&quot;: &quot;Start of article content&quot;
                }
            ]
        },
        &quot;values&quot;: {
            &quot;main&quot;: &quot;value&quot;
        },
        &quot;name&quot;: &quot;Początek treści&quot;,
        &quot;clicked&quot;: false,
        &quot;id&quot;: 3,
        &quot;enabled&quot;: true
    },
    {
        &quot;type&quot;: &quot;count&quot;,
        &quot;filter&quot;: {
            &quot;type&quot;: &quot;and&quot;,
            &quot;children&quot;: [
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;event.type&quot;,
                    &quot;value&quot;: &quot;check-point&quot;
                },
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;check_point.name&quot;,
                    &quot;value&quot;: &quot;Start of article lead&quot;
                }
            ]
        },
        &quot;values&quot;: {
            &quot;main&quot;: &quot;value&quot;
        },
        &quot;name&quot;: &quot;Początek leadu&quot;,
        &quot;clicked&quot;: false,
        &quot;id&quot;: 4,
        &quot;enabled&quot;: true
    },
    {
        &quot;type&quot;: &quot;count&quot;,
        &quot;filter&quot;: {
            &quot;type&quot;: &quot;and&quot;,
            &quot;children&quot;: [
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;event.type&quot;,
                    &quot;value&quot;: &quot;check-point&quot;
                },
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;check_point.name&quot;,
                    &quot;value&quot;: &quot;Start of article text&quot;
                }
            ]
        },
        &quot;values&quot;: {
            &quot;main&quot;: &quot;value&quot;
        },
        &quot;name&quot;: &quot;Początek tekstu&quot;,
        &quot;clicked&quot;: false,
        &quot;id&quot;: 6,
        &quot;enabled&quot;: true
    },
    {
        &quot;type&quot;: &quot;count&quot;,
        &quot;filter&quot;: {
            &quot;type&quot;: &quot;and&quot;,
            &quot;children&quot;: [
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;event.type&quot;,
                    &quot;value&quot;: &quot;check-point&quot;
                },
                {
                    &quot;type&quot;: &quot;eq&quot;,
                    &quot;field&quot;: &quot;check_point.name&quot;,
                    &quot;value&quot;: &quot;End of article&quot;
                }
            ]
        },
        &quot;values&quot;: {
            &quot;main&quot;: &quot;value&quot;
        },
        &quot;name&quot;: &quot;Koniec tekstu&quot;,
        &quot;clicked&quot;: false,
        &quot;id&quot;: 13,
        &quot;enabled&quot;: true
    }
],
&quot;from&quot;: &quot;TvH38YhQ0u5d&quot;,
&quot;top&quot;: 10,
&quot;granularity&quot;: &quot;all&quot;,
&quot;realtime&quot;: false,
&quot;intervals&quot;: {
    &quot;dates&quot;: [
        &quot;2022-06-03T00:00:00.000&quot;,
        &quot;2022-06-04T00:00:00.000&quot;
    ],
    &quot;translatedFrom&quot;: &quot;2022-06-03T00:00:00+02:00/2022-06-03T23:59:59+02:00&quot;,
    &quot;strict&quot;: true
},
&quot;timeZoneOffset&quot;: -120,
&quot;dashboard&quot;: {
    &quot;_id&quot;: &quot;62e0e9e3d65b2200087afe93&quot;,
    &quot;name&quot;: &quot;{OS} Kontrolne&quot;,
    &quot;type&quot;: &quot;default&quot;,
    &quot;organizationId&quot;: &quot;5c666b78c66c847f427326e0&quot;,
    &quot;createdAt&quot;: &quot;2022-07-27T07:31:47.723Z&quot;,
    &quot;owner&quot;: &quot;myemail@mycompany.com&quot;,
    &quot;__v&quot;: 0,
    &quot;privilege&quot;: &quot;edit&quot;,
    &quot;dashboardId&quot;: &quot;62e0e9e3d65b2200087afe93&quot;
},
&quot;offset&quot;: 0,
&quot;splits&quot;: [
    {
        &quot;name&quot;: &quot;ID&quot;,
        &quot;field&quot;: &quot;mycustomvalue.article.id&quot;,
        &quot;regex&quot;: &quot;&quot;,
        &quot;id&quot;: 10
    }
],
&quot;order&quot;: [
    {
        &quot;metricIndex&quot;: 0,
        &quot;ascending&quot;: false
    }
],
&quot;filters&quot;: {
    &quot;type&quot;: &quot;and&quot;,
    &quot;children&quot;: [
        {
            &quot;type&quot;: &quot;eq&quot;,
            &quot;field&quot;: &quot;event.type&quot;,
            &quot;value&quot;: &quot;check-point&quot;
        },
        {
            &quot;type&quot;: &quot;eq&quot;,
            &quot;field&quot;: &quot;page.domain&quot;,
            &quot;value&quot;: &quot;mycustomvalue.pl&quot;
        },
        {
            &quot;type&quot;: &quot;eq&quot;,
            &quot;field&quot;: &quot;user.device.crawler.miscellaneous.iscrawler&quot;,
            &quot;value&quot;: &quot;false&quot;
        },
        {
            &quot;type&quot;: &quot;gt&quot;,
            &quot;field&quot;: &quot;source.mycustomvalue.article.id&quot;,
            &quot;value&quot;: &quot;0&quot;
        }
    ]
}}}'
</code></pre>
<p>And this works in Postman.</p>
<p>However when I try to rewrite it to M, I am getting errors (most often &quot;invalid identifier&quot; after &quot;query&quot;.</p>
<pre><code>let 

RequestBody =Json.Document(Text.ToBinary(&quot;{&quot; &quot;&quot;query&quot;&quot;:{
    &quot;&quot;metrics&quot;&quot;: [
        {
            &quot;&quot;type&quot;&quot;: &quot;&quot;count&quot;&quot;,
            &quot;&quot;filter&quot;&quot;: {
                &quot;&quot;type&quot;&quot;: &quot;&quot;and&quot;&quot;,
                &quot;&quot;children&quot;&quot;: [
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;event.type&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;check-point&quot;&quot;
                    },
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;check_point.name&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;Start of article&quot;&quot;
                    }
                ]
            },
            &quot;&quot;values&quot;&quot;: {
                &quot;&quot;main&quot;&quot;: &quot;&quot;value&quot;&quot;
            },
            &quot;&quot;name&quot;&quot;: &quot;&quot;Początek strony artykułowej&quot;&quot;,
            &quot;&quot;clicked&quot;&quot;: false,
            &quot;&quot;id&quot;&quot;: 2,
            &quot;&quot;enabled&quot;&quot;: true
        },
        {
            &quot;&quot;type&quot;&quot;: &quot;&quot;count&quot;&quot;,
            &quot;&quot;filter&quot;&quot;: {
                &quot;&quot;type&quot;&quot;: &quot;&quot;and&quot;&quot;,
                &quot;&quot;children&quot;&quot;: [
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;event.type&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;check-point&quot;&quot;
                    },
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;check_point.name&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;Start of article content&quot;&quot;
                    }
                ]
            },
            &quot;&quot;values&quot;&quot;: {
                &quot;&quot;main&quot;&quot;: &quot;&quot;value&quot;&quot;
            },
            &quot;&quot;name&quot;&quot;: &quot;&quot;Początek treści&quot;&quot;,
            &quot;&quot;clicked&quot;&quot;: false,
            &quot;&quot;id&quot;&quot;: 3,
            &quot;&quot;enabled&quot;&quot;: true
        },
        {
            &quot;&quot;type&quot;&quot;: &quot;&quot;count&quot;&quot;,
            &quot;&quot;filter&quot;&quot;: {
                &quot;&quot;type&quot;&quot;: &quot;&quot;and&quot;&quot;,
                &quot;&quot;children&quot;&quot;: [
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;event.type&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;check-point&quot;&quot;
                    },
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;check_point.name&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;Start of article lead&quot;&quot;
                    }
                ]
            },
            &quot;&quot;values&quot;&quot;: {
                &quot;&quot;main&quot;&quot;: &quot;&quot;value&quot;&quot;
            },
            &quot;&quot;name&quot;&quot;: &quot;&quot;Początek leadu&quot;&quot;,
            &quot;&quot;clicked&quot;&quot;: false,
            &quot;&quot;id&quot;&quot;: 4,
            &quot;&quot;enabled&quot;&quot;: true
        },
        {
            &quot;&quot;type&quot;&quot;: &quot;&quot;count&quot;&quot;,
            &quot;&quot;filter&quot;&quot;: {
                &quot;&quot;type&quot;&quot;: &quot;&quot;and&quot;&quot;,
                &quot;&quot;children&quot;&quot;: [
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;event.type&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;check-point&quot;&quot;
                    },
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;check_point.name&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;Start of article text&quot;&quot;
                    }
                ]
            },
            &quot;&quot;values&quot;&quot;: {
                &quot;&quot;main&quot;&quot;: &quot;&quot;value&quot;&quot;
            },
            &quot;&quot;name&quot;&quot;: &quot;&quot;Początek tekstu&quot;&quot;,
            &quot;&quot;clicked&quot;&quot;: false,
            &quot;&quot;id&quot;&quot;: 6,
            &quot;&quot;enabled&quot;&quot;: true
        },
        {
            &quot;&quot;type&quot;&quot;: &quot;&quot;count&quot;&quot;,
            &quot;&quot;filter&quot;&quot;: {
                &quot;&quot;type&quot;&quot;: &quot;&quot;and&quot;&quot;,
                &quot;&quot;children&quot;&quot;: [
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;event.type&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;check-point&quot;&quot;
                    },
                    {
                        &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                        &quot;&quot;field&quot;&quot;: &quot;&quot;check_point.name&quot;&quot;,
                        &quot;&quot;value&quot;&quot;: &quot;&quot;End of article&quot;&quot;
                    }
                ]
            },
            &quot;&quot;values&quot;&quot;: {
                &quot;&quot;main&quot;&quot;: &quot;&quot;value&quot;&quot;
            },
            &quot;&quot;name&quot;&quot;: &quot;&quot;Koniec tekstu&quot;&quot;,
            &quot;&quot;clicked&quot;&quot;: false,
            &quot;&quot;id&quot;&quot;: 13,
            &quot;&quot;enabled&quot;&quot;: true
        }
    ],
    &quot;&quot;from&quot;&quot;: &quot;&quot;TvH38YhQ0u5d&quot;&quot;,
    &quot;&quot;top&quot;&quot;: 10,
    &quot;&quot;granularity&quot;&quot;: &quot;&quot;all&quot;&quot;,
    &quot;&quot;realtime&quot;&quot;: false,
    &quot;&quot;intervals&quot;&quot;: {
        &quot;&quot;dates&quot;&quot;: [
            &quot;&quot;2022-06-03T00:00:00.000&quot;&quot;,
            &quot;&quot;2022-06-04T00:00:00.000&quot;&quot;
        ],
        &quot;&quot;translatedFrom&quot;&quot;: &quot;&quot;2022-06-03T00:00:00+02:00/2022-06-03T23:59:59+02:00&quot;&quot;,
        &quot;&quot;strict&quot;&quot;: true
    },
    &quot;&quot;timeZoneOffset&quot;&quot;: -120,
    &quot;&quot;dashboard&quot;&quot;: {
        &quot;&quot;_id&quot;&quot;: &quot;&quot;62e0e9e3d65b2200087afe93&quot;&quot;,
        &quot;&quot;name&quot;&quot;: &quot;&quot;{OS} Kontrolne&quot;&quot;,
        &quot;&quot;type&quot;&quot;: &quot;&quot;default&quot;&quot;,
        &quot;&quot;organizationId&quot;&quot;: &quot;&quot;5c666b78c66c847f427326e0&quot;&quot;,
        &quot;&quot;createdAt&quot;&quot;: &quot;&quot;2022-07-27T07:31:47.723Z&quot;&quot;,
        &quot;&quot;owner&quot;&quot;: &quot;&quot;myemail@mycompany.com&quot;&quot;,
        &quot;&quot;__v&quot;&quot;: 0,
        &quot;&quot;privilege&quot;&quot;: &quot;&quot;edit&quot;&quot;,
        &quot;&quot;dashboardId&quot;&quot;: &quot;&quot;62e0e9e3d65b2200087afe93&quot;&quot;
    },
    &quot;&quot;offset&quot;&quot;: 0,
    &quot;&quot;splits&quot;&quot;: [
        {
            &quot;&quot;name&quot;&quot;: &quot;&quot;ID&quot;&quot;,
            &quot;&quot;field&quot;&quot;: &quot;&quot;mycustomvalue.article.id&quot;&quot;,
            &quot;&quot;regex&quot;&quot;: &quot;&quot;&quot;&quot;,
            &quot;&quot;id&quot;&quot;: 10
        }
    ],
    &quot;&quot;order&quot;&quot;: [
        {
            &quot;&quot;metricIndex&quot;&quot;: 0,
            &quot;&quot;ascending&quot;&quot;: false
        }
    ],
    &quot;&quot;filters&quot;&quot;: {
        &quot;&quot;type&quot;&quot;: &quot;&quot;and&quot;&quot;,
        &quot;&quot;children&quot;&quot;: [
            {
                &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                &quot;&quot;field&quot;&quot;: &quot;&quot;event.type&quot;&quot;,
                &quot;&quot;value&quot;&quot;: &quot;&quot;check-point&quot;&quot;
            },
            {
                &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                &quot;&quot;field&quot;&quot;: &quot;&quot;page.domain&quot;&quot;,
                &quot;&quot;value&quot;&quot;: &quot;&quot;mycustomvalue.pl&quot;&quot;
            },
            {
                &quot;&quot;type&quot;&quot;: &quot;&quot;eq&quot;&quot;,
                &quot;&quot;field&quot;&quot;: &quot;&quot;user.device.crawler.miscellaneous.iscrawler&quot;&quot;,
                &quot;&quot;value&quot;&quot;: &quot;&quot;false&quot;&quot;
            },
            {
                &quot;&quot;type&quot;&quot;: &quot;&quot;gt&quot;&quot;,
                &quot;&quot;field&quot;&quot;: &quot;&quot;source.mycustomvalue.article.id&quot;&quot;,
                &quot;&quot;value&quot;&quot;: &quot;&quot;0&quot;&quot;
            }
        ]
    }
} &quot;}&quot;)]))),
Source = Web.Contents(&quot;https://api.xxxxxxxxxx&amp;Authorization=Bearer xxxxxxxxxx&amp;Content-Type=application/json&quot;, [Content = Json.FromValue(RequestBody)])

in 

Source
</code></pre>
<p>I tried many combinations in M, however any attempt to connect with this query is rejected. Did anyone have such a problem with Druid? Thanks in advance.</p>

## Answers
### Answer ID: 73451424
<blockquote>
<p>However when I try to rewrite it to M, I am getting errors (most often
&quot;invalid identifier&quot; after &quot;query&quot;.</p>
</blockquote>
<p>It seems like you have a couple of extra &quot; characters, looking at the first</p>
<blockquote>
<p>let</p>
<p>RequestBody =Json.Document(Text.ToBinary(&quot;{&quot; &quot;&quot;query&quot;&quot;:{</p>
</blockquote>
<p>and last</p>
<blockquote>
<p>} &quot;}&quot;)]))),</p>
</blockquote>
<p>lines of your query. I think the extra quote is causing the early termination to your string.</p>
<p>This is how those lines should probably look:</p>
<pre><code>let 

RequestBody =Json.Document(Text.ToBinary(&quot;{ &quot;&quot;query&quot;&quot;:{
</code></pre>
<p>and</p>
<pre><code>} }&quot;)]))),
</code></pre>

