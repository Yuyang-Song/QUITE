# Laravel Interface to multiple models
[Link to question](https://stackoverflow.com/questions/21681866/laravel-interface-to-multiple-models)
**Creation Date:** 1392047854
**Score:** 2
**Tags:** php, interface, laravel, laravel-4, eloquent
## Question Body
<p>I'm writing a system around an existing database structure using Laravel 4.1. The current system is based around two websites which use their own table, <code>a</code> and <code>b</code>, both of which are identical. This is an unavoidable problem until we rewrite the other system.</p>

<p>I need to be able to query both tables at the same time using Eloquents Query Builder, so I may need to get a list of rows from both tables, or <code>INSERT</code> or <code>UPDATE</code> from either at any time.</p>

<p>Currently we have a model for both tables, but no way to link between them and implement the missing methods such as <code>all</code> or <code>find</code>.</p>

<p>Our thought is to have an <code>Interface</code> which will bind these results together, however we're not sure how to go about this at all.</p>

<pre><code>&lt;?php

    interface HotelInterface {
        public function all();
        public function find();
    }

    use Illuminate\Database\Model;

    class Hotel implements HotelInterface {

    }

?&gt;
</code></pre>

<p>Is all we have so far.</p>

## Answers
### Answer ID: 21753940
<p>I asked on the Laravel forums and got the answer I was looking for! I'm reposting here incase.</p>

<p>What we're actually after is a <code>Repository</code> which would look like this:</p>

<pre><code>&lt;?php
    class HotelRepository {
        public $A;
        public $B;

        public function __construct(A $A, B $B) {
            $this-&gt;A = $A;
            $this-&gt;B  = $B;
        }

        public function find($iso = NULL, $hotelid = NULL) {
            $A = $B = NULL;

            if($iso !== NULL) {
                $A = $this-&gt;A-&gt;where('country', $iso);
                $B  = $this-&gt;B-&gt;where('country', $iso);

                if($hotelid !== NULL) {
                    $A = $A-&gt;where('id', $hotelid);
                    $B = $B-&gt;where('id', $hotelid);
                }
            }

            if($hotelid !== NULL) {
                if($A-&gt;first()) {
                    return $A-&gt;first();
                }
                if($B-&gt;first()) {
                    return $B-&gt;first();
                }
            }else{
                return $A-&gt;get()-&gt;merge($B-&gt;get());
            }
        }

        public function all() {
            $aCollection = $this-&gt;A-&gt;all();
            $bCollection  = $this-&gt;B-&gt;all();
            return $aCollection-&gt;merge($bCollection);
        }
    }
</code></pre>

<p>Now in the controller where I want to call this, I just add:</p>

<pre><code>&lt;?php
    class HomeController extends BaseController {
        public function __construct(HotelRepository $hotels) {
            $this-&gt;hotels = $hotels;
        }
    }
</code></pre>

<p>And I can now use <code>$this-&gt;hotels</code> to access the <code>find</code> and <code>all</code> method that I created.</p>

### Answer ID: 21703483
<p>If the tables are identical you should only need one model, the connection is the only thing that needs to change. Have a read here: <a href="http://fideloper.com/laravel-multiple-database-connections" rel="nofollow">http://fideloper.com/laravel-multiple-database-connections</a>.</p>

<p>There's a Eloquent method <a href="https://github.com/laravel/framework/blob/master/src/Illuminate/Database/Eloquent/Model.php#L472" rel="nofollow">on()</a> for specifying the connection, here's an example:</p>

<p>The Eloquent example looks like what you need:</p>

<pre><code>$results = Model::on('mysql')-&gt;find(1);
</code></pre>

<p>Add both connections to your database config and then change the on() part depending on which DB you need to query.</p>

<p><strong>Update: misunderstood the question</strong></p>

<p>If you only need to change the table and not the database, you can use setTable()</p>

<pre><code>$model = new Model
$model-&gt;setTable('b');
$model-&gt;find(1);
</code></pre>

<p>Although that may get confusing.</p>

<p>Instead, you could also define a base model and then extend it with the only difference being the table <code>protected $table = 'b';</code></p>

### Answer ID: 21682877
<p>You can always change the default database for the one you need. I use this <code>Config::set('database.default', 'chronos');</code>, where <strong>chronos</strong> is one of my databases. When I need to change to the "other", I just change de database name. You can call it wherever you want. I think that what you're looking for is just switch between the databases. </p>

<p>You need to have two different models, one for each table on each database, though.</p>

<p>Let me know if I got it wrong.</p>

