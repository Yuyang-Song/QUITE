# Autoloaded php code not updating after edits inside of Lando environment
[Link to question](https://stackoverflow.com/questions/58677094/autoloaded-php-code-not-updating-after-edits-inside-of-lando-environment)
**Creation Date:** 1572750074
**Score:** 1
**Tags:** php, docker, docker-compose, composer-php, lando
## Question Body
<p>The crux of the issue is that I <strong>edit a code file and the change does not take effect</strong> until after I rebuild my entire environment. Weird thing is that I haven't been having this issue for months of development so far. I just decided to dust off this project and work on it this week and <strong>all of a sudden</strong> editing files no longer works (without a rebuild).</p>

<p>I don't even know where to begin to try and tackle this. Any advise helps, especially from people who have experience with Lando and Docker. Alright, so because I don't have any idea what's causing this, I'll just try and explain my whole set up and go from there:</p>

<p>I'm using Lando to run a container which is running PHP 7.3. When I SSH into the running container and execute my script <code>php worker.php</code> my script runs no problems. Then if I edit it, say to add a var_dump('hello world!'), I get the expected output. However, if I edit an autoloaded class file, say MyClass.php, and add a var_dump there, nothing happens. In fact I have to completely rebuild the environment with <code>lando rebuild</code> in order to get the var_dump to show up. Weird right?</p>

<p>Ok so here are some things I've tried:</p>

<ul>
<li>I've tried restarting Docker.</li>
<li>I've tried restarting my computer.</li>
<li>I've tried <code>lando destroy</code> and <code>lando rebuild</code> to start fresh.</li>
<li>I've tried SSHing into the container and running <code>cat mylib/MyClass.php</code> and I see the added var_dump statement!! However when I run <code>php worker.php</code> the var_dump added to MyClass isn't there. How can it be present in the filesystem, yet absent during execution? This is really throwing me for a loop.</li>
<li>I've tried renaming MyClass.php to MyClass2.php and this fixes the issue ONCE. I.e. after it updates I then need to rename it again and again each time there is a change. This obviously isn't a real solution, but it's food for thought.</li>
<li>I've tried manually loading classes using <code>include_once</code>. This works perfectly, edits take effect as soon as they happen. The problem is that I don't want to manually include all my files, I want to use the composer autoloader. I've been using it for a long time, I'd prefer to just fix whatever has suddenly gone wrong with it.</li>
</ul>

<p>Ok lastly, some theories of mine:</p>

<ul>
<li>Something is obviously caching stuff but I have no idea what. I thought maybe it was something to do with the PHP Opcode caching, but I, to my knowledge, don't have php opcode caching enabled.</li>
<li>Another theory is that maybe the filesystem mount isn't working. It is working, however, because when I edit worker.php the changes are instantly there each time. This would not be happening if there was no filesystem mount.</li>
<li>One more theory is that either Docker is caching something somehow (I have no idea how), or maybe Lando is? I don't know Lando inside and out. Maybe it has some sort of caching scheme I'm not aware of.</li>
<li>Last theory is that somehow autoloaded classes are cached by PHP itself or my composer or something like that. I also don't know how this is possible, but I'm not an expert on the inner workings of composer or php so if there is a code cache involved here somewhere I'm not aware of it.</li>
</ul>

<p>So some things I know people might ask for:
Dockerfile</p>

<pre><code>FROM php:7.3-apache

RUN apt-get update \
    &amp;&amp; apt-get install -y \
       git \
       zip \
       unzip \
       libzip-dev \
       libxml2-dev \
       libssl-dev \
       libc-client-dev \
       libkrb5-dev \
    &amp;&amp; docker-php-ext-configure imap --with-kerberos --with-imap-ssl \
    &amp;&amp; CFLAGS="-I/usr/src/php" docker-php-ext-install zip mysqli pdo pdo_mysql xmlreader imap

RUN curl --silent --show-error https://getcomposer.org/installer | php
RUN mv composer.phar /usr/local/bin/composer

# Bake composer dependencies into the image for production
WORKDIR /app

COPY composer.json ./
COPY composer.lock ./

RUN export COMPOSER_ALLOW_SUPERUSER=1 &amp;&amp; \
    composer install --no-scripts --no-autoloader --no-dev

COPY . ./

RUN export COMPOSER_ALLOW_SUPERUSER=1 &amp;&amp; \
    composer dump-autoload --optimize &amp;&amp; \
    composer run-script post-install-cmd

COPY vhost.conf /etc/apache2/sites-available/000-default.conf

RUN chown -R www-data:www-data ./ &amp;&amp; \
    a2enmod rewrite

EXPOSE 80
</code></pre>

<p>.lando.yml</p>

<pre><code>name: mysite
env_file:
  - .env
proxy:
  appserver:
    - mysite.lndo.site
  database:
    - db.mysite.lndo.site
services:
  appserver:
    type: compose
    services:
      build: .
      command: apache2-foreground
  database:
    type: mysql
    portforward: 3306
    creds:
      ---super secret---
</code></pre>

<p>composer.json</p>

<pre><code>{
    "name": "MySite/MySite",
    "description": "Would work great if not for caching issues. :(",
    "type": "project",
    "require": {
        "ext-json": "*",
        "ext-imap": "*",
        "doctrine/orm": "^2.6.2",
        "doctrine/migrations": "^2.0",
        "zbateson/mail-mime-parser": "^1.1",
        "rct567/dom-query": "^0.7.0",
        "sabre/xml": "^2.1",
        "phpmailer/phpmailer": "^6.0"
    },
    "autoload": {
        "psr-4": {
            "MySite\\": "./lib"
        }
    }
}
</code></pre>

<hr>

<p>Update:
I've found that by deleting <code>vendor/symfony/console</code> and then running <code>composer install</code> it seems to clear the cache. I wish I could figure it out from here, but the answer still eludes me. What does symfony console have to do with autoload caching code?? I have no idea.</p>

## Answers
### Answer ID: 58678227
<p>I finally figured it out, but it took me all day. I hope someone stumbles across this and it saves you time. Here is what I had to do, it was so easy:</p>

<p>Just put the following code into your composer.json file and run <code>composer install</code>!</p>

<pre><code>    "config": {
        "optimize-autoloader": true
    },
</code></pre>

<p>I don't know WHY this works though. I kind of would assume that enabling the optimizer would CAUSE caching, but instead it seems to disable it. I honestly have no idea why this works. If someone else can explain this better than me, then I'd vote for your answer over mine.</p>

