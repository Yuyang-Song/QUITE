rules_pool = [
    {
        "id": 4,
        "name": "testAggregateConstantKeyRule3",
        "key": "testAggregateConstantKeyRule3",
        "pattern": "SELECT t7.<x5> FROM (SELECT <x9>, <x10> AS JOB, <x12> AS \"$f2\" FROM <x1> WHERE <<y3>> GROUP BY <x9>) AS t7 WHERE t7.<x3> > <x8>",
        "rewrite": "SELECT <x1>.<x5> FROM <x1> WHERE <<y3>> GROUP BY <x9>, <x1>.<x5> HAVING <x12> > <x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 10,
        "name": "testCastInAggregateReduceFunctions",
        "key": "testCastInAggregateReduceFunctions",
        "pattern": "SELECT CAST(POWER((SUM(<x1>.<x5> * <x1>.<x5>) - (SUM(<x1>.<x5>) * SUM(<x1>.<x5>)) / COUNT(<x4>)) / COUNT(<x4>), <x6>) AS INTEGER), CAST(SUM(<x1>.<x5>) / COUNT(<x4>) AS INTEGER), CAST(POWER((SUM(<x1>.<x5> * <x1>.<x5>) - (SUM(<x1>.<x5>) * SUM(<x1>.<x5>)) / COUNT(<x4>)) / (CASE WHEN COUNT(<x4>) = <x7> THEN NULL ELSE COUNT(<x4>) - <x7> END), <x6>) AS INTEGER), CAST((SUM(<x1>.<x5> * <x1>.<x5>) - (SUM(<x1>.<x5>) * SUM(<x1>.<x5>)) / COUNT(<x4>)) / COUNT(<x4>) AS INTEGER), CAST((SUM(<x1>.<x5> * <x1>.<x5>) - (SUM(<x1>.<x5>) * SUM(<x1>.<x5>)) / COUNT(<x4>)) / (CASE WHEN COUNT(<x4>) = <x7> THEN NULL ELSE COUNT(<x4>) - <x7> END) AS INTEGER)",
        "rewrite": "SELECT STDDEV_POP(<x1>.<x5>), AVG(<x1>.<x5>), STDDEV_SAMP(<x1>.<x5>), VAR_POP(<x1>.<x5>), VAR_SAMP(<x1>.<x5>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 13,
        "name": "testDecorrelateTwoExists",
        "key": "testDecorrelateTwoExists",
        "pattern": "SELECT <x1>.<x9>, <x1>.<x10>, <x1>.<x14>, <x1>.<x16>, <x1>.<x8>, <x1>.<x11>, <x1>.<x17>, <x1>.<x15>, <x1>.<x13> FROM <x1> INNER JOIN (SELECT <x2>.<x15>, <x18> AS \"$f1\" FROM <x2> GROUP BY <x2>.<x15>) AS t5 ON <x1>.<x15> = t5.<x15> LEFT JOIN (SELECT <x3>.<x14>, <x18> AS \"$f1\" FROM <x3> WHERE <x3>.<x11> = <x19> GROUP BY <x3>.<x14>) AS <x7> ON <x1>.<x14> = t10.<x14> WHERE t10.<x12> IS NULL",
        "rewrite": "SELECT <x7> FROM <x1> WHERE EXISTS (SELECT <x7> FROM <x5> WHERE <x1>.<x15> = <x5>.<x15>) AND NOT EXISTS (SELECT <x7> FROM <x6> WHERE <x6>.<x14> = <x1>.<x14> AND <x6>.<x11> = <x19>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 24,
        "name": "testDistinctNonDistinctAggregates",
        "key": "testDistinctNonDistinctAggregates",
        "pattern": "SELECT t2.<x8>, SUM(AVG(DISTINCT <x5>)), AVG(SUM(AVG(DISTINCT <x5>))) FROM (SELECT <<y3>>, <x3>.<x7> AS DEPTNO0 FROM <x1> INNER JOIN <x3> ON <<y1>> GROUP BY <x10>, <x3>.<x7>) AS t2 GROUP BY t2.<x8>",
        "rewrite": "SELECT <<y3>>, AVG(DISTINCT <x3>.<x7>) FROM <x1> INNER JOIN <x3> ON <<y1>> GROUP BY <x10>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 42,
        "name": "testExpandFilterExists",
        "key": "testExpandFilterExists",
        "pattern": "FROM <x1> LEFT JOIN (SELECT <x9> AS i FROM <x2> WHERE <x2>.<x5> < <x11> GROUP BY <x9>) AS <x7> ON <x9> WHERE t4.<x8> IS NOT NULL OR <x12>",
        "rewrite": "FROM <x1> WHERE EXISTS (SELECT <x5> FROM <x4> WHERE <x4>.<x5> < <x11>) OR <x12>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 44,
        "name": "testExpandFilterExistsSimpleAnd",
        "key": "testExpandFilterExistsSimpleAnd",
        "pattern": "FROM <x1>, (SELECT <x7> AS i FROM <x2> WHERE <x2>.<x5> < <x9> GROUP BY <x7>) AS t4 WHERE <<y1>>",
        "rewrite": "FROM <x1> WHERE EXISTS (SELECT <x5> FROM <x4> WHERE <x4>.<x5> < <x9>) AND <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 45,
        "name": "testExpandFilterIn",
        "key": "testExpandFilterIn",
        "pattern": "FROM <x1> LEFT JOIN (SELECT <x2>.<x5>, <x10> AS i FROM <x2> WHERE <x2>.<x6> < <x12> GROUP BY <x2>.<x5>, <x10>) AS <x7> ON <x1>.<x5> = t6.<x5> WHERE t6.<x9> IS NOT NULL OR <x13>",
        "rewrite": "FROM <x1> WHERE <x1>.<x5> IN (SELECT <x4>.<x5> FROM <x4> WHERE <x4>.<x6> < <x12>) OR <x13>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 47,
        "name": "testExpandFilterInComposite",
        "key": "testExpandFilterInComposite",
        "pattern": "FROM <x1> LEFT JOIN (SELECT <x2>.<x7>, <x2>.<x5>, True AS i FROM <x2> WHERE <x2>.<x7> < <x11>) AS <x6> ON <x1>.<x7> = t5.<x7> AND <x1>.<x5> = t5.<x5> WHERE t5.<x8> IS NOT NULL OR <x12>",
        "rewrite": "FROM <x1> WHERE (<x1>.<x7>, <x1>.<x5>) IN (SELECT <x4>.<x7>, <x4>.<x5> FROM <x4> WHERE <x4>.<x7> < <x11>) OR <x12>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 48,
        "name": "testExpandFilterScalar",
        "key": "testExpandFilterScalar",
        "pattern": "FROM <x1> LEFT JOIN (SELECT SINGLE_VALUE(<x2>.<x8>) AS \"$f0\" FROM <x2> WHERE <x2>.<x10> < <x15>) AS <x9> ON <x13> LEFT JOIN (SELECT SINGLE_VALUE(<x3>.<x8>) AS \"$f0\" FROM <x3> WHERE <x3>.<x10> > <x14>) AS <x7> ON <x13> WHERE t7.<x11> < t10.<x11> OR <x16>",
        "rewrite": "FROM <x1> WHERE (SELECT <x5>.<x8> FROM <x5> WHERE <x5>.<x10> < <x15>) < (SELECT <x6>.<x8> FROM <x6> WHERE <x6>.<x10> > <x14>) OR <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 50,
        "name": "testExpandProjectExists",
        "key": "testExpandProjectExists",
        "pattern": "SELECT <<y2>>, CASE WHEN t3.<x7> IS NOT NULL THEN <x8> ELSE False END AS D FROM <x1> LEFT JOIN (SELECT <x8> AS i FROM <x2> WHERE <x2>.<x5> < <x9> GROUP BY <x8>) AS <x6> ON <x8>",
        "rewrite": "SELECT <<y2>>, EXISTS (SELECT <x5> FROM <x3> WHERE <x3>.<x5> < <x9>) AS D FROM <x1>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 51,
        "name": "testExpandProjectIn",
        "key": "testExpandProjectIn",
        "pattern": "SELECT <<y2>>, CASE WHEN t5.<x5> IS NOT NULL THEN <x9> ELSE False END AS D FROM <x1> LEFT JOIN (SELECT <x2>.<x8>, <x9> AS i FROM <x2> WHERE <x2>.<x7> < <x10> GROUP BY <x2>.<x8>, <x9>) AS <x6> ON <x1>.<x8> = t5.<x8>",
        "rewrite": "SELECT <<y2>>, <x1>.<x8> IN (SELECT <x3>.<x8> FROM <x3> WHERE <x3>.<x7> < <x10>) AS D FROM <x1>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 52,
        "name": "testExpandProjectInComposite",
        "key": "testExpandProjectInComposite",
        "pattern": "SELECT <<y2>>, CASE WHEN t4.<x6> IS NOT NULL THEN <x9> ELSE False END AS D FROM <x1> LEFT JOIN (SELECT <x2>.<x7>, <x2>.<x8>, <x9> AS i FROM <x2> WHERE <x2>.<x7> < <x10>) AS <x5> ON <x1>.<x7> = t4.<x7> AND <x1>.<x8> = t4.<x8>",
        "rewrite": "SELECT <<y2>>, (<x1>.<x7>, <x1>.<x8>) IN (SELECT <x3>.<x7>, <x3>.<x8> FROM <x3> WHERE <x3>.<x7> < <x10>) AS D FROM <x1>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 54,
        "name": "testExpandProjectScalar",
        "key": "testExpandProjectScalar",
        "pattern": "SELECT <<y2>>, t4.<x8> AS D FROM <x1> LEFT JOIN (SELECT SINGLE_VALUE(<x2>.<x6>) AS \"$f0\" FROM <x2> WHERE <x2>.<x7> < <x9>) AS <x5> ON True",
        "rewrite": "SELECT <<y2>>, (SELECT <x3>.<x6> FROM <x3> WHERE <x3>.<x7> < <x9>) AS D FROM <x1>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 55,
        "name": "testExtractJoinFilterRule",
        "key": "testExtractJoinFilterRule",
        "pattern": "FROM <x1>, <x3> WHERE <<y1>>",
        "rewrite": "FROM <x1> INNER JOIN <x3> ON <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 65,
        "name": "testMergeMinus",
        "key": "testMergeMinus",
        "pattern": "SELECT <<y5>> FROM <x1> WHERE <<y3>> EXCEPT SELECT <<y5>> FROM <x2> WHERE <x2>.<x8> = <x10> EXCEPT SELECT <<y5>> FROM <x3> WHERE <x3>.<x8> = <x11>",
        "rewrite": "SELECT <<y5>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>> EXCEPT SELECT <<y5>> FROM <x5> WHERE <x5>.<x8> = <x10>) AS t1 EXCEPT SELECT <<y5>> FROM <x6> WHERE <x6>.<x8> = <x11>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 68,
        "name": "testMergeUnionAll",
        "key": "testMergeUnionAll",
        "pattern": "SELECT <<y5>> FROM <x1> WHERE <<y3>>\nUNION ALL\nSELECT <<y5>> FROM <x2> WHERE <x2>.<x8> = <x10>\nUNION ALL\nSELECT <<y5>> FROM <x3> WHERE <x3>.<x8> = <x11>",
        "rewrite": "SELECT <<y5>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>>\nUNION ALL\nSELECT <<y5>> FROM <x5> WHERE <x5>.<x8> = <x10>) AS t1\nUNION ALL\nSELECT <<y5>> FROM <x6> WHERE <x6>.<x8> = <x11>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 72,
        "name": "testMinusMergeRule",
        "key": "testMinusMergeRule",
        "pattern": "EXCEPT_ALL(EXCEPT_ALL(EXCEPT_ALL((SELECT <<y4>> FROM <x1> GROUP BY <<y2>>), (SELECT <x2>.<x11>, <x2>.<x13> FROM <x2>)), (SELECT <<y3>> FROM EXCEPT_ALL((SELECT <x3>.<x11>, <x3>.<x13> FROM <x3>), (SELECT <x4>.<x11>, <x4>.<x13> FROM <x4> GROUP BY <x4>.<x11>, <x4>.<x13>)) AS t22)), (SELECT <x5>.<x11>, <x5>.<x13> FROM <x5>))",
        "rewrite": "EXCEPT_ALL((SELECT <<y3>> FROM EXCEPT_ALL((SELECT t2.<x11>, t2.<x13> FROM EXCEPT_ALL((SELECT <<y4>>, COUNT(<x12>) FROM <x1> GROUP BY <<y2>>), (SELECT <x7>.<x11>, <x7>.<x13>, <x14> FROM <x7>)) AS t2), (SELECT t7.<x11>, t7.<x13> FROM EXCEPT_ALL((SELECT <x8>.<x11>, <x8>.<x13>, <x14> FROM <x8>), (SELECT <x9>.<x11>, <x9>.<x13>, COUNT(<x12>) FROM <x9> GROUP BY <x9>.<x11>, <x9>.<x13>)) AS t7)) AS t9), (SELECT <x10>.<x11>, <x10>.<x13> FROM <x10>))",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 74,
        "name": "testPullAggregateThroughUnion",
        "key": "testPullAggregateThroughUnion",
        "pattern": "SELECT t7.<x6>, t7.<x5> FROM (SELECT <<y2>> FROM <x1>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5> FROM <x2>) AS t7 GROUP BY t7.<x6>, t7.<x5>",
        "rewrite": "SELECT t3.<x6>, t3.<x5> FROM (SELECT <<y2>> FROM <x1> GROUP BY <<y1>>\nUNION ALL\nSELECT <x4>.<x6>, <x4>.<x5> FROM <x4> GROUP BY <x4>.<x6>, <x4>.<x5>) AS t3 GROUP BY t3.<x6>, t3.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 76,
        "name": "testPullConstantIntoJoin",
        "key": "testPullConstantIntoJoin",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t0 LEFT JOIN (SELECT <<y4>> FROM <x3> WHERE <x3>.<x7> = <x9>) AS <x6> ON True",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t LEFT JOIN <x3> ON t.<x8> = <x3>.<x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 77,
        "name": "testPullConstantIntoJoin2",
        "key": "testPullConstantIntoJoin2",
        "pattern": "SELECT <x16> AS EMPNO, t5.<x12>, t5.<x8>, t5.<x10>, t5.<x5>, t5.<x7>, t5.<x14>, t5.<x9>, t5.<x13>, <x16> AS DEPTNO0, t7.<x11> FROM (SELECT <x16> AS EMPNO, <<y5>>, <x1>.<x9> + <x16> AS \"$f9\" FROM <x1> WHERE <<y2>>) AS t5 INNER JOIN (SELECT <x16> AS DEPTNO, <<y4>>, <x17> AS \"$f2\" FROM <x3> WHERE <x3>.<x9> = <x16>) AS t7 ON t5.<x15> = <x17>",
        "rewrite": "SELECT t0.<x6>, t0.<x12>, t0.<x8>, t0.<x10>, t0.<x5>, t0.<x7>, t0.<x14>, t0.<x9>, t0.<x13>, t1.<x9> AS DEPTNO0, t1.<x11> FROM (SELECT <x1>.<x6>, <<y5>>, <x1>.<x9> + <x1>.<x6> AS \"$f9\" FROM <x1> WHERE <<y2>>) AS t0 INNER JOIN (SELECT <x3>.<x9>, <<y4>>, <x3>.<x9> + 5 AS \"$f2\" FROM <x3>) AS t1 ON t0.<x6> = t1.<x9> AND t0.<x15> = t1.\"$f2\"",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 87,
        "name": "testPullConstantThroughUnion",
        "key": "testPullConstantThroughUnion",
        "pattern": "SELECT <<y4>>, t6.<x6>, t6.<x5> FROM (SELECT <<y3>> FROM <x1>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5> FROM <x2>) AS t6",
        "rewrite": "SELECT <<y4>>, <<y3>> FROM <x1>\nUNION ALL\nSELECT <<y4>>, <x4>.<x6>, <x4>.<x5> FROM <x4>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 93,
        "name": "testPushAggregateFunctionsThroughJoin",
        "key": "testPushAggregateFunctionsThroughJoin",
        "pattern": "SELECT t1.<x16>, t1.<x14>, t1.<x15>, CAST(t1.<x13> * t2.<x11> AS INTEGER) + <x18> AS SUM_SAL_PLUS, t1.<x8>, CAST(t1.<x13> * t2.<x11> AS INTEGER) AS SUM_SAL_2, t1.<x5> * t2.<x11> AS COUNT_SAL, t1.<x10> * t2.<x11> AS COUNT_MGR FROM (SELECT <<y3>> FROM <x1> GROUP BY <x21>) AS t1 INNER JOIN (SELECT <x19>, <x20> AS \"$f1\" FROM <x3> GROUP BY <x19>) AS t2 ON t1.<x16> = t2.<x6>",
        "rewrite": "SELECT <<y3>>, <x24> + <x18> AS SUM_SAL_PLUS FROM <x1> INNER JOIN <x3> ON <x1>.<x16> = <x3>.<x6> GROUP BY <<y1>>, <x19>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 97,
        "name": "testPushAggregateThroughJoin2",
        "key": "testPushAggregateThroughJoin2",
        "pattern": "SELECT t5.<x7>, t7.<x5> FROM (SELECT <<y9>> FROM <x1> WHERE <<y2>> GROUP BY <<y3>>, <x20>) AS t5 INNER JOIN (SELECT <<y8>> FROM <x3> GROUP BY <<y1>>, <x18>) AS t7 ON t5.<x7> = t7.<x5> AND t5.<x10> = t7.<x9> GROUP BY t5.<x7>, t7.<x5>",
        "rewrite": "SELECT t0.<x7>, t1.<x5> FROM (SELECT <x1>.<x6>, <x1>.ENAME, <<y9>>, <x1>.MGR, <x1>.HIREDATE, <x1>.SAL, <x1>.COMM, <x1>.<x8>, <x1>.SLACKER FROM <x1> WHERE <<y2>>) AS t0 INNER JOIN (SELECT <x3>.<x8>, <<y8>> FROM <x3>) AS t1 ON t0.<x7> = t1.<x5> AND t0.<x10> = t1.<x9> GROUP BY t0.<x7>, t1.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 101,
        "name": "testPushAggregateThroughJoinDistinct",
        "key": "testPushAggregateThroughJoinDistinct",
        "pattern": "SELECT t2.<x6>, t1.<x5>, t1.<x10> FROM (SELECT <x1>.<x8>, <<y5>> FROM <x1> GROUP BY <x1>.<x8>) AS t1 INNER JOIN (SELECT <<y4>> FROM <x3> GROUP BY <x11>) AS t2 ON t1.<x8> = t2.<x6>",
        "rewrite": "SELECT t.<x6>, <<y5>> FROM <x1> INNER JOIN (SELECT <<y4>> FROM <x3> GROUP BY <x11>) AS t ON <x1>.<x8> = t.<x6> GROUP BY t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 111,
        "name": "testPushFilterPastAggTwo",
        "key": "testPushFilterPastAggTwo",
        "pattern": "SELECT t5.<x4> FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t5 WHERE t5.<x4> > <x12> GROUP BY t5.<x4> HAVING <x15> OR t5.<x4> < <x10>",
        "rewrite": "SELECT <<y4>> FROM <x1> WHERE <<y2>> GROUP BY <x14> HAVING <x1>.<x3> > <x12> AND (<x15> OR <x1>.<x3> < <x10>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 114,
        "name": "testPushFilterThroughSemiJoin",
        "key": "testPushFilterThroughSemiJoin",
        "pattern": "FROM (SELECT <<y3>> FROM <x1> WHERE <<y2>>) AS t1 INNER JOIN (SELECT <<y4>> FROM <x3>) AS t2 ON t1.<x6> = t2.<x6>",
        "rewrite": "FROM <x1> INNER JOIN (SELECT <<y4>> FROM <x3>) AS t ON <x1>.<x6> = t.<x6> WHERE <<y2>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 117,
        "name": "testPushJoinCondDownToProject",
        "key": "testPushJoinCondDownToProject",
        "pattern": "SELECT t1.<x12>, t2.<x12> AS DEPTNO0 FROM (SELECT <<y2>>, <x1>.<x5>, <x21> AS \"$f2\" FROM <x1>) AS t1 INNER JOIN (SELECT <x3>.<x7>, <x3>.<x8>, <x3>.<x11>, <x3>.<x14>, <x3>.<x6>, <x3>.<x9>, <x3>.<x15>, <x20>, <x3>.<x10>, <x19> AS \"$f9\" FROM <x3>) AS t2 ON t1.<x13> = t2.<x16>",
        "rewrite": "SELECT <<y2>>, <x3>.<x12> AS DEPTNO0 FROM <x1>, <x3> WHERE <x21> = <x19>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 125,
        "name": "testPushProjectPastFilter",
        "key": "testPushProjectPastFilter",
        "pattern": "SELECT t1.<x5> + t1.<x3> FROM (SELECT <x1>.<x5>, <x1>.<x6>, <x1>.<x7>, <x1>.<x4>, <x1>.<x3> FROM <x1>) AS t1 WHERE t1.<x7> = <x8> * t1.<x4> AND UPPER(t1.<x6>) = <x10>",
        "rewrite": "SELECT <x1>.<x5> + <x1>.<x3> FROM <x1> WHERE <x1>.<x7> = <x8> * <x1>.<x4> AND UPPER(<x1>.<x6>) = <x10>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 127,
        "name": "testPushProjectPastFullJoin",
        "key": "testPushProjectPastFullJoin",
        "pattern": "SELECT <<y2>>, CASE WHEN t2.<x7> THEN <x10> ELSE t2.<x4> END FROM (SELECT <x1>.<x8>, <x13> AS expr1, <x12> AS expr2 FROM <x1>) AS t2 FULL JOIN (SELECT <x3>.<x8> FROM <x3>) AS <x6> ON t2.<x8> = t3.<x8> GROUP BY CASE WHEN t2.<x7> THEN <x10> ELSE t2.<x4> END",
        "rewrite": "SELECT <<y2>>, CASE WHEN <x13> THEN <x10> ELSE <x12> END FROM <x1> FULL JOIN BONUS AS BONUS ON <x1>.<x8> = <x3>.<x8> GROUP BY CASE WHEN <x13> THEN <x10> ELSE <x12> END",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 128,
        "name": "testPushProjectPastFullJoinStrong",
        "key": "testPushProjectPastFullJoinStrong",
        "pattern": "SELECT <<y4>>, t2.<x6> FROM (SELECT <x1>.<x7>, <x16> AS expr1 FROM <x1>) AS t2 FULL JOIN (SELECT <x3>.<x7> FROM <x3>) AS <x5> ON t2.<x7> = t3.<x7> GROUP BY t2.<x6>",
        "rewrite": "SELECT <<y4>>, <x16> FROM <x1> FULL JOIN BONUS AS BONUS ON <x1>.<x7> = <x3>.<x7> GROUP BY <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 129,
        "name": "testPushProjectPastInnerJoin",
        "key": "testPushProjectPastInnerJoin",
        "pattern": "SELECT <<y4>>, t2.<x7> FROM (SELECT <x1>.<x6>, <x16> AS \"CASE\" FROM <x1>) AS t2 INNER JOIN (SELECT <x3>.<x6> FROM <x3>) AS t3 ON t2.<x6> = t3.<x6> GROUP BY t2.<x7>",
        "rewrite": "SELECT <<y4>>, <x16> FROM <x1> INNER JOIN <x3> ON <x1>.<x6> = <x3>.<x6> GROUP BY <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 130,
        "name": "testPushProjectPastInnerJoinStrong",
        "key": "testPushProjectPastInnerJoinStrong",
        "pattern": "SELECT <<y4>>, t2.<x6> FROM (SELECT <x1>.<x7>, <x16> AS \"CASE\" FROM <x1>) AS t2 INNER JOIN (SELECT <x3>.<x7> FROM <x3>) AS t3 ON t2.<x7> = t3.<x7> GROUP BY t2.<x6>",
        "rewrite": "SELECT <<y4>>, <x16> FROM <x1> INNER JOIN <x3> ON <x1>.<x7> = <x3>.<x7> GROUP BY <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 131,
        "name": "testPushProjectPastLeftJoin",
        "key": "testPushProjectPastLeftJoin",
        "pattern": "SELECT <<y4>>, t2.<x7> FROM (SELECT <x1>.<x8>, <x17> AS expr1 FROM <x1>) AS t2 LEFT JOIN (SELECT <x3>.<x8> FROM <x3>) AS <x6> ON t2.<x8> = t3.<x8> GROUP BY t2.<x7>",
        "rewrite": "SELECT <<y4>>, <x17> FROM <x1> LEFT JOIN <x3> ON <x1>.<x8> = <x3>.<x8> GROUP BY <x17>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 132,
        "name": "testPushProjectPastLeftJoinSwap",
        "key": "testPushProjectPastLeftJoinSwap",
        "pattern": "SELECT <<y2>>, CASE WHEN t3.<x8> THEN <x11> ELSE t3.<x5> END FROM (SELECT <x1>.<x9> FROM <x1>) AS t2 LEFT JOIN (SELECT <x3>.<x9>, <x14> AS expr1, <x13> AS expr2 FROM <x3>) AS <x7> ON t2.<x9> = t3.<x9> GROUP BY CASE WHEN t3.<x8> THEN <x11> ELSE t3.<x5> END",
        "rewrite": "SELECT <<y2>>, CASE WHEN <x14> THEN <x11> ELSE <x13> END FROM <x1> LEFT JOIN <x3> ON <x1>.<x9> = <x3>.<x9> GROUP BY CASE WHEN <x14> THEN <x11> ELSE <x13> END",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 133,
        "name": "testPushProjectPastLeftJoinSwapStrong",
        "key": "testPushProjectPastLeftJoinSwapStrong",
        "pattern": "SELECT <<y4>>, t3.<x7> FROM (SELECT <x1>.<x8> FROM <x1>) AS t2 LEFT JOIN (SELECT <x3>.<x8>, <x17> AS expr1 FROM <x3>) AS <x6> ON t2.<x8> = t3.<x8> GROUP BY t3.<x7>",
        "rewrite": "SELECT <<y4>>, <x17> FROM <x1> LEFT JOIN <x3> ON <x1>.<x8> = <x3>.<x8> GROUP BY <x17>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 134,
        "name": "testPushProjectPastRightJoin",
        "key": "testPushProjectPastRightJoin",
        "pattern": "SELECT <<y2>>, CASE WHEN t2.<x7> THEN <x10> ELSE t2.<x4> END FROM (SELECT <x1>.<x8>, <x13> AS expr1, <x12> AS expr2 FROM <x1>) AS t2 RIGHT JOIN (SELECT <x3>.<x8> FROM <x3>) AS <x6> ON t2.<x8> = t3.<x8> GROUP BY CASE WHEN t2.<x7> THEN <x10> ELSE t2.<x4> END",
        "rewrite": "SELECT <<y2>>, CASE WHEN <x13> THEN <x10> ELSE <x12> END FROM <x1> RIGHT JOIN BONUS AS BONUS ON <x1>.<x8> = <x3>.<x8> GROUP BY CASE WHEN <x13> THEN <x10> ELSE <x12> END",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 135,
        "name": "testPushProjectPastRightJoinStrong",
        "key": "testPushProjectPastRightJoinStrong",
        "pattern": "SELECT <<y4>>, t2.<x6> FROM (SELECT <x1>.<x7>, <x16> AS expr1 FROM <x1>) AS t2 RIGHT JOIN (SELECT <x3>.<x7> FROM <x3>) AS <x5> ON t2.<x7> = t3.<x7> GROUP BY t2.<x6>",
        "rewrite": "SELECT <<y4>>, <x16> FROM <x1> RIGHT JOIN BONUS AS BONUS ON <x1>.<x7> = <x3>.<x7> GROUP BY <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 136,
        "name": "testPushProjectPastRightJoinSwap",
        "key": "testPushProjectPastRightJoinSwap",
        "pattern": "SELECT <<y4>>, t3.<x6> FROM (SELECT <x1>.<x7> FROM <x1>) AS t2 RIGHT JOIN (SELECT <x3>.<x7>, <x16> AS expr1 FROM <x3>) AS <x5> ON t2.<x7> = t3.<x7> GROUP BY t3.<x6>",
        "rewrite": "SELECT <<y4>>, <x16> FROM <x1> RIGHT JOIN EMP AS EMP ON <x1>.<x7> = <x3>.<x7> GROUP BY <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 137,
        "name": "testPushProjectPastRightJoinSwapStrong",
        "key": "testPushProjectPastRightJoinSwapStrong",
        "pattern": "SELECT <<y4>>, t3.<x6> FROM (SELECT <x1>.<x7> FROM <x1>) AS t2 RIGHT JOIN (SELECT <x3>.<x7>, <x16> AS expr1 FROM <x3>) AS <x5> ON t2.<x7> = t3.<x7> GROUP BY t3.<x6>",
        "rewrite": "SELECT <<y4>>, <x16> FROM <x1> RIGHT JOIN EMP AS EMP ON <x1>.<x7> = <x3>.<x7> GROUP BY <x16>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 139,
        "name": "testPushSemiJoinPastFilter",
        "key": "testPushSemiJoinPastFilter",
        "pattern": "SELECT t1.<x6> FROM (SELECT <x1>.<x7>, <<y5>> FROM <x1> INNER JOIN <x3> ON <<y1>> WHERE <<y3>>) AS t1 INNER JOIN <x4> ON t1.<x7> = <x4>.<x7>",
        "rewrite": "SELECT <<y5>> FROM <x1>, <x3> WHERE <<y1>> AND <<y3>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 140,
        "name": "testPushSemiJoinPastJoinRuleLeft",
        "key": "testPushSemiJoinPastJoinRuleLeft",
        "pattern": "FROM <x1> INNER JOIN <x6> ON <<y1>> INNER JOIN <x2> ON <x1>.<x9> = <x2>.<x9> INNER JOIN <x7> ON <x1>.<x11> = <x7>.<x11> INNER JOIN <x3> ON <x1>.<x9> = <x3>.<x9>",
        "rewrite": "FROM <x1>, <x6>, <x5> WHERE <<y1>> AND <x1>.<x9> = <x5>.<x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 141,
        "name": "testPushSemiJoinPastJoinRuleRight",
        "key": "testPushSemiJoinPastJoinRuleRight",
        "pattern": "FROM <x1> INNER JOIN <x6> ON <<y1>> INNER JOIN <x7> ON <x1>.<x10> = <x7>.<x10> INNER JOIN <x2> ON <x7>.<x10> = <x2>.<x10> INNER JOIN <x3> ON <x6>.<x10> = <x3>.<x10>",
        "rewrite": "FROM <x1>, <x6>, <x5> WHERE <<y1>> AND <x6>.<x10> = <x5>.<x10>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 143,
        "name": "testPushSumConstantGroupingSetsThroughUnion",
        "key": "testPushSumConstantGroupingSetsThroughUnion",
        "pattern": "SELECT t8.<x6>, t8.<x5>, SUM(SUM(<x8>)) FROM (SELECT <<y2>>, SUM(<x7>) FROM <x1> GROUP BY <<y1>>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5>, SUM(<x8>) FROM <x2> GROUP BY <x2>.<x6>, <x2>.<x5>) AS t8 GROUP BY t8.<x6>, t8.<x5>",
        "rewrite": "SELECT t1.<x6>, t1.<x5>, SUM(t1.U) FROM (SELECT <x1>.EMPNO, <x1>.ENAME, <<y2>>, <x1>.MGR, <x1>.HIREDATE, <x1>.SAL, <x1>.COMM, <x1>.SLACKER, <x7> AS U FROM <x1>\nUNION ALL\nSELECT <x4>.EMPNO, <x4>.ENAME, <x4>.<x5>, <x4>.MGR, <x4>.HIREDATE, <x4>.SAL, <x4>.COMM, <x4>.<x6>, <x4>.SLACKER, <x8> AS U FROM <x4>) AS t1 GROUP BY t1.<x6>, t1.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 147,
        "name": "testPushSumNullableNOGBYThroughUnion",
        "key": "testPushSumNullableNOGBYThroughUnion",
        "pattern": "SELECT SUM(t6.<x6>) FROM (SELECT SUM(<x1>.<x5>) AS sum1 FROM <x1>\nUNION ALL\nSELECT SUM(<x2>.<x5>) AS sum2 FROM <x2>) AS t6",
        "rewrite": "SELECT SUM(t.<x5>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 151,
        "name": "testReduceAverage",
        "key": "testReduceAverage",
        "pattern": "CAST(SUM(<x1>.<x5>) / COUNT(<x4>) AS INTEGER)",
        "rewrite": "AVG(<x1>.<x5>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 185,
        "name": "testRemoveSemiJoinRightWithFilter",
        "key": "testRemoveSemiJoinRightWithFilter",
        "pattern": "FROM <x1> INNER JOIN (SELECT <x7> FROM <x5> WHERE <<y2>>) AS t1 ON <x1>.<x10> = t1.<x10> INNER JOIN <x2> ON t1.<x10> = <x2>.<x10>",
        "rewrite": "FROM <x1>, <x5>, <x4> WHERE <x1>.<x10> = <x5>.<x10> AND <x5>.<x10> = <x4>.<x10> AND <<y2>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 186,
        "name": "testRemoveSemiJoinWithFilter",
        "key": "testRemoveSemiJoinWithFilter",
        "pattern": "SELECT t1.<x5> FROM (SELECT <x5> FROM <x1> WHERE <<y1>>) AS t1 INNER JOIN <x3> ON t1.<x7> = <x3>.<x7>",
        "rewrite": "SELECT <x1>.<x5> FROM <x1>, <x3> WHERE <x1>.<x7> = <x3>.<x7> AND <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 187,
        "name": "testRightOuterJoinSimplificationToInner",
        "key": "testRightOuterJoinSimplificationToInner",
        "pattern": "FROM (SELECT <x4> FROM <x1> WHERE <<y2>>) AS t1 INNER JOIN <x3> ON t1.<x6> = <x3>.<x6>",
        "rewrite": "FROM <x1> RIGHT JOIN EMP AS EMP ON <x1>.<x6> = <x3>.<x6> WHERE <<y2>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 207,
        "name": "testTransitiveInferenceAggregate",
        "key": "testTransitiveInferenceAggregate",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>> GROUP BY <x9>) AS t5 INNER JOIN (SELECT <x5> FROM <x2> WHERE <x2>.<x6> > <x8>) AS t6 ON t5.<x6> = t6.<x6>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>> GROUP BY <x9>) AS t1 INNER JOIN <x4> ON t1.<x6> = <x4>.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 209,
        "name": "testTransitiveInferenceConjunctInPullUp",
        "key": "testTransitiveInferenceConjunctInPullUp",
        "pattern": "FROM (SELECT <<y5>> FROM <x1> WHERE <<y4>>) AS t1 INNER JOIN (SELECT <<y5>> FROM <x2> WHERE <x2>.<x6> = <x8> OR <x2>.<x6> = <x9> OR <x2>.<x6> > <x10>) AS t2 ON t1.<x6> = t2.<x6>",
        "rewrite": "FROM (SELECT <<y5>> FROM <x1> WHERE <<y4>>) AS t INNER JOIN <x4> ON t.<x6> = <x4>.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 212,
        "name": "testTransitiveInferenceJoin",
        "key": "testTransitiveInferenceJoin",
        "pattern": "FROM (SELECT <<y3>> FROM <x1> WHERE <x1>.<x6> > <x8>) AS t1 INNER JOIN (SELECT <<y3>> FROM <x2> WHERE <x2>.<x6> > <x8>) AS t2 ON t1.<x6> = t2.<x6>",
        "rewrite": "FROM <x1> INNER JOIN (SELECT <<y3>> FROM <x4> WHERE <x4>.<x6> > <x8>) AS t ON <x1>.<x6> = t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 214,
        "name": "testTransitiveInferenceJoin3wayAgg",
        "key": "testTransitiveInferenceJoin3wayAgg",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>> GROUP BY <x11>) AS t5 INNER JOIN (SELECT <x7> FROM <x2> WHERE <x2>.<x8> > <x10>) AS t6 ON t5.<x8> = t6.<x8> INNER JOIN (SELECT <x7> FROM <x3> WHERE <x3>.<x8> > <x10>) AS t7 ON t6.<x8> = t7.<x8>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>> GROUP BY <x11>) AS t1 INNER JOIN <x5> ON t1.<x8> = <x5>.<x8> INNER JOIN <x6> ON <x5>.<x8> = <x6>.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 215,
        "name": "testTransitiveInferenceLeftOuterJoin",
        "key": "testTransitiveInferenceLeftOuterJoin",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t2 LEFT JOIN (SELECT <<y4>> FROM <x2> WHERE <x2>.<x7> > <x10>) AS <x5> ON t2.<x7> = t3.<x7> WHERE t3.<x7> > <x9>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t LEFT JOIN <x4> ON t.<x7> = <x4>.<x7> WHERE <x4>.<x7> > <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 219,
        "name": "testTransitiveInferencePullUpThruAlias",
        "key": "testTransitiveInferencePullUpThruAlias",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>) AS t3 INNER JOIN (SELECT <x5> FROM <x2> WHERE <x2>.<x7> > <x9>) AS t4 ON t3.<x7> = t4.<x7>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>) AS t0 INNER JOIN <x4> ON t0.<x7> = <x4>.<x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 220,
        "name": "testTransitiveInferenceRightOuterJoin",
        "key": "testTransitiveInferenceRightOuterJoin",
        "pattern": "FROM (SELECT <<y3>> FROM <x1> WHERE <x1>.<x7> > <x8>) AS t2 RIGHT JOIN (SELECT <<y3>> FROM <x2> WHERE <x2>.<x7> > <x8>) AS <x5> ON t2.<x7> = t3.<x7> WHERE t2.<x7> > <x10>",
        "rewrite": "FROM <x1> RIGHT JOIN (SELECT <<y3>> FROM <x4> WHERE <x4>.<x7> > <x8>) AS t ON <x1>.<x7> = t.<x7> WHERE <x1>.<x7> > <x10>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 226,
        "name": "testWhereExpressionInCorrelated",
        "key": "testWhereExpressionInCorrelated",
        "pattern": "SELECT t4.<x8> FROM (SELECT <<y3>> FROM <x1>) AS t4 INNER JOIN (SELECT t5.<x12>, t5.<x15> FROM (SELECT <x2>.<x7>, <x2>.<x8>, <x2>.<x11>, <x2>.<x14>, <x2>.<x5>, <x2>.<x9>, <x2>.<x13>, <x2>.<x12>, <x2>.<x10>, <x2>.<x9> + <x16> AS expr1 FROM <x2>) AS t5 WHERE t5.<x9> + <x16> = t5.<x15> GROUP BY t5.<x12>, t5.<x15>) AS t8 ON t4.<x6> = t8.<x15> AND t4.<x12> = t8.<x12>",
        "rewrite": "SELECT t.<x8> FROM (SELECT <<y3>> FROM <x1>) AS t WHERE t.<x12> IN (SELECT <x4>.<x12> FROM <x4> WHERE <x4>.<x9> + <x16> = <x4>.<x11>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 228,
        "name": "testWhereNotInCorrelated",
        "key": "testWhereNotInCorrelated",
        "pattern": "FROM <x1> LEFT JOIN (SELECT <x3>.<x6>, COUNT(<x7>) AS c, COUNT(<x3>.<x15>) AS ck FROM <x3> GROUP BY <x3>.<x6>) AS <x14> ON <x1>.<x16> = t4.<x6> LEFT JOIN (SELECT <x4>.<x15>, <x18> AS i, <x4>.<x6> FROM <x4>) AS <x9> ON <x1>.<x10> = t5.<x15> AND <x1>.<x16> = t5.<x6> WHERE NOT CASE WHEN t4.<x12> = <x17> THEN <x17> WHEN t5.<x8> IS NOT NULL THEN <x18> WHEN t4.<x11> < t4.<x12> THEN <x18> ELSE <x17> END",
        "rewrite": "FROM <x1> WHERE <x1>.<x10> NOT IN (SELECT <x3>.<x15> FROM <x3> WHERE <x1>.<x16> = <x3>.<x6>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 229,
        "name": "testWhereNotInCorrelated2",
        "key": "testWhereNotInCorrelated2",
        "pattern": "SELECT <x1>.<x11>, <x1>.<x12>, <x1>.<x18>, <x1>.<x20>, <x1>.<x7>, <x1>.<x14>, <x1>.<x21>, <x1>.<x19>, <x1>.<x17> FROM <x1> LEFT JOIN (SELECT t4.<x12>, COUNT(<x6>) AS c, COUNT(t4.<x11>) AS ck FROM (SELECT <x2>.<x12>, <x2>.<x11>, <x2>.<x14> AS R FROM <x2>) AS t3 WHERE t3.<x8> > <x24> GROUP BY t4.<x12>) AS <x9> ON <x1>.<x12> = t7.<x12> LEFT JOIN (SELECT t9.<x11>, <x23> AS i, t9.<x12> FROM (SELECT <x3>.<x12>, <x3>.<x11>, <x3>.<x14> AS R FROM <x3>) AS t8 WHERE t8.<x8> > <x24>) AS <x16> ON <x1>.<x11> = t11.<x11> AND <x1>.<x12> = t11.<x12> WHERE NOT CASE WHEN t7.<x15> = <x22> THEN <x22> WHEN t11.<x10> IS NOT NULL THEN <x23> WHEN t7.<x13> < t7.<x15> THEN <x23> ELSE <x22> END",
        "rewrite": "SELECT <x6> FROM <x1> WHERE <x1>.<x11> NOT IN (SELECT t0.<x11> FROM (SELECT <x5>.<x12>, <x5>.<x11>, <x5>.<x14> AS R FROM <x5>) AS t WHERE t.<x8> > <x24> AND <x1>.<x12> = t.<x12>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    }
]
import sys
# append the current directory
sys.path.append(".")
# append the parent directory
sys.path.append("..")
import json
from core.rule_parser import RuleParser




