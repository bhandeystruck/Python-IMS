# alerts.py
from ..db.models import check_low_stock

def low_stock_alerts():
    low_stock_items = check_low_stock()
    if low_stock_items:
        print("Low stock alert for items:")
        for item in low_stock_items:
            print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
