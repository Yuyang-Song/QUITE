# how to use redis and sequelize together
[Link to question](https://stackoverflow.com/questions/63705091/how-to-use-redis-and-sequelize-together)
**Creation Date:** 1599048073
**Score:** 1
**Tags:** node.js, caching, redis, sequelize.js
## Question Body
<p>im using redis for caching and sequelize as my orm.
i want to cache every query as key and it's result as value.
let me give you an example of how i'm trying to do it<br />
imagine user request for all blogs that are created by himself, normally we would write something like this</p>
<pre><code>blogs.findAll({where:{author:req.params.id}})
</code></pre>
<p>when i want to cache something like this i add an attribute named as model and for this example model would be equal to blog after that i will stringify this object and use it as key. this way i can easily create the key and check whether user response is cached or not, but i don't want to rewrite code for every request for checking redis and deciding to make query to database or not and i have 2 models now so i write this piece of code</p>
<pre><code>for (m in models) {
        models[m].myFindAll = function (options = {}) {
            return new Promise(async function (resolve, reject) {
                try {
                    const key = Object.assign({}, options);
                    key.model = m;
                    key.method = &quot;findAll&quot;;
                    var result = await redis.get(JSON.stringify(key));
                    if (result) {
                        resolve(JSON.parse(result));
                    }
                    result = await models[m].findAll(options);
                    redis.set(JSON.stringify(key), JSON.stringify(result));
                    resolve(result);
                } catch (err) {
                    reject(err);
                }
            });
        };
    }
</code></pre>
<p>as you can see i have an object that contains every model that i have and it is named models.
firstly i added User and after that i added Blog.
my problem is that when i try to use myFindAll function on User Model it won't work becuse it tries to set key.model with value of variable m which will be Blog in the run time, i solved it when i passed the model name an argument to my function but i don't want it that way and i think there should be a better way be i can't find it, isn't there some way of accessing right model through this object?</p>
<p>another thing that i tried to used libraries like sequelize-redis-cache and ... but i wanted to do it my way and i don't want to use this library</p>

