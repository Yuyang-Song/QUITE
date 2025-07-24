# Yii fixture objects are null when trying to access them
[Link to question](https://stackoverflow.com/questions/13722356/yii-fixture-objects-are-null-when-trying-to-access-them)
**Creation Date:** 1354707234
**Score:** 0
**Tags:** yii
## Question Body
<p>I have the following test file</p>

<pre><code>&lt;?php

class DisplayAlbumTest extends CDbTestCase
{

  public $fixtures = array(
    'displayalbums' =&gt; 'DisplayAlbum',
    'displayphotos' =&gt; 'DisplayPhoto',
  );

  /**
   * Get title
   * 
   * @group v1.0
   * @group now
   */
  public function testGetTitle()
  {
    $oAlbum = $this-&gt;displayalbums('get_title');

    var_dump($oAlbum);

    die('nope!');

    $this-&gt;assertEquals('Get title test', $oAlbum-&gt;getTitle());
  }

}
</code></pre>

<p>and its associated fixture file</p>

<pre><code>&lt;?php
return array(
  'get_title' =&gt; array(
    'title' =&gt; 'Get title test'
  )
);
</code></pre>

<p>and the following config</p>

<pre><code>&lt;?php
Yii::setPathOfAlias('api', '../api/');

return CMap::mergeArray(
  require(dirname(__FILE__).'/main.php'),
  array(
    'components'=&gt;array(
      'fixture'=&gt;array(
        'class'=&gt;'system.test.CDbFixtureManager',
      ),
      /* uncomment the following to provide test database connection
      'db'=&gt;array(
        'connectionString'=&gt;'DSN for test database',
      ),
      */
      'db'=&gt;$TEST_DB_SETTINGS,
    ),
  )
);
</code></pre>

<p>The data is inserted into the database when running the tests but the <code>var_dump</code> prints <code>NULL</code>. If I try to access any methods on the model I get the following error (because I'm trying to access a method on NULL)
    PHP Fatal error:  Call to a member function getTitle() on a non-object</p>

<p>Other tests for other models with different fixtures work without any problem, but those that use the same fixture as this model test case fail.</p>

<p>If I do <code>var_dump($this-&gt;displayalbums)</code> inside the test this is the result that I get:</p>

<pre><code>array(1) {
  ["get_title"]=&gt;
  array(2) {
    ["title"]=&gt;
    string(14) "Get title test"
    ["displayalbumid"]=&gt;
    string(1) "1"
  }
}
</code></pre>

<p>I could create new objects with the data from the array and test the methods but that would mean I'd have to rewrite all of my tests (others in this file are failing because of this) and it's weird because I use this method in other tests that do not fail.</p>

<p>I looked in the MySQL logs and the last query ran was the one to select the album I wanted</p>

<pre><code>SELECT * FROM `DisplayAlbum` `t` WHERE `t`.`displayalbumid`=60 LIMIT 1
</code></pre>

<p>If I run the query it returns the proper result so the problem is not with the DB.</p>

<p>Why is the value NULL when I try to access the items from the fixture ?</p>

## Answers
### Answer ID: 16282255
<p>I had the same problem and the solution was that the default scope "blocked" it. </p>

<p>In mysql I set the default attribute of an attribute to zero but the default scope condition was <code>$t.'attribute' = 1</code>. Probably you have a simliar problem...</p>

