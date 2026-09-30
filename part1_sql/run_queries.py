import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "part1_sql", "output")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;
"""

cursor.execute(query)
rows = cursor.fetchall()

output_file = os.path.join(OUTPUT_DIR, "monthly_category_revenue.csv")

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["month", "category", "revenue", "n_orders"])
    writer.writerows(rows)
# Query 2: Region-wise total revenue and order count
query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""

cursor.execute(query2)
rows2 = cursor.fetchall()

output_file2 = os.path.join(OUTPUT_DIR, "region_revenue_orders.csv")

with open(output_file2, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["region", "total_revenue", "n_orders"])
    writer.writerows(rows2)

print(f"Created: {output_file2}")
print(f"Rows written: {len(rows2)}")
# Query 3: Top resellers by total spend
query3 = """
SELECT
    o.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

cursor.execute(query3)
rows3 = cursor.fetchall()

output_file3 = os.path.join(OUTPUT_DIR, "top_resellers.csv")

with open(output_file3, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "total_spend"])
    writer.writerows(rows3)

print(f"Created: {output_file3}")
print(f"Rows written: {len(rows3)}")
# Query 4: Resellers who never placed an order
query4 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

cursor.execute(query4)
rows4 = cursor.fetchall()

output_file4 = os.path.join(OUTPUT_DIR, "zero_order_resellers.csv")

with open(output_file4, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "region"])
    writer.writerows(rows4)

print(f"Created: {output_file4}")
print(f"Rows written: {len(rows4)}")
# Query 4b: Demonstrate COUNT(*) vs COUNT(order_id)
query4b = """
SELECT
    r.reseller_id,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;
"""

cursor.execute(query4b)
rows4b = cursor.fetchall()

output_file4b = os.path.join(OUTPUT_DIR, "zero_order_count_test.csv")

with open(output_file4b, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "count_star", "count_order_id"])
    writer.writerows(rows4b)

print(f"Created: {output_file4b}")
print(f"Rows written: {len(rows4b)}")
# Query 5: AOV for June Delivered orders
query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

cursor.execute(query5)
rows5 = cursor.fetchall()

output_file5 = os.path.join(OUTPUT_DIR, "june_delivered_aov.csv")

with open(output_file5, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["aov"])
    writer.writerows(rows5)

print(f"Created: {output_file5}")
print(f"Rows written: {len(rows5)}")
conn.close()

print(f"Created: {output_file}")
print(f"Rows written: {len(rows)}")