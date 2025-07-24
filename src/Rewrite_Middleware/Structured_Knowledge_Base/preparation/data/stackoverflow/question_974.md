# query with result based on two tables without join
[Link to question](https://stackoverflow.com/questions/52552113/query-with-result-based-on-two-tables-without-join)
**Creation Date:** 1538126329
**Score:** 1
**Tags:** typo3, typo3-8.x
## Question Body
<p>i want to create query in <code>Query Builder</code> The query should at least looks like (plus default typo3 fields hidden, deleted etc.):</p>

<pre>

    SELECT DISTINCT
        *
    FROM
        domain_model_topic,
        domain_model_post
    WHERE
        domain_model_topic.uid = domain_model_post.topic
            AND (domain_model_topic.title LIKE '%test%'
            OR domain_model_post.text LIKE '%test%')

</pre>

<p>Query is usage to search forum for selected word
In this query i have one variables from user: its text to search in topics and posts.</p>

<p>Based on documentation from <a href="https://docs.typo3.org/typo3cms/CoreApiReference/8.7/ApiOverview/Database/QueryBuilder/" rel="nofollow noreferrer">https://docs.typo3.org/typo3cms/CoreApiReference/8.7/ApiOverview/Database/QueryBuilder/</a></p>

<p>i created something like:</p>

<pre>

    /** @var \TYPO3\CMS\Core\Database\Query\QueryBuilder $queryBuilder */
    $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)->getQueryBuilderForTable('domain_model_topic');
    $queryBuilder->getRestrictions()->removeAll();
    $queryBuilder
        ->select('*')
        ->from('domain_model_post')
        ->from('domain_model_topic')
        ->where(
            $queryBuilder->expr()
                ->eq('domain_model_topic.uid', 'domain_model_post.topic') . ' AND ' .
            $queryBuilder->expr()
                ->like('domain_model_topic.title', $queryBuilder->createNamedParameter('%' . $queryBuilder->escapeLikeWildcards($search->getSWord()) . '%')) . ' OR ' .
            $queryBuilder->expr()
                ->like('domain_model_post.text', $queryBuilder->createNamedParameter('%' . $queryBuilder->escapeLikeWildcards($search->getSWord()) . '%'))
        );
    $test = $queryBuilder->execute()->fetchAll();

</pre>

<p>but this code cause error <code>Allowed memory size of XXX bytes exhausted</code> for any assigned number of memory </p>

<p>i tried rewrite query to have its simpler (without  <code>$queryBuilder-&gt;expr():</code> )</p>

<pre>

    $queryBuilder
        ->select('*')
        ->from('domain_model_post')
        ->from('domain_model_topic')
        ->where(
    "domain_model_topic.uid = domain_model_post.topic
    AND (domain_model_topic.title LIKE '%" . $variableStringFromUser . "%'
    OR domain_model_post.text LIKE '%" . $variableStringFromUser . "%')"
    );

</pre>

<p>And it work, but have seriously problems with security, then i tried do add <code>$queryBuilder-&gt;createNamedParameter($variableStringFromUser)</code>
and that didn't work</p>

<p>My goal is to create search by search word for forum for topics from one table and post from another. I can't use left join because its have seriously performance issue and after some test in mysql, select from two tables give best result (and work in mysql)</p>

<p>What can i do to create query from begining of post in typo3_8 (best with query builder) in secure way (and as clean as possible)</p>

## Answers
### Answer ID: 52586388
<p>After long trying i found solution to create query which work fast. </p>

<pre>

    $queryBuilder
        ->select('*')
        ->from('domain_model_post')
        ->from('domain_model_topic')
        ->orWhere(
            $queryBuilder->expr()->like('domain_model_topic.title', $queryBuilder->createNamedParameter('%' . $queryBuilder->escapeLikeWildcards($search->getSWord()) . '%')),
            $queryBuilder->expr()
                ->like('domain_model_post.text', $queryBuilder->createNamedParameter('%' . $queryBuilder->escapeLikeWildcards($search->getSWord()) . '%'))
        )
        ->andWhere(
            $queryBuilder->expr()->eq('domain_model_topic.uid', 'domain_model_post.topic')
        );

</pre>

<p>Query for this code:</p>

<pre>

    SELECT 
        *
    FROM
        `domain_model_post`,
        `domain_model_topic`
    WHERE
        ((`domain_model_topic`.`title` LIKE '%test%')
            OR (`domain_model_post`.`text` LIKE '%test%'))
            AND (`domain_model_topic`.`uid` = domain_model_post.topic)

</pre>

<p>its work hundred time faster than previous query. I recommend for everyone to try optimize searches by text with doable <code>from</code> and <code>where</code> instead of join</p>

