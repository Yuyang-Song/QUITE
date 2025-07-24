# Jobs processing in background from web application
[Link to question](https://stackoverflow.com/questions/21313028/jobs-processing-in-background-from-web-application)
**Creation Date:** 1390492190
**Score:** 8
**Tags:** php, resque, sidekiq
## Question Body
<p>I want to schedule and run a lot of jobs in the background during a web application execution.<br>
The web app is built on top of Symfony 2 and Doctrine 2.  </p>

<p>I know the job-processing can be done with libraries like Resque or Sidekiq. 
However, these libraries and my application are written in different languages, so I am wondering how I can run Sidekiq jobs written in Ruby which should integrate with my app written in PHP.  </p>

<p>What I'm asking myself is if the only way to do this is rewriting a large amount of code to query the database from PHP to ruby, to be able to execute the job in Sidekiq/Resque.</p>

## Answers
### Answer ID: 27244727
<p>I have made use of Resque in several projects using <a href="https://github.com/chrisboulton/php-resque" rel="noreferrer">https://github.com/chrisboulton/php-resque</a> and <a href="https://github.com/chrisboulton/php-resque-scheduler" rel="noreferrer">https://github.com/chrisboulton/php-resque-scheduler</a></p>

<p>Its been working really well, I even made a Symfony bundle to make working with it really easy. <a href="https://github.com/mcfedr/resque-bundle" rel="noreferrer">https://github.com/mcfedr/resque-bundle</a> - supports background jobs and scheduled jobs. Much more powerful than using cron.</p>

<p>The main reason for choosing Resque over other options is that it works on Redis, which is easy to deploy and scale. On AWS I use Elasticache managed instances for a completely hassle free setup. </p>

### Answer ID: 21319390
<p>Have you taken a look at <a href="http://gearman.org/" rel="noreferrer">Gearman</a>? It lets you run background jobs just like Sidekiq, but it's language agnostic. For example, you can use PHP for everything, or you can queue up jobs in PHP and have the actual workers written in Ruby.</p>

