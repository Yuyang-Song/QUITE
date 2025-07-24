# Save entities to a REST API instead of DB using Doctrine 2
[Link to question](https://stackoverflow.com/questions/20555763/save-entities-to-a-rest-api-instead-of-db-using-doctrine-2)
**Creation Date:** 1386888005
**Score:** 26
**Tags:** php, rest, symfony, doctrine-orm, persistence
## Question Body
<p>This is related to my other question: <a href="https://stackoverflow.com/questions/20380245/persisting-entities-using-a-rest-api">Persisting entities using a REST API</a>.</p>

<p>For a project in Symfony2 I need to be able to persist entities <em>using an remote (third-party) RESTful API</em>. I also want to be able to retrieve entities with data from that API.</p>

<p>In other words, <strong>my objects are saved in the third-party database</strong>. They <strong>are not</strong> saved in my own database. Whenever I need to save data, or find data, I use their REST API.</p>

<p>I have been pointed to several libraries, including <a href="https://github.com/doctrine/rest" rel="noreferrer">one made by Doctrine itself</a>. However, none of them offers me what I'm looking for. The one made by Doctrine is the best option, but uses the Active Record pattern and doesn't offer all the sweet Doctrine 2 stuff. Don't get me wrong, I've been using Active Record implementations for a long time, but I've fallen in love with Doctrine's Data Mapper pattern now.</p>

<p>Ideally, I'd like to be able to use Doctrine's ORM and simply replace the database-specific part with logic that saves entities using an API call. (and of course retrieves them using that same API). This way I can save my entities using roughly the same syntax:</p>

<pre><code>// current way to save $entity in database:
$em = $this-&gt;getDoctrine()-&gt;getManager();
$em-&gt;persist($entity);
$em-&gt;flush();

// desired way to save $entity using REST API:
// (just an example, it doesn't have to be exactly like this)
$em = $this-&gt;getDoctrine()-&gt;getManager('rest');
$em-&gt;persist($entity);
$em-&gt;flush();
</code></pre>

<p>Note that I'm not trying to build my own API, I'm simply trying to communicate with a third party API in order to save my entities. I'm relatively new to Doctrine, but I'm liking it so far. I really like the idea of seperating the persistence logic from the entities, but so far I can't find out how I can use that to save them using an API.</p>

<p>There is an article in Symfony's documentation, describing <a href="http://symfony.com/doc/current/cookbook/doctrine/multiple_entity_managers.html" rel="noreferrer">how to work with multiple Entity Managers</a>. I'm looking for a solution similar to this, but with an entity manager that enables me to use REST instead of the DB.</p>

<p>I've been trying to tweak Doctrine's ORM myself, but I only end up rewriting half their code because it (seems to be) too tightly coupled to the Database-specific logic. I might be doing something stupid of course.</p>

<p>So my question is, <strong>is there a way to replace / override the database-specific parts of Doctrine's ORM with custom ones</strong>? Without rewriting a lot of things that should be common for all persistence methods? Has it been done before? Or is it simply not possible because Doctrine is intended for use with a database and isn't flexible enough for other uses?</p>

<h2>My own progress</h2>

<p>CakePHP seems to be able to do this, by letting you define a custom <a href="http://book.cakephp.org/2.0/en/models/datasources.html" rel="noreferrer">DataSource</a>. This way you can save your models using an SQL database, but also using an API, sessions, etc. I want to do roughly the same, but using Doctrine instead of CakePHP.</p>

<h3>Update 1</h3>

<p>The actual database queries seem to be executed by the
<a href="https://github.com/doctrine/doctrine2/blob/master/lib/Doctrine/ORM/Persisters/BasicEntityPersister.php" rel="noreferrer"><code>Doctrine\ORM\Persisters\BasicEntityPersister</code> class</a>. There are several other xxxPersister classes, to deal with different types of inheritance. It might be possible to replace the xxxPersister classes with our own, so we can replace the DB code with REST API code.</p>

<p>The persister objects are created within the <code>getEntityPersister()</code> method of the <a href="https://github.com/doctrine/doctrine2/blob/master/lib/Doctrine/ORM/UnitOfWork.php" rel="noreferrer"><code>Doctrine\ORM\UnitOfWork</code></a> class. The classnames are hardcoded so we need to override <code>Doctrine\ORM\UnitOfWork</code> if we want to use our own persisters.</p>

<h3>Update 2</h3>

<p><code>Doctrine\ORM\UnitOfWork</code> seems to be hardcoded into <a href="https://github.com/doctrine/doctrine2/blob/master/lib/Doctrine/ORM/EntityManager.php" rel="noreferrer"><code>Doctrine\ORM\EntityManager</code></a>, so we need to override that one as well. However, this class seems to contain some database-specific parts. For instance, it's constructor requires a <code>Doctrine\DBAL\Connection</code> object as parameter. Perhaps it's better to create our own EntityManger (implementing the <code>Doctrine\Common\Persistence\ObjectManager</code> interface), as long as that doesn't take too much time / effort.</p>

<h3>Update 3</h3>

<p>The database-specific code for retrieving/loading/finding objects lives in the same class as the code for persisting / deleting etc: the <code>Doctrine\ORM\Persisters\xxxPersister</code> classes. So if we are able to replace them with our own, in order to persist objects, we can retrieve objects as well. When you call <code>$entityRepository-&gt;findAll()</code>, for instance, it will return <code>$entityRepository-&gt;findBy(array())</code> (because <code>findAll()</code> is simply an alias for <code>findBy(array())</code>) which will run the following code:</p>

<pre><code>$persister = $this-&gt;_em-&gt;getUnitOfWork()-&gt;getEntityPersister($this-&gt;_entityName);

return $persister-&gt;loadAll($criteria, $orderBy, $limit, $offset);
</code></pre>

<p>In other words, once we get <code>EntityManager</code> to create the right <code>UnitOfWork</code> and <code>xxxPersister</code> objects, we will be able to use the <code>find</code> methods in the <code>EntityRepository</code>.</p>

<h3>Update 4</h3>

<p>I discovered that a new feature is developed for Doctrine: <a href="https://github.com/doctrine/doctrine2/pull/769" rel="noreferrer">custom persisters</a> (also see <a href="http://www.doctrine-project.org/jira/browse/DDC-391" rel="noreferrer">this</a>). This should make it easier to use a custom persister class. I don't know yet if it will enable us to create a non-DB persister, but it looks promising. However, the last updates were in August, so I'm not sure if it's still in active development.</p>

## Answers
### Answer ID: 36251447
<p>DoctrineRestDriver is exactly doing what you are looking for.
<a href="https://github.com/CircleOfNice/DoctrineRestDriver">https://github.com/CircleOfNice/DoctrineRestDriver</a></p>

<p>Configure Doctrine:</p>

<p><code>doctrine:
      dbal:
          driver_class: "Circle\\DoctrineRestDriver\\Driver"
          host:         "http://www.your-url.com/api"
          port:         80
          user:         "Circle"
          password:     "CantRenember"
</code></p>

<p>Build entity:</p>

<pre><code>/**
 * This annotation marks the class as managed entity:
 *
 * @ORM\Entity
 *
 * You can either only use a resource name or the whole url of
 * the resource to define your target. In the first case the target 
 * url will consist of the host, configured in your options and the 
 * given name. In the second one your argument is used as it is.
 * Important: The resource name must begin with its protocol.
 *
 * @ORM\Table("products|http://www.yourSite.com/api/products")
 */
class Product {

    /**
     * @ORM\Column(type="integer")
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="AUTO")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=100)
     */
    private $name;

    public function getId() {
        return $this-&gt;id;
    }

    public function setName($name) {
        $this-&gt;name = $name;
        return $this;
    }

    public function getName() {
        return $this-&gt;name;
    }
}
</code></pre>

<p>Let's assume we have used the value <a href="http://www.yourSite.com/api/products">http://www.yourSite.com/api/products</a> for the product entity's @Table annotation.</p>

<p>Controller:</p>

<pre><code>&lt;?php

namespace CircleBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\HttpFoundation\Response;

class UserController extends Controller {

    /**
     * Sends the following request to the API:
     * POST http://www.yourSite.com/api/products HTTP/1.1
     * {"name": "Circle"}
     *
     * Let's assume the API responded with:
     * HTTP/1.1 200 OK
     * {"id": 1, "name": "Circle"}
     *
     * Response body is "1"
     */
    public function createAction() {
        $em     = $this-&gt;getDoctrine()-&gt;getManager();
        $entity = new CircleBundle\Entity\Product();
        $entity-&gt;setName('Circle');
        $em-&gt;persist($entity);
        $em-&gt;flush();

        return new Response($entity-&gt;getId());
    }

    /**
     * Sends the following request to the API by default:
     * GET http://www.yourSite.com/api/products/1 HTTP/1.1
     *
     * which might respond with:
     * HTTP/1.1 200 OK
     * {"id": 1, "name": "Circle"}
     *
     * Response body is "Circle"
     */
    public function readAction($id = 1) {
        $em     = $this-&gt;getDoctrine()-&gt;getManager();
        $entity = $em-&gt;find('CircleBundle\Entity\Product', $id);

        return new Response($entity-&gt;getName());
    }

    /**
     * Sends the following request to the API:
     * GET http://www.yourSite.com/api/products HTTP/1.1
     *
     * Example response:
     * HTTP/1.1 200 OK
     * [{"id": 1, "name": "Circle"}]
     *
     * Response body is "Circle"
     */
    public function readAllAction() {
        $em       = $this-&gt;getDoctrine()-&gt;getManager();
        $entities = $em-&gt;getRepository('CircleBundle\Entity\Product')-&gt;findAll();

        return new Response($entities-&gt;first()-&gt;getName());
    }

    /**
     * After sending a GET request (readAction) it sends the following
     * request to the API by default:
     * PUT http://www.yourSite.com/api/products/1 HTTP/1.1
     * {"name": "myName"}
     *
     * Let's assume the API responded the GET request with:
     * HTTP/1.1 200 OK
     * {"id": 1, "name": "Circle"}
     *
     * and the PUT request with:
     * HTTP/1.1 200 OK
     * {"id": 1, "name": "myName"}
     *
     * Then the response body is "myName"
     */
    public function updateAction($id = 1) {
        $em     = $this-&gt;getDoctrine()-&gt;getManager();
        $entity = $em-&gt;find('CircleBundle\Entity\Product', $id);
        $entity-&gt;setName('myName');
        $em-&gt;flush();

        return new Response($entity-&gt;getName());
    }

    /**
     * After sending a GET request (readAction) it sends the following
     * request to the API by default:
     * DELETE http://www.yourSite.com/api/products/1 HTTP/1.1
     *
     * If the response is:
     * HTTP/1.1 204 No Content
     *
     * the response body is ""
     */
    public function deleteAction($id = 1) {
        $em     = $this-&gt;getDoctrine()-&gt;getManager();
        $entity = $em-&gt;find('CircleBundle\Entity\Product', $id);
        $em-&gt;remove($entity);
        $em-&gt;flush();

        return new Response();
    }
}
</code></pre>

<p>You can even use DQL or native queries.</p>

### Answer ID: 33232424
<p>I wanted to do a similar thing, so I built this library to help expose doctrine entities as RESTful resources. It has a fair amount of features, and allows you to define exactly what you want to have exposed via both pull (GET) and push (POST/PUT/PATCH) methods.</p>

<p><a href="http://leedavis81.github.io/drest/" rel="nofollow">http://leedavis81.github.io/drest/</a></p>

<p><a href="https://github.com/leedavis81/drest" rel="nofollow">https://github.com/leedavis81/drest</a></p>

<p>Hope it helps</p>

### Answer ID: 23389418
<p>As a ready-to-use solution wasn't available, I decided to write my own. I called it <a href="https://github.com/rapl/rapl" rel="nofollow noreferrer">RAPL</a>. It's heavily inspired by Doctrine's ORM (in fact, it uses many of the interfaces provided by Doctrine Common).</p>

<p>Using RAPL I can simply write a small YAML file to configure the mapping between my entities and the web service, allowing me to persist/retrieve entities using the custom EntityManager.</p>

### Answer ID: 20719324
<p>I'm not sure, but you can try to use <a href="http://docs.doctrine-project.org/en/2.0.x/reference/events.html" rel="nofollow">lifecycle callback events</a> for entities to perform persisting logic via REST.</p>

### Answer ID: 20679037
<p>I think you are in not right way.<br>
I'm not ready to dig into the documentation now, but I understand doctrine stack as:</p>

<p>ORM -> DQL (doctrine query language) ->dbal ->Some database sql</p>

<p>And point for implementation you feature in DBAL as custom database driver.</p>

<p>I think create common REST-Driver realy interesting feature and it will do easy integration  with third-party services. </p>

### Answer ID: 20602760
<p>You might use <a href="https://github.com/doctrine/rest">https://github.com/doctrine/rest</a> to build a REST client, which talks to the target server. The essential part here is the mapping from entity (local) to REST API (target).</p>

<p>In short: Doctrine2 (local DB) -> Rest client (entity to rest mapping) -> Request (target server)</p>

<p>Doctrine/Rest provides also the other way around: a Doctrine Rest Server, to expose your local entities via REST (requests to your server). But thats not what you are looking for.</p>

