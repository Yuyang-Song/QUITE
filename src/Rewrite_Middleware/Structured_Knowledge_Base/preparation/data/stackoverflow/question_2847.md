# How to apply condition to a relation, or how to properly handle JOIN queries with WHERE clause in Room?
[Link to question](https://stackoverflow.com/questions/55522673/how-to-apply-condition-to-a-relation-or-how-to-properly-handle-join-queries-wit)
**Creation Date:** 1554402215
**Score:** 5
**Tags:** android, android-room, pojo, relation, android-livedata
## Question Body
<p>Please bear with me, i'm new to architecture components and android in general.
My question is similar to <a href="https://stackoverflow.com/questions/49005681/room-relations-with-conditions#50698610">this question</a> but unfortunately the accepted answer doesn't seem to work.
I have an example one to many relation like in  <a href="https://stackoverflow.com/questions/44330452/android-persistence-room-cannot-figure-out-how-to-read-this-field-from-a-curso/44424148#44424148">this answer</a>. My example database has two tables USERS and PETS as shown in the following images:</p>

<p><img src="https://i.postimg.cc/t4J66zJv/table-users.png" alt="1"><img src="https://i.postimg.cc/zX0W3QzR/table-pets.png" alt="2"></p>

<p>Let's say I want to get a list of users containing a list of their pets grouped by user id <strong>only</strong> with pets younger than 5. 
The result should look like this (pseudo code):</p>

<p>{uId: 2, [Pet3, Pet4]; uId: 4, [Pet6, Pet7];}</p>

<p>Another requirement is that the Dao needs to return the list as a LiveData object because I'm using MVVM architecture and want it to be Lifecycle aware and observable.</p>

<p>With these requirements, the <strong>UserDao</strong> would look like this:</p>

<pre><code>@Dao
interface UserDao {

    @Insert
    void insert(User user);

    @Transaction
    @Query("SELECT USERS.uId, PETS.pId , PETS.userId, PETS.age " + 
    "FROM USERS INNER JOIN PETS ON PETS.userId = USERS.uId " +
    "WHERE PETS.age &lt; 5 " +
    "GROUP BY USERS.uId")
    LiveData&lt;List&lt;UserWithPets&gt;&gt; getUserPets();

}
</code></pre>

<p><strong>User</strong> Entity:</p>

<pre><code>@Entity
public class User {
    @PrimaryKey
    public int id; // User id
}
</code></pre>

<p><strong>Pet</strong> Entity:</p>

<pre><code>@Entity
public class Pet {
    @PrimaryKey
    public int id;     // Pet id
    public int userId; // User id
    public int age;
}
</code></pre>

<p>The problem is now: how should i design the UserWithPets that room understands it and maps the cursor the way i want?
Here is what i tried so far:</p>

<h2>Approach 1:</h2>

<p>The most convenient way in my opinion would be using a Relation, like in the POJO below.</p>

<p><strong>UserWithPets</strong> POJO:</p>

<pre><code>public class UserWithPets {
    @Embedded
    public User user;

    @Relation(parentColumn = "id", entityColumn = "userId", entity = Pet.class)
    public List&lt;Pet&gt; pets; 

}
</code></pre>

<p>Unfortunately, the functionality to assign a condition to a relation is not yet implemented by google. So we always get a full list of pets for every user that owns a pet younger than 5. Hopefully this will be possible soon, since the feature request is already assigned <a href="https://issuetracker.google.com/issues/65509934" rel="nofollow noreferrer">here</a> and <a href="https://issuetracker.google.com/issues/112665535" rel="nofollow noreferrer">here</a>.</p>

<p>Statement from google from <a href="https://issuetracker.google.com/issues/63621744" rel="nofollow noreferrer">this</a> feature request:  "we are planning to implement some query rewriting logic to fix these, not for 2.1 but hopefully in 2.2 where we'll focus more on relations."</p>

<h2>Approach 2:</h2>

<p>Another option would be Embedding both, User and Pet like:</p>

<pre><code>public class UserWithPets {
    @Embedded
    public User user;

    @Embedded
    public Pet pet;

}
</code></pre>

<p>This doesn't work either, because now we only get 1 pet per user.</p>

<h2>Approach 3:</h2>

<p><a href="https://stackoverflow.com/a/50698610/11278807">this answer</a> suggests to just create a merged class that extends from user like:</p>

<pre><code>public class UserWithPets extends User {

    @Embedded(prefix = "PETS_")
    List&lt;Pet&gt; pets = new ArrayList&lt;&gt;();
}
</code></pre>

<p>I tried in many ways, with contructor and without, but i can't get it to work. it always gives errors like "Entities and Pojos must have a usable public constructor. You can have an empty constructor or a constructor whose parameters match the fields (by name and type). - java.util.List"
or
The query returns some columns ... which are not used by UserWithPets. So any advice is welcome here.</p>

<h2>Approach 4:</h2>

<p>Just make two queries and stitch the results together. How would i do that using LiveData? Where should the joining operation be done? I can't do it in the Activity, that's not the point of an MVVM pattern. And not in the repository or viewmodel, since LiveData is immutable. Or is there another way? </p>

<p>What would be a working solution to get a result with the above requirements?</p>

