# Text Game: Asynchronous Node - Prompts and MySQL
[Link to question](https://stackoverflow.com/questions/47717071/text-game-asynchronous-node-prompts-and-mysql)
**Creation Date:** 1512745853
**Score:** 0
**Tags:** javascript, mysql, node.js, callback, promise
## Question Body
<p><strong>PREFACE</strong>
So it seems I've coded myself into a corner again. I've been teaching myself how to code for about 6 months now and have a really bad habit of starting over and changing projects so please, if my code reveals other bad practices let me know, but help me figure out how to effectively use promises/callbacks in this project first before my brain explodes. I currently want to delete it all and start over but I'm trying to break that habit. I did not anticipate the brain melting difficulty spike of asynchronicity (is that the word? spellcheck hates it)</p>

<p><strong>The Project</strong> 
WorldBuilder - simply a CLI that will talk to a MySQL database on my machine and mimic basic text game features to allow building out an environment quickly in my spare time. It should allow me to MOVE [DIRECTION] LOOK at and CREATE [ rooms / objects ]. </p>

<p>Currently it works like this:
I use Inquirer to handle the prompt...</p>

<pre><code>  request_command: function(){
    var command = {type:"input",name:"command",message:"CMD:&gt;"}
    inquirer.prompt(command).then(answers=&gt;{
      parser.parse(answers.command);
    }).catch((error)=&gt;{
      console.log(error);
    });
  }`
</code></pre>

<p>The prompt passed whatever the user types to the parser</p>

<pre><code>  parse: function(text) {
      player_verbs = [
        'look',
        'walk',
        'build',
        'test'
      ]
      words = text.split(' ');
      found_verb = this.find(player_verbs, words)[0];
      if (found_verb == undefined) {
        console.log('no verb found');
      } else {
        this.verbs.execute(found_verb, words)
      }
  }
</code></pre>

<p>The parser breaks the string into words and checks those words against possible verbs. Once it finds the verb in the command it accesses the verbs object... 
(ignore scope mouthwash, that is for another post)</p>

<pre><code>verbs: {
    look: function(cmds) {
      // ToDo: Check for objects in the room that match a word in cmds
      player.look();
    },
    walk: function(cmds) {
      possible_directions = ['north','south','east','west'];
      direction = module.exports.find(possible_directions, cmds);
      player.walk(direction[0]);
    },
    build: function(cmds) {
      // NOTE scope_mouthwash exists because for some
      // reason I cannot access the global constant
      // from within this particular nested function
      // scope_mouthwash == menus
      const scope_mouthwash = require('./menus.js');
      scope_mouthwash.room_creation_menu();
    },
    execute: function(verb, args) {
      try{
        this[verb](args);
      }catch(e){
        throw new Error(e);
      }
    }
  }
</code></pre>

<p>Those verbs then access other objects and do various things but essentially it breaks down to querying the database an unknown number of times to either retrieve info about an object and make a calculation or store info about an object. Currently my database query function returns a promise.</p>

<pre><code>  query: function (sql) {
    return new Promise(function(resolve, reject){
      db.query(sql, (err, rows)=&gt;{
          if (err) {
            reject(err);
          }
          else {
            resolve(rows);
          }
      });
    });
  },
</code></pre>

<p><strong>The Problem</strong>
Unfortunately I jumped the gun and started using promises before I fully understood when to use them and I believe I should have used callbacks in some of these situations but I just don't quite get it yet. I solved 'callback hell' before I had to experience 'callback hell' and now am trying to avoid 'promise hell'. My prompt used to call itself in a loop after it triggered the required verbs but this whole approach broke down when I realized I'd get prompt messages in the middle of other prompt cycles for room building and such.</p>

<p>Should my queries be returning promises or should I rewrite them to use callback functions handled by whichever verb calls the query? How should I determine when to prompt the user again in the situation of having an unknown number of asynchronous processes?</p>

<p>So, put in a different way, my question is..</p>

<p><strong>Given the parameters of my program how should I be visualizing and managing the asynchronous flow of commands, each of which may chain to an unknown number of database queries?</strong></p>

<p>Possible Solution directions that have occurred to me..</p>

<p>Create an object that keeps track of when there are pending promises and
simply prompts the user when all promises are resolved or failed.</p>

<p>Rewrite my program to use callback functions where possible and force a known number of promises. If I can get all verbs to work off callback functions I might be able to say something like Prompt.then(resolve verb).then(Prompt)...</p>

<p>Thank you for bearing with me, I know that was a long post. I know enough to get myself in trouble and Im pretty lost in the woods right now.</p>

