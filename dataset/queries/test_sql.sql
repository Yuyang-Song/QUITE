-- TPC-H Query: Find supplier count by part brand, type, and size
-- Excludes specific brand and type patterns, and suppliers with customer complaints

SELECT 
    p_brand,
    p_type,
    p_size,
    COUNT(DISTINCT ps_suppkey) AS supplier_cnt
FROM partsupp ps
JOIN part p ON p.p_partkey = ps.ps_partkey
WHERE p.p_brand <> 'Brand#43'
  AND p.p_type NOT LIKE 'PROMO PLATED%'
  AND p.p_size IN (18, 8, 33, 17, 27, 6, 1, 50)
  AND ps.ps_suppkey NOT IN (
      SELECT s_suppkey 
      FROM supplier 
      WHERE s_comment LIKE '%Customer%Complaints%'
  )
GROUP BY 
    p_brand,
    p_type,
    p_size
ORDER BY 
    supplier_cnt DESC,
    p_brand,
    p_type,
    p_size;