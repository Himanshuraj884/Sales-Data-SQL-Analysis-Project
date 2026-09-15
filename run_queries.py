import sqlite3
import re

DB_PATH = "sales_analysis.db"
SQL_PATH = "sales_analysis.sql"

def split_queries(sql_text):
    """Split the .sql file into (title, query) blocks based on '-- N. TITLE' headers."""
    blocks = []
    current_title = None
    current_lines = []
    for line in sql_text.splitlines():
        m = re.match(r"-- (\d+)\.\s+(.*)", line.strip())
        if m:
            if current_title and current_lines:
                blocks.append((current_title, "\n".join(current_lines)))
            current_title = f"{m.group(1)}. {m.group(2)}"
            current_lines = []
        elif current_title is not None:
            if line.strip().startswith("--"):
                continue
            current_lines.append(line)
    if current_title and current_lines:
        blocks.append((current_title, "\n".join(current_lines)))
    return blocks


def main():
    with open(SQL_PATH) as f:
        sql_text = f.read()

    blocks = split_queries(sql_text)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    out_lines = []
    for title, query in blocks:
        query = query.strip().rstrip(";")
        if not query:
            continue
        out_lines.append(f"\n### {title}\n")
        try:
            cur.execute(query)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            # limit preview rows for very long result sets
            preview = rows[:12]
            out_lines.append(" | ".join(cols))
            out_lines.append(" | ".join(["---"] * len(cols)))
            for r in preview:
                out_lines.append(" | ".join(str(x) for x in r))
            if len(rows) > 12:
                out_lines.append(f"... ({len(rows)} rows total, showing first 12)")
            elif len(rows) == 0:
                out_lines.append("(no rows)")
        except Exception as e:
            out_lines.append(f"ERROR: {e}")

    conn.close()
    with open("query_results.md", "w") as f:
        f.write("\n".join(out_lines))
    print("Done. Wrote query_results.md")


if __name__ == "__main__":
    main()
