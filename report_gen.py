import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os

def generate_monthly_report():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    current_month = datetime.datetime.now().strftime("%Y-%m")
    monthly_data = [row for row in rows if row[0].startswith(current_month)]

    if not monthly_data:
        return False, "No data found for this month."

    summary = {}
    total = 0
    for _, category, amount in monthly_data:
        summary[category] = summary.get(category, 0) + amount
        total += amount

    labels = list(summary.keys())
    values = list(summary.values())

    plt.figure(figsize=(6,6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(f'Expense Breakdown - {current_month}')
    chart_file = 'monthly_chart.png'
    plt.savefig(chart_file)
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"Expense Report - {current_month}", ln=1, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for category, amount in summary.items():
        pdf.cell(200, 10, txt=f"{category}: Rs. {amount:.2f}", ln=1)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total: Rs. {total:.2f}", ln=1)

    pdf.image(chart_file, x=50, y=pdf.get_y()+10, w=100)
    output_file = f"Expense_Report_{current_month}.pdf"
    pdf.output(output_file)

    os.remove(chart_file)  

    return True, output_file
