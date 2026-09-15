# Sales Data SQL Analysis — MySQL 8.0

A self-contained SQL analytics project using a synthetic e-commerce dataset. The project uses **MySQL 8.0** as its target database and contains 10 analytical queries covering filtering, aggregation, joins, subqueries, CTEs, and business-metric analysis.

## Requirements

- MySQL 8.0+
- MySQL Workbench or the `mysql` CLI (recommended for the interview demo)
- Python 3.8+ only if you want to regenerate the synthetic CSV data

## Run the project in MySQL

1. Open MySQL Workbench.
2. Open `sales_analysis_mysql.sql`.
3. Run the entire script.
4. The script creates the `sales_analysis` database, creates the four tables, loads the included synthetic data, and runs no destructive operations outside that database.
5. After the database is created, run any of the 10 analysis queries at the bottom of the script individually or together.

The script is written for **MySQL 8.0**. In particular, the monthly-trend query uses MySQL's `DATE_FORMAT()`.

## Dataset

- 200 customers
- 30 products across 5 categories
- 1,500 orders
- 2,861 order items
- Period: January–December 2025
- Synthetic and reproducible; not real customer or company data

## Schema

```text
customers(customer_id, customer_name, region, segment, signup_date)
products(product_id, product_name, category, unit_price)
orders(order_id, customer_id, order_date, status)
order_items(order_item_id, order_id, product_id, quantity, unit_price, discount_pct)
```

Relationships:
- `orders.customer_id` → `customers.customer_id`
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`

## Queries demonstrated

1. Q4 completed-order filtering
2. Total revenue, order count, and average order value
3. Monthly revenue trend
4. Top 10 products by revenue
5. Category revenue using `GROUP BY` + `HAVING`
6. Revenue/order count by region and segment using 3-table joins
7. Top 10 customers by completed-order spend
8. Order-status breakdown and percentage of total
9. Customers with no orders using `NOT IN`
10. Best-selling product per category using a CTE + correlated subquery

## Supporting files

- `sales_analysis_mysql.sql` — primary MySQL 8.0 script: schema, data inserts, and 10 queries
- `customers.csv`, `products.csv`, `orders.csv`, `order_items.csv` — source synthetic data
- `generate_data.py` — regenerates the seeded source data and the SQLite verification mirror
- `sales_analysis.sql` — SQLite verification version of the same 10 analytical queries
- `sales_analysis.db` — SQLite verification mirror
- `run_queries.py` — executes the SQLite verification query set
- `verify_project.py` — checks the SQLite mirror and query outputs
- `query_results.md` — verified SQLite output preview
- `Sales_Data_SQL_Analysis_Report.md` — project report

## Important scope note

The resume project is **MySQL**. The SQLite database/files are retained only as a lightweight local verification mirror because a MySQL server is not bundled with the project. The primary interview/demo artifact is `sales_analysis_mysql.sql`.

Monetary values are illustrative numeric amounts from the synthetic dataset; no external currency is claimed.
