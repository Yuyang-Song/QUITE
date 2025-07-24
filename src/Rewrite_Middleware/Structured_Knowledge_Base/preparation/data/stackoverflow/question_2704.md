# October cms long load time for query
[Link to question](https://stackoverflow.com/questions/48253576/october-cms-long-load-time-for-query)
**Creation Date:** 1515959710
**Score:** 0
**Tags:** mysql, activerecord, octobercms, octobercms-plugins
## Question Body
<p>I'm trying to optimize this nested query which takes a very long time to load.</p>

<p>The basic idea is to get all the series that belong to a department, in the middle the're products that belong to many departments and many series. 
the table structure</p>

<p>departments*&lt;-->*products*&lt;->*series</p>

<p>In the models the relationships are defined as follows Department model</p>

<pre><code>public $belongsToMany  = [
      'products' =&gt; [
        '\depcore\parts\Models\Product',
        'table' =&gt; 'depcore_parts_products_departments',
      ],
      // 'series' =&gt; [
      //   '\depcore\parts\Models\Series',
      //   'table' =&gt; 'depcore_parts_products_series',
      // ]
    ];
</code></pre>

<p>Series model </p>

<pre><code>public $hasMany = [
      'products' =&gt; [
        '\depcore\parts\Models\Product',
        'table' =&gt; 'depcore_parts_products_departments',
      ]
    ];
</code></pre>

<p>The product model</p>

<pre><code>public $belongsToMany = [
      'series' =&gt; [
        'depcore\parts\Models\Series',
        'table' =&gt; 'depcore_parts_products_series',
        'order' =&gt; 'name',
        ],
      'departments' =&gt; [
        'depcore\parts\Models\Department',
        'table' =&gt; 'depcore_parts_products_departments',
        // 'order' =&gt; 'name'
        ]
    ];
</code></pre>

<p>In the Department model I've created a method to retrieve all the series that belong to the department which after analyzing is causing some serious performance issues </p>

<pre><code>public function series (){

      $seriesArray = array( );
      $products = $this-&gt;products()-&gt;remember(100)-&gt;get();
      foreach ($products as $product) {
        $productSeries = $product-&gt;series()-&gt;remember(100)-&gt;get();
        foreach ($productSeries as $series) {
            if (!isset($seriesArray[$series-&gt;id]) and $series-&gt;published )
                $seriesArray[$series-&gt;id] = $series;
        }
      }

     return \Illuminate\Database\Eloquent\Collection::make($seriesArray);

    }
</code></pre>

<p>I'guess this could be done with raw SQL or better implementation in the active record but I'm stuck on both. </p>

<p>I've added the <code>remember()</code> method later on but with no results. 
Right now the loading time for the webpage is about 20s. when removing this code ist instantly.</p>

<p>Any advice is appreciated.</p>

<p>From the table structure I guess this would be the apropriate SQL command (commands) to run in order to get the result needed</p>

<pre><code>SELECT DISTINCT series_id FROM depcore_parts_products_series WHERE product_id IN (SELECT DISTINCT product_id FROM depcore_parts_products_departments WHERE department_id = 3);
</code></pre>

<p>This query runs only on the intermediate tables and gets the right results (in phpmyadmin) of <code>series_id</code> (the department_id = 3 is as an example)</p>

<p>Using Hardik Satasiya code I had to change a couple of lines or the view would not show any series just empty lines.</p>

<pre><code>public function series (){

        $sql = 'SELECT DISTINCT series_id FROM depcore_parts_products_series WHERE product_id IN (SELECT DISTINCT product_id FROM depcore_parts_products_departments WHERE department_id = :dep_id)';

        $data = ['dep_id' =&gt; $this-&gt;id];
        $query = \DB::select($sql, $data);
        $data = $query;

        $ids = array();
        // I had to rewrite this pare and make it more inelegant still 
        // but the refresh method appeared to made it step out the execution cycle 
        foreach ($data as $key =&gt; $value) {
            $ids[] = $value-&gt;series_id;
        }

        // in $data we are passing only id information
        // so this records have only id, not db all attributes
        // what ever you pass in $data will become model attributes if its in list
        $collection = \depcore\parts\Models\Series::hydrate($ids);
        return Series::published()-&gt;whereIn('id',$ids)-&gt;get();

    }
</code></pre>

<p>The block partial</p>

<pre><code>&lt;div class="element-grid"&gt;
    &lt;h4 {% if hideChildren|length and departmentModel.id not in filters.departments %} class='inactive' {% endif %}  &gt;&lt;a href="{{ url('/')}}/parts?Filter[departments][]={{ departmentModel.id }}"&gt;{{ departmentModel.name }}&lt;/a&gt;&lt;/h4&gt;
    {% if not hideChildren|length %}
    &lt;div class="list"&gt;
      &lt;div class="block left-block"&gt;
          {% if departmentModel.getChildren|length %}
              &lt;ul class='departments'&gt;
                {% for child in departmentModel.getChildren %}
                     {% if child.published %}
                        &lt;li&gt;&lt;strong&gt;&lt;a href="{{ url('/')}}/parts?Filter[departments][]={{ departmentModel.id }}&amp;Filter[departments][]={{ child.id }}"&gt;{{ child.name }}&lt;/a&gt;&lt;/li&gt;&lt;/strong&gt;
                     {% endif %}

                {% endfor %}
              &lt;/ul&gt;
          {% endif %}
         &lt;ul class="series"&gt;
           {% for series in departmentModel.departmentSeries.series|slice(0,10) %}
             &lt;li&gt;&lt;a href="{{ url('/')}}/parts?Filter[departments][]={{ departmentModel.id }}&amp;{{ departmentModel.departmentSeries.childrenString }}&amp;Filter[series][]={{ series.id }}"&gt;{{ series.name }}&lt;/a&gt;&lt;/li&gt;
           {% endfor %}
         &lt;/ul&gt;
        &lt;/div&gt;
        &lt;div class="block right-block"&gt;
             &lt;ul class="series series-right"&gt;
                {% for series in departmentModel.departmentSeries.series|slice(10,length) %}
                    &lt;li&gt;&lt;a href="{{ url('/')}}/parts?Filter[departments][]={{ departmentModel.id }}&amp;{{ departmentModel.departmentSeries.childrenString }}&amp;Filter[series][]={{ series.id }}"&gt;{{ series.name }}&lt;/a&gt;&lt;/li&gt;
                {% endfor %}
             &lt;/ul&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;img src="{{ departmentModel.image.file_name | media }}" alt=""&gt;
    {% endif %}
&lt;/div&gt;
</code></pre>

<p>The departmentSeries scope.</p>

<pre><code>public function scopeDepartmentSeries( $query ){
        $children = $query-&gt;getModel()-&gt;getChildren();
        // dd($children);
        if ( count( $children ) &gt; 0 ) {
            $seriesArray = array (  );

            foreach ($children as $child) {
                $childrenIds[] = 'Filter[departments][]='.$child-&gt;id;

                foreach ($child-&gt;series (  ) as $series) {

                    if (!in_array($series-&gt;id,$seriesArray)) $seriesArray[] = $series-&gt;id;

                    if (!array_key_exists($series-&gt;id,$seriesArray)) $seriesArray[$series-&gt;id] = $series-&gt;name;

                }
            } // endforeach children as child
            $childrenString = implode( '&amp;', $childrenIds );
            return ["series" =&gt; Series::whereIn ( 'id',$seriesArray )-&gt;get (  ),
                    "childrenString" =&gt; $childrenString];
        }
        return ["series" =&gt; $query-&gt;getModel()-&gt;series(  )];
    }
</code></pre>

## Answers
### Answer ID: 48270482
<p>you can utilize Raw queries and to convert <code>fetched id</code> in to model you can write this code.</p>

<pre><code>$sql = 'SELECT DISTINCT series_id FROM depcore_parts_products_series WHERE product_id IN (SELECT DISTINCT product_id FROM depcore_parts_products_departments WHERE department_id = :dep_id');

