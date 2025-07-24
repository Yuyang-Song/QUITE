# Stitching schemas in graphql not being resolved and returning null?
[Link to question](https://stackoverflow.com/questions/49502135/stitching-schemas-in-graphql-not-being-resolved-and-returning-null)
**Creation Date:** 1522106516
**Score:** 1
**Tags:** node.js, reactjs, graphql, express-graphql
## Question Body
<p>I have recently started using apollo/graphql to develop an api for my project and mongodb as my backend database. I have followed this tutorial on the apollo website <a href="https://www.apollographql.com/docs/graphql-tools/schema-stitching.html" rel="nofollow noreferrer">https://www.apollographql.com/docs/graphql-tools/schema-stitching.html</a>
to develop a merged schema so i can write queries connecting different schemas. 
The tutorial says to create executable schemas based of your individual schemas</p>

<pre><code>//ExecutableSchemas     
const postSchema  = makeExecutableSchema({
                typeDefs: PostSchema,
     });

    const usersSchema = makeExecutableSchema({
                typeDefs: UsersSchema,

    }); 
</code></pre>

<p>I also have resolvers for the individual schemas which I have tested and work</p>

<pre><code>//Resolvers merged using lodash 
const resolverK= merge(PostResolver, UsersResolver);
</code></pre>

<p>Then i extended the post schema with an author property which should return a User </p>

<pre><code>// Extend schema with new fields
const linkTypeDefs = `
    extend type Post {
        author: Users
    }

`;
</code></pre>

<p>The merged schema will take the userID from the Post typeDef, and pipe that into a user resolver function (userByID) to get the User data relating to that Post </p>

<pre><code>type Post {
  _id: String
  topic: String
  userid: String
}

//Final Schema 
module.exports = mergeSchemas({
        schemas: [postSchema, usersSchema, linkTypeDefs],
        resolvers: mergeInfo =&gt; (

            {
           Post: {
            author: {
              fragment: `fragment PostFragment on Post { userid }`,
              resolve(parent, args, context, info) {
                const id = parent.userid;
                return mergeInfo.delegate(
                  'query',
                  'userByID',
                  {
                    id,
                  },
                  context,
                  info,
                );
              },
            },
          },
        }, 
         resolverK //resolvers for my individual schemas
        ),

      });
</code></pre>

<p>so when i run the query inside graphiql </p>

<pre><code>{
  getPost(id:"5ab7f6adaf915a1d2093fa48"){
     _id
     topic
    userid
    author{
      name
    }
  }
}
</code></pre>

<p>//Output </p>

<pre><code>{
  "data": {
    "getPost": {
      "_id": "5ab7f6adaf915a1d2093fa48",
      "topic": "Some random post topic",
      "userid": "5ab7bf090b9b1a0a5cd3f6db",
      "author": null
    }
  }
}
</code></pre>

<p>I get a null for the author. It seems its not executing my resolver function for Users because i have tested it in isolation and works all the time. It could be the resolver's for the user and post schema's shown as "resolverk" is overriding the merge resolver because all the other queries and mutations work but i'm not entirely sure.  </p>

<pre><code>const UsersResolver = {
    Query: {

      userByID: async (parent, { id }, { UsersModel }) =&gt; {
                        //Retrieve User from mongodb  
                       const user  = await UsersModel.findById(id); 
                       return user; 
      }

    },

    Mutation: {
       ...


    }



  }
</code></pre>

<p>I know i could simply pass a user object for the Post typeDef instead of userid, but im starting with a simple case to see how it works which i will need as my web app gets more complicated and avoid rewriting stuff later on </p>

<p>thanks </p>

