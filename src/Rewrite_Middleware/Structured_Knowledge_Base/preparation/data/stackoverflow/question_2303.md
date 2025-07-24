# Drupal 7 rewrite is removing get parameters from query string
[Link to question](https://stackoverflow.com/questions/28303387/drupal-7-rewrite-is-removing-get-parameters-from-query-string)
**Creation Date:** 1422979367
**Score:** 0
**Tags:** php, drupal, drupal-7, url-rewriting
## Question Body
<p>I've recently upgraded a site to the latest release of Drupal 7.  The site has a view that retrieves a url with query string parameters from the database and then uses the Drupal rewrite functionality to add a class to the link like so: 
    <code>&lt;a class="purple-button pull-right" href="[field_database_link-url]" target="_blank"&gt;View&lt;/a&gt;</code></p>

<p>The issue is, since the upgrade the rewrite now removes the query string parameters.  If I modify the view to display a simple link the parameters are there and it works fine.  However, the rewrite applies styling to present a button rather than a simple link.  I can't find any settings to resolve the issue so I suspect the upgrade overwrote a modification to the Drupal core made by the original developer of the site.  Any idea how I can address this issue?</p>

## Answers
### Answer ID: 28598454
<p>It turns out that there was a bug in the latest release that in /modules/contrib/link/link.module that was causing the query strings to be stripped from the url in the token. I replaced the code in this file with the code from the pre-upgrade version and it began behaving as expected again. This, of course, is not a resolution to the issue, but at least the source of the problem has been identified. For more info: <a href="https://www.drupal.org/node/2367069" rel="nofollow">https://www.drupal.org/node/2367069</a></p>

<p>I later found that there is a patch for this issue in the dev version (7.x-1.x-dev) of this module available here: <a href="https://www.drupal.org/project/link" rel="nofollow">https://www.drupal.org/project/link</a>.  Download this module and replace it in your install and you should be all set.</p>

