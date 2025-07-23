import sqlite3
from llm_utils import question_to_sql

# Optional: For generating charts
import plotly.express as px
import pandas as pd

def generate_chart(data, columns, filename="chart.html", title="Chart"):
    df = pd.DataFrame(data, columns=columns)
    fig = px.bar(df, x=columns[0], y=columns[1], title=title)
    fig.write_html(filename)
    return filename

def process_question(question):
    sql_query = question_to_sql(question)
    print("[INFO] Generated SQL:\n", sql_query)

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No data found for your query."

        # Check if the user wants a chart
        if "chart" in question.lower() or "graph" in question.lower() or "visual" in question.lower():
            filename = generate_chart(rows, columns, title=question)
            return f"Chart generated: {filename} (Open this file to view the chart)"

        # Build a clean string response
        result = ""
        for row in rows:
            result += ", ".join(f"{col}: {val}" for col, val in zip(columns, row)) + "\n"
        return result.strip()

    except Exception as e:
        conn.close()
        print("[ERROR] SQL execution error:", e)
        return f"Error: {e}"
