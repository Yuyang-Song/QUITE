## Join总表

| 类别编号 | 策略名称 | 主要特征 | ID | 平均 timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Join 顺序与层级优化 | 通过改变 Join 操作在查询执行计划中的层级和时机，来尽早过滤数据、简化聚合或消除冗余计算 | DSB_38, DSB_80, DSB_136, DSB_137，Calcite_40, Calcite_53，SQLStorm_25 | 39.60429 |
| 2 | EXISTS 替代复杂 JOIN | 使用 EXISTS (半连接) 替代 LEFT JOIN ，以避免生成不必要的中间结果集，仅用于存在性检查。 | Calcite_6 | 20.43797 |
| 3 | 去重替代复杂 JOIN | 当 JOIN (尤其是 OUTER JOIN) 和 GROUP BY 的唯一目的是为了获取唯一值时，将其替换为更高效的 DISTINCT 操作。 | Calcite_50 | 27.93877 |

---

## CTE总表

| 类别编号 | 策略名称 | 主要特征 | ID | 平均 timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | CTE+Join 改写嵌套子查询 | 将 WHERE /SELECT 子句中的相关子查询（为每行重复执行）重写为单个 CTE，并使用 JOIN 连接，从而将 N*M 次计算减少为 N+M 次。 | DSB_5, DSB_6, DSB_55, DSB_57, DSB_109, DSB_110, DSB_111, DSB_138, TPC-H_5, TPC-H_6, TPC-H_47, TPC-H_56, SQLStorm_41 | 79.49654 |
| 2 | CTE 预聚合/过滤/复用 | 创建 CTE 来预先计算、聚合或过滤数据（如日期范围、GROUP BY、IN 子句），并在查询中复用或 JOIN 这个更小的结果集，以避免重复计算或减少 JOIN 的数据量。 | DSB_56, DSB_136, DSB_137, TPC-H_46, TPC-H_55, SQLStorm_8, SQLStorm_24, SQLStorm_27, SQLStorm_29 | 35.25680 |
| 3 | Join/Filter 下推至 CTE | 将 JOIN 或 WHERE 过滤条件下推（Pushdown）到现有 CTE 的（例如 UNION ALL）分支内部，以便在合并数据前尽早过滤。 | DSB_79, DSB_80 | 66.80019 |
| 4 | Join 移出 CTE 优化 | 将 JOIN 操作从聚合 CTE 中移出到主查询，使得 CTE 内部的 GROUP BY 可以在更少、更简单的数据上（例如用 ID 代替字符串）执行。 | SQLStorm_25 | 11.95327 |

---

## Predicate总表

| 类别编号 | 策略名称 | 主要特征 | ID | 平均 timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 谓词下推 (Predicate Pushdown) | 将 WHERE 过滤条件（或 JOIN）下推到 CTE、UNION ALL 分支、子查询内部，或从 HAVING 移至 WHERE，或通过预计算提前应用，以便尽早过滤数据。 | DSB_5, DSB_79, DSB_81, TPC-H_55, Calcite_44, Calcite_51, Calcite_53, SQLStorm_24, SQLStorm_27, SQLStorm_41 | 26.99197 |
| 2 | 谓词/表达式简化与重写 | 重写谓词中的算术运算，或将复杂的多列表达式（尤其是 JOIN 条件）转换为更简单、等效的 WHERE 表达式，或简化选择列表中的计算逻辑，以提高效率。 | DSB_6, DSB_57, Calcite_40, SQLStorm_8 | 50.63979 |
| 3 | EXISTS 替代 JOIN | 使用 EXISTS (半连接) 进行存在性检查，而不是执行完整的 JOIN，以避免构建大型中间结果集。 | Calcite_6 | 20.43797 |