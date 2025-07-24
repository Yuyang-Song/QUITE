# How do I batch process my R machine learning model?
[Link to question](https://stackoverflow.com/questions/55803864/how-do-i-batch-process-my-r-machine-learning-model)
**Creation Date:** 1555989758
**Score:** 4
**Tags:** python, r, amazon-web-services, amazon-redshift, amazon-elastic-beanstalk
## Question Body
<p>I have an R script for a random forest classification model. I connected my R instance to my redshift postgres database with <code>RPostgreSQL</code> and then ran a series of data transformation and model commands, using the <code>caret</code> library. </p>

<p>My model assigns a score to every user. I've been running the model on my own and uploading the data s3 and then <a href="https://stackoverflow.com/questions/20257226/how-to-import-data-files-from-s3-to-postgresql-rds">transferring it</a> to postgres with <code>\copy</code></p>

<p>I'd like to automate the process. All the queries stay the same every time, including the R script to build the model, but the underlying data changes and so I want to make sure my model is calculating from the most up to date data and then rewriting the <code>scores</code> table.</p>

<p>I was going to use <code>AWS lambda</code> and set up a cron job, but the model takes more than 300 seconds. Instead, I'm thinking about this architecture:</p>

<p>1- Write a script that triggers the R job to run with a curl request. It would cause the R script to download the new data and create the model with a rest API through  <a href="https://cran.r-project.org/web/packages/plumber/plumber.pdf" rel="nofollow noreferrer"><code>plumbR</code></a> </p>

<p>2- Have the R API return the new <code>scores</code> as a JSON object and then use the Python script to upload the scores to <code>s3</code> and then<code>\copy</code> them over to redshift postgres.</p>

<p>3- Set up a cron job on AWS elastic beanstalk to trigger this every Monday, </p>

<p>Could that work? Can I use AWS beanstalk to set up a python script to run automatically and, if so, does that mean I need an ec2 instance running 24/7? </p>

