# Remove column from Group By
[Link to question](https://stackoverflow.com/questions/60360986/remove-column-from-group-by)
**Creation Date:** 1582451461
**Score:** 1
**Tags:** sql, t-sql
## Question Body
<p>The query I'm attempting to create:</p>

<blockquote>
  <p>Find the recipe(s) that use the most cloves of Garlic. (1 column, 1 row)</p>
</blockquote>

<p>My issue is that I have to include <code>Recipes.RecipeTitle</code> in my <code>Group By</code> clause or else I get an error. And whenever I include it in <code>Group By</code>, my query returns 4 results instead of 1 (Roast Beef). </p>

<p>Can someone help explain how to rewrite this so that I possibly won't need the <code>Group By</code> clause.</p>

<pre><code>select distinct 
    Recipes.RecipeTitle
from 
    Recipes
inner join 
    Recipe_Ingredients on Recipes.RecipeID = Recipe_Ingredients.RecipeID
inner join 
    Ingredients on Recipe_Ingredients.IngredientID = Ingredients.IngredientID
group by 
    Recipe_Ingredients.Amount, Recipes.RecipeTitle
having 
    Recipe_Ingredients.Amount = max(Recipe_Ingredients.Amount)
    and Recipes.RecipeTitle IN (select Recipes.RecipeTitle
                                from Recipes
                                inner join Recipe_Ingredients on Recipes.RecipeID = Recipe_Ingredients.RecipeID
                                inner join Ingredients on Recipe_Ingredients.IngredientID = Ingredients.IngredientID
                                group by Recipes.RecipeTitle, Ingredients.IngredientName
                                having Ingredients.IngredientName in ('garlic'));
</code></pre>

<p>Database diagram:</p>

<p><a href="https://i.sstatic.net/8vk5W.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/8vk5W.jpg" alt="enter image description here"></a></p>

<p><a href="https://dbfiddle.uk/?rdbms=sqlserver_2019&amp;fiddle=6da5ce3483176069239a515758ac6af1" rel="nofollow noreferrer">Also here is a DB Fiddle I created</a></p>

## Answers
### Answer ID: 60362386
<p>Filter for the garlic <em>before</em> aggregating.  After all, you want recipes that have some amount of garlic in them.</p>

<p>Second, this needs to assume that the measurements for garlic are all the same, so you can just use the <code>amount</code> as a measure.</p>

<p>Then, one method is to use <code>select top (1)</code> or <code>select top (1) with ties</code> to get the results.  The difference is that <code>select top (1)</code> always returns exactly one row even when multiple recipes have the same maximum amount of garlic.</p>

<p>So:</p>

<pre><code>select top (1) with ties r.RecipeTitle
from Recipes r join
     Recipe_Ingredients ri
     on r.RecipeID = ri.RecipeID join
     Ingredients i
     on ri.IngredientID = i.IngredientID
where i.IngredientName = 'garlic'
group by r.RecipeID, r.RecipeTitle
order by sum(amount) desc;
</code></pre>

<p>It is possible to measure garlic in different units -- for instance, "heads" versus "cloves", so you might need to take the measurement unit into account:</p>

<pre><code>select top (1) with ties r.RecipeTitle
from Recipes r join
     Recipe_Ingredients ri
     on r.RecipeID = ri.RecipeID join
     Ingredients i
     on ri.IngredientID = i.IngredientID join
     Measurements m
     on ri.measurementAmountID = m.measurementAmountID
where i.IngredientName = 'garlic' and
      i.MeasurementDescription = 'clove'
group by r.RecipeID, r.RecipeTitle
order by sum(amount) desc;
</code></pre>

### Answer ID: 60361051
<p>You can aggregate, sort and limit:</p>

<pre><code>select top (1) with ties r.RecipeTitle
from Recipes r
inner join Recipe_Ingredients ri on r.RecipeID = ri.RecipeID
inner join Ingredients i on ri.IngredientID = i.IngredientI
group by r.RecipeID, r.RecipeTitle
order by sum(case when i.IngredientName = 'garlic' then 1 else 0 end) desc 
</code></pre>

<p>Notes:</p>

<ul>
<li><p>I used <code>with ties</code> so if there are top ties, the query returns them</p></li>
<li><p>table aliases make the query shorter to write</p></li>
</ul>

