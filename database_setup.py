import sqlite3
import pandas as pd
import os

# Connect to SQLite DB in your working folder
conn = sqlite3.connect("ecommerce.db")

# Folder containing your Excel files
data_folder = "data"

# Mapping exact file names to expected table names
file_table_map = {
    "Product-Level Total Sales and Metrics.xlsx": "product_level_total_sales_and_metrics",
    "Product-Level Ad Sales and Metrics.xlsx": "product_level_ad_sales_and_metrics",
    "Product-Level Eligibility Table.xlsx": "product_level_eligibility_table"
}

for file in os.listdir(data_folder):
    if file.endswith(".xlsx"):
        file_path = os.path.join(data_folder, file)
        df = pd.read_excel(file_path)
        table_name = file_table_map.get(file)
        if table_name:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"[INFO] Loaded {table_name} from {file}")
        else:
            print(f"[WARNING] {file} is not recognized, skipping.")

conn.close()
print("[INFO] Database setup completed.")
