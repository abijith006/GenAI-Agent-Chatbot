import os
USE_MOCK = False  # Set True for offline demo fallback
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAkJAgISTkpj9gqKloxzuXwqN0ONtEq29g")

if not USE_MOCK:
    import google.generativeai as genai
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

def question_to_sql(question):
    if USE_MOCK:
        print("[INFO] Using MOCK mode for:", question)
        q = question.lower()
        if "total sales" in q:
            return "SELECT SUM(total_sales) AS total_sales FROM product_level_total_sales_and_metrics;"
        elif "roas" in q:
            return "SELECT SUM(ad_sales) * 1.0 / SUM(ad_spend) AS roas FROM product_level_ad_sales_and_metrics;"
        elif "highest ad spend" in q:
            return "SELECT item_id, ad_spend FROM product_level_ad_sales_and_metrics ORDER BY ad_spend DESC LIMIT 1;"
        elif "chart" in q or "graph" in q:
            return "SELECT date, SUM(total_sales) AS total_sales FROM product_level_total_sales_and_metrics GROUP BY date;"
        else:
            return "-- Mock SQL: Question unrecognized for MOCK"

    prompt = f"""
You are an SQL generator for SQLite.

Available tables and columns:

1) product_level_total_sales_and_metrics
   - date
   - item_id
   - total_sales
   - total_units_ordered

2) product_level_ad_sales_and_metrics
   - date
   - item_id
   - ad_sales
   - impressions
   - ad_spend
   - clicks
   - units_sold

3) product_level_eligibility_table
   - eligibility_datetime_utc
   - item_id
   - eligibility
   - message

STRICT INSTRUCTIONS:
- Use EXACT table and column names as above without typos.
- Do NOT add or remove 's' in table names.
- Do NOT pluralize, singularize, or abbreviate names.
- If asked for ROAS (Return on Ad Spend), generate:
  SELECT SUM(ad_sales) * 1.0 / SUM(ad_spend) AS roas FROM product_level_ad_sales_and_metrics;
- If asked for charts or graphs, generate queries that return (date, numeric_value) pairs suitable for plotting.

Return ONLY the SQL query without explanation or markdown.

Question: {question}
"""

    try:
        print("[INFO] Sending prompt to Gemini for SQL generation...")
        response = model.generate_content(prompt)
        sql = response.text.strip().strip("```sql").strip("```")
        print("[INFO] Generated SQL from Gemini:\n", sql)
        return sql
    except Exception as e:
        print("[ERROR] Gemini call failed:", e)
        return f"-- Gemini call failed: {e}"
