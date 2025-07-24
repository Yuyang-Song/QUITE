# How can I work with mongoose following my design pattern?
[Link to question](https://stackoverflow.com/questions/75740640/how-can-i-work-with-mongoose-following-my-design-pattern)
**Creation Date:** 1678855488
**Score:** 1
**Tags:** javascript, node.js
## Question Body
<p>I have a question about how to do something on my structure pattern.
I'm using MongoDB as the database, and Mongoose as the ORM.</p>
<p>Basically, I have the following model for Users:</p>
<pre><code>import { Schema, model } from 'mongoose'

export interface IUser {
    _id: string,
    email: string,
    name: string,
    password: string,
    picture: string,
    description: string,
    plans: [
        {
            name: string,
            price: string,
            monthsDuration: number,
        }
    ],
    role: string,
    balance: number,
    createdAt: Date,
}

const UserSchema = new Schema&lt;IUser&gt;({
    email: {
        type: String,
        index: true,
    },
    name: String,
    password: String,
    picture: String,
    description: String,
    plans: [],
    role: String,
    balance: Number,
    createdAt: {
        type: Date,
        default: Date.now
    }
})

const UserModel = model('pvf2_users', UserSchema)
export { UserModel }
</code></pre>
<p>And then I have the repository that manages the insertion of a new user into the database:</p>
<pre><code>import { User } from &quot;@domain/entities/user.entity.js&quot;;
import { UserModel } from &quot;@domain/models/user.model.js&quot;;
import { UserRepositoryInterface } from &quot;@domain/repositories/user.repository.js&quot;;

export class UserDatabaseRepository implements UserRepositoryInterface {

    async insert(user: User): Promise&lt;void&gt; {
        await UserModel.create(user.data)
    }

}
</code></pre>
<p>The problem is, let's say I want to change from MongoDB to Postgres or whatever other database. Since I'm directly calling the mongoose schema to run the query, I would have to change all repositories that deals with database queries and such. I guess it goes against my design pattern.</p>
<p>How could I build it on a way that I could easily change my database without having to rewrite every file that handles queries? Is it possible?</p>

## Answers
### Answer ID: 75740861
<p>Solved by creating a mongoose abstract class:</p>
<pre><code>import mongoose from &quot;mongoose&quot;

export abstract class MongooseAbstract {

    public constructor(protected modelName: string) { }

    public async db_insert(data: any): Promise&lt;any&gt; {
        const creation = await mongoose.model(this.modelName).create(data)
        return creation
    }

    public async db_findOne(query: any): Promise&lt;any&gt; {
        const doc = await mongoose.model(this.modelName).findOne(query).lean().exec()
        return doc
    }

    public async db_find(query: any, limit = 15): Promise&lt;any&gt; {
        const docs = await mongoose.model(this.modelName).find(query).limit(limit).lean().exec()
        return docs
    }

    public async db_updateOne(id: string, doc: any): Promise&lt;any&gt; {
        const updatedDoc = await mongoose.model(this.modelName).findOneAndUpdate({ _id: id }, doc, { new: true }).lean().exec()
        return updatedDoc
    }

}
</code></pre>

