# How can I release the semaphore when two futures are completed?
[Link to question](https://stackoverflow.com/questions/62676769/how-can-i-release-the-semaphore-when-two-futures-are-completed)
**Creation Date:** 1593606197
**Score:** 1
**Tags:** java, spring, java-8, guava, future
## Question Body
<p>I am having a Springboot java application that talks to cassandra database and also using google guava libaries.</p>
<p>currently i am facing a an issue. I have a semaphore object in the code.</p>
<p>in my my method i have to perform two write queries simulatenously using two objects( mapper and parameterisedListMsisdnMapper).</p>
<p>Firing each queries using the mappers returns ListenableFuture future  &amp; ListenableFuture future1 objects .  How can I rewrited the below code, so that i will release the semaphore upon completion of both future and future1 object.</p>
<pre><code>public class ParameterisedListItemRepository {
        
        public ParameterisedListItemRepository() {
         this.executor = MoreExecutors.directExecutor();
         this.semaphore = new Semaphore(getNumberOfRequests(session));
        }
       
       public void saveAsync(ParameterisedListItem parameterisedListItem) {
           try {
             semaphore.acquire();
             ListenableFuture&lt;Void&gt; future = mapper.saveAsync(parameterisedListItem);
             ListenableFuture&lt;Void&gt; future1 = parameterisedListMsisdnMapper.saveAsync( mapParameterisedList(parameterisedListItem));
             future.addListener(() -&gt; semaphore.release(), executor);
            } catch (InterruptedException e) {
                        throw new RuntimeException(&quot;Semaphore was interrupted.&quot;);
            }
       }
    
    }
</code></pre>
<p>appreciate any help</p>

## Answers
### Answer ID: 62721399
<p>I have used Futures.whenAllSucceed and it worked</p>
<pre><code>  public void saveAsync(ParameterisedListItem parameterisedListItem) {
        if (parameterisedListItem.getId() == null) {
            parameterisedListItem.setId(UUID.randomUUID());
        }
        Set&lt;ConstraintViolation&lt;ParameterisedListItem&gt;&gt; violations = validator.validate(parameterisedListItem);
        if (violations != null &amp;&amp; !violations.isEmpty()) {
            throw new ConstraintViolationException(violations);
        }

        Callable releasePermit = () -&gt; { semaphore.release();
            return null;
        };
        
        try {
            semaphore.acquire();
            ListenableFuture&lt;Void&gt; future1 = mapper.saveAsync(parameterisedListItem);
            ListenableFuture&lt;Void&gt; future2 = parameterisedListMsisdnMapper.saveAsync( mapParameterisedList(parameterisedListItem));
            Futures.whenAllSucceed(future1, future2).call(releasePermit, executor);

        } catch (InterruptedException e) {
            //FIXME handle exception in better way
            throw new RuntimeException(&quot;Semaphore was interrupted.&quot;);
        }
    }
</code></pre>

