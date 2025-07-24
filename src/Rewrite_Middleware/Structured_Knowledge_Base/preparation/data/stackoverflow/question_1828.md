# Can a separate WordPress (same server) get posts from an existing one, but have different settings?
[Link to question](https://stackoverflow.com/questions/9469348/can-a-separate-wordpress-same-server-get-posts-from-an-existing-one-but-have)
**Creation Date:** 1330363642
**Score:** 0
**Tags:** mysql, wordpress, testing, wordpress-theming
## Question Body
<p>When developing WordPress themes for a site with a large amount of posts, how can I dynamically pull existing post data from the live version of the site onto my testing site? I already know about WordPress's export feature, but that's one-and-done, not dynamically queried.</p>

<ol>
<li><strong>Plan A:</strong>

<ul>
<li><em>Proposed Solution:</em>

<ul>
<li>Create read-only user in live site's database</li>
<li>PRECAUTION: change test site's prefix from "wp_" to "test_"</li>
</ul></li>
<li><em>Problems:</em>

<ul>
<li>Settings (like current theme) on test site cannot be changed, thanks to read-only user</li>
<li>No posts found in "test_posts", even though I'd like it to search "wp_posts" </li>
</ul></li>
</ul></li>
</ol>

<p>Is there an easier way or existing solution to avoid rewriting WordPress system files on the test site? I'd really rather not rewrite WordPress's database interface...</p>

<p><strong>Similar:</strong> <a href="https://stackoverflow.com/questions/997007/can-two-different-wordpress-blogs-on-the-same-server-use-a-common-theme-folder">Linking themes across WP installations</a></p>

## Answers
### Answer ID: 10901755
<p>just duplicate the DB, re-name and call DB in wp-config!</p>

