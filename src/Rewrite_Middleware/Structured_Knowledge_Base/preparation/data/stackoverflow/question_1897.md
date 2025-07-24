# Delete stored apc keys with a regular expression
[Link to question](https://stackoverflow.com/questions/11515579/delete-stored-apc-keys-with-a-regular-expression)
**Creation Date:** 1342495259
**Score:** 5
**Tags:** php, caching, apc
## Question Body
<p>Is it possible to use a method to enable you to delete stored apc entries with regular expressions?</p>

<p>For example some users queries I want to delete from the cache when new data is entered into the database so that the new data is shown the next time the query is run.</p>

<p>Say you have a friend list query which is cached, but when a new friend is added all cached friend queries for that user would be deleted ...</p>

<p>If I have keys like this for the users friendlist:</p>

<pre><code>$sql = "SELECT * FROM friends WHERE userId = :userId";

$sqlKey = str_replace(":userId", $userId, $sql);    
$key = $userId."-friend".md5('query'.$sqlKey);

$data = friendsArray;
apc_add($key, $data, 60 * 10);
</code></pre>

<p>Then the desired outcome would be to delete all entries that began with the current userId after running the add new friend query to ensure the friend list displays the new user on the next viewing:</p>

<pre><code>apc_delete("~$userId-friend([a-f0-9]+)~");
</code></pre>

<p>As the friends list sql and the add friend sql are in different documents this seems the simplest way to go about doing it without rewriting and keying the sql but I don't think regular expressions are supported?</p>

## Answers
### Answer ID: 19405501
<p>As <a href="http://www.php.net/manual/en/function.apc-delete.php#101794" rel="nofollow">J Fox wrote on php.net</a>, apc_delete also accepts and array of keys or APCIterator object. And APCIterator accepts regex. So your code should look about like that:</p>

<pre><code>// delete all keys beginning with a regex match
$toDelete = new APCIterator('user', '/^' . $userId . '-friend([a-f0-9]+)/', APC_ITER_VALUE);

var_dump( apc_delete($toDelete) );
// returns boolean true|false on success or failure
</code></pre>