def get_rule(key: str) -> dict:
    rule = next(filter(lambda x: x['key'] == key, rules_pool), None)
    rule['pattern_json'], rule['rewrite_json'], rule['mapping'] = RuleParser.parse(rule['pattern'], rule['rewrite'])
    rule['constraints_json'] = RuleParser.parse_constraints(rule['constraints'], rule['mapping'])
    rule['actions_json'] = RuleParser.parse_actions(rule['actions'], rule['mapping'])
    return {
        'id': rule['id'],
        'key': rule['key'], 
        'name': rule['name'], 
        'pattern': rule['pattern'], 
        'pattern_json': json.loads(rule['pattern_json']),
        'constraints': rule['constraints'],
        'constraints_json': json.loads(rule['constraints_json']),
        'rewrite': rule['rewrite'],
        'rewrite_json': json.loads(rule['rewrite_json']),
        'actions': rule['actions'],
        'actions_json': json.loads(rule['actions_json']),
        'mapping': json.loads(rule['mapping']),
        'database': rule['database']
    }

# data = []
# for item in rules_pool:
#     result = {
#         "id": int(item["id"]),
#         "name": item["name"],
#         "key": item["name"],
#         "pattern": item["pattern"],
#         "rewrite": item["rewrite"],
#         "constraints": item["constraints"],
#         "actions": item["actions"],
#         "database" : "postgresql"
#     }
#     data.append(result)
# def save_file(result,save_path):
#     with open(save_path, 'w') as f:
#         json.dump(result, f, indent=4)


#         # 更新 save_path.py 文件
#         with open(save_path, 'r') as f:
#             content = f.read()

#         # print(rules_pool)
#         # 替换原有的 rules_pool 定义
#         new_content = content.replace("rules_pool = []", f"rules_pool = {json.dumps(rules_pool, indent=4)}")

#         # 将更新后的内容写回文件
#         with open(save_path, 'w') as f:
#             f.write(new_content)

# save_file(data,"/home/orderheart/syy/sql_rewriter/A_result/positive_data.py")