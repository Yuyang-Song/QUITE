# Setting up Geocoder with Sinatra and ActiveRecord?
[Link to question](https://stackoverflow.com/questions/51520034/setting-up-geocoder-with-sinatra-and-activerecord)
**Creation Date:** 1532525041
**Score:** 1
**Tags:** ruby, activerecord, sinatra, geocoder
## Question Body
<p>I have a MYSQL database which is accessed using ActiveRecord and Sinatra. I am trying to perform certain geolocation task on the records in the tables.</p>

<p>However, i believe my syntax is wrong as extending the geocoder class makes my CRUD request fail:</p>

<p><strong>myapp.rb</strong></p>

<pre><code>require 'rubygems'
require 'sinatra'
require 'active_record'
require 'table_print'
require 'json'

ActiveRecord::Base.establish_connection(
  :adapter  =&gt; "mysql2",
  :host     =&gt; "localhost",
  :username =&gt; "root",
  :database =&gt; "orbital"
)

class Post &lt; ActiveRecord::Base
  extend Geocoder::Model::ActiveRecord

 # attr_accessor :latitude, :longitude
end

class Comment &lt; ActiveRecord::Base
  #extend Geocoder::Model::ActiveRecord
end

class MyApp &lt; Sinatra::Application
  #extend Geocoder::Model::ActiveRecord
end

post '/post' do
  @user = params[:user]
  @content = params[:content]
  @latitude = params[:latitude]
  @longitude = params[:longitude]
  @timestamp = params[:timestamp]
  record = Post.create(user: @user, content: @content, longitude: @longitude, latitude: @latitude, timestamp: @timestamp)
  record.save
end
</code></pre>

<p>The query I am trying to perform is:
<code>Post.near([@lat, @long], @dist, units: :km).offset(10 * @var.to_i).first(10)</code></p>

<p>This stackoverflow thread <a href="https://stackoverflow.com/questions/23796364/problems-implementing-ruby-geocoder-using-sinatra">here</a> also suggests that I need to setup additional arguments such as <code>attr_accessors</code>. How do I go about setting up rewriting the above so i can use Geocoder's <code>near</code> method?</p>

## Answers
### Answer ID: 51525568
<p>I fixed the above by adding:</p>

<pre><code>require 'geocoder'
</code></pre>

<p>and</p>

<pre><code>reverse_geocoded_by :latitude, :longitude
</code></pre>

