# Rewriting nested loop
[Link to question](https://stackoverflow.com/questions/10932575/rewriting-nested-loop)
**Creation Date:** 1339074899
**Score:** 1
**Tags:** ruby, architecture
## Question Body
<p>I know, it looks awful but it worked for a while. But now the number of users is so large that the system started to "forget" where exactly it was (losing connection to database)
What's the best practice to rewrite this nested loop? </p>

<pre><code>User.all.each_with_index do
 get Subset of criteria to select data
 Subset1.each do
  getSubset2
   Subset2.each do
    getSubset3
     Subset3.each do
      getSubset4
       Subset4.each do
        compute something
         open file A
          create or update a line
         end
        end
       end
     end
   end 
end
</code></pre>

<p>edit:
Subsets are either queries or predefined arrays. I am trying to combine it as suggested, will brb</p>

<pre><code>User.all.each_with_index do |user|
 Subset1.each do |parameter1|
   Subset2(function(user,parameter1)).each do |object2|
     Subset3.each do |parameter3|
       getSubset4(user, parameter1, object2, parameter3)
         Subset4.each do |data|
          p data
         end
     end
   end
 end
end 
</code></pre>

## Answers
### Answer ID: 10938752
<p>Piggy backing off of @steenslag's answer, let's say your users are</p>

<pre><code>#name, gender, city, profession
Alice, female, Los Angeles, doctor
Bob, male, Los Angeles, lawyer
Carol, female, New York, astronaut
David, male, New York, programmer
</code></pre>

<p>Rather than loop through all users, then all users of a city, then all users of a gender, break those nested queries out.</p>

<pre><code>#bad
User.each do |u1|
  u1.cities.each do |u2|
    u2.genders.each do |u3|
      u3.professions.each do |u4|
        u4.some_method
      end
    end
  end
end

#better
cities = ["Los Angeles", "New York"]
genders = ["female", "male"]
professions = ["lawyer", "doctor", "astronaut", "programmer"]
criteria = cities.product(genders, professions)
</code></pre>

<p>Now you can iterate through one array (criteria) that collects the cross product of all those arrays.</p>

<pre><code>criteria.each do |cr|
  city, gender, profession = cr
  u = User.find_by_city_and_gender_and_profession(city, gender, profession)
  u.some_method
end
</code></pre>

### Answer ID: 10933327
<pre><code>subset1 = %w(a b c )
subset2 = %w(d e f g )
subset3 = [1,2,3,4,5]

subset1.product(subset2, subset3) do |data|
  p data
end
</code></pre>

<p>This has the same effect as a triple loop.</p>

