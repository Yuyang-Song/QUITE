# Autowire EntityManager without Entity class in Symfony 6.4 - Problem and solution
[Link to question](https://stackoverflow.com/questions/78854222/autowire-entitymanager-without-entity-class-in-symfony-6-4-problem-and-solutio)
**Creation Date:** 1723229019
**Score:** 0
**Tags:** php, doctrine, symfony6
## Question Body
<p>For the modernisation of a legacy code base I want to retrieve page contents from a database without relying on proper entity classes. Since the database structure itself requires redesign, I  want to execute the queries found in the legacy code base and do things properly after the initial rewrite phase.</p>
<p>Following the recommended Symfony steps, I provided a condition service and implemented the service lookup in the code.</p>
<p>But I ended up with the following HTTP 500 Internal Server Error message:</p>
<pre><code>Cannot autowire service &quot;App\Repository\PageRepository&quot;: argument &quot;$entityClass&quot; of method &quot;Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepositoryProxy::__construct()&quot; is type-hinted &quot;string&quot;, you should configure its value explicitly.
</code></pre>
<p>To do so, I've created a PageRepository class, using the following code:</p>
<pre class="lang-php prettyprint-override"><code>&lt;?php
declare(strict_types=1);

namespace App\Repository;

use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;

class PageRepository extends ServiceEntityRepository
{
    public function findPageByUri(string $uri): array
    {
        $db = $this-&gt;getEntityManager()-&gt;getConnection();

        $query = 'SELECT * FROM pages WHERE url LIKE :uri';

        $stmt = $db-&gt;prepare($query);
        $stmt-&gt;bindValue('uri', $uri);
        $resultSet = $stmt-&gt;executeQuery();

        if (false === ($result = $resultSet-&gt;fetchAssociative())) {
            throw new NotFoundHttpException(sprintf('Page &quot;%s&quot; was not found', $uri));
        }
        return $result;
    }
}
</code></pre>
<p>This repository is injected into a PageLookupService class with the following code:</p>
<pre class="lang-php prettyprint-override"><code>&lt;?php
declare(strict_types=1);

namespace App\Service;

use App\Repository\PageRepository;
use Symfony\Bundle\FrameworkBundle\Routing\Attribute\AsRoutingConditionService;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;

#[AsRoutingConditionService(alias: 'lookup_service')]
class PageLookupService
{
    private UrlGeneratorInterface $router;
    private PageRepository $pageRepository;
    public function __construct(
        UrlGeneratorInterface $router,
        PageRepository $pageRepository
    ) {
        $this-&gt;router = $router;
        $this-&gt;pageRepository = $pageRepository;
    }

    public function lookup(Request $request): array
    {
        $uri = $request-&gt;getPathInfo();
        return $this-&gt;pageRepository-&gt;findPageByUri($uri);
    }

    // To trigger a not found exception, return true for route lookups
    public function doesPageExists(Request $request): bool
    {
        return true;
    }
}
</code></pre>
<p>My page controller has the following code:</p>
<pre class="lang-php prettyprint-override"><code>&lt;?php
declare(strict_types=1);

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class HomeController extends AbstractController
{
    #[Route('/{slug}', name: 'page', condition: &quot;service('lookup_service').doesPageExists(request)&quot;)]
    public function page(PageLookupService $lookupService, Request $request): Response
    {
        $page = $lookupService-&gt;lookup($request);
        return $this-&gt;render('page.html.twig', [
            'title' =&gt; $page['title'],
            'contents' =&gt; $page['contents'],
        ]);
    }
}
</code></pre>
<h2>Solution I found</h2>
<p>Since I was extending the ServiceEntityRepository, I should have injected the entity class name into its constructor, which I hadn't created yet. In order to use the db connection directly, I needed to remove the ServiceEntityRepository extension and inject the EntityManagerInterface directly in this class.</p>
<pre class="lang-php prettyprint-override"><code>&lt;?php
declare(strict_types=1);

namespace App\Repository;

use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

class PageRepository
{
    private EntityManagerInterface $entityManager;

    public function __construct(EntityManagerInterface $entityManager)
    {
        $this-&gt;entityManager = $entityManager;
    }
    public function findPageByUri(string $uri): array
    {
        $db = $this-&gt;entityManager-&gt;getConnection();
        $query = 'SELECT * FROM pages WHERE url LIKE :uri';

        $stmt = $db-&gt;prepare($query);
        $stmt-&gt;bindValue('uri', $uri);
        $resultSet = $stmt-&gt;executeQuery();

        if (false === ($result = $resultSet-&gt;fetchAssociative())) {
            throw new NotFoundHttpException(sprintf('Page &quot;%s&quot; was not found', $uri));
        }
        return $result;
    }
}
</code></pre>
<p>Because I was not able to find this particular error on the internet, I thought it might be useful to share it here. Let me know if there's an easier way to accommodate this quick retrieval of data without the overhead of heaving entities.</p>
<p><strong>CREDITS:</strong> A big shout-out to Stefan Koopmanschap for guiding me towards this solution!</p>

