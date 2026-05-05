import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
# main
DATA_FILE = "expenses.json"
expenses = []

def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Дата должна быть YYYY-MM-DD")
        return

    expenses.append({
        "amount": amount,
        "category": category,
        "date": date
    })

    save_data()
    refresh_table()


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    for e in expenses:
        tree.insert("", tk.END, values=(e["amount"], e["category"], e["date"]))


def apply_filter():
    category = filter_category.get()
    from_date_val = from_date.get()
    to_date_val = to_date.get()

    filtered = expenses

    if category:
        filtered = [e for e in filtered if e["category"] == category]

    try:
        if from_date_val:
            fd = datetime.strptime(from_date_val, "%Y-%m-%d")
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") >= fd]

        if to_date_val:
            td = datetime.strptime(to_date_val, "%Y-%m-%d")
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") <= td]
    except:
        messagebox.showerror("Ошибка", "Неверная дата")
        return

    show_filtered(filtered)


def show_filtered(data):
    for row in tree.get_children():
        tree.delete(row)

    for e in data:
        tree.insert("", tk.END, values=(e["amount"], e["category"], e["date"]))


def calculate_total():
    total = sum(e["amount"] for e in expenses)
    total_label.config(text=f"Сумма: {total}")


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)


def load_data():
    global expenses
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            expenses = json.load(f)


# GUI

root = tk.Tk()
root.title("Expense Tracker")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Сумма").grid(row=0, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1)

tk.Label(frame, text="Категория").grid(row=1, column=0)
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1)

tk.Label(frame, text="Дата (YYYY-MM-DD)").grid(row=2, column=0)
date_entry = tk.Entry(frame)
date_entry.grid(row=2, column=1)

tk.Button(frame, text="Добавить расход", command=add_expense).grid(row=3, columnspan=2)

tree = ttk.Treeview(root, columns=("amount", "category", "date"), show="headings")
tree.heading("amount", text="Сумма")
tree.heading("category", text="Категория")
tree.heading("date", text="Дата")
tree.pack()

filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Категория").grid(row=0, column=0)
filter_category = tk.Entry(filter_frame)
filter_category.grid(row=0, column=1)

tk.Label(filter_frame, text="С даты").grid(row=1, column=0)
from_date = tk.Entry(filter_frame)
from_date.grid(row=1, column=1)

tk.Label(filter_frame, text="По дату").grid(row=2, column=0)
to_date = tk.Entry(filter_frame)
to_date.grid(row=2, column=1)

tk.Button(filter_frame, text="Фильтр", command=apply_filter).grid(row=3, columnspan=2)
tk.Button(filter_frame, text="Сброс", command=refresh_table).grid(row=4, columnspan=2)

total_label = tk.Label(root, text="Сумма: 0")
total_label.pack()

tk.Button(root, text="Подсчитать", command=calculate_total).pack()

# start
load_data()
refresh_table()

root.mainloop()