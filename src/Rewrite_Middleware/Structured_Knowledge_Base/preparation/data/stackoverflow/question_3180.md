# JQuery http post request between docker containers fails
[Link to question](https://stackoverflow.com/questions/70265767/jquery-http-post-request-between-docker-containers-fails)
**Creation Date:** 1638904449
**Score:** 0
**Tags:** php, jquery, mongodb, docker, rest
## Question Body
<p>I am new in web development and especially in Docker and I am trying to use Docker for a webpage I am working on as part of a semester project. I have created 3 containers. One for my application logic (ui), one for the REST api service (both with php:7.2-apache images) and one for a MongoDB. I have tried many different things, so there may be some unnecessary code below. The problem seems to be that the POST request made by the $.post part of the index.php code (see below) is not done properly, as I am not redirected to the welcome.php page of my web app and I cannot find the reason why.</p>
<p>The docker-compose.yml file is the following:</p>
<pre><code>version: &quot;3.7&quot;

services:
  mongo_db:
    image: mongo
    container_name: mongodb
    restart: always
    ports:
      - &quot;270187:27017&quot;
    expose:
      - &quot;27017&quot;
    volumes:
      - mongo-data:/var/lib/mongo
      - .mongo/mongoinit.js:/docker-entrypoint-initdb.d/
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: plh513   
      MONGO_INITDB_DATABASE: plh513       
  
  restapi:
    build:
      context: .
      dockerfile: Dockerfile1
    container_name: restapi
    ports:
      - &quot;27018:27018&quot;
    expose:
      - &quot;27018&quot;
    volumes:
      - .:/var/www
    depends_on:
      - mongo_db
    links:
      - mongo_db

  app: 
    build:
     context: .
     dockerfile: Dockerfile
    container_name: applogic
    ports:
      - &quot;80:80&quot;
    expose:
      - &quot;80&quot;
    volumes:
      - .:/var/www
    depends_on:
      - restapi

volumes:
  mongo-data: {}
</code></pre>
<p>The Dockerfile (Dockerfile1 is similar) I am using is:</p>
<pre><code>FROM php:7.2-apache 

RUN apt-get update \
 &amp;&amp; apt-get install -y git zlib1g-dev \
 &amp;&amp; docker-php-ext-install zip \
 &amp;&amp; apt-get install -y zlib1g-dev libicu-dev g++ \
 &amp;&amp; docker-php-ext-configure intl \
 &amp;&amp; docker-php-ext-install intl \
 &amp;&amp; apt-get install -y libcurl4-openssl-dev pkg-config libssl-dev \
 &amp;&amp; echo &quot;extension=mongodb.so&quot; &gt; $PHP_INI_DIR/conf.d/mongodb.ini \
 &amp;&amp; pecl install mongodb \
 &amp;&amp; a2enmod rewrite \
 &amp;&amp; sed -i 's!/var/www/html!/var/www/src!g' /etc/apache2/sites-available/000-default.conf \
 &amp;&amp; mv /var/www/html /var/www/src \
 &amp;&amp; curl -sS https://getcomposer.org/installer \
  | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www
</code></pre>
<p>The index.php code (HTML and JQuery included) for the login page is the following:</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;meta charset=&quot;UTF-8&quot;&gt;
&lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1, shrink-to-fit=yes&quot;&gt;
&lt;script src=&quot;https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js&quot;&gt;&lt;/script&gt;
&lt;head&gt;
    &lt;title&gt;LOGIN&lt;/title&gt;
    &lt;link rel=&quot;stylesheet&quot; type=&quot;text/css&quot; href=&quot;loginstyle.css&quot;&gt;
&lt;/head&gt;

&lt;body&gt;
    &lt;div class=&quot;center&quot;&gt;
     &lt;form id=&quot;loginform&quot; action=&quot;index.php&quot; method=&quot;post&quot;&gt;

        &lt;div class=&quot;imgcontainer&quot;&gt;
            &lt;img src=&quot;logo1.png&quot; alt=&quot;Logo&quot; class=&quot;logo&quot;&gt;
        &lt;/div&gt;
        
        &lt;div class=&quot;container&quot;&gt;
            &lt;label&gt;&lt;b&gt;Username&lt;/b&gt;&lt;/label&gt;
            &lt;input type=&quot;text&quot; placeholder=&quot;Enter Username&quot; name=&quot;uname&quot; required&gt;
            &lt;label&gt;&lt;b&gt;Password&lt;/b&gt;&lt;/label&gt;
            &lt;input type=&quot;password&quot; placeholder=&quot;Enter Password&quot; name=&quot;pass&quot; required&gt;
        &lt;/div&gt;
        &lt;input type=&quot;submit&quot; id=&quot;login&quot; value=&quot;Login&quot;&gt;
        &lt;div class=&quot;errormsg&quot; id=&quot;errormsg&quot;&gt;&lt;/div&gt;    
     &lt;/form&gt;
    &lt;/div&gt;
&lt;/body&gt;

&lt;script&gt;
    // JQuery actions for HTML body content
    // Action when the login button in clicked
        $(&quot;#login&quot;).click(function(){
        // create a variable based on the user's input in class = container
        var credentials = {
            uname: $(&quot;.container input[name='uname']&quot;)[0].value,
            pass: $(&quot;.container input[name='pass']&quot;)[0].value
        };
        var url = document.location.protocol + &quot;//&quot; + document.location.hostname + &quot;:27018&quot;;
        var api = &quot;url:27018/user_validate.php&quot;;
        
        $.post(api,JSON.stringify(credentials),function(data,status,xhr){
            var jsonData = JSON.parse(data);
            // if server_data.message is an error case
            if(jsonData.message == &quot;user_not_confirmed&quot;){
                $(&quot;#errormsg&quot;).text(&quot;Login failed: This user has not yet been confirmed by an administrator&quot;);
                $(&quot;#errormsg&quot;).delay(3000).fadeOut(&quot;slow&quot;);
            }else if(jsonData.message == &quot;wrong_credentials&quot;){
                $(&quot;#errormsg&quot;).text(&quot;Login failed: Wrong username or password&quot;);
                $(&quot;#errormsg&quot;).delay(3000).fadeOut(&quot;slow&quot;);
            // user successfully logged in
            }else if(jsonData.message == &quot;success_login&quot;){
                if(jsonData.validate == &quot;true&quot;){
                    sessionStorage.setItem(&quot;already_logged&quot;, true);
                    sessionStorage.setItem(&quot;id&quot;, jsonData.id);
                    sessionStorage.setItem(&quot;username&quot;, jsonData.username);
                    sessionStorage.setItem(&quot;name&quot;, jsonData.name);
                    sessionStorage.setItem(&quot;surname&quot;, jsonData.surname);
                    sessionStorage.setItem(&quot;role&quot;, jsonData.role);
                    sessionStorage.setItem(&quot;confirmed&quot;, jsonData.confirmed);
                    window.location.replace(&quot;localhost/welcome.php&quot;);
                }
            }

        },&quot;json&quot;);
    });
&lt;/script&gt;
&lt;/html&gt;
</code></pre>
<p>The user_validate.php file (part of the REST api) is:</p>
<pre><code>&lt;?php 
// required headers
header(&quot;Access-Control-Allow-Origin: *&quot;);
header(&quot;Content-Type: application/json; charset=UTF-8&quot;);
header(&quot;Access-Control-Allow-Methods: POST&quot;);
header(&quot;Access-Control-Max-Age: 3600&quot;);
header(&quot;Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With&quot;);

// validate user
// include database file
include_once 'mongodb_config.php';

$dbname = 'plh513';
$collection = 'users';
// DB connection - works fine
$db = new DbManager();
$conn = $db-&gt;getConnection();

// read data from HTTP body and set variables $uname, $password
$contents = file_get_contents('php://input');
$contents = stripslashes(html_entity_decode($contents));
$data = json_decode($contents,true);

// Read a single user from db (at variable $user_data)
$option = ['limit' =&gt; 1];
$read = new MongoDB\Driver\Query($data, $option);
$user_data = $conn-&gt;executeQuery(&quot;$dbname.$collection&quot;, $read);

// actions based on query's result
foreach ($user_data as $user){
    if(empty($user))
    {   
        echo json_encode(
            array(&quot;message&quot; =&gt; &quot;wrong_credentials&quot;)
        );
    }
    else if($user-&gt;confirmed == &quot;0&quot;)
    {
        echo json_encode(
            array(&quot;message&quot; =&gt; &quot;user_not_confirmed&quot;)
        );
    }
    else
    {
        echo json_encode(
            array(&quot;message&quot; =&gt; &quot;success_login&quot;,
                &quot;validate&quot; =&gt; &quot;true&quot;,
                &quot;id&quot; =&gt; $user-&gt;_id,
                &quot;username&quot; =&gt; $user-&gt;username,
                &quot;name&quot; =&gt; $user-&gt;name,
                &quot;surname&quot; =&gt; $user-&gt;surname,
                &quot;role&quot; =&gt; $user-&gt;role,
                &quot;confirmed&quot; =&gt; $user-&gt;confirmed
            )
        );
    }
}

?&gt;
</code></pre>
<p>I have made sure that the MongoDB is working properly and executes the queries inside user_validate.php.</p>
<p>Any suggestion of why I am always redirected to localhost/index.php and not to localhost/welcome.php, while using the correct credentials?</p>