$data = ['dep_id' =&gt; 2];
$query = \DB::select($sql, $data);
$data = $query;

foreach ($data as $model) {
    $ids[] = $model-&gt;series_id;
}

$returnData = Series::whereIn('id',$ids)-&gt;get();
// dd($returnData);

return $returnData;
</code></pre>

<p>if you find any difficulties please comment.</p>

<h2>update</h2>

<blockquote>
  <p>my <strong>department</strong> model</p>
</blockquote>

<pre><code>use \October\Rain\Database\Traits\SimpleTree;

public $belongsTo = [
    'parent'    =&gt; ['HardikSatasiya\StackDemo\Models\Departments', 'key' =&gt; 'parent_id'],
];

public $hasMany = [
    'children'    =&gt; ['HardikSatasiya\StackDemo\Models\Departments', 'key' =&gt; 'parent_id'],
];

public function series() {

    $sql = 'SELECT DISTINCT series_id FROM hardiksatasiya_stackdemo_product_series WHERE product_id IN (SELECT DISTINCT product_id FROM hardiksatasiya_stackdemo_department_product WHERE department_id = :dep_id)';

    $data = ['dep_id' =&gt;  $this-&gt;id];
    $query = \DB::select($sql, $data);
    $data = $query;
    foreach ($data as $model) {
        $ids[] = $model-&gt;series_id;
    }

    $returnData = Series::whereIn('id',$ids)-&gt;get();
    // dd($returnData);

    return $returnData;
}

public function scopeDepartmentSeries( $query ) {
    $children = $query-&gt;getModel()-&gt;getChildren();
    //dd($children);
    if ( count( $children ) &gt; 0 ) {
        $seriesArray = array (  );

        foreach ($children as $child) {
            $childrenIds[] = 'Filter[departments][]='.$child-&gt;id;

            foreach ($child-&gt;series (  ) as $series) {

                if (!in_array($series-&gt;id,$seriesArray)) $seriesArray[] = $series-&gt;id;

                // if (!array_key_exists($series-&gt;id,$seriesArray)) $seriesArray[$series-&gt;id] = $series-&gt;name;

            }
        } // endforeach children as child
        $childrenString = implode( '&amp;', $childrenIds );
        return ["series" =&gt; Series::whereIn ( 'id',$seriesArray )-&gt;get (  ),
                "childrenString" =&gt; $childrenString];
    }
    return ["series" =&gt; $query-&gt;getModel()-&gt;series(  )];
}
</code></pre>

<blockquote>
  <p>and <strong><code>page code section</code></strong></p>
</blockquote>

<pre><code>function onInit() {
    $departmentModel = \HardikSatasiya\StackDemo\Models\Departments::find(1);
    //dd($departmentModel-&gt;getChildren());
    $this['departmentModel'] = $departmentModel;
}
</code></pre>

<blockquote>
  <p><strong>and I am using <code>html/partial</code> you provided.</strong> and it seems its working here</p>
</blockquote>

