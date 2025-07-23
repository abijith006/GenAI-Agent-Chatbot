import plotly.express as px
import pandas as pd

def generate_sales_chart(data):
    # data: list of tuples (date, total_sales)
    df = pd.DataFrame(data, columns=['date', 'total_sales'])
    fig = px.line(df, x='date', y='total_sales', title='Daily Sales')
    fig.write_html('sales_chart.html')
    return 'sales_chart.html'
