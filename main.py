import json
import os
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

DATA_FILE = "expenses.json"

# Загрузка данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Трекер расходов")
        self.root.geometry("900x600")
        self.data = load_data()

        # ========== Поля ввода ==========
        input_frame = LabelFrame(root, text="Добавить расход", padx=10, pady=10)
        input_frame.pack(fill=X, padx=10, pady=5)

        Label(input_frame, text="Сумма (₽):").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Категория:").grid(row=0, column=2, padx=5, pady=5)
        self.category_var = StringVar(value="еда")
        self.category_menu = ttk.Combobox(input_frame, textvariable=self.category_var,
                                          values=["еда", "транспорт", "развлечения", "коммунальные", "здоровье", "другое"],
                                          width=15, state="readonly")
        self.category_menu.grid(row=0, column=3, padx=5, pady=5)

        Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
        self.date_entry = Entry(input_frame, width=12)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        Button(input_frame, text="➕ Добавить расход", command=self.add_expense, bg="lightgreen").grid(row=0, column=6, padx=10, pady=5)

        # ========== Фильтры ==========
        filter_frame = LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill=X, padx=10, pady=5)

        Label(filter_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_category = StringVar(value="все")
        ttk.Combobox(filter_frame, textvariable=self.filter_category,
                     values=["все", "еда", "транспорт", "развлечения", "коммунальные", "здоровье", "другое"],
                     width=15, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        Label(filter_frame, text="Дата от (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.date_from = Entry(filter_frame, width=12)
        self.date_from.grid(row=0, column=3, padx=5, pady=5)

        Label(filter_frame, text="Дата до (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
        self.date_to = Entry(filter_frame, width=12)
        self.date_to.grid(row=0, column=5, padx=5, pady=5)

        Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter, bg="lightyellow").grid(row=0, column=6, padx=10, pady=5)
        Button(filter_frame, text="🔄 Сбросить фильтр", command=self.reset_filter, bg="lightgray").grid(row=0, column=7, padx=5, pady=5)

        # ========== Сумма за период ==========
        sum_frame = Frame(root)
        sum_frame.pack(fill=X, padx=10, pady=5)
        Button(sum_frame, text="💰 Подсчитать сумму за период", command=self.calc_sum, bg="lightblue").pack(side=LEFT, padx=5)
        self.sum_label = Label(sum_frame, text="Сумма: 0 ₽", font=("Arial", 12, "bold"), fg="green")
        self.sum_label.pack(side=LEFT, padx=20)

        # ========== Таблица с расходами ==========
        table_frame = Frame(root)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Сумма", "Категория", "Дата"), show="headings", height=15)
        self.tree.heading("ID", text="№")
        self.tree.heading("Сумма", text="Сумма (₽)")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")

        self.tree.column("ID", width=40)
        self.tree.column("Сумма", width=100)
        self.tree.column("Категория", width=120)
        self.tree.column("Дата", width=100)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True)

        # Кнопка удаления
        Button(root, text="🗑 Удалить выбранную запись", command=self.delete_expense, bg="lightcoral").pack(pady=5)

        self.display_data(self.data)

    # Валидация и добавление
    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()
        date = self.date_entry.get().strip()

        if not amount:
            messagebox.showerror("Ошибка", "Введите сумму!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return

        expense = {
            "id": len(self.data) + 1,
            "amount": amount,
            "category": category,
            "date": date
        }
        self.data.append(expense)
        save_data(self.data)
        self.display_data(self.data)
        self.amount_entry.delete(0, END)
        messagebox.showinfo("Успех", f"Расход {amount}₽ добавлен!")

    def display_data(self, records):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in records:
            self.tree.insert("", END, values=(r["id"], r["amount"], r["category"], r["date"]))

    def apply_filter(self):
        filtered = self.data.copy()
        category = self.filter_category.get()
        date_from = self.date_from.get().strip()
        date_to = self.date_to.get().strip()

        if category != "все":
            filtered = [e for e in filtered if e["category"] == category]

        if date_from:
            try:
                datetime.strptime(date_from, "%Y-%m-%d")
                filtered = [e for e in filtered if e["date"] >= date_from]
            except:
                messagebox.showerror("Ошибка", "Неверный формат даты 'от'!")
                return

        if date_to:
            try:
                datetime.strptime(date_to, "%Y-%m-%d")
                filtered = [e for e in filtered if e["date"] <= date_to]
            except:
                messagebox.showerror("Ошибка", "Неверный формат даты 'до'!")
                return

        self.display_data(filtered)
        self.calc_sum_for_list(filtered)

    def reset_filter(self):
        self.filter_category.set("все")
        self.date_from.delete(0, END)
        self.date_to.delete(0, END)
        self.display_data(self.data)
        self.calc_sum()

    def calc_sum(self):
        self.calc_sum_for_list(self.get_current_list())

    def calc_sum_for_list(self, records):
        total = sum(e["amount"] for e in records)
        self.sum_label.config(text=f"Сумма: {total} ₽")

    def get_current_list(self):
        items = self.tree.get_children()
        records = []
        for item in items:
            values = self.tree.item(item)["values"]
            records.append({"amount": values[1]})
        return records

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись для удаления!")
            return

        item = selected[0]
        values = self.tree.item(item)["values"]
        expense_id = values[0]

        self.data = [e for e in self.data if e["id"] != expense_id]
        # Перенумеровка ID
        for i, e in enumerate(self.data):
            e["id"] = i + 1

        save_data(self.data)
        self.apply_filter()
        messagebox.showinfo("Успех", "Запись удалена!")

# Запуск
if __name__ == "__main__":
    root = Tk()
    app = ExpenseApp(root)
    root.mainloop()