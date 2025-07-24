# How do you deal with legacy data integrity issues when rewriting software?
[Link to question](https://stackoverflow.com/questions/37200356/how-do-you-deal-with-legacy-data-integrity-issues-when-rewriting-software)
**Creation Date:** 1463106846
**Score:** 4
**Tags:** domain-driven-design, cqrs
## Question Body
<p>I am working on a project which is a rewrite of an existing legacy software. The legacy software primarily consists of CRUD operations (create, read, update, delete) on an SQL database.</p>

<p>Despite the CRUD-based style of coding, the legacy software is extremely complex. This software complexity is not only the result of the complexity of the problem domain itself, but also the result of poor (and regularly bordering on insane) design decision. This poor coding has lead to the data in the database lacking integrity. These integrity issues are not solely in terms of relationships (foreign keys), but also in terms of the integrity within a single row. E.g., the meaning of column "x" outright contradicts the meaning of column "y". (Before you ask, the answer is "yes", I have analysed the problem domain and correctly understand the meaning and purpose of these columns, and better than the original software developers it seems).</p>

<p>When writing the replacement software, I have used principles from Domain Driven Design and Command Query Reponsibility Segregation, primarily due to the complexity of the domain. E.g., I've designed aggregate roots to enforce invariants in the write model, command handlers to perform "cross-aggregate" consistency checks, query handlers to query intentionally denormalised data in a manner appropriate for various screens, etc, etc.</p>

<p>The replacement software works very well when entering new data, in terms of accuracy and ease of use. In that respect, it is successful. However, because the existing data is full of integrity issues, operations that involve the existing data regularly fail by throwing an exception. This typically occurs because an aggregate can't be read from a repository because the data passed to the constructor violates the aggregate's invariants.</p>

<p>How should I deal with this legacy data that "breaks the rules". The old software worked fine in this respect, because it performed next to no validation. Because of this lack of validation, it was easy for inexperienced users to enter nonsensical data (and experienced users became <em>very</em> valuable because they had years of understanding it's "idiosyncrasies").</p>

<p>The data itself is very important, so it cannot be discarded. What can I do? I've tried sorting out the integrity issues as I go, and this has worked in some cases, but in others it is nearly impossible (e.g., data is outright missing from the database because the original developers decided not to save it). The sheer number of data integrity issues is overwhelming.</p>

<p>What can I do?</p>

## Answers
### Answer ID: 37227274
<p>for a question tagged with DDD the answer is almost always talk to your domain expert. How do they want things to work.</p>

<p>I also noticed your question is tagged with CQRS. are you actually implementing CQRS? in that case it should be almost a non-issue.</p>

<p>Your domain model will live on the command side of your application and always enforce validation. The read stack will provide just dumb viewmodels. This means that on a read, your domain model isn't even involved and also no validation is applied. It will just show whatever nonsense it can use to populate your viewmodel. However on a write validations are triggered. and any write will need to adher to the full validations of your viewmodel.</p>

<p>Now back to reality: be VERY sure that the validations you implement are actually the valididations required. For example even something simple as a telephone number (often implemented as 3 digits dash 3 digits dash 4 digits). But then companies haver special phone numbers like 1800-CALLME which not only have digits but also have letters, and could even be of different lengths (and different countries might also have different rules). If your system needs to handle this it pritty much means you can't apply any validation on phonenumbers.</p>

<p>This is just an example how what you might think is a real validation really can't be implemented at all because that 1 special case it needs to handle. The rule here becomes again. Talk to your domain expert how he wants to have things handled. But be VERY careful that your validations doens't make it near impossible for real users to use your system. since that's the fastest way to have your project killed.</p>

<p><strong>Update:</strong> In DDD you would also hear the term anti-corruption layer. This layer ensures that incomming data meets the expectations of your domain model. This might be the prefered method but if you say you cannot ignore items with garbage data then this might not solve the problem in your case.</p>

