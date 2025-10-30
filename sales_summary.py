# sales_summary.py
# Requirements: pandas, matplotlib
# Run: python sales_summary.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

DB_FILE = "sales_data.db"
CHART_FILE = "sales_chart.png"

def create_sample_db(db_file: str):
    """Create DB and insert sample rows only if table doesn't exist."""
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        product TEXT,
        quantity INTEGER,
        price REAL
    )
    """)
    # Check if table already has rows
    cur.execute("SELECT COUNT(1) FROM sales")
    count = cur.fetchone()[0]
    if count == 0:
        sample_rows = [
            ("2025-10-01", "Widget A", 10, 9.99),
            ("2025-10-02", "Widget B", 5, 19.50),
            ("2025-10-02", "Widget A", 7, 9.99),
            ("2025-10-03", "Widget C", 3, 29.99),
            ("2025-10-03", "Widget B", 2, 19.50),
            ("2025-10-04", "Widget C", 4, 29.99),
            ("2025-10-04", "Widget A", 1, 9.99),
        ]
        cur.executemany("INSERT INTO sales (date, product, quantity, price) VALUES (?, ?, ?, ?)", sample_rows)
        conn.commit()
    conn.close()

def run_queries_and_plot(db_file: str, chart_file: str):
    conn = sqlite3.connect(db_file)

    # Query 1: total quantity and revenue by product
    query1 = """
    SELECT
      product,
      SUM(quantity) AS total_qty,
      SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product
    ORDER BY revenue DESC
    """
    df_by_product = pd.read_sql_query(query1, conn)
    print("=== Sales summary by product ===")
    print(df_by_product.to_string(index=False))

    # Query 2: overall totals (single-row)
    query2 = """
    SELECT
      SUM(quantity) as total_quantity,
      SUM(quantity * price) as total_revenue
    FROM sales
    """
    df_totals = pd.read_sql_query(query2, conn)
    print("\n=== Overall totals ===")
    print(df_totals.to_string(index=False))

    # Simple bar chart: revenue by product
    if not df_by_product.empty:
        ax = df_by_product.plot(kind="bar", x="product", y="revenue", legend=False, rot=0)
        ax.set_xlabel("Product")
        ax.set_ylabel("Revenue (currency)")
        ax.set_title("Revenue by Product")
        plt.tight_layout()
        plt.savefig(chart_file)
        print(f"\nBar chart saved to: {os.path.abspath(chart_file)}")
        plt.show()
    else:
        print("No data to plot.")

    conn.close()

if __name__ == "__main__":
    create_sample_db(DB_FILE)
    run_queries_and_plot(DB_FILE, CHART_FILE)
