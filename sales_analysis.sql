-- =====================================================================
-- SALES DATA SQL ANALYSIS
-- Dataset: customers, products, orders, order_items (SQLite dialect)
-- Goal: explore sales patterns and summarize key business metrics using
--       filtering, aggregation (GROUP BY / HAVING), and multi-table joins.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 0. Schema reference
-- ---------------------------------------------------------------------
-- customers(customer_id, customer_name, region, segment, signup_date)
-- products(product_id, product_name, category, unit_price)
-- orders(order_id, customer_id, order_date, status)
-- order_items(order_item_id, order_id, product_id, quantity, unit_price, discount_pct)

-- ---------------------------------------------------------------------
-- 1. FILTERING: completed orders placed in Q4 2025
-- ---------------------------------------------------------------------
SELECT order_id, customer_id, order_date, status
FROM orders
WHERE status = 'Completed'
  AND order_date BETWEEN '2025-10-01' AND '2025-12-31'
ORDER BY order_date;

-- ---------------------------------------------------------------------
-- 2. AGGREGATION: total revenue, order count, and average order value
--    (revenue = quantity * unit_price * (1 - discount_pct/100),
--     completed orders only)
-- ---------------------------------------------------------------------
SELECT
    COUNT(DISTINCT o.order_id)                                   AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0)), 2)                AS total_revenue,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0))
          / COUNT(DISTINCT o.order_id), 2)                        AS avg_order_value
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed';

-- ---------------------------------------------------------------------
-- 3. JOIN + AGGREGATION: monthly sales trend
-- ---------------------------------------------------------------------
SELECT
    strftime('%Y-%m', o.order_date)                               AS month,
    COUNT(DISTINCT o.order_id)                                    AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0)), 2)                 AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY month
ORDER BY month;

-- ---------------------------------------------------------------------
-- 4. JOIN + AGGREGATION: top 10 products by revenue
-- ---------------------------------------------------------------------
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity)                                              AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0)), 2)                 AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o   ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- 5. AGGREGATION + HAVING: categories generating over 50,000 in revenue
-- ---------------------------------------------------------------------
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0)), 2)                 AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o   ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
HAVING revenue > 50000
ORDER BY revenue DESC;

-- ---------------------------------------------------------------------
-- 6. JOIN across 3 tables: revenue and order count by region and segment
-- ---------------------------------------------------------------------
SELECT
    c.region,
    c.segment,
    COUNT(DISTINCT o.order_id)                                    AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0)), 2)                 AS revenue
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY c.region, c.segment
ORDER BY c.region, revenue DESC;

-- ---------------------------------------------------------------------
-- 7. TOP CUSTOMERS: highest completed-order spend
-- ---------------------------------------------------------------------
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COUNT(DISTINCT o.order_id)                                    AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price
              * (1 - oi.discount_pct / 100.0)), 2)                 AS completed_spend
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id
ORDER BY completed_spend DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- 8. ORDER STATUS BREAKDOWN: cancellation / return rate
-- ---------------------------------------------------------------------
SELECT
    status,
    COUNT(*)                                                      AS order_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 2)    AS pct_of_total
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- ---------------------------------------------------------------------
-- 9. SUBQUERY: customers who have never placed an order (filtering with NOT IN)
-- ---------------------------------------------------------------------
SELECT customer_id, customer_name, region, segment
FROM customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM orders);

-- ---------------------------------------------------------------------
-- 10. CTE + CORRELATED SUBQUERY: best-selling product per category
--     (returns all tied top products within each category)
-- ---------------------------------------------------------------------
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price
            * (1 - oi.discount_pct / 100.0))                       AS revenue
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    JOIN orders o   ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
    GROUP BY p.product_id
)
SELECT category, product_name, ROUND(revenue, 2) AS revenue
FROM product_revenue pr
WHERE revenue = (
    SELECT MAX(revenue) FROM product_revenue pr2
    WHERE pr2.category = pr.category
)
ORDER BY category;
