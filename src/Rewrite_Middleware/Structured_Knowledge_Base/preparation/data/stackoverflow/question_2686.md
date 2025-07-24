# Iterate over struct and perform database queries
[Link to question](https://stackoverflow.com/questions/47299504/iterate-over-struct-and-perform-database-queries)
**Creation Date:** 1510721097
**Score:** 0
**Tags:** go, iteration
## Question Body
<p>So I'm new to go and I come from a javascript/node background and for practice, I've been rewriting some of my javascript code into go.</p>

<p>I have a situation where I have an struct (in node it was my object) and I need to iterate over it and perform two database queries. I have something that works but it seems costly and repetitive.</p>

<p><strong>Struct:</strong></p>

<pre><code>type SiteUsers struct {
    Active struct {
        Moderators []string `json:"moderators"`
        Admins     []string `json:"admins"`
        Regulars   []string `json:"regulars"`
    } `json:"active"`
}
</code></pre>

<p>Then in the function where I handle an api request that returns JSON binded to this struct I use a for range loop for each role under active. For each one I perform the same first query and then a second one that is specific to each one.</p>

<pre><code>v := getSiteUsers(&amp;usrs, website)

for _, moderators := range v.Active.Moderators {
    // Insert into user table
    // Insert into user table with role of moderator
}

for _, admins := range v.Active.Admins {
    // Insert into user table
    // Insert into user table with role of admin
}

for _, regulars := range v.Active.Regulars {
    // Insert into user table
    // Insert into user table with role of regular
}
</code></pre>

<p>This method will work but it doesn't feel completely right and I would love to get some input from people experienced with go.</p>

## Answers
### Answer ID: 47314869
<p>Would something like this be better?</p>

<pre><code>v := getSiteUsers(&amp;usrs, website)

insertUsers := func(users []string, role roleType) {
    for _, user := range users {
        // Insert into user table
        // Insert into user table with given role
    }
}

insertUsers(v.Active.Moderators, moderatorRole)
insertUsers(v.Active.Admins, adminRole)
insertUsers(v.Active.Regulars, regularRole)
</code></pre>

