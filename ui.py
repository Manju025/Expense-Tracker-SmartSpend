import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from db import insert_expense, fetch_expenses
from report_gen import generate_monthly_report
from excel_export import export_to_excel


def start_gui():
    root = tk.Tk()
    root.title("SmartSpend - Expense Tracker 💸")
    root.geometry("800x650")
    root.configure(bg="#f4f4f4")

    tk.Label(root, text="Date (YYYY-MM-DD)", bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    date_var = tk.StringVar()
    tk.Entry(root, textvariable=date_var, width=30).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Category", bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    category_var = tk.StringVar()
    tk.Entry(root, textvariable=category_var, width=30).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Amount", bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    amount_var = tk.StringVar()
    tk.Entry(root, textvariable=amount_var, width=30).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Description", bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    desc_var = tk.StringVar()
    tk.Entry(root, textvariable=desc_var, width=30).grid(row=3, column=1, padx=10, pady=5)
    
    # ---- FILTER AREA ----
    tk.Label(root, text="🔍 Filters", bg="#f4f4f4", font=("Arial", 12, "bold")).grid(row=6, column=0, pady=10)

    tk.Label(root, text="Date (YYYY-MM-DD)", bg="#f4f4f4").grid(row=7, column=0, sticky="w", padx=10)
    filter_date_var = tk.StringVar()
    tk.Entry(root, textvariable=filter_date_var, width=20).grid(row=7, column=1, padx=5)

    tk.Label(root, text="Category", bg="#f4f4f4").grid(row=8, column=0, sticky="w", padx=10)
    filter_category_var = tk.StringVar()
    tk.Entry(root, textvariable=filter_category_var, width=20).grid(row=8, column=1, padx=5)

    tk.Label(root, text="Min Amount", bg="#f4f4f4").grid(row=7, column=2, sticky="w", padx=10)
    min_amount_var = tk.StringVar()
    tk.Entry(root, textvariable=min_amount_var, width=15).grid(row=7, column=3, padx=5)

    tk.Label(root, text="Max Amount", bg="#f4f4f4").grid(row=8, column=2, sticky="w", padx=10)
    max_amount_var = tk.StringVar()
    tk.Entry(root, textvariable=max_amount_var, width=15).grid(row=8, column=3, padx=5)

    def clear_fields():
        date_var.set("")
        category_var.set("")
        amount_var.set("")
        desc_var.set("")
        min_amount_var.set("")
        max_amount_var.set("")
        filter_date_var.set("")
        filter_category_var.set("")

    def add_expense():
        try:
            date = date_var.get()
            category = category_var.get()
            amount = float(amount_var.get())
            description = desc_var.get()

            insert_expense(date, category, amount, description)
            messagebox.showinfo("Success", "Expense added successfully!")
            clear_fields()
            refresh_table()
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="➕ Add Expense", command=add_expense, bg="#007bff", fg="white", width=20)\
        .grid(row=4, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Description"), show='headings', height=10)
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.heading("Description", text="Description")
    tree.column("Date", width=100)
    tree.column("Category", width=100)
    tree.column("Amount", width=80)
    tree.column("Description", width=200)

    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def refresh_table():
        for i in tree.get_children():
            tree.delete(i)
        for row in fetch_expenses():
            tree.insert("", "end", values=row[1:])

    refresh_table()

    def filter_expenses():
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if filter_date_var.get():
            query += " AND date = ?"
            params.append(filter_date_var.get())

        if filter_category_var.get():
            query += " AND category LIKE ?"
            params.append(f"%{filter_category_var.get()}%")

        if min_amount_var.get():
            query += " AND amount >= ?"
            try:
                params.append(float(min_amount_var.get()))
            except:
                messagebox.showerror("Invalid Input", "Min amount must be a number.")
                return

        if max_amount_var.get():
            query += " AND amount <= ?"
            try:
                params.append(float(max_amount_var.get()))
            except:
                messagebox.showerror("Invalid Input", "Max amount must be a number.")
                return

        try:
            conn = sqlite3.connect("expenses.db")
            c = conn.cursor()
            c.execute(query, params)
            rows = c.fetchall()
            conn.close()

            tree.delete(*tree.get_children())
            for row in rows:
                tree.insert("", "end", values=row[1:])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="🔎 Filter Expenses", command=filter_expenses, bg="#6c757d", fg="white", width=20)\
        .grid(row=9, column=0, columnspan=4, pady=10)

    def export_report():
        success, message = generate_monthly_report()
        if success:
            messagebox.showinfo("Report Created", f"PDF saved: {message}")
        else:
            messagebox.showinfo("No Data", message)
        
    def export_excel():
        success, message = export_to_excel()
        if success:
            messagebox.showinfo("Excel Exported", f"File saved at:\n{message}")
        else:
            messagebox.showwarning("Export Failed", message)

    tk.Button(root, text="📊 Generate Monthly Report", command=export_report, bg="green", fg="white", width=30)\
        .grid(row=10, column=0, columnspan=4, pady=20)
        
    tk.Button(root, text="📤 Export to Excel", command=export_excel, bg="#ffa500", fg="black", width=30)\
        .grid(row=11, column=0, columnspan=4, pady=5)


    root.mainloop()
