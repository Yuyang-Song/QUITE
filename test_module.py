"""
####################################################################
#                       Test Module                               #
####################################################################

Simple unit test for Knowledge Base Tool and DBMS Explain Tool components.

Author: Yuyang Song
Date: 2025-07-23

####################################################################
"""

import os
import sys
import unittest
import asyncio
from pathlib import Path
sys.path.append('../')
sys.path.append('./')

from QUITE.src.Rewrite_Middleware.middleware import Knowledge_Base_Tool, DBMS_EXPLAIN_Tool, DBMS_Syntax_Tool, Equivalence_Check_Tool, DBMS
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))


class TestRewriteMiddleware(unittest.TestCase):
    """
    ####################################################################
    #                   Rewrite Middleware Tests                      #
    ####################################################################
    """
    
    def setUp(self):
        """Setup test data"""
        self.input_sql = """
        WITH min_supply AS (
            SELECT ps.ps_partkey, MIN(ps.ps_supplycost) AS min_supplycost
            FROM partsupp ps
            JOIN supplier s ON ps.ps_suppkey = s.s_suppkey
            JOIN nation n ON s.s_nationkey = n.n_nationkey
            JOIN region r ON n.n_regionkey = r.r_regionkey
            WHERE r.r_name = 'EUROPE'
            GROUP BY ps.ps_partkey
        )
        SELECT s.s_acctbal, s.s_name, n.n_name, p.p_partkey, p.p_mfgr, s.s_address, s.s_phone, s.s_comment
        FROM part p
        JOIN partsupp ps ON p.p_partkey = ps.ps_partkey
        JOIN supplier s ON ps.ps_suppkey = s.s_suppkey
        JOIN nation n ON s.s_nationkey = n.n_nationkey
        JOIN min_supply ms ON p.p_partkey = ms.ps_partkey AND ps.ps_supplycost = ms.min_supplycost
        WHERE p.p_size = 6
          AND p.p_type LIKE '%NICKEL'
        ORDER BY s.s_acctbal DESC, n.n_name, s.s_name, p.p_partkey
        LIMIT 100;
        """
        
        self.origin_suggestion_list = [
            {
                "group": "Subquery_optimization",
                "origin_suggestion": "Ensure the CTE precomputes the minimum supply cost for parts from European suppliers, thus avoiding repetitive execution."
            },
            {
                "group": "Join_optimization",
                "origin_suggestion": "Simplify the main query by leveraging this CTE and reducing redundant joins, particularly eliminating unnecessary joins to the `region` table in the main query."
            },
            {
                "group": "Predication_simplification",
                "origin_suggestion": "Replace the correlated subquery that finds the minimum `ps_supplycost` with a more efficient Common Table Expression (CTE)."
            }
        ]
        
        # Test SQL for DBMS_EXPLAIN_Tool
        self.explain_test_sql = "select p_brand, p_type, p_size, count(distinct ps_suppkey) as supplier_cnt from partsupp, part where p_partkey = ps_partkey and p_brand <> 'Brand#43' and p_type not like 'PROMO PLATED%' and p_size in (18, 8, 33, 17, 27, 6, 1, 50) and ps_suppkey not in ( select s_suppkey from supplier where s_comment like '%Customer%Complaints%' ) group by p_brand, p_type, p_size order by supplier_cnt desc, p_brand, p_type, p_size;"
        
        # Test SQL Pairs for Euiqvalence_Check_Tool
        # Initialize DBMS instance
        self.dbms = DBMS()


    def test_dbms_explain_tool(self):
        """
        ############################################################
        #               Test: DBMS Explain Tool                   #
        ############################################################
        """
        print("\n" + "="*50)
        print("🧪 Testing DBMS Explain Tool")
        print("="*50)
        
        try:
            result = asyncio.run(DBMS_EXPLAIN_Tool(self.dbms, self.explain_test_sql))
            
            # Basic assertions
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)
            
            print("✅ Test PASSED!")
            print(f"📋 Query plans generated: {len(result)} items")
            
        except Exception as e:
            self.fail(f"❌ Test FAILED: {str(e)}")

    # def test_knowledge_base_tool(self):
    #     """
    #     ############################################################
    #     #               Test: Knowledge Base Tool                 #
    #     ############################################################
    #     """
    #     print("\n" + "="*50)
    #     print("🧪 Testing Knowledge Base Tool")
    #     print("="*50)
        
    #     try:
    #         output = asyncio.run(Knowledge_Base_Tool(self.input_sql, self.origin_suggestion_list))
            
    #         # Basic assertions
    #         self.assertIsNotNone(output)
            
    #         print("✅ Test PASSED!")
    #         # print(f"📋 Output: {output}")
            
    #     except Exception as e:
    #         self.fail(f"❌ Test FAILED: {str(e)}")

    def test_dbms_syntax_tool(self):
        """
        ############################################################
        #               Test: DBMS Syntax Tool                     #
        ############################################################
        """
        print("\n" + "="*50)
        print("🧪 Testing DBMS Syntax Tool")
        print("="*50)
        
        try:
            # Assuming DBMS has a method to check syntax
            result = asyncio.run(DBMS_Syntax_Tool(self.dbms, self.input_sql))
            
            # Basic assertions
            self.assertTrue(result, "Syntax check failed")
            
            print("✅ Test PASSED!")
            
        except Exception as e:
            self.fail(f"❌ Test FAILED: {str(e)}")

    def test_equivalence_check_tool(self): 
        """
        ############################################################
        #               Test: Equivalence Check Tool               #
        ############################################################
        """
        print("\n" + "="*50)
        print("🧪 Testing Equivalence Check Tool")
        print("="*50)

        os.environ['LD_LIBRARY_PATH'] = str(PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Hybrid_SQL_Corrector" )

        SCHEMA_PATH = PROJECT_ROOT / "dataset" / "schemas" / "calcite.sql"
        with open(SCHEMA_PATH, 'r') as f:
            schema_content = f.read()
            if not schema_content.strip():
                raise ValueError(f"Schema file {SCHEMA_PATH} is empty or not found.")
            print(f"Schema content loaded from {SCHEMA_PATH}")

        try:
            # Example SQL pairs for equivalence check
            # EQ case
            original_sql = "SELECT * FROM (VALUES (1,2)) WHERE FALSE"
            rewritten_sql = "SELECT * FROM (SELECT NULL AS EXPR$0, NULL AS EXPR$1) AS t WHERE 1 = 0"
            result = []
            result.append(asyncio.run(Equivalence_Check_Tool(original_sql, rewritten_sql, SCHEMA_PATH)))  
            # Basic assertions
            self.assertIsNotNone(result)
            # NEQ case
            original_sql = "SELECT * FROM (VALUES (1,2)) WHERE FALSE"
            rewritten_sql = "SELECT * FROM (VALUES (1,2)) WHERE TRUE"
            result.append(asyncio.run(Equivalence_Check_Tool(original_sql, rewritten_sql, SCHEMA_PATH)))  
            # Basic assertions
            self.assertIsNotNone(result)
            # Unknown case
            original_sql = "SELECT 2, EMP.DEPTNO, EMP.JOB FROM EMP AS EMP UNION ALL SELECT 1, EMP0.DEPTNO, EMP0.JOB FROM EMP AS EMP0"
            rewritten_sql = "SELECT 2, EMP1.DEPTNO, EMP1.JOB FROM EMP AS EMP1 UNION ALL SELECT 1, EMP2.DEPTNO, EMP2.JOB FROM EMP AS EMP2"
            result.append(asyncio.run(Equivalence_Check_Tool(original_sql, rewritten_sql, SCHEMA_PATH)))  
            # Basic assertions
            self.assertIsNotNone(result)
            
            print("✅ Test PASSED!")
            print(f"📋 Equivalence results: {result}")
            
        except Exception as e:
            self.fail(f"❌ Test FAILED: {str(e)}")


def main():
    """
    ####################################################################
    #                         Main Runner                              #
    ####################################################################
    """
    print("="*60)
    print("🚀 Starting SQL Optimization Tests")
    print("="*60)
    
    unittest.main(verbosity=1)


if __name__ == "__main__":
    main()






