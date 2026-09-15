# Sales Data SQL Analysis

**Tools:** MySQL 8.0 (primary), Python for seeded synthetic-data generation | **Period:** Jan–Dec 2025

## 1. Overview

This project analyzes a relational e-commerce dataset across four related tables — `customers`, `products`, `orders`, and `order_items` — to explore sales patterns and summarize business metrics. The SQL workflow demonstrates filtering, aggregation, `GROUP BY`/`HAVING`, multi-table joins, subqueries, and CTE-based analysis.

## 2. Schema

| Table | Key columns |
|---|---|
| `customers` | customer_id, customer_name, region, segment, signup_date |
| `products` | product_id, product_name, category, unit_price |
| `orders` | order_id, customer_id, order_date, status |
| `order_items` | order_item_id, order_id, product_id, quantity, unit_price, discount_pct |

The dataset contains 200 customers, 30 products across 5 categories, 1,500 orders, and 2,861 order items.

## 3. Verified findings from the SQLite mirror

- 1,366 orders are completed; completed-order revenue is **651,942.50** illustrative monetary units, with an average completed order value of **477.26**.
- Revenue rises toward the final quarter, with **October** the highest-revenue month in the verified dataset.
- Electronics, Furniture, and Home & Kitchen are the categories above the 50,000 revenue threshold.
- Desk Lamp is the highest-revenue individual product in the verified dataset.
- The Consumer segment leads revenue in each region in the verified dataset.
- 91.1% of all orders are completed, 4.9% returned, and 4.0% cancelled.
- The no-order customer query identifies customers with no corresponding order records.

These findings are based on the included seeded SQLite verification mirror. The MySQL script contains the same source data and analytical logic, but this package was not executed against a live MySQL server in the build environment.

## 4. Query techniques demonstrated

1. Filtering with `WHERE` and date ranges
2. Aggregation with `SUM`, `COUNT`, and `AVG`
3. `GROUP BY` and `HAVING`
4. Multi-table joins
5. Subqueries with `NOT IN`
6. CTEs with `WITH`
7. Correlated subqueries for per-category maximums
8. Business KPI calculations

## 5. Interview explanation

> “I built a relational e-commerce sales analysis project in MySQL using four related tables: customers, products, orders, and order_items. I wrote 10 queries using filtering, aggregation, joins, GROUP BY/HAVING, subqueries, and a CTE to analyze revenue trends, top products, category performance, customer spend, and order status.”

## 6. Scope and reproducibility

The dataset is synthetic and seeded for reproducibility. It is not real customer or company data. The primary database target is MySQL 8.0 and the file `sales_analysis_mysql.sql` is the main interview/demo artifact. A SQLite mirror is included only for lightweight verification of the data relationships and analytical query logic.
