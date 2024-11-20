# report_generator.py
import pandas as pd
from ..db.database import get_connection

def generate_report():
    with get_connection() as conn:
        items_df = pd.read_sql_query("SELECT * FROM items", conn)
        transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
        items_df.to_csv('data/reports/inventory_report.csv', index=False)
        transactions_df.to_csv('data/reports/transaction_log.csv', index=False)
    print("Reports generated as CSV files.")
