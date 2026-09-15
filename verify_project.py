import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("sales_analysis.db")
SQL = Path(__file__).with_name("sales_analysis.sql")

def split_queries(sql_text):
    import re
    blocks, title, lines = [], None, []
    for line in sql_text.splitlines():
        m = re.match(r"-- (\d+)\.\s+(.*)", line.strip())
        if m:
            if title and lines:
                blocks.append((title, "\n".join(lines)))
            title = f"{m.group(1)}. {m.group(2)}"
            lines = []
        elif title is not None and not line.strip().startswith("--"):
            lines.append(line)
    if title and lines:
        blocks.append((title, "\n".join(lines)))
    return blocks

def main():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    blocks = split_queries(SQL.read_text(encoding="utf-8"))
    blocks = [(t, q) for t, q in blocks if q.strip()]
    assert len(blocks) == 10, f"Expected 10 queries, found {len(blocks)}"
    for title, query in blocks:
        cur = conn.execute(query.strip().rstrip(";"))
        cur.fetchall()
        print(f"PASS: {title}")
    # Basic integrity checks
    checks = {
        "customers": 200,
        "products": 30,
        "orders": 1500,
        "order_items": 2861,
    }
    for table, expected in checks.items():
        actual = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert actual == expected, f"{table}: expected {expected}, got {actual}"
    orphan_orders = conn.execute("""
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON c.customer_id = o.customer_id
        WHERE c.customer_id IS NULL
    """).fetchone()[0]
    orphan_items = conn.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN orders o ON o.order_id = oi.order_id
        WHERE o.order_id IS NULL
    """).fetchone()[0]
    orphan_products = conn.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN products p ON p.product_id = oi.product_id
        WHERE p.product_id IS NULL
    """).fetchone()[0]
    assert orphan_orders == orphan_items == orphan_products == 0
    conn.close()
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
