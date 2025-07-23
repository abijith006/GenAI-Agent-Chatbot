import pandas as pd

# Paths to your actual uploaded files
files = [
    "data/Product-Level Total Sales and Metrics.xlsx",
    "data/Product-Level Ad Sales and Metrics.xlsx",
    "data/Product-Level Eligibility Table.xlsx"
]

for file in files:
    df = pd.read_excel(file)
    print(f"\n {file}")
    print(df.columns)
