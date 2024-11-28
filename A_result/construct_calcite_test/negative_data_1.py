rules_pool = [
    {
        "id": 2,
        "name": "testAggregateConstantKeyRule",
        "key": "testAggregateConstantKeyRule",
        "pattern": "GROUP BY <x7>",
        "rewrite": "GROUP BY <x1>.<x5>, <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 3,
        "name": "testAggregateConstantKeyRule2",
        "key": "testAggregateConstantKeyRule2",
        "pattern": "<x1>",
        "rewrite": "<x1>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 5,
        "name": "testAggregateGroupingSetsProjectMerge",
        "key": "testAggregateGroupingSetsProjectMerge",
        "pattern": "SELECT ",
        "rewrite": "SELECT ",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 6,
        "name": "testAggregateProjectMerge",
        "key": "testAggregateProjectMerge",
        "pattern": "SELECT ",
        "rewrite": "SELECT ",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 7,
        "name": "testAggregateProjectPullUpConstants",
        "key": "testAggregateProjectPullUpConstants",
        "pattern": "SELECT <<y4>>, <x6> AS EMPNO GROUP BY <<y2>>",
        "rewrite": "SELECT <<y4>>, <x1>.<x4> GROUP BY <<y2>>, <x1>.<x4>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 8,
        "name": "testAlreadyFalseEliminatesFilter",
        "key": "testAlreadyFalseEliminatesFilter",
        "pattern": "FROM <x1>",
        "rewrite": "FROM (SELECT 1, 2) AS t WHERE False",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 9,
        "name": "testCastInAggregateExpandDistinctAggregatesRule",
        "key": "testCastInAggregateExpandDistinctAggregatesRule",
        "pattern": "SELECT t3.<x3>, CAST(SUM(t3.<x6>) AS BIGINT), CAST(SUM(t3.<x5>) AS INTEGER) FROM (SELECT <<y3>> FROM <x1> GROUP BY <x9>) AS t3 GROUP BY t3.<x3>",
        "rewrite": "SELECT t0.<x3>, SUM(DISTINCT t0.\"EXPR$1\"), SUM(DISTINCT t0.\"EXPR$2\") FROM (SELECT <<y3>> FROM <x1> GROUP BY <x9>) AS t0 GROUP BY t0.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 11,
        "name": "testCustomColumnResolvingInNonCorrelatedSubQuery",
        "key": "testCustomColumnResolvingInNonCorrelatedSubQuery",
        "pattern": "SELECT <x1>.<x13>, <x1>.<x5>, <x1>.<x7>, <x1>.<x14>, <x1>.<x11>, <x1>.<x6>, <x1>.<x9>, <x1>.<x8>, <x1>.<x10> FROM <x1> INNER JOIN (SELECT <x2>.<x6> AS C0 FROM <x2> GROUP BY <x2>.<x6>) AS t2 ON <x1>.<x11> = t2.<x12>",
        "rewrite": "SELECT <x5> FROM <x1> WHERE <x1>.<x11> IN (SELECT <x4>.<x6> AS C0 FROM <x4>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 12,
        "name": "testDecorrelateExists",
        "key": "testDecorrelateExists",
        "pattern": "SELECT <x1>.<x6>, <x1>.<x7>, <x1>.<x10>, <x1>.<x12>, <x1>.<x5>, <x1>.<x8>, <x1>.<x13>, <x1>.<x11>, <x1>.<x9> FROM <x1> INNER JOIN (SELECT <x2>.<x11>, True AS \"$f1\" FROM <x2> GROUP BY <x2>.<x11>) AS t4 ON <x1>.<x11> = t4.<x11>",
        "rewrite": "SELECT <x5> FROM <x1> WHERE EXISTS (SELECT <x5> FROM <x4> WHERE <x1>.<x11> = <x4>.<x11>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 14,
        "name": "testDecorrelateTwoIn",
        "key": "testDecorrelateTwoIn",
        "pattern": "FROM INNER JOIN <x5> ON <<y1>> AND <x1>.<x10> = <x5>.<x9> INNER JOIN (SELECT <x2>.<x10>, <x2>.<x11> FROM <x2>) AS t5 ON <x1>.<x11> = t5.<x11> AND <x1>.<x10> = t5.<x10>",
        "rewrite": "WHERE <x1>.<x10> IN (SELECT <x5>.<x9> FROM <x5> WHERE <<y1>>) AND <x1>.<x10> IN (SELECT <x4>.<x10> FROM <x4> WHERE <x1>.<x11> = <x4>.<x11>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 15,
        "name": "testDistinctCount1",
        "key": "testDistinctCount1",
        "pattern": "SELECT COUNT(DISTINCT t1.<x3>) AS DEPTNO, COUNT(t1.<x4>) FROM (SELECT <x1>.<x3>, <<y2>> FROM <x1> GROUP BY <x1>.<x3>, <<y1>>) AS t1 GROUP BY COUNT(DISTINCT t1.<x3>)",
        "rewrite": "SELECT <<y2>>, COUNT(DISTINCT <x1>.<x3>) FROM <x1> GROUP BY <x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 16,
        "name": "testDistinctCount2",
        "key": "testDistinctCount2",
        "pattern": "SELECT <x8>, CAST(MIN(<x7>) AS INTEGER)",
        "rewrite": "SELECT COUNT(DISTINCT <x1>.<x3>), <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 17,
        "name": "testDistinctCount3",
        "key": "testDistinctCount3",
        "pattern": "SELECT <x7>, CAST(MIN(<x6>) AS INTEGER)",
        "rewrite": "SELECT COUNT(DISTINCT <x1>.<x4>), <x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 18,
        "name": "testDistinctCountGroupingSets1",
        "key": "testDistinctCountGroupingSets1",
        "pattern": "<x8>",
        "rewrite": "COUNT(DISTINCT <x1>.<x5>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 19,
        "name": "testDistinctCountGroupingSets2",
        "key": "testDistinctCountGroupingSets2",
        "pattern": "SELECT <x10>, CAST(MIN(<x9>) AS INTEGER)",
        "rewrite": "SELECT COUNT(DISTINCT <x1>.<x5>), <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 20,
        "name": "testDistinctCountMixed",
        "key": "testDistinctCountMixed",
        "pattern": "SELECT <x8> AS CDDJ, CAST(MIN(<x7>) AS INTEGER) AS S",
        "rewrite": "SELECT COUNT(DISTINCT (<x1>.<x5>, <x1>.<x4>)) AS CDDJ, <x7> AS S",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 21,
        "name": "testDistinctCountMixed2",
        "key": "testDistinctCountMixed2",
        "pattern": "SELECT <x12> AS CDE, <x11> AS CDJE, <x10> AS CDDJ, CAST(MIN(<x9>) AS INTEGER) AS S",
        "rewrite": "SELECT COUNT(DISTINCT <x1>.<x5>) AS CDE, COUNT(DISTINCT (<x1>.<x3>, <x1>.<x5>)) AS CDJE, COUNT(DISTINCT (<x1>.<x4>, <x1>.<x3>)) AS CDDJ, <x9> AS S",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 22,
        "name": "testDistinctCountMultiple",
        "key": "testDistinctCountMultiple",
        "pattern": "SELECT <x9>, <x8>",
        "rewrite": "SELECT COUNT(DISTINCT <x1>.<x3>), COUNT(DISTINCT <x1>.<x4>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 23,
        "name": "testDistinctCountMultipleNoGroup",
        "key": "testDistinctCountMultipleNoGroup",
        "pattern": "SELECT <x7>, <x6> GROUP BY <x1>.<x3>, <x1>.<x4>",
        "rewrite": "SELECT COUNT(DISTINCT <x1>.<x3>), COUNT(DISTINCT <x1>.<x4>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 25,
        "name": "testDistinctNonDistinctAggregatesWithGrouping1",
        "key": "testDistinctNonDistinctAggregatesWithGrouping1",
        "pattern": "SELECT t2.<x3>, SUM(<x5>), SUM(SUM(<x13>)), MAX(<x10>), MAX(<x9>) FROM (SELECT <<y2>>, <x1>.<x6>, <x11> AS sum1, <x10> AS max1, <x9> AS max2 FROM <x1> GROUP BY <<y1>>, <x1>.<x6>) AS t2 GROUP BY t2.<x3>",
        "rewrite": "SELECT <<y2>>, <x11>, <x13>, <x10>, <x9> FROM <x1> GROUP BY <x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 26,
        "name": "testDistinctNonDistinctAggregatesWithGrouping2",
        "key": "testDistinctNonDistinctAggregatesWithGrouping2",
        "pattern": "SELECT t2.<x4>, SUM(<x10>), SUM(SUM(<x10>)) FROM (SELECT <<y2>>, <x1>.<x5> FROM <x1> GROUP BY <x7>, <x1>.<x5>) AS t2 GROUP BY t2.<x4>",
        "rewrite": "SELECT <<y2>>, <x10> FROM <x1> GROUP BY <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 27,
        "name": "testDistinctWithGrouping",
        "key": "testDistinctWithGrouping",
        "pattern": "SELECT t2.<x5>, SUM(t2.<x4>), MIN(t2.<x6>), SUM(t2.<x5>) FROM (SELECT <<y2>>, <x9> AS sum1, <x8> AS min1 FROM <x1> GROUP BY <x7>) AS t2 GROUP BY t2.<x5>",
        "rewrite": "SELECT <<y2>>, <x9>, <x8>, SUM(DISTINCT <x1>.<x5>) FROM <x1> GROUP BY <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 28,
        "name": "testEmptyAggregate",
        "key": "testEmptyAggregate",
        "pattern": "SELECT <x3> FROM <x1>",
        "rewrite": "SELECT SUM(<x2>.EMPNO) FROM <x2> GROUP BY <x2>.DEPTNO",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 29,
        "name": "testEmptyAggregateEmptyKey",
        "key": "testEmptyAggregateEmptyKey",
        "pattern": "SELECT SUM(<x1>.<x3>) FROM <x1>",
        "rewrite": "SELECT SUM(<x2>.<x3>) FROM <x2>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 30,
        "name": "testEmptyAggregateEmptyKeyWithAggregateValuesRule",
        "key": "testEmptyAggregateEmptyKeyWithAggregateValuesRule",
        "pattern": "SELECT <x1> FROM (SELECT 0, NULL) AS t1",
        "rewrite": "SELECT COUNT(<x1>), SUM(t.EMPNO) FROM VALUES AS t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 31,
        "name": "testEmptyFilterProjectUnion",
        "key": "testEmptyFilterProjectUnion",
        "pattern": "FROM (SELECT <x3>, <x2>) AS t3",
        "rewrite": "FROM (SELECT <<y1>> FROM (VALUES (10, 1), ('<x3>', '<x2>')) AS t\nUNION ALL\nSELECT <<y1>> FROM (SELECT 20, 2) AS t0) AS t1 WHERE t1.X + t1.Y > <x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 32,
        "name": "testEmptyIntersect",
        "key": "testEmptyIntersect",
        "pattern": "SELECT <<y2>> FROM <x1>",
        "rewrite": "SELECT <<y2>> FROM (SELECT <<y2>> FROM (SELECT <x4>, <x3>) AS t INTERSECT SELECT <<y2>> FROM (VALUES (10, 1), ('<x4>', '<x3>')) AS t0 WHERE t0.\"EXPR$0\" > 50) AS t2 INTERSECT SELECT <<y2>> FROM (SELECT <x4>, <x3>) AS t3",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 33,
        "name": "testEmptyJoin",
        "key": "testEmptyJoin",
        "pattern": "FROM <x1>",
        "rewrite": "FROM (SELECT <<y1>> FROM EMP AS EMP WHERE False) AS t INNER JOIN DEPT AS DEPT ON t.DEPTNO = DEPT.DEPTNO",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 34,
        "name": "testEmptyJoinLeft",
        "key": "testEmptyJoinLeft",
        "pattern": "FROM <x1>",
        "rewrite": "FROM (SELECT <<y1>> FROM EMP AS EMP WHERE False) AS t LEFT JOIN DEPT AS DEPT ON t.DEPTNO = DEPT.DEPTNO",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 35,
        "name": "testEmptyJoinRight",
        "key": "testEmptyJoinRight",
        "pattern": "FROM <x1> RIGHT JOIN <x2> AS <x3> ON <x1>.<x5> = DEPT0.<x5>",
        "rewrite": "FROM (SELECT <<y1>> FROM EMP AS EMP WHERE False) AS t RIGHT JOIN <x2> AS <x2> ON t.<x5> = DEPT.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 36,
        "name": "testEmptyMinus",
        "key": "testEmptyMinus",
        "pattern": "SELECT <<y2>> FROM <x1>",
        "rewrite": "SELECT <<y2>> FROM (SELECT <<y2>> FROM (SELECT <x3>, 3) AS t WHERE t.\"EXPR$0\" > <x3> EXCEPT SELECT <<y2>> FROM (SELECT 20, 2) AS t1) AS t2 EXCEPT SELECT <<y2>> FROM (SELECT 40, 4) AS t3",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 37,
        "name": "testEmptyMinus2",
        "key": "testEmptyMinus2",
        "pattern": "SELECT <<y6>> FROM (SELECT <<y7>>) AS t8 EXCEPT SELECT <<y6>> FROM (SELECT <<y5>>) AS t9",
        "rewrite": "SELECT <<y6>> FROM (SELECT <<y6>> FROM (SELECT <<y6>> FROM (SELECT <<y7>>) AS t EXCEPT SELECT <<y6>> FROM (SELECT 20, 2) AS t0 WHERE t0.\"EXPR$0\" > <x6>) AS t2 EXCEPT SELECT <<y6>> FROM (SELECT <<y5>>) AS t3) AS t4 EXCEPT SELECT <<y6>> FROM (SELECT <x2>, 5) AS t5 WHERE t5.\"EXPR$0\" > <x2>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 38,
        "name": "testEmptyProject",
        "key": "testEmptyProject",
        "pattern": "SELECT <x1>.<x3> + <x1>.<x2> + <x1>.<x3> FROM <x1>",
        "rewrite": "SELECT t0.\"EXPR$0\" + t0.\"EXPR$1\" + t0.\"EXPR$0\" FROM (VALUES (10, 1), (30, 3)) AS t WHERE t.\"EXPR$0\" + t.\"EXPR$1\" > 50",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 39,
        "name": "testEmptyProject2",
        "key": "testEmptyProject2",
        "pattern": "SELECT <x2> FROM <x1>",
        "rewrite": "SELECT t0.\"EXPR$0\" + t0.\"EXPR$1\" + t0.\"EXPR$0\" FROM (VALUES (10, 1), (30, 3)) AS t WHERE t.\"EXPR$0\" + t.\"EXPR$1\" > 50",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 40,
        "name": "testEmptySort",
        "key": "testEmptySort",
        "pattern": "FROM <x1> ORDER BY <x1>.<x3>",
        "rewrite": "FROM EMP AS EMP WHERE False ORDER BY EMP.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 43,
        "name": "testExpandFilterExistsSimple",
        "key": "testExpandFilterExistsSimple",
        "pattern": "SELECT <x6> AS i FROM <x2> WHERE <x2>.<x5> < <x7> GROUP BY <x6> AS <x9>",
        "rewrite": "WHERE EXISTS (SELECT <x5> FROM <x4> WHERE <x4>.<x5> < <x7>)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 56,
        "name": "testFullOuterJoinSimplificationToInner",
        "key": "testFullOuterJoinSimplificationToInner",
        "pattern": "FROM (SELECT <x4> FROM <x1> WHERE <<y3>>) AS t1 INNER JOIN (SELECT <x4> FROM <x3> WHERE <<y1>>) AS t2 ON t1.<x7> = t2.<x7>",
        "rewrite": "FROM <x1> FULL JOIN EMP AS EMP ON <x1>.<x7> = <x3>.<x7> WHERE <<y3>> AND <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 57,
        "name": "testFullOuterJoinSimplificationToLeftOuter",
        "key": "testFullOuterJoinSimplificationToLeftOuter",
        "pattern": "FROM (SELECT <x4> FROM <x1> WHERE <<y2>>) AS t1 LEFT JOIN <x3> ON t1.<x6> = <x3>.<x6>",
        "rewrite": "FROM <x1> FULL JOIN EMP AS EMP ON <x1>.<x6> = <x3>.<x6> WHERE <<y2>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 58,
        "name": "testFullOuterJoinSimplificationToRightOuter",
        "key": "testFullOuterJoinSimplificationToRightOuter",
        "pattern": "FROM <x1> RIGHT JOIN (SELECT <x4> FROM <x3> WHERE <<y1>>) AS <x5> ON <x1>.<x7> = t1.<x7>",
        "rewrite": "FROM <x1> FULL JOIN EMP AS EMP ON <x1>.<x7> = <x3>.<x7> WHERE <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 59,
        "name": "testIntersectToDistinct",
        "key": "testIntersectToDistinct",
        "pattern": "SELECT t10.<x8>, t10.<x14>, t10.<x10>, t10.<x12>, t10.<x7>, t10.<x9>, t10.<x16>, t10.<x11>, t10.<x15> FROM (SELECT <x1>.<x8>, <x1>.<x14>, <x1>.<x10>, <x1>.<x12>, <x1>.<x7>, <x1>.<x9>, <x1>.<x16>, <x1>.<x11>, <x1>.<x15>, COUNT(<x13>) AS \"$f9\" FROM <x1> WHERE <<y1>> GROUP BY <x1>.<x8>, <x1>.<x14>, <x1>.<x10>, <x1>.<x12>, <x1>.<x7>, <x1>.<x9>, <x1>.<x16>, <x1>.<x11>, <x1>.<x15>\nUNION ALL\nSELECT <x2>.<x8>, <x2>.<x14>, <x2>.<x10>, <x2>.<x12>, <x2>.<x7>, <x2>.<x9>, <x2>.<x16>, <x2>.<x11>, <x2>.<x15>, COUNT(<x13>) AS \"$f9\" FROM <x2> WHERE <x2>.<x11> = <x18> GROUP BY <x2>.<x8>, <x2>.<x14>, <x2>.<x10>, <x2>.<x12>, <x2>.<x7>, <x2>.<x9>, <x2>.<x16>, <x2>.<x11>, <x2>.<x15>\nUNION ALL\nSELECT <x3>.<x8>, <x3>.<x14>, <x3>.<x10>, <x3>.<x12>, <x3>.<x7>, <x3>.<x9>, <x3>.<x16>, <x3>.<x11>, <x3>.<x15>, COUNT(<x13>) AS \"$f9\" FROM <x3> WHERE <x3>.<x11> = <x19> GROUP BY <x3>.<x8>, <x3>.<x14>, <x3>.<x10>, <x3>.<x12>, <x3>.<x7>, <x3>.<x9>, <x3>.<x16>, <x3>.<x11>, <x3>.<x15>) AS t10 GROUP BY t10.<x8>, t10.<x14>, t10.<x10>, t10.<x12>, t10.<x7>, t10.<x9>, t10.<x16>, t10.<x11>, t10.<x15> HAVING COUNT(<x13>) = 3",
        "rewrite": "SELECT <x7> FROM (SELECT <x7> FROM <x1> WHERE <<y1>> INTERSECT SELECT <x7> FROM <x5> WHERE <x5>.<x11> = <x18>) AS t1 INTERSECT SELECT <x7> FROM <x6> WHERE <x6>.<x11> = <x19>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 61,
        "name": "testLeftOuterJoinSimplificationToInner",
        "key": "testLeftOuterJoinSimplificationToInner",
        "pattern": "FROM <x1> INNER JOIN (SELECT <x5> FROM <x3> WHERE <<y1>>) AS t1 ON <x1>.<x7> = t1.<x7>",
        "rewrite": "FROM <x1> LEFT JOIN <x3> ON <x1>.<x7> = <x3>.<x7> WHERE <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 62,
        "name": "testMergeFilter",
        "key": "testMergeFilter",
        "pattern": "SELECT <x1>.<x3> FROM <x1> WHERE <<y1>>",
        "rewrite": "SELECT t.<x3> FROM (SELECT <x3> FROM <x1> WHERE <<y1>>) AS t WHERE t.<x4> = <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 63,
        "name": "testMergeIntersect",
        "key": "testMergeIntersect",
        "pattern": "SELECT <<y5>> FROM <x1> WHERE <<y3>> INTERSECT SELECT <<y5>> FROM <x2> WHERE <x2>.<x8> = <x10> INTERSECT SELECT <<y5>> FROM <x3> WHERE <x3>.<x8> = <x11>",
        "rewrite": "SELECT <<y5>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>> INTERSECT SELECT <<y5>> FROM <x5> WHERE <x5>.<x8> = <x10>) AS t1 INTERSECT SELECT <<y5>> FROM <x6> WHERE <x6>.<x8> = <x11>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 64,
        "name": "testMergeJoinFilter",
        "key": "testMergeJoinFilter",
        "pattern": "SELECT t1.<x7>, <<y5>> FROM <x1> INNER JOIN (SELECT <<y4>> FROM <x3> WHERE <<y1>>) AS t1 ON <x1>.<x7> = t1.<x7>",
        "rewrite": "SELECT <<y4>> FROM (SELECT <x3>.<x7>, <<y5>> FROM <x1> INNER JOIN <x3> ON <x1>.<x7> = <x3>.<x7> AND <<y1>>) AS t WHERE t.<x7> = <x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 66,
        "name": "testMergeMinusRightDeep",
        "key": "testMergeMinusRightDeep",
        "pattern": "SELECT <<y13>> FROM <x2> WHERE <x2>.<x8> = <x10> EXCEPT SELECT <<y13>> FROM <x3> WHERE <x3>.<x8> = <x11> AS <x22>",
        "rewrite": "SELECT <<y13>> FROM <x5> WHERE <x5>.<x8> = <x10> EXCEPT SELECT <<y13>> FROM <x6> WHERE <x6>.<x8> = <x11> AS t2",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 67,
        "name": "testMergeSetOpMixed",
        "key": "testMergeSetOpMixed",
        "pattern": "SELECT <<y13>> FROM <x2> WHERE <x2>.<x8> = <x10> INTERSECT SELECT <<y13>> FROM <x3> WHERE <x3>.<x8> = <x11> AS <x22>",
        "rewrite": "SELECT <<y13>> FROM <x5> WHERE <x5>.<x8> = <x10> INTERSECT SELECT <<y13>> FROM <x6> WHERE <x6>.<x8> = <x11> AS t2",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 69,
        "name": "testMergeUnionDistinct",
        "key": "testMergeUnionDistinct",
        "pattern": "SELECT <<y5>> FROM <x1> WHERE <<y3>>\nUNION\nSELECT <<y5>> FROM <x2> WHERE <x2>.<x8> = <x10>\nUNION\nSELECT <<y5>> FROM <x3> WHERE <x3>.<x8> = <x11>",
        "rewrite": "SELECT <<y5>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>>\nUNION\nSELECT <<y5>> FROM <x5> WHERE <x5>.<x8> = <x10>) AS t1\nUNION\nSELECT <<y5>> FROM <x6> WHERE <x6>.<x8> = <x11>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 70,
        "name": "testMergeUnionMixed",
        "key": "testMergeUnionMixed",
        "pattern": "SELECT <<y6>> FROM (SELECT <<y6>> FROM <x1> WHERE <<y3>>\nUNION\nSELECT <<y6>> FROM <x2> WHERE <x2>.<x8> = <x10>) AS t6\nUNION ALL\nSELECT <<y6>> FROM <x3> WHERE <x3>.<x8> = <x11>",
        "rewrite": "SELECT <<y6>> FROM (SELECT <<y6>> FROM <x1> WHERE <<y3>>\nUNION\nSELECT <<y6>> FROM <x5> WHERE <x5>.<x8> = <x10>) AS t1\nUNION ALL\nSELECT <<y6>> FROM <x6> WHERE <x6>.<x8> = <x11>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 71,
        "name": "testMergeUnionMixed2",
        "key": "testMergeUnionMixed2",
        "pattern": "SELECT <<y5>> FROM <x1> WHERE <<y3>>\nUNION\nSELECT <<y5>> FROM <x2> WHERE <x2>.<x8> = <x10>\nUNION\nSELECT <<y5>> FROM <x3> WHERE <x3>.<x8> = <x11>",
        "rewrite": "SELECT <<y5>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>>\nUNION ALL\nSELECT <<y5>> FROM <x5> WHERE <x5>.<x8> = <x10>) AS t1\nUNION\nSELECT <<y5>> FROM <x6> WHERE <x6>.<x8> = <x11>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 75,
        "name": "testPullConstantIntoFilter",
        "key": "testPullConstantIntoFilter",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>) AS t1 WHERE 15 > t1.<x3>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>) AS t WHERE t.<x5> + 5 > t.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 78,
        "name": "testPullConstantIntoProject",
        "key": "testPullConstantIntoProject",
        "pattern": "SELECT <x5> AS DEPTNO, 11, <x1>.<x3> + <x5>",
        "rewrite": "SELECT <x1>.<x4>, <x1>.<x4> + 1, <x1>.<x3> + <x1>.<x4>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 79,
        "name": "testPullConstantThroughAggregateAllConst",
        "key": "testPullConstantThroughAggregateAllConst",
        "pattern": "GROUP BY <x7>",
        "rewrite": "GROUP BY <x7>, <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 80,
        "name": "testPullConstantThroughAggregateAllLiterals",
        "key": "testPullConstantThroughAggregateAllLiterals",
        "pattern": "GROUP BY <x7>",
        "rewrite": "GROUP BY <x7>, <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 81,
        "name": "testPullConstantThroughAggregateConstGroupBy",
        "key": "testPullConstantThroughAggregateConstGroupBy",
        "pattern": "GROUP BY <x7>",
        "rewrite": "GROUP BY <x7>, <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 82,
        "name": "testPullConstantThroughAggregatePermuted",
        "key": "testPullConstantThroughAggregatePermuted",
        "pattern": "<x7>",
        "rewrite": "GROUP BY 4, 2 + 3",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 83,
        "name": "testPullConstantThroughAggregatePermutedConstFirst",
        "key": "testPullConstantThroughAggregatePermutedConstFirst",
        "pattern": "GROUP BY <x5>",
        "rewrite": "GROUP BY 4, <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 84,
        "name": "testPullConstantThroughAggregatePermutedConstGroupBy",
        "key": "testPullConstantThroughAggregatePermutedConstGroupBy",
        "pattern": "GROUP BY <x5>",
        "rewrite": "GROUP BY 42 + 24, <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 85,
        "name": "testPullConstantThroughAggregateSimpleNonNullable",
        "key": "testPullConstantThroughAggregateSimpleNonNullable",
        "pattern": "GROUP BY <x5>",
        "rewrite": "GROUP BY <x5>, 4",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 86,
        "name": "testPullConstantThroughConstLast",
        "key": "testPullConstantThroughConstLast",
        "pattern": "GROUP BY <x5>",
        "rewrite": "GROUP BY <x5>, 4",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 88,
        "name": "testPullConstantThroughUnion2",
        "key": "testPullConstantThroughUnion2",
        "pattern": "SELECT <<y3>>, <x2>.<x6>, <x2>.<x5> FROM <x2>",
        "rewrite": "SELECT <<y3>>, <x4>.<x6>, <x4>.<x5> FROM <x4>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 90,
        "name": "testPullFilterThroughAggregate",
        "key": "testPullFilterThroughAggregate",
        "pattern": "SELECT <<y2>> FROM <x1> GROUP BY <<y1>> HAVING <x1>.<x5> > <x6>",
        "rewrite": "SELECT t0.<x4>, t0.<x5>, t0.<x3> FROM (SELECT <<y2>> FROM <x1>) AS t0 WHERE t0.<x5> > <x6> GROUP BY t0.<x4>, t0.<x5>, t0.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 91,
        "name": "testPullFilterThroughAggregateGroupingSets",
        "key": "testPullFilterThroughAggregateGroupingSets",
        "pattern": "SELECT t4.<x4>, t4.<x5>, t4.<x3> FROM (SELECT <<y2>> FROM <x1> GROUP BY <<y1>> HAVING <x1>.<x5> > <x6>) AS t4 GROUP BY t4.<x4>, t4.<x5>, t4.<x3>",
        "rewrite": "SELECT t0.<x4>, t0.<x5>, t0.<x3> FROM (SELECT <<y2>> FROM <x1>) AS t0 WHERE t0.<x5> > <x6> GROUP BY t0.<x4>, t0.<x5>, t0.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 92,
        "name": "testPullNull",
        "key": "testPullNull",
        "pattern": "SELECT <x12> AS EMPNO, <x1>.<x5>, <x1>.<x8>, NULL AS MGR, <x1>.<x3>, <x1>.<x6>, <x1>.<x11>, <x13> AS DEPTNO, <x1>.<x7>",
        "rewrite": "SELECT <x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 94,
        "name": "testPushAggregateSumNoGroup",
        "key": "testPushAggregateSumNoGroup",
        "pattern": "SELECT SUM(t0.<x9> * t1.<x5>) FROM (SELECT <x1>.<x8>, <x10> AS count1 FROM <x1> GROUP BY <x1>.<x8>) AS t0 INNER JOIN (SELECT <x3>.<x6>, <x10> AS count2 FROM <x3> GROUP BY <x3>.<x6>) AS t1 ON t0.<x8> = t1.<x6>",
        "rewrite": "SELECT <x10> FROM <x1> INNER JOIN <x3> ON <x1>.<x8> = <x3>.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 95,
        "name": "testPushAggregateSumThroughJoin",
        "key": "testPushAggregateSumThroughJoin",
        "pattern": "SELECT t3.<x10>, CAST(SUM(<x1>.<x8>) * t4.<x9> AS INTEGER) FROM (SELECT <x1>.<x10>, SUM(<x1>.<x8>) FROM <x1> WHERE <<y1>> GROUP BY <x1>.<x10>) AS t3 INNER JOIN (SELECT <x12>, COUNT(<x6>) AS \"$f1\" FROM <x3> GROUP BY <x12>) AS t4 ON t3.<x10> = t4.<x5>",
        "rewrite": "SELECT t.<x10>, SUM(t.<x8>) FROM (SELECT <x5> FROM <x1> WHERE <<y1>>) AS t INNER JOIN <x3> ON t.<x10> = <x3>.<x5> GROUP BY t.<x10>, <x12>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 96,
        "name": "testPushAggregateThroughJoin1",
        "key": "testPushAggregateThroughJoin1",
        "pattern": "SELECT <<y5>> FROM (SELECT <x1>.<x8> FROM <x1> WHERE <<y2>> GROUP BY <x1>.<x8>) AS t2 INNER JOIN (SELECT <<y4>> FROM <x3> GROUP BY <x10>) AS t3 ON t2.<x8> = t3.<x6>",
        "rewrite": "SELECT t.<x8>, <<y4>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y2>>) AS t INNER JOIN <x3> ON t.<x8> = <x3>.<x6> GROUP BY t.<x8>, <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 98,
        "name": "testPushAggregateThroughJoin3",
        "key": "testPushAggregateThroughJoin3",
        "pattern": "SELECT t1.<x7>, <<y6>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y1>>) AS t1 INNER JOIN <x3> ON t1.<x7> = <x3>.<x6> GROUP BY t1.<x7>, <x9>",
        "rewrite": "SELECT t.<x7>, <<y6>> FROM (SELECT <<y5>> FROM <x1> WHERE <<y1>>) AS t INNER JOIN <x3> ON t.<x7> = <x3>.<x6> GROUP BY t.<x7>, <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 99,
        "name": "testPushAggregateThroughJoin4",
        "key": "testPushAggregateThroughJoin4",
        "pattern": "SELECT t0.<x5> FROM (SELECT <<y2>> FROM <x1> GROUP BY <x6>) AS t0 INNER JOIN <x3> ON t0.<x5> = <x3>.<x5>",
        "rewrite": "SELECT <<y2>> FROM <x1> INNER JOIN <x3> ON <x1>.<x5> = <x3>.<x5> GROUP BY <x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 102,
        "name": "testPushAvgGroupingSetsThroughUnion",
        "key": "testPushAvgGroupingSetsThroughUnion",
        "pattern": "SELECT t4.<x6>, t4.<x5>, AVG(t4.<x7>) FROM (SELECT <x1>.<x6>, <x1>.<x5>, <x1>.<x7> FROM <x1>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5>, <x2>.<x7> FROM <x2>) AS t4 GROUP BY t4.<x6>, t4.<x5>",
        "rewrite": "SELECT t.<x6>, t.<x5>, AVG(t.<x7>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>, t.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 103,
        "name": "testPushAvgThroughUnion",
        "key": "testPushAvgThroughUnion",
        "pattern": "SELECT t4.<x6>, AVG(t4.<x5>) FROM (SELECT <x1>.<x6>, <x1>.<x5> FROM <x1>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5> FROM <x2>) AS t4 GROUP BY t4.<x6>",
        "rewrite": "SELECT t.<x6>, AVG(t.<x5>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 104,
        "name": "testPushCountFilterThroughUnion",
        "key": "testPushCountFilterThroughUnion",
        "pattern": "SELECT t10.<x7>, SUM(t10.<x5>) FROM (SELECT <x1>.<x7>, <x10> AS count1 FROM <x1> WHERE <<y1>> GROUP BY <x1>.<x7>\nUNION ALL\nSELECT <x2>.<x7>, <x10> AS count1 FROM <x2> WHERE <x2>.<x7> > <x9> GROUP BY <x2>.<x7>) AS t10 GROUP BY t10.<x7>",
        "rewrite": "SELECT t1.<x7>, <x10> FROM (SELECT <x5> FROM <x1> WHERE <<y1>>\nUNION ALL\nSELECT <x5> FROM <x4> WHERE <x4>.<x7> > <x9>) AS t1 GROUP BY t1.<x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 105,
        "name": "testPushCountNullableGroupingSetsThroughUnion",
        "key": "testPushCountNullableGroupingSetsThroughUnion",
        "pattern": "SELECT t6.<x6>, t6.<x5>, SUM(t6.<x7>) FROM (SELECT <x1>.<x6>, <x1>.<x5>, COUNT(<x1>.<x8>) AS count1 FROM <x1> GROUP BY <x1>.<x6>, <x1>.<x5>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5>, COUNT(<x2>.<x8>) AS count1 FROM <x2> GROUP BY <x2>.<x6>, <x2>.<x5>) AS t6 GROUP BY t6.<x6>, t6.<x5>",
        "rewrite": "SELECT t.<x6>, t.<x5>, COUNT(t.<x8>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>, t.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 106,
        "name": "testPushCountNullableThroughUnion",
        "key": "testPushCountNullableThroughUnion",
        "pattern": "SELECT t6.<x6>, SUM(<x7>) FROM (SELECT <x1>.<x6>, COUNT(<x1>.<x5>) AS sum1 FROM <x1> GROUP BY <x1>.<x6>\nUNION ALL\nSELECT <x2>.<x6>, COUNT(<x2>.<x5>) FROM <x2> GROUP BY <x2>.<x6>) AS t6 GROUP BY t6.<x6>",
        "rewrite": "SELECT t.<x6>, COUNT(t.<x5>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 107,
        "name": "testPushCountStarGroupingSetsThroughUnion",
        "key": "testPushCountStarGroupingSetsThroughUnion",
        "pattern": "SELECT t6.<x7>, t6.<x6>, SUM(<x8>) FROM (SELECT <x1>.<x7>, <x1>.<x6>, <x9> AS count1 FROM <x1> GROUP BY <x1>.<x7>, <x1>.<x6>\nUNION ALL\nSELECT <x2>.<x7>, <x2>.<x6>, <x9> AS count1 FROM <x2> GROUP BY <x2>.<x7>, <x2>.<x6>) AS t6 GROUP BY t6.<x7>, t6.<x6>",
        "rewrite": "SELECT t.<x7>, t.<x6>, <x9> FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x7>, t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 108,
        "name": "testPushCountStarThroughUnion",
        "key": "testPushCountStarThroughUnion",
        "pattern": "SELECT t6.<x6>, SUM(<x5>) FROM (SELECT <x1>.<x6>, <x8> AS count1 FROM <x1> GROUP BY <x1>.<x6>\nUNION ALL\nSELECT <x2>.<x6>, <x8> AS count1 FROM <x2> GROUP BY <x2>.<x6>) AS t6 GROUP BY t6.<x6>",
        "rewrite": "SELECT t.<x6>, <x8> FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 110,
        "name": "testPushFilterPastAggThree",
        "key": "testPushFilterPastAggThree",
        "pattern": "<x9>",
        "rewrite": "<x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 112,
        "name": "testPushFilterPastAggWithGroupingSets1",
        "key": "testPushFilterPastAggWithGroupingSets1",
        "pattern": "SELECT ",
        "rewrite": "SELECT ",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 118,
        "name": "testPushJoinThroughUnionOnLeft",
        "key": "testPushJoinThroughUnionOnLeft",
        "pattern": "SELECT t1.<x8> FROM (SELECT <<y3>> FROM <x1>, <x2>\nUNION ALL\nSELECT <<y3>> FROM <x3>, <x4>) AS t1",
        "rewrite": "SELECT t.<x8> FROM (SELECT <<y3>> FROM <x1>\nUNION ALL\nSELECT <<y3>> FROM <x6>) AS t, <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 119,
        "name": "testPushJoinThroughUnionOnRight",
        "key": "testPushJoinThroughUnionOnRight",
        "pattern": "SELECT t1.<x8> FROM (SELECT <<y3>> FROM <x1>, <x2>\nUNION ALL\nSELECT <<y3>> FROM <x3>, <x4>) AS t1",
        "rewrite": "SELECT <x1>.<x8> FROM <x1>, (SELECT <<y3>> FROM <x6>\nUNION ALL\nSELECT <<y3>> FROM <x7>) AS t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 120,
        "name": "testPushMaxNullableGroupingSetsThroughUnion",
        "key": "testPushMaxNullableGroupingSetsThroughUnion",
        "pattern": "SELECT t6.<x7>, t6.<x6>, MAX(<x5>) FROM (SELECT <x1>.<x7>, <x1>.<x6>, MAX(<x1>.<x8>) AS max1 FROM <x1> GROUP BY <x1>.<x7>, <x1>.<x6>\nUNION ALL\nSELECT <x2>.<x7>, <x2>.<x6>, MAX(<x2>.<x8>) AS max1 FROM <x2> GROUP BY <x2>.<x7>, <x2>.<x6>) AS t6 GROUP BY t6.<x7>, t6.<x6>",
        "rewrite": "SELECT t.<x7>, t.<x6>, MAX(t.<x8>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x7>, t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 121,
        "name": "testPushMaxNullableThroughUnion",
        "key": "testPushMaxNullableThroughUnion",
        "pattern": "SELECT t6.<x7>, MAX(t6.<x5>) FROM (SELECT <x1>.<x7>, MAX(<x1>.<x6>) AS max1 FROM <x1> GROUP BY <x1>.<x7>\nUNION ALL\nSELECT <x2>.<x7>, MAX(<x2>.<x6>) AS max1 FROM <x2> GROUP BY <x2>.<x7>) AS t6 GROUP BY t6.<x7>",
        "rewrite": "SELECT t.<x7>, MAX(t.<x6>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 122,
        "name": "testPushMinGroupingSetsThroughUnion",
        "key": "testPushMinGroupingSetsThroughUnion",
        "pattern": "SELECT t6.<x6>, t6.<x5>, MIN(t6.<x8>) FROM (SELECT <x1>.<x6>, <x1>.<x5>, MIN(<x1>.<x7>) AS min1 FROM <x1> GROUP BY <x1>.<x6>, <x1>.<x5>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5>, MIN(<x2>.<x7>) AS min1 FROM <x2> GROUP BY <x2>.<x6>, <x2>.<x5>) AS t6 GROUP BY t6.<x6>, t6.<x5>",
        "rewrite": "SELECT t.<x6>, t.<x5>, MIN(t.<x7>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>, t.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 123,
        "name": "testPushMinThroughUnion",
        "key": "testPushMinThroughUnion",
        "pattern": "SELECT t2.<x3>, SUM(<x8>), MIN(<x11>), SUM(SUM(<x8>)) FROM (SELECT <<y2>>, <x1>.<x5> FROM <x1> GROUP BY <x7>, <x1>.<x5>) AS t2 GROUP BY t2.<x3>",
        "rewrite": "SELECT <<y2>>, <x11> FROM <x1> GROUP BY <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 124,
        "name": "testPushMinThroughUnion",
        "key": "testPushMinThroughUnion",
        "pattern": "SELECT t6.<x6>, MIN(MIN(<x2>.<x5>)) FROM (SELECT <x1>.<x6>, MIN(<x1>.<x5>) FROM <x1> GROUP BY <x1>.<x6>\nUNION ALL\nSELECT <x2>.<x6>, MIN(<x2>.<x5>) FROM <x2> GROUP BY <x2>.<x6>) AS t6 GROUP BY t6.<x6>",
        "rewrite": "SELECT t.<x6>, MIN(t.<x5>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 126,
        "name": "testPushProjectPastFilter2*",
        "key": "testPushProjectPastFilter2*",
        "pattern": "SELECT <x3> FROM (SELECT <<y2>> FROM <x1>) AS t2 WHERE t2.<x3> < <x5>",
        "rewrite": "SELECT <<y2>> FROM <x1> WHERE CASE WHEN <x1>.<x3> < <x5> THEN True ELSE False END",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 138,
        "name": "testPushProjectPastSetOp",
        "key": "testPushProjectPastSetOp",
        "pattern": "SELECT <x1>.<x5> FROM <x1>\nUNION ALL\nSELECT <x2>.<x5> FROM <x2>",
        "rewrite": "SELECT t.<x5> FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 144,
        "name": "testPushSumCountStarGroupingSetsThroughUnion",
        "key": "testPushSumCountStarGroupingSetsThroughUnion",
        "pattern": "SELECT t6.<x11>, t6.<x10>, SUM(t6.<x12>), SUM(t6.<x6>), MIN(t6.<x8>), MAX(t6.<x9>) FROM (SELECT <x1>.<x11>, <x1>.<x10>, SUM(<x1>.<x7>) AS sum1, <x13> AS count1, MIN(<x1>.<x11>) AS min1, MAX(<x1>.<x7>) AS max1 FROM <x1> GROUP BY <x1>.<x11>, <x1>.<x10>\nUNION ALL\nSELECT <x2>.<x11>, <x2>.<x10>, SUM(<x2>.<x7>) AS sum1, <x13> AS count1, MIN(<x2>.<x11>) AS min1, MAX(<x2>.<x7>) AS max1 FROM <x2> GROUP BY <x2>.<x11>, <x2>.<x10>) AS t6 GROUP BY t6.<x11>, t6.<x10>",
        "rewrite": "SELECT t.<x11>, t.<x10>, SUM(t.<x7>), <x13>, MIN(t.<x11>), MAX(t.<x7>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x11>, t.<x10>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 145,
        "name": "testPushSumCountStarThroughUnion",
        "key": "testPushSumCountStarThroughUnion",
        "pattern": "SELECT t6.<x8>, SUM(t6.<x12>), SUM(t6.<x6>), MIN(t6.<x9>), MAX(t6.<x10>) FROM (SELECT <x1>.<x8>, SUM(<x1>.<x7>) AS sum1, <x13> AS count1, MIN(<x1>.<x11>) AS min1, MAX(<x1>.<x7>) AS max1 FROM <x1> GROUP BY <x1>.<x8>\nUNION ALL\nSELECT <x2>.<x8>, SUM(<x2>.<x7>) AS sum1, <x13> AS count1, MIN(<x2>.<x11>) AS min1, MAX(<x2>.<x7>) AS max1 FROM <x2> GROUP BY <x2>.<x8>) AS t6 GROUP BY t6.<x8>",
        "rewrite": "SELECT t.<x8>, SUM(t.<x7>), <x13>, MIN(t.<x11>), MAX(t.<x7>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 146,
        "name": "testPushSumNullableGroupingSetsThroughUnion",
        "key": "testPushSumNullableGroupingSetsThroughUnion",
        "pattern": "SELECT t6.<x6>, t6.<x5>, SUM(t6.<x8>) FROM (SELECT <x1>.<x6>, <x1>.<x5>, SUM(<x1>.<x7>) AS sum1 FROM <x1> GROUP BY <x1>.<x6>, <x1>.<x5>\nUNION ALL\nSELECT <x2>.<x6>, <x2>.<x5>, SUM(<x2>.<x7>) AS sum1 FROM <x2> GROUP BY <x2>.<x6>, <x2>.<x5>) AS t6 GROUP BY t6.<x6>, t6.<x5>",
        "rewrite": "SELECT t.<x6>, t.<x5>, SUM(t.<x7>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>, t.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 148,
        "name": "testPushSumNullableThroughUnion",
        "key": "testPushSumNullableThroughUnion",
        "pattern": "SELECT t6.<x6>, SUM(<x7>) FROM (SELECT <x1>.<x6>, SUM(<x1>.<x5>) AS sum1 FROM <x1> GROUP BY <x1>.<x6>\nUNION ALL\nSELECT <x2>.<x6>, SUM(<x2>.<x5>) FROM <x2> GROUP BY <x2>.<x6>) AS t6 GROUP BY t6.<x6>",
        "rewrite": "SELECT t.<x6>, SUM(t.<x5>) FROM (SELECT <x5> FROM <x1>\nUNION ALL\nSELECT <x5> FROM <x4>) AS t GROUP BY t.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 150,
        "name": "testPushSumNullConstantThroughUnion",
        "key": "testPushSumNullConstantThroughUnion",
        "pattern": "SELECT t8.<x5>, SUM(t8.<x6>) FROM (SELECT <<y2>>, SUM(NULL) AS sum1 FROM <x1> GROUP BY <x7>\nUNION ALL\nSELECT <x2>.<x5>, SUM(NULL) FROM <x2> GROUP BY <x2>.<x5>) AS t8 GROUP BY t8.<x5>",
        "rewrite": "SELECT t1.<x5>, SUM(t1.U) FROM (SELECT <x1>.EMPNO, <<y2>>, <x1>.JOB, <x1>.MGR, <x1>.HIREDATE, <x1>.SAL, <x1>.COMM, <x1>.DEPTNO, <x1>.SLACKER, NULL AS U FROM <x1>\nUNION ALL\nSELECT <x4>.EMPNO, <x4>.<x5>, <x4>.JOB, <x4>.MGR, <x4>.HIREDATE, <x4>.SAL, <x4>.COMM, <x4>.DEPTNO, <x4>.SLACKER, NULL AS U FROM <x4>) AS t1 GROUP BY t1.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 152,
        "name": "testReduceCastAndConsts",
        "key": "testReduceCastAndConsts",
        "pattern": "<x1>.<x3> + 5",
        "rewrite": "CAST(<x1>.<x3> + 10 / 2 AS INTEGER)",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 154,
        "name": "testReduceCastTimeUnchanged",
        "key": "testReduceCastTimeUnchanged",
        "pattern": "<x5>",
        "rewrite": "<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 155,
        "name": "testReduceCompositeInSubQuery",
        "key": "testReduceCompositeInSubQuery",
        "pattern": "(<x1>.<x5>, <x1>.<x7>) IN (SELECT <x2>.<x5>, <x2>.<x7> FROM <x2> GROUP BY <x2>.<x5>, <x2>.<x7>) OR <x1>.<x7> < 100",
        "rewrite": "(<x1>.<x5>, <x1>.<x7>) IN (SELECT <x4>.<x5>, <x4>.<x7> FROM <x4> GROUP BY <x4>.<x5>, <x4>.<x7>) OR <x1>.<x7> < 40 + 60",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 157,
        "name": "testReduceConstants2",
        "key": "testReduceConstants2",
        "pattern": "SELECT <<y2>> FROM (SELECT <<y2>>) AS t2",
        "rewrite": "SELECT CAST(CASE WHEN NULL IS NULL THEN <x2> IS NULL WHEN <x2> IS NULL THEN NULL IS NULL ELSE <x2> IS NULL END AS BOOLEAN) FROM (SELECT <<y2>>) AS t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 159,
        "name": "testReduceConstantsCaseEquals",
        "key": "testReduceConstantsCaseEquals",
        "pattern": "<x7>",
        "rewrite": "(CASE WHEN <x1>.<x4> = 20 THEN 2 WHEN <x7> THEN <x5> ELSE 3 END) = <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 160,
        "name": "testReduceConstantsCaseEquals2",
        "key": "testReduceConstantsCaseEquals2",
        "pattern": "<x7>",
        "rewrite": "(CASE WHEN <x1>.<x4> = 20 THEN 2 WHEN <x7> THEN <x5> ELSE NULL END) = <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 161,
        "name": "testReduceConstantsCaseEquals3",
        "key": "testReduceConstantsCaseEquals3",
        "pattern": "<x9> OR <x8>",
        "rewrite": "(CASE WHEN <x9> THEN <x5> WHEN <x1>.<x4> = 20 THEN 2 WHEN <x8> THEN <x5> WHEN <x9> THEN 111 ELSE 0 END) = <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 162,
        "name": "testReduceConstantsDup",
        "key": "testReduceConstantsDup",
        "pattern": "SELECT <x1>.<x2> FROM <x1>",
        "rewrite": "SELECT DEPT.<x2> FROM DEPT AS DEPT WHERE DEPT.<x2> = 7 AND DEPT.<x2> = 8",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 163,
        "name": "testReduceConstantsDup2",
        "key": "testReduceConstantsDup2",
        "pattern": "SELECT <x9> AS EMPNO, <x1>.<x6>, <x1>.<x4>, NULL AS MGR, <x1>.<x3>, <x1>.<x8>, <x1>.<x5>, <x1>.<x7>, <x1>.<x2> FROM <x1>",
        "rewrite": "SELECT <x2> FROM EMP AS EMP WHERE EMP.<x7> = 7 AND EMP.<x7> = 8 AND EMP.EMPNO = <x9> AND EMP.MGR IS NULL AND EMP.EMPNO = <x9>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 164,
        "name": "testReduceConstantsEliminatesFilter",
        "key": "testReduceConstantsEliminatesFilter",
        "pattern": "FROM <x1>",
        "rewrite": "FROM (SELECT <x3>, <x4>) AS t WHERE <x3> + <x4> > 3 + NULL",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 165,
        "name": "testReduceConstantsIsNotNull",
        "key": "testReduceConstantsIsNotNull",
        "pattern": "<<y1>>",
        "rewrite": "<<y1>> AND <x1>.<x3> IS NOT NULL",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 166,
        "name": "testReduceConstantsIsNull",
        "key": "testReduceConstantsIsNull",
        "pattern": "SELECT <x1>.<x2> FROM <x1>",
        "rewrite": "SELECT EMP.<x2> FROM EMP AS EMP WHERE EMP.<x2> = 10 AND EMP.<x2> IS NULL",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 167,
        "name": "testReduceConstantsNegated",
        "key": "testReduceConstantsNegated",
        "pattern": "SELECT <x1>.<x2> FROM <x1>",
        "rewrite": "SELECT EMP.<x2> FROM EMP AS EMP WHERE EMP.<x2> = <x3> AND NOT EMP.<x2> = <x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 168,
        "name": "testReduceConstantsNegatedInverted",
        "key": "testReduceConstantsNegatedInverted",
        "pattern": "SELECT <x1>.<x2> FROM <x1>",
        "rewrite": "SELECT EMP.<x2> FROM EMP AS EMP WHERE EMP.<x2> > <x3> AND EMP.<x2> <= <x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 169,
        "name": "testReduceConstantsNull",
        "key": "testReduceConstantsNull",
        "pattern": "SELECT NULL AS N FROM <x1>",
        "rewrite": "SELECT * FROM (SELECT * FROM (SELECT NULL AS N FROM <x1>) AS t WHERE t.N IS NULL AND t.N IS NULL) AS t0 WHERE t0.N IS NULL",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 170,
        "name": "testReduceConstantsNullEqualsOne",
        "key": "testReduceConstantsNullEqualsOne",
        "pattern": "FROM <x1>",
        "rewrite": "FROM EMP AS EMP WHERE 1 IS NULL",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 171,
        "name": "testReduceConstantsProjectNullable*",
        "key": "testReduceConstantsProjectNullable*",
        "pattern": "<x4> AS <x6>",
        "rewrite": "<x1>.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 172,
        "name": "testReduceConstantsRequiresExecutor",
        "key": "testReduceConstantsRequiresExecutor",
        "pattern": "<x10>",
        "rewrite": "t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 173,
        "name": "testReduceExpressionsNot",
        "key": "testReduceExpressionsNot",
        "pattern": "FROM (SELECT <<y5>>\nUNION ALL\nSELECT <<y4>>) AS t1 WHERE NOT t1.<x1>",
        "rewrite": "FROM (SELECT <<y5>>\nUNION ALL\nSELECT <<y4>>) AS t WHERE NOT t.<x1>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 174,
        "name": "testReduceNestedCaseWhen",
        "key": "testReduceNestedCaseWhen",
        "pattern": "CASE WHEN <x8> THEN <x8> ELSE <x7> END",
        "rewrite": "(CASE WHEN <x8> THEN (CASE WHEN <x8> THEN NULL ELSE <x5> END) IS NULL ELSE (CASE WHEN <x7> THEN NULL ELSE <x5> END) IS NULL END) = <x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 175,
        "name": "testReduceNot",
        "key": "testReduceNot",
        "pattern": "FROM (SELECT CASE WHEN <x8> THEN NULL ELSE <x7> END AS CASECOL FROM <x1>) AS t1 WHERE NOT t1.<x4>",
        "rewrite": "FROM (SELECT CASE WHEN <x8> THEN NULL ELSE <x7> END AS CASECOL FROM <x1>) AS t WHERE NOT t.<x4>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 176,
        "name": "testReduceNullableCase",
        "key": "testReduceNullableCase",
        "pattern": "SELECT CAST(<x3> AS INTEGER) FROM (SELECT <<y4>>) AS t2 LEFT JOIN (SELECT <<y4>>) AS <x1> ON <<y1>>",
        "rewrite": "SELECT CASE WHEN <<y1>> = <x3> THEN CAST(t0.\"EXPR$0\" AS INTEGER) ELSE <x3> END FROM (SELECT <<y4>>) AS t LEFT JOIN (SELECT <<y4>>) AS t0 ON <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 177,
        "name": "testReduceNullableCase2",
        "key": "testReduceNullableCase2",
        "pattern": "SELECT <<y2>>, NULL GROUP BY <<y1>>, NULL",
        "rewrite": "SELECT <<y2>>, CASE WHEN <x5> = <x6> THEN CAST(SUBSTRING(<x1>.<x3> FROM <x5> FOR <x6>) AS VARCHAR(<x7>)) ELSE NULL END GROUP BY <<y1>>, CASE WHEN <x5> = <x6> THEN CAST(SUBSTRING(<x1>.<x3> FROM <x5> FOR <x6>) AS VARCHAR(<x7>)) ELSE NULL END",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 178,
        "name": "testReduceOrCaseWhen",
        "key": "testReduceOrCaseWhen",
        "pattern": "<x8> OR <x7>",
        "rewrite": "(CASE WHEN <x8> THEN NULL ELSE <x5> END) IS NULL OR (CASE WHEN <x7> THEN NULL ELSE <x5> END) IS NULL",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 179,
        "name": "testReduceValuesToEmpty",
        "key": "testReduceValuesToEmpty",
        "pattern": "SELECT <x2> FROM <x1>",
        "rewrite": "SELECT t0.\"EXPR$0\" + t0.\"EXPR$1\" AS X, t0.\"EXPR$1\" AS B, t0.\"EXPR$0\" AS A FROM (VALUES (10, 1), (30, 7)) AS t WHERE t.\"EXPR$0\" - t.\"EXPR$1\" < 0",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 180,
        "name": "testReduceValuesUnderFilter",
        "key": "testReduceValuesUnderFilter",
        "pattern": "FROM (SELECT <x2>, '<x3>') AS t1",
        "rewrite": "FROM (VALUES ('<x2>', '<x3>'), (20, 'y')) AS t WHERE t.\"EXPR$0\" < 15",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 181,
        "name": "testReduceValuesUnderProject",
        "key": "testReduceValuesUnderProject",
        "pattern": "SELECT <x1> FROM (SELECT 11\nUNION ALL\nSELECT 23) AS t1",
        "rewrite": "SELECT t.\"EXPR$0\" + t.\"EXPR$1\" FROM (VALUES (10, 1), (20, 3)) AS t",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 182,
        "name": "testReduceValuesUnderProjectFilter",
        "key": "testReduceValuesUnderProjectFilter",
        "pattern": "SELECT <x1> FROM (VALUES (11, '<x2>', '<x3>'), (23, '<x4>', '<x5>')) AS t2",
        "rewrite": "SELECT t0.\"EXPR$0\" + t0.\"EXPR$1\" AS X, t0.\"EXPR$1\" AS B, t0.\"EXPR$0\" AS A FROM (VALUES ('<x3>', '<x2>'), (30, 7), ('<x5>', '<x4>')) AS t WHERE t.\"EXPR$0\" - t.\"EXPR$1\" < 21",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 183,
        "name": "testRemoveSemiJoin",
        "key": "testRemoveSemiJoin",
        "pattern": "FROM <x1> INNER JOIN <x3> ON <<y1>>",
        "rewrite": "FROM <x1>, <x3> WHERE <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 184,
        "name": "testRemoveSemiJoinRight",
        "key": "testRemoveSemiJoinRight",
        "pattern": "FROM <x1> INNER JOIN <x5> ON <<y1>> INNER JOIN <x2> ON <x5>.<x8> = <x2>.<x8>",
        "rewrite": "FROM <x1>, <x5>, <x4> WHERE <<y1>> AND <x5>.<x8> = <x4>.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 188,
        "name": "testSemiJoinReduceConstants",
        "key": "testSemiJoinReduceConstants",
        "pattern": "SELECT t6.<x6> FROM (SELECT <<y4>> FROM (SELECT <<y3>> FROM <x1>) AS t5 WHERE t5.<x5> = <x8>) AS t6 INNER JOIN (SELECT t7.<x5> FROM (SELECT <x2>.<x6>, <x2>.<x5> FROM <x2>) AS t7 WHERE t7.<x6> = <x9>) AS t9 ON t6.<x5> = t9.<x5>",
        "rewrite": "SELECT t0.<x6> FROM (SELECT <<y4>> FROM (SELECT <<y3>> FROM <x1>) AS t WHERE t.<x5> = <x8>) AS t0 INNER JOIN (SELECT t1.<x5> FROM (SELECT <x4>.<x6>, <x4>.<x5> FROM <x4>) AS t1 WHERE t1.<x6> = <x9>) AS t3 ON t0.<x5> = t3.<x5>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 192,
        "name": "testSemiJoinRuleLeft",
        "key": "testSemiJoinRuleLeft",
        "pattern": "FROM <x1>",
        "rewrite": "FROM <x1> LEFT JOIN (SELECT EMP.DEPTNO FROM EMP AS EMP WHERE EMP.SAL > 100 GROUP BY EMP.DEPTNO) AS t1 ON <x1>.DEPTNO = t1.DEPTNO",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 205,
        "name": "testStrengthenJoinType",
        "key": "testStrengthenJoinType",
        "pattern": "SELECT <x1>.<x13>, <x1>.<x5>, CAST(t0.<x8> AS INTEGER) AS EMPNO, CAST(t0.<x9> AS VARCHAR(20)) AS ENAME, CAST(t0.<x12> AS VARCHAR(10)) AS JOB, t0.<x14>, CAST(t0.<x7> AS TIMESTAMP) AS HIREDATE, CAST(t0.<x10> AS INTEGER) AS SAL, CAST(t0.<x15> AS INTEGER) AS COMM, CAST(t0.<x13> AS INTEGER) AS DEPTNO0, CAST(t0.<x11> AS BOOLEAN) AS SLACKER FROM <x1> INNER JOIN (SELECT <<y3>> FROM <x3> WHERE <<y1>>) AS t0 ON <x1>.<x13> = t0.<x13>",
        "rewrite": "SELECT <<y3>> FROM <x1> LEFT JOIN <x3> ON <x1>.<x13> = <x3>.<x13> WHERE <x3>.<x13> IS NOT NULL AND <<y1>>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 206,
        "name": "testSwapOuterJoin",
        "key": "testSwapOuterJoin",
        "pattern": "FROM <x1> RIGHT JOIN <x4> AS <x5> ON <x1>.<x3> = DEPT0.<x3>",
        "rewrite": "FROM DEPT AS DEPT LEFT JOIN <x1> ON DEPT.<x3> = <x1>.<x3>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 208,
        "name": "testTransitiveInferenceComplexPredicate",
        "key": "testTransitiveInferenceComplexPredicate",
        "pattern": "FROM (SELECT <<y11>> FROM <x1> WHERE <<y10>>) AS t2 INNER JOIN (SELECT <<y11>> FROM (SELECT <<y11>> FROM <x2> WHERE <x2>.<x6> = <x2>.<x8>) AS t3 WHERE t3.<x8> > <x11>) AS t4 ON t2.<x8> = t4.<x8>",
        "rewrite": "FROM (SELECT <<y11>> FROM <x1> WHERE <<y10>>) AS t INNER JOIN (SELECT <<y11>> FROM <x4> WHERE <x4>.<x6> = <x4>.<x8>) AS t0 ON t.<x8> = t0.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 211,
        "name": "testTransitiveInferenceFullOuterJoin",
        "key": "testTransitiveInferenceFullOuterJoin",
        "pattern": "FROM <x1> FULL JOIN <x4> AS <x3> ON <x1>.<x5> = EMP2.<x5> WHERE <<y1>> AND EMP2.<x5> > <x7>",
        "rewrite": "FROM <x1> FULL JOIN <x4> AS EMP0 ON <x1>.<x5> = EMP0.<x5> WHERE <<y1>> AND EMP0.<x5> > <x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 213,
        "name": "testTransitiveInferenceJoin3way",
        "key": "testTransitiveInferenceJoin3way",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t1 INNER JOIN (SELECT <<y4>> FROM <x2> WHERE <x2>.<x8> > <x10>) AS t2 ON t1.<x8> = t2.<x8> INNER JOIN (SELECT <<y4>> FROM <x3> WHERE <x3>.<x8> > <x10>) AS t3 ON t2.<x8> = t3.<x8>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t INNER JOIN <x5> ON t.<x8> = <x5>.<x8> INNER JOIN <x6> ON <x5>.<x8> = <x6>.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 216,
        "name": "testTransitiveInferenceNoPullUpExprs",
        "key": "testTransitiveInferenceNoPullUpExprs",
        "pattern": "FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>>) AS t1 INNER JOIN <x2> ON t1.<x7> = <x2>.<x7>",
        "rewrite": "FROM (SELECT <<y5>> FROM <x1> WHERE <<y3>>) AS t INNER JOIN <x4> ON t.<x7> = <x4>.<x7>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 217,
        "name": "testTransitiveInferencePreventProjectPullUp",
        "key": "testTransitiveInferencePreventProjectPullUp",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>) AS t3 INNER JOIN <x2> ON t3.<x6> = <x2>.<x6>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>) AS t0 INNER JOIN <x4> ON t0.<x6> = <x4>.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 218,
        "name": "testTransitiveInferenceProject",
        "key": "testTransitiveInferenceProject",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t1 INNER JOIN (SELECT <<y4>> FROM <x2> WHERE <x2>.<x6> > <x8>) AS t2 ON t1.<x6> = t2.<x6>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t INNER JOIN <x4> ON t.<x6> = <x4>.<x6>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 221,
        "name": "testTransitiveInferenceUnion",
        "key": "testTransitiveInferenceUnion",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>\nUNION ALL\nSELECT <x2>.<x8> FROM <x2> WHERE <x2>.<x8> > <x11>) AS t9 INNER JOIN (SELECT <x7> FROM <x3> WHERE <x3>.<x8> > <x10> OR <x3>.<x8> > <x11>) AS t10 ON t9.<x8> = t10.<x8>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y1>>\nUNION ALL\nSELECT <x5>.<x8> FROM <x5> WHERE <x5>.<x8> > <x11>) AS t3 INNER JOIN <x6> ON t3.<x8> = <x6>.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 222,
        "name": "testTransitiveInferenceUnion3way",
        "key": "testTransitiveInferenceUnion3way",
        "pattern": "FROM (SELECT <<y5>> FROM (SELECT <<y6>> FROM <x1> WHERE <<y2>>\nUNION ALL\nSELECT <x2>.<x10> FROM <x2> WHERE <x2>.<x10> > <x13>) AS t12\nUNION ALL\nSELECT <x3>.<x10> FROM <x3> WHERE <x3>.<x10> > <x11>) AS t15 INNER JOIN (SELECT <<y5>> FROM <x4> WHERE <x4>.<x10> > <x12> OR <x4>.<x10> > <x13> OR <x4>.<x10> > <x11>) AS t16 ON t15.<x10> = t16.<x10>",
        "rewrite": "FROM (SELECT <<y5>> FROM (SELECT <<y6>> FROM <x1> WHERE <<y2>>\nUNION ALL\nSELECT <x6>.<x10> FROM <x6> WHERE <x6>.<x10> > <x13>) AS t3\nUNION ALL\nSELECT <x7>.<x10> FROM <x7> WHERE <x7>.<x10> > <x11>) AS t6 INNER JOIN <x8> ON t6.<x10> = <x8>.<x10>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 223,
        "name": "testTransitiveInferenceUnionAlwaysTrue",
        "key": "testTransitiveInferenceUnionAlwaysTrue",
        "pattern": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t6 INNER JOIN (SELECT <<y1>> FROM (SELECT <x2>.<x8> FROM <x2> WHERE <x2>.<x8> > <x10>\nUNION ALL\nSELECT <x3>.<x8> FROM <x3>) AS t10 WHERE t10.<x8> < <x9>) AS t11 ON t6.<x8> = t11.<x8>",
        "rewrite": "FROM (SELECT <<y4>> FROM <x1> WHERE <<y2>>) AS t0 INNER JOIN (SELECT <x5>.<x8> FROM <x5> WHERE <x5>.<x8> > <x10>\nUNION ALL\nSELECT <x6>.<x8> FROM <x6>) AS t4 ON t0.<x8> = t4.<x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 224,
        "name": "testUnionMergeRule",
        "key": "testUnionMergeRule",
        "pattern": "SELECT <<y2>> FROM <x1>\nUNION ALL\nSELECT <x2>.<x9>, <x2>.<x10> FROM <x2> GROUP BY <x2>.<x9>, <x2>.<x10>\nUNION ALL\nSELECT <x3>.<x9>, <x3>.<x10> FROM <x3> GROUP BY <x3>.<x9>, <x3>.<x10>\nUNION ALL\nSELECT <x4>.<x9>, <x4>.<x10> FROM <x4>",
        "rewrite": "SELECT <x9> FROM (SELECT <<y2>> FROM <x1>\nUNION ALL\nSELECT t4.<x9>, t4.<x10> FROM (SELECT <x6>.<x9>, <x6>.<x10>, COUNT(*) FROM <x6> GROUP BY <x6>.<x9>, <x6>.<x10>\nUNION ALL\nSELECT <x7>.<x9>, <x7>.<x10>, COUNT(*) FROM <x7> GROUP BY <x7>.<x9>, <x7>.<x10>) AS t4) AS t6\nUNION ALL\nSELECT <x8>.<x9>, <x8>.<x10> FROM <x8>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 225,
        "name": "testUnionToDistinctRule",
        "key": "testUnionToDistinctRule",
        "pattern": "SELECT t0.<x7>, t0.<x5> FROM (SELECT <<y3>> FROM <x1>\nUNION ALL\nSELECT <<y3>> FROM <x2>) AS t0 GROUP BY t0.<x7>, t0.<x5>",
        "rewrite": "SELECT <<y3>> FROM <x1>\nUNION\nSELECT <<y3>> FROM <x4>",
        "constraints": "",
        "actions": "",
        "database": "postgresql"
    },
    {
        "id": 230,
        "name": "testWhereOrSubQuery",
        "key": "testWhereOrSubQuery",
        "pattern": "SELECT <x1>.<x7>, <x1>.<x8>, <x1>.<x12>, <x1>.<x14>, <x1>.<x5>, <x1>.<x9>, <x1>.<x15>, <x1>.<x13>, <x1>.<x11> FROM <x1> LEFT JOIN (SELECT <<y2>>, <x16> AS i FROM <x3>) AS <x10> ON <x1>.<x7> = t2.<x13> WHERE <x18> OR NOT CASE WHEN t2.<x6> IS NOT NULL THEN <x16> ELSE False END",
        "rewrite": "SELECT <x5> FROM <x1> WHERE <x18> OR <x1>.<x7> NOT IN (SELECT <<y2>> FROM <x3>)",
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

# import sys
# # append the current directory
# sys.path.append(".")
# # append the parent directory
# sys.path.append("..")
# import json
# from core.rule_parser import RuleParser

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

# save_file(data,"/home/orderheart/syy/sql_rewriter/A_result/neg_data.py")

