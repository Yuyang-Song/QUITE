# How to set association class_name based on model attribute
[Link to question](https://stackoverflow.com/questions/57502912/how-to-set-association-class-name-based-on-model-attribute)
**Creation Date:** 1565822307
**Score:** 1
**Tags:** ruby-on-rails, model, rails-activerecord
## Question Body
<p>I have the following models:</p>

<pre><code>class Schematic &lt; ApplicationRecord
  belongs_to :branch, foreign_key: :location_cd
  has_many :schematics_stocks, class_name: 'SchematicsStock', dependent: :destroy
end

class SchematicsStock &lt; ApplicationRecord
  belongs_to :schematic
  belongs_to :stock, foreign_key: "stock_no"
end

class Stock &lt; ApplicationRecord
  self.table_name = 'stockslc'
  self.primary_key = 'stock_no'
  has_one :schematics_stock
end
</code></pre>

<p>There are various stock tables (stockslc, stockalb, etc.) based on the location_cd (slc, alb, etc.) of the schematic. Is there some way I can do schematic.schematics_stocks[0].stock and have it automatically choose the right stock table?</p>

<p>I thought about creating a model for each stock table. In the SchematicsStock class I could do</p>

<pre><code>Object.const_get("Stock#{schematic.location_cd.downcase}").find(stock_no)
</code></pre>

<p>but this would query the database for every stock no, whereas previously it only did one db call for all the schematics.</p>

<p>I looked into <a href="https://guides.rubyonrails.org/association_basics.html#association-extensions" rel="nofollow noreferrer">ActiveRecord association extensions</a> to see if I could define a belongs_to stock method based on the location_cd at the same time schematics_stocks is defined. Something like</p>

<pre><code>class Schematic &lt; ApplicationRecord
  belongs_to :branch, foreign_key: :location_cd
  has_many :schematics_stocks, class_name: 'SchematicsStock', dependent: :destroy do
    belongs_to stock, class_name: "Stock#{location_cd.downcase}"
  end
end
</code></pre>

<p>This looks like a perfect opportunity to use <a href="https://www.postgresql.org/docs/current/ddl-partitioning.html" rel="nofollow noreferrer">Postgresql table partioning</a> where I could partition a stock table based on the location_cd, but changing the stock schema isn't an option and the there is already a lot of production data in the other tables.</p>

<p>I have code like the following in my view.</p>

<pre><code>  &lt;% @schematic.schematics_stocks.includes(:stock)
    .order(:stock_no).each do |s_stock| %&gt;
</code></pre>

<p>I am trying to decide if I should just write a query to get it from the correct table and then rewrite my view code or if there is a way to keep my view code the same.</p>

## Answers
### Answer ID: 57512027
<p>I realized that I could set the model's table_name at runtime. Initially I used the following code to use the correct stock table</p>

<pre><code>&lt;% Stock.table_name = "stock" + @schematic.location_cd.downcase %&gt;
&lt;% @schematic.schematics_stocks.includes(:stock)
  .order(:stock_no).each do |s_stock| %&gt;
</code></pre>

<p>Based on <a href="https://stackoverflow.com/questions/57502912/how-to-set-association-class-name-based-on-model-attribute/57509096#57509096">Jay-Ar Polidario's answer</a>, I decided to make a method in the schematic model to change the table_name.</p>

<pre><code># schematic.rb
def schematics_stocks_with_stocks
  Stock.table_name = 'stock' + location_cd.downcase
  schematics_stocks.includes(:stock)
end

# view 
&lt;% @schematic.schematics_stocks_with_stocks
  .order(:stock_no).each do |s_stock| %&gt;
</code></pre>

### Answer ID: 57509096
<p>Maybe the following is a workound, if you just want to be efficient with SQL?</p>

<pre><code>class Schematic &lt; ApplicationRecord
  has_many :schematic_stocks, dependent: :destroy

  def stocks
    # say if `location_cd` == 'alb', then
    # you'll need to create a model named Stockalb in your app/models
    # and a model for each "stock table" you have.
    stock_class = ('Stock' + location_cd).constantize
    stock_class.joins(:schematic_stocks)
  end
end
</code></pre>

