import sqlite3
import random
import csv
import datetime

random.seed(42)

DB_PATH = "sales_analysis.db"

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------
REGIONS = ["North", "South", "East", "West", "Central"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]

CATEGORIES = {
    "Electronics": ["Wireless Mouse", "Mechanical Keyboard", "27in Monitor", "USB-C Hub",
                    "Bluetooth Speaker", "Webcam HD", "Laptop Stand", "Power Bank"],
    "Furniture": ["Office Chair", "Standing Desk", "Bookshelf", "Filing Cabinet",
                  "Desk Lamp", "Monitor Arm"],
    "Stationery": ["Notebook Pack", "Sticky Notes", "Gel Pens", "Whiteboard",
                   "Binder Set", "Highlighter Pack"],
    "Apparel": ["Cotton T-Shirt", "Hoodie", "Cap", "Backpack", "Water Bottle"],
    "Home & Kitchen": ["Coffee Maker", "Blender", "Air Fryer", "Cutlery Set", "Storage Boxes"],
}

FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Ishaan", "Rohan", "Kabir", "Ananya", "Diya",
               "Saanvi", "Meera", "Kiara", "Priya", "Arjun", "Neha", "Sanya", "Karan",
               "Riya", "Manav", "Tanya", "Rahul"]
LAST_NAMES = ["Sharma", "Verma", "Gupta", "Iyer", "Nair", "Reddy", "Singh", "Mehta",
              "Kapoor", "Chatterjee", "Joshi", "Bose", "Rao", "Malhotra", "Das"]

START_DATE = datetime.date(2025, 1, 1)
END_DATE = datetime.date(2025, 12, 31)


def random_date(start, end):
    delta = (end - start).days
    return start + datetime.timedelta(days=random.randint(0, delta))


def build_products():
    products = []
    pid = 1
    for category, names in CATEGORIES.items():
        for name in names:
            base_price = {
                "Electronics": random.uniform(15, 250),
                "Furniture": random.uniform(40, 400),
                "Stationery": random.uniform(2, 25),
                "Apparel": random.uniform(8, 60),
                "Home & Kitchen": random.uniform(20, 150),
            }[category]
            products.append((pid, name, category, round(base_price, 2)))
            pid += 1
    return products


def build_customers(n=200):
    customers = []
    for cid in range(1, n + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        region = random.choice(REGIONS)
        segment = random.choices(SEGMENTS, weights=[0.55, 0.25, 0.20])[0]
        signup_date = random_date(datetime.date(2023, 1, 1), datetime.date(2025, 6, 30))
        customers.append((cid, name, region, segment, signup_date.isoformat()))
    return customers


def build_orders_and_items(customers, products, n_orders=1500):
    orders = []
    order_items = []
    item_id = 1
    # Slightly seasonal weighting: more orders in Oct-Dec (festive/holiday season)
    month_weights = [0.7, 0.6, 0.7, 0.8, 0.8, 0.9, 0.9, 1.0, 1.1, 1.4, 1.6, 1.5]

    for oid in range(1, n_orders + 1):
        customer = random.choice(customers)
        month = random.choices(range(1, 13), weights=month_weights)[0]
        day = random.randint(1, 28)
        order_date = datetime.date(2025, month, day)
        status = random.choices(
            ["Completed", "Completed", "Completed", "Cancelled", "Returned"],
            weights=[0.7, 0.1, 0.1, 0.05, 0.05]
        )[0]
        orders.append((oid, customer[0], order_date.isoformat(), status))

        n_items = random.choices([1, 2, 3, 4], weights=[0.45, 0.3, 0.15, 0.10])[0]
        chosen_products = random.sample(products, k=min(n_items, len(products)))
        for prod in chosen_products:
            qty = random.randint(1, 5)
            unit_price = prod[3]
            # small random discount on some line items
            discount_pct = random.choices([0, 5, 10, 15], weights=[0.6, 0.2, 0.15, 0.05])[0]
            order_items.append((item_id, oid, prod[0], qty, unit_price, discount_pct))
            item_id += 1

    return orders, order_items


def main():
    products = build_products()
    customers = build_customers()
    orders, order_items = build_orders_and_items(customers, products)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS products;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        region TEXT NOT NULL,
        segment TEXT NOT NULL,
        signup_date TEXT NOT NULL
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_price REAL NOT NULL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        discount_pct REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)

    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers)
    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)", order_items)

    conn.commit()

    # Also export as CSVs so they can be opened outside SQLite (e.g. Excel, MySQL import)
    tables = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
    }
    headers = {
        "customers": ["customer_id", "customer_name", "region", "segment", "signup_date"],
        "products": ["product_id", "product_name", "category", "unit_price"],
        "orders": ["order_id", "customer_id", "order_date", "status"],
        "order_items": ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"],
    }
    for table, rows in tables.items():
        with open(f"{table}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers[table])
            writer.writerows(rows)

    conn.close()
    print(f"Generated {len(customers)} customers, {len(products)} products, "
          f"{len(orders)} orders, {len(order_items)} order items.")


if __name__ == "__main__":
    main()
