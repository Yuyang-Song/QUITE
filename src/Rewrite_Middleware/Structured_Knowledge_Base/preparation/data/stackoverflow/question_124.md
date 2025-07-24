# Custom filter/scope based on project model
[Link to question](https://stackoverflow.com/questions/13774260/custom-filter-scope-based-on-project-model)
**Creation Date:** 1354938372
**Score:** 0
**Tags:** ruby-on-rails, ruby-on-rails-3, squeel
## Question Body
<p>I'll try to be brief, but some detail is required. I'm trying to prototype a rewrite (in Rails) of a custom project management system. The primary purpose is to help companies who are relocating or expanding in Alabama to recruit, screen, and hire their workforce. The current system run on 4D and Active4D, which most people have never heard of. Horrible DB, but decent desktop client/server system.</p>

<p>For those who may have not heard, they build Mercedes, Honda and Hyundais in Alabama and most employees of those companies were hired through this agency using this system. Beside the big guys, there are numerous other companies who use this economic development agency to select their workforce. The process is mainly a project is started with the goal of hiring x amount of employees. Candidate are recruited from the Citizen of the state. The Candidates go through a selection process that has many phases or Stages - mainly Application, Interview, Assessment, Training, and Hire. Each Project is different and may have some custom Stages. Each Stage may have numerous assessments that are scored in some way (online application, interview score sheet, etc). After completion of the assessments in each Stage, Candidates are Progressed to the next stage, or eliminated from the project.</p>

<p>While the current DB structure is okay, we've tried to make some improvements. The below model and relations are snippets of the current prototype, going top down from the Citizen to the Project. Some of the through relations were added just to give a better picture of the DB structure. I forgot to point out that each Project may have different Programs that are usually job based. There are also numerous other models to aid in this management process (schedule events, manage instructors, etc) that are not depicted.</p>

<pre><code>class Citizen &lt; ActiveRecord::Base
  has_one :user, :as =&gt; :loginable
  has_many :candidates
  has_many :educations
  has_many :work_histories
  has_many :skills
end
class Candidate &lt; ActiveRecord::Base
  belongs_to :program
  belongs_to :citizen
  has_many :progressions
end
class Progression &lt; ActiveRecord::Base
  belongs_to :candidate
  belongs_to :stage
  has_many :scores
  has_one :citizen, :through =&gt; :candidate
end
class Stage &lt; ActiveRecord::Base
  belongs_to :program
  has_many :assessors, :dependent =&gt; :destroy
  has_many :progressions, :dependent =&gt; :destroy
  has_many :candidates, :through =&gt; :progressions
  has_many :citizens, :through =&gt; :candidates
  has_many :educations, :through =&gt; :citizens
end
class Program &lt; ActiveRecord::Base
  belongs_to :project
  has_many :stages, :order =&gt; "sequence", :dependent =&gt; :destroy
  has_many :candidates, :dependent =&gt; :destroy
end
</code></pre>

<p>There is a question coming! The Stage model is the key part of the system because it is where candidates are selected to progress to the next Stage. Since the current system was designed before an on-line presence, semi-static information such as education, skills, work history were not well defined and added as an assessment in the on-line application - which resulted in duplication of static information (Citizens apply for multiple projects and had to repeat the information that is part of their profile).  The prototype still wants to evaluate some of that information (Do you have a high school diploma or GED?) along with custom Program specific assessments (How may years of welding experience do you have?).</p>

<p>We figured we could write a filter search to screen that static information and combine it with custom assessment score - that's easier said that done. Each project may be looking for different education and skill requirements. It is almost like I need a custom scope for each project/program. I just started to look at things like Ransack and Squeel and they may help, but it would be up to the screeners to use the same filter - consistently. </p>

<p>Before the filter approach, I though about adding an feature to the assessment engine I wrote to somehow query the static information as basically a question and answer and score it.  The question is how would you approach a filter that would look for Citizens who have specific Education accomplishments, have specific levels of experience in different Skills, have a certain status in in their current Progression, etc, etc.  and then customize it for different Programs?</p>

<p>Of course I'm not looking for a specific answer, but approaches.</p>

## Answers
### Answer ID: 13789742
<p>Sorry for the long post, but sometimes you have to write out what you are trying to figure out, before you figure it out! </p>

<p>My solution ended up going back to my generic assessments engine and writing a method that would score things like education and other things connected to the Citizens model. The engine usually scored responses from a question/answer form. I just had to create a score object. The score is then part of the selection filter.</p>

<p>I still would like to expand the filter capability and from a post on the Ransack wiki, it looks like it creates a search object (json?) that can be captured and probably stashed away someplace related to a project. </p>

<p>Again, I apologize for the long post.</p>

