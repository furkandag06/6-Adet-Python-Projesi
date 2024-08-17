import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
import sqlite3

# Veritabanı oluşturma
def create_database():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY,
            amount REAL,
            source TEXT,
            date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value REAL
        )
    ''')
    conn.commit()
    conn.close()

# JSON dosyasına veri kaydetme
def save_data(data, filename='finances.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# JSON dosyasından veri okuma
def load_data(filename='finances.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        return {"income": [], "expenses": [], "budget": 0.0}

# Veritabanına veri ekleme
def insert_income(amount, source, date):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('INSERT INTO income (amount, source, date) VALUES (?, ?, ?)', (amount, source, date))
    conn.commit()
    conn.close()

def insert_expense(amount, category, date):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)', (amount, category, date))
    conn.commit()
    conn.close()

def get_income():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('SELECT * FROM income')
    rows = c.fetchall()
    conn.close()
    return rows

def get_expenses():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    conn.close()
    return rows

def get_budget():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = "budget"')
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0.0

def set_budget(budget):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('REPLACE INTO settings (key, value) VALUES ("budget", ?)', (budget,))
    conn.commit()
    conn.close()

# Veriyi doğrulama
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Gelir ekleme
def add_income(data):
    amount = simpledialog.askfloat("Gelir Ekle", "Gelir miktarını girin:", minvalue=0.0)
    if amount is None:
        return
    
    source = simpledialog.askstring("Gelir Ekle", "Gelirin kaynağını girin:")
    date = simpledialog.askstring("Gelir Ekle", "Tarihi girin (YYYY-MM-DD) veya boş bırakın (bugün):") or str(datetime.today().date())
    
    if not validate_date(date):
        date = str(datetime.today().date())
    
    income = {"amount": amount, "source": source, "date": date}
    data["income"].append(income)
    insert_income(amount, source, date)
    save_data(data)
    messagebox.showinfo("Başarılı", "Gelir başarıyla eklendi.")

# Gider ekleme
def add_expense(data):
    amount = simpledialog.askfloat("Gider Ekle", "Gider miktarını girin:", minvalue=0.0)
    if amount is None:
        return
    
    category = simpledialog.askstring("Gider Ekle", "Gider kategorisini girin:")
    date = simpledialog.askstring("Gider Ekle", "Tarihi girin (YYYY-MM-DD) veya boş bırakın (bugün):") or str(datetime.today().date())
    
    if not validate_date(date):
        date = str(datetime.today().date())
    
    expense = {"amount": amount, "category": category, "date": date}
    data["expenses"].append(expense)
    insert_expense(amount, category, date)
    save_data(data)
    messagebox.showinfo("Başarılı", "Gider başarıyla eklendi.")

# Gelirleri görüntüleme
def view_income(data):
    output = "\n--- Gelirler ---\n"
    for income in data["income"]:
        output += f"Tarih: {income['date']} - Kaynak: {income['source']} - Miktar: {income['amount']:.2f} TL\n"
    output += "-----------------\n"
    messagebox.showinfo("Gelirler", output)

# Giderleri görüntüleme
def view_expenses(data):
    output = "\n--- Giderler ---\n"
    for expense in data["expenses"]:
        output += f"Tarih: {expense['date']} - Kategori: {expense['category']} - Miktar: {expense['amount']:.2f} TL\n"
    output += "-----------------\n"
    messagebox.showinfo("Giderler", output)

# Harcamaların analizi
def analyze_expenses(data):
    start_date = simpledialog.askstring("Harcamaları Analiz Et", "Başlangıç tarihini girin (YYYY-MM-DD):")
    end_date = simpledialog.askstring("Harcamaları Analiz Et", "Bitiş tarihini girin (YYYY-MM-DD):")

    if not (validate_date(start_date) and validate_date(end_date)):
        messagebox.showwarning("Hata", "Geçersiz tarih formatı. Analiz işlemi iptal edildi.")
        return

    total_expense = 0.0
    output = "\n--- Harcama Analizi ---\n"
    for expense in data["expenses"]:
        if start_date <= expense["date"] <= end_date:
            output += f"Tarih: {expense['date']} - Kategori: {expense['category']} - Miktar: {expense['amount']:.2f} TL\n"
            total_expense += expense["amount"]
    output += f"Toplam harcama: {total_expense:.2f} TL\n"
    messagebox.showinfo("Harcama Analizi", output)

# Kategorilere göre harcama raporu
def expense_report_by_category(data):
    categories = {}
    for expense in data["expenses"]:
        category = expense["category"]
        amount = expense["amount"]
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    output = "\n--- Kategori Bazında Harcama Raporu ---\n"
    for category, total in categories.items():
        output += f"Kategori: {category} - Toplam Harcama: {total:.2f} TL\n"
    output += "----------------------------------------\n"
    messagebox.showinfo("Kategori Raporu", output)

# Kategorilere göre harcamaları grafikle göster
def plot_expenses_by_category(data):
    categories = {}
    for expense in data["expenses"]:
        category = expense["category"]
        amount = expense["amount"]
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    plt.figure(figsize=(10, 7))
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Kategori Bazında Harcamalar')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Bütçe belirleme ve takibi
def set_budget(data):
    budget = simpledialog.askfloat("Bütçe Belirle", "Aylık bütçenizi girin:", minvalue=0.0)
    if budget is None:
        return
    
    data["budget"] = budget
    set_budget(budget)
    save_data(data)
    messagebox.showinfo("Başarılı", f"Aylık bütçeniz: {budget:.2f} TL olarak ayarlandı.")

def check_budget(data):
    budget = get_budget()
    if budget == 0:
        messagebox.showwarning("Hata", "Öncelikle bir bütçe belirlemeniz gerekiyor.")
        return
    
    current_month = datetime.today().strftime('%Y-%m')
    total_expense = sum(
        expense["amount"]
        for expense in data["expenses"]
        if expense["date"].startswith(current_month)
    )

    output = f"\n--- Bütçe Kontrolü ---\n"
    output += f"Bu ayki toplam harcamanız: {total_expense:.2f} TL\n"
    output += f"Aylık bütçeniz: {budget:.2f} TL\n"
    output += f"Bütçe durumu: {'Aşıldı' if total_expense > budget else 'Aşılmadı'}\n"
    messagebox.showinfo("Bütçe Kontrolü", output)

# Veriyi CSV'ye aktar
def export_to_csv(data):
    df_income = pd.DataFrame(data["income"])
    df_expenses = pd.DataFrame(data["expenses"])

    df_income.to_csv('income.csv', index=False)
    df_expenses.to_csv('expenses.csv', index=False)
    messagebox.showinfo("Başarılı", "Veriler CSV dosyalarına aktarıldı.")

# CSV'den veri içeri aktarma
def import_data_from_csv(data):
    if os.path.exists('income.csv'):
        df_income = pd.read_csv('income.csv')
        data["income"] = df_income.to_dict(orient='records')
    
    if os.path.exists('expenses.csv'):
        df_expenses = pd.read_csv('expenses.csv')
        data["expenses"] = df_expenses.to_dict(orient='records')
    
    save_data(data)
    messagebox.showinfo("Başarılı", "CSV dosyalarından veriler başarıyla içeri aktarıldı.")

# Ana GUI oluşturma
def create_gui():
    root = tk.Tk()
    root.title("Kişisel Finans Takip Uygulaması")
    create_database()
    
    data = load_data()

    # Menü oluştur
    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu)
    menu.add_cascade(label="Dosya", menu=file_menu)
    file_menu.add_command(label="CSV'ye Aktar", command=lambda: export_to_csv(data))
    file_menu.add_command(label="CSV'den İçeri Aktar", command=lambda: import_data_from_csv(data))
    file_menu.add_separator()
    file_menu.add_command(label="Çıkış", command=root.quit)

    manage_menu = tk.Menu(menu)
    menu.add_cascade(label="Yönetim", menu=manage_menu)
    manage_menu.add_command(label="Gelir Ekle", command=lambda: add_income(data))
    manage_menu.add_command(label="Gider Ekle", command=lambda: add_expense(data))
    manage_menu.add_command(label="Gelirleri Görüntüle", command=lambda: view_income(data))
    manage_menu.add_command(label="Giderleri Görüntüle", command=lambda: view_expenses(data))
    manage_menu.add_command(label="Harcama Analizi", command=lambda: analyze_expenses(data))
    manage_menu.add_command(label="Kategori Raporu", command=lambda: expense_report_by_category(data))
    manage_menu.add_command(label="Kategori Grafik Raporu", command=lambda: plot_expenses_by_category(data))
    manage_menu.add_command(label="Bütçe Belirle", command=lambda: set_budget(data))
    manage_menu.add_command(label="Bütçeyi Kontrol Et", command=lambda: check_budget(data))

    root.mainloop()

create_gui()
