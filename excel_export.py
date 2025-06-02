import openpyxl
from db import fetch_expenses
from datetime import datetime
import os
def export_to_excel():
    expenses = fetch_expenses()
    if not expenses:
        return False, "No expenses to export!"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"

    headers = ["Date", "Category", "Amount", "Description"]
    ws.append(headers)

    for row in expenses:
        ws.append(row[1:])  

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"SmartSpend_Report_{now}.xlsx"
    save_path = os.path.join(os.getcwd(), filename)

    wb.save(save_path)
    return True, save_path
