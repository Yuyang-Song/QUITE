# Symfony 5 @required annotation weird caching issue during setter injection?
[Link to question](https://stackoverflow.com/questions/59992879/symfony-5-required-annotation-weird-caching-issue-during-setter-injection)
**Creation Date:** 1580411173
**Score:** 0
**Tags:** apache, docker, symfony, caching, annotations
## Question Body
<p>I discovered this strange issue in Symfony 5 which I believe is connected to docker and Symfony itself.</p>

<h1>MY SETUP</h1>

<p><code>docker-compose.yml</code></p>

<pre><code>version: '3.7'
services:
  webapp:
    build:
      context: ./php/
      dockerfile: Dockerfile
    container_name: webapp
    image: php:7.4.1-fpm-alpine
    volumes:
      - ../:/srv/app
  apache2:
    build:
      network: host
      context: ./apache2/
      dockerfile: Dockerfile
    container_name: apache2
    image: httpd:2.4.39-alpine
    ports:
      - 8080:80
    volumes:
      - ../:/srv/app
  mysql:
    container_name: mysql
    image: mysql:latest
    ports:
      - 13306:3306
    volumes:
      - mysql:/var/lib/mysql:cached
    environment:
      MYSQL_ROOT_USER: XXX
      MYSQL_ROOT_PASSWORD: XXX
      MYSQL_DATABASE: XXX
      MYSQL_USER: XXX
      MYSQL_PASSWORD: XXX
  redis:
    container_name: redis
    image: redis:5.0.6-alpine
    ports:
      - 16379:6379
    volumes:
      - redis:/data:cached

volumes:
  mysql:
    driver: local
  redis:
    driver: local
</code></pre>

<p>For framework I am of course using Symfony 5. I am quite sure this setup is correct because I am using something like that for my other Laravel project and it is working very well.</p>

<h1>THE PROBLEM</h1>

<p>On my trait I am using <code>@required</code> annotation. To be more exact I am using that on a setter like this:</p>

<pre><code>    /**
     * Get the current request out of RequestStack object.
     *
     * @param RequestStack $requestStack
     * @required
     */
    public function setRequest(RequestStack $requestStack): void
    {
        $this-&gt;currentRequest = $requestStack-&gt;getCurrentRequest();
    }
</code></pre>

<p>I know this bit is fine as it always worked in previous version. The problem seems to be in <code>@required</code> annotation. I am not sure why but every time I add it I get:</p>

<p><a href="https://i.sstatic.net/Qu7XY.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Qu7XY.png" alt="enter image description here"></a></p>

<p>It looks like there is something wrong with the server, however as soon as I manually clear the cache it works and then after another call (and changing something in code and in postman call like query parameter's content) it breaks again until I either remove <code>@required</code> or clear the cache.</p>

<p>I am confused - I am not sure if it is to do with my docker setup or there is a bug in Symfony's caching mechanism or maybe it is combination off all of my suspicions and even more. </p>

<p>My bet would be a bug in Symfony caching or there is something wrong with how I set up the docker. However I just started working on that, I don't even connect to the database at this point, these are literally first steps in rewriting that project so nothing funky is happening.</p>

<p>What do you think guys? Did anyone see something like that before?</p>

<h1>WHAT DID I TRY</h1>

<p>I did try clear cache, removing and adding that annotation I did try rebooting my docker, I did prune the whole thing and made brand new setup. Nothing worked so far.</p>

<h1>UPDATE 30.01.2020 19:45</h1>

<p>I did try the same setter injection directly on the controller and I can't reproduce the error. I think that for some reason it doesn't like it on the trait. </p>

## Answers
### Answer ID: 60144385
<p>The answer to my problem is an upgrade. Like Cerad mentioned in his comment - updating PHP from 7.4.1 to 7.4.2 could solve the problem and it did.</p>

<p>If you are on Symfony 5 make sure you have PHP 7.4.2 to avoid this particular issue. </p>

