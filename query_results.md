
### 1. FILTERING: completed orders placed in Q4 2025

order_id | customer_id | order_date | status
--- | --- | --- | ---
193 | 24 | 2025-10-01 | Completed
743 | 161 | 2025-10-01 | Completed
1113 | 142 | 2025-10-01 | Completed
1408 | 102 | 2025-10-01 | Completed
1436 | 192 | 2025-10-01 | Completed
53 | 43 | 2025-10-02 | Completed
408 | 41 | 2025-10-02 | Completed
564 | 86 | 2025-10-02 | Completed
1180 | 63 | 2025-10-02 | Completed
1282 | 101 | 2025-10-02 | Completed
1428 | 138 | 2025-10-02 | Completed
1500 | 179 | 2025-10-02 | Completed
... (514 rows total, showing first 12)

### 2. AGGREGATION: total revenue, order count, and average order value

total_orders | total_revenue | avg_order_value
--- | --- | ---
1366 | 651942.5 | 477.26

### 3. JOIN + AGGREGATION: monthly sales trend

month | orders | revenue
--- | --- | ---
2025-01 | 75 | 35825.77
2025-02 | 76 | 39011.55
2025-03 | 65 | 27282.39
2025-04 | 85 | 34151.05
2025-05 | 78 | 32558.48
2025-06 | 125 | 61736.9
2025-07 | 104 | 53404.02
2025-08 | 109 | 56322.41
2025-09 | 135 | 62098.55
2025-10 | 176 | 89523.08
2025-11 | 177 | 84056.39
2025-12 | 161 | 75971.9

### 4. JOIN + AGGREGATION: top 10 products by revenue

product_name | category | units_sold | revenue
--- | --- | --- | ---
Desk Lamp | Furniture | 301 | 79402.96
Bluetooth Speaker | Electronics | 262 | 51623.86
Laptop Stand | Electronics | 256 | 51047.19
Wireless Mouse | Electronics | 296 | 47176.32
Mechanical Keyboard | Electronics | 270 | 45410.52
USB-C Hub | Electronics | 269 | 37395.88
Monitor Arm | Furniture | 315 | 37295.19
Filing Cabinet | Furniture | 299 | 29416.1
Power Bank | Electronics | 201 | 28186.17
Bookshelf | Furniture | 241 | 26921.72

### 5. AGGREGATION + HAVING: categories generating over 50,000 in revenue

category | revenue
--- | ---
Electronics | 302529.65
Furniture | 209723.18
Home & Kitchen | 75930.56

### 6. JOIN across 3 tables: revenue and order count by region and segment

region | segment | orders | revenue
--- | --- | --- | ---
Central | Consumer | 146 | 68642.11
Central | Corporate | 74 | 32469.5
Central | Small Business | 38 | 16310.16
East | Consumer | 145 | 70861.1
East | Corporate | 91 | 44476.01
East | Small Business | 51 | 25856.96
North | Consumer | 102 | 44452.99
North | Corporate | 82 | 41077.85
North | Small Business | 74 | 31391.26
South | Consumer | 166 | 83009.16
South | Small Business | 57 | 28936.87
South | Corporate | 36 | 14099.57
... (15 rows total, showing first 12)

### 7. TOP CUSTOMERS: highest completed-order spend

customer_id | customer_name | region | total_orders | completed_spend
--- | --- | --- | --- | ---
138 | Karan Mehta | East | 12 | 8714.0
62 | Kiara Chatterjee | East | 9 | 7845.33
190 | Saanvi Reddy | Central | 8 | 7475.44
130 | Meera Nair | South | 10 | 7460.31
161 | Karan Kapoor | West | 11 | 7145.63
171 | Sanya Das | West | 12 | 7129.89
91 | Meera Rao | West | 11 | 7067.05
110 | Diya Verma | East | 8 | 6556.9
72 | Diya Joshi | East | 8 | 6482.68
64 | Arjun Bose | East | 11 | 6400.01

### 8. ORDER STATUS BREAKDOWN: cancellation / return rate

status | order_count | pct_of_total
--- | --- | ---
Completed | 1366 | 91.07
Returned | 74 | 4.93
Cancelled | 60 | 4.0

### 9. SUBQUERY: customers who have never placed an order (filtering with NOT IN)

customer_id | customer_name | region | segment
--- | --- | --- | ---
26 | Neha Joshi | Central | Corporate

### 10. CTE + CORRELATED SUBQUERY: best-selling product per category

category | product_name | revenue
--- | --- | ---
Apparel | Cotton T-Shirt | 10142.01
Electronics | Bluetooth Speaker | 51623.86
Furniture | Desk Lamp | 79402.96
Home & Kitchen | Coffee Maker | 24150.62
Stationery | Notebook Pack | 6353.27