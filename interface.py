import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import database
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys
import os

# Inicializar o banco de dados
database.create_tables()

# Variáveis globais
root = tk.Tk()
root.title("Sistema de Compras")
root.geometry("800x600")

# Carregar o logotipo como fundo
def load_background():
    try:
        # Determina o caminho base dependendo se é executável ou script
        if getattr(sys, 'frozen', False):
            # Se for um executável PyInstaller, o caminho está no diretório do executável
            base_path = sys._MEIPASS
        else:
            # Se for um script, usa o diretório atual
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Caminho completo para o arquivo Logo.jpg
        logo_path = os.path.join(base_path, "Logo.jpg")
        
        # Carrega a imagem e ajusta ao tamanho da janela
        img = Image.open(logo_path)
        img = img.resize((800, 600), Image.Resampling.LANCZOS)  # Ajusta ao tamanho da janela
        background_image = ImageTk.PhotoImage(img)
        
        # Cria um label com a imagem de fundo
        background_label = tk.Label(root, image=background_image)
        background_label.image = background_image  # Mantém referência para evitar garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche a janela toda
    except Exception as e:
        messagebox.showwarning("Aviso", f"Erro ao carregar o logotipo: {e}. Continuando sem fundo.")

# Funções da interface
def add_item():
    description = entry_description.get()
    code = entry_code.get()
    supplier = entry_supplier.get()
    price = entry_price.get()
    if not description or not code or not supplier or not price:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    status = "A Comprar"
    suppliers_prices = {supplier: float(price)}
    database.insert_item(description, code, status, suppliers_prices)
    update_item_list()
    clear_entries()

def update_item_list(items=None):
    list_items.delete(0, tk.END)
    if items is None:
        items = database.get_all_items()
    for item in items:
        item_text = f"{item[1]} - {item[2]} - {item[3]}"
        list_items.insert(tk.END, item_text)
        if item[3] == "A Comprar":
            list_items.itemconfig(tk.END, {'fg': 'red'})
        elif item[3] == "Comprado":
            list_items.itemconfig(tk.END, {'fg': 'green'})
        elif item[3] == "Parcialmente Comprado":
            list_items.itemconfig(tk.END, {'fg': 'orange'})

def clear_entries():
    entry_description.delete(0, tk.END)
    entry_code.delete(0, tk.END)
    entry_supplier.delete(0, tk.END)
    entry_price.delete(0, tk.END)

def mark_as_purchased():
    selected = list_items.curselection()
    if not selected:
        messagebox.showerror("Erro", "Selecione um item!")
        return
    item_id = database.get_all_items()[selected[0]][0]
    item = database.get_all_items()[selected[0]]
    database.update_item(item_id, item[1], item[2], "Comprado", item[4])
    update_item_list()

def mark_as_partially_purchased():
    selected = list_items.curselection()
    if not selected:
        messagebox.showerror("Erro", "Selecione um item!")
        return
    item_id = database.get_all_items()[selected[0]][0]
    item = database.get_all_items()[selected[0]]
    database.update_item(item_id, item[1], item[2], "Parcialmente Comprado", item[4])
    update_item_list()

def filter_items():
    status = combo_status.get()
    supplier = combo_supplier.get()
    if status and not supplier:
        items = database.get_items_by_status(status)
    elif supplier and not status:
        items = database.get_items_by_supplier(supplier)
    else:
        items = database.get_all_items()
    update_item_list(items)

def generate_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Itens"
    ws.append(["Descrição", "Código", "Fornecedor", "Preço"])
    items = database.get_all_items()
    for item in items:
        for supplier, price in item[4].items():
            ws.append([item[1], item[2], supplier, ""])
    wb.save("itens.xlsx")
    messagebox.showinfo("Sucesso", "Planilha gerada como 'itens.xlsx'")

def import_excel():
    try:
        wb = openpyxl.load_workbook("itens_preenchidos.xlsx")
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            description, code, supplier, price = row
            items = database.get_all_items()
            for item in items:
                if item[1] == description and item[2] == code:
                    suppliers_prices = item[4]
                    suppliers_prices[supplier] = float(price) if price else 0
                    database.update_item(item[0], item[1], item[2], item[3], suppliers_prices)
        update_item_list()
        messagebox.showinfo("Sucesso", "Preços atualizados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar planilha: {e}")

def generate_pdf():
    company = database.get_company()
    if not company:
        messagebox.showerror("Erro", "Cadastre a empresa primeiro!")
        return
    selected = list_items.curselection()
    if not selected:
        messagebox.showerror("Erro", "Selecione um item para gerar o pedido!")
        return
    item = database.get_all_items()[selected[0]]
    order_number = len(database.get_all_items()) + 1
    c = canvas.Canvas(f"pedido_{order_number}.pdf", pagesize=letter)
    c.drawString(100, 750, f"Pedido #{order_number}")
    c.drawString(100, 730, f"Empresa: {company[1]} - CNPJ: {company[2]}")
    c.drawString(100, 710, f"Comprador: {company[3]}")
    c.drawString(100, 690, f"Item: {item[1]} - Código: {item[2]}")
    c.drawString(100, 670, "Fornecedores e Preços:")
    y = 650
    for supplier, price in item[4].items():
        c.drawString(100, y, f"{supplier}: R${price:.2f}")
        y -= 20
    c.save()
    messagebox.showinfo("Sucesso", f"Pedido gerado como 'pedido_{order_number}.pdf'")

def register_company():
    name = entry_company_name.get()
    cnpj = entry_company_cnpj.get()
    buyer_name = entry_buyer_name.get()
    if not name or not cnpj or not buyer_name:
        messagebox.showerror("Erro", "Preencha todos os campos da empresa!")
        return
    database.insert_company(name, cnpj, buyer_name)
    messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")
    company_window.destroy()

def register_supplier():
    name = entry_supplier_name.get()
    cnpj = entry_supplier_cnpj.get()
    seller_name = entry_seller_name.get()
    if not name or not cnpj or not seller_name:
        messagebox.showerror("Erro", "Preencha todos os campos do fornecedor!")
        return
    database.insert_supplier(name, cnpj, seller_name)
    messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
    supplier_window.destroy()
    combo_supplier['values'] = database.get_suppliers()

def open_company_window():
    global company_window, entry_company_name, entry_company_cnpj, entry_buyer_name
    company_window = tk.Toplevel(root)
    company_window.title("Cadastrar Empresa")
    tk.Label(company_window, text="Nome:").pack()
    entry_company_name = tk.Entry(company_window)
    entry_company_name.pack()
    tk.Label(company_window, text="CNPJ:").pack()
    entry_company_cnpj = tk.Entry(company_window)
    entry_company_cnpj.pack()
    tk.Label(company_window, text="Nome do Comprador:").pack()
    entry_buyer_name = tk.Entry(company_window)
    entry_buyer_name.pack()
    tk.Button(company_window, text="Cadastrar", command=register_company).pack()

def open_supplier_window():
    global supplier_window, entry_supplier_name, entry_supplier_cnpj, entry_seller_name
    supplier_window = tk.Toplevel(root)
    supplier_window.title("Cadastrar Fornecedor")
    tk.Label(supplier_window, text="Nome:").pack()
    entry_supplier_name = tk.Entry(supplier_window)
    entry_supplier_name.pack()
    tk.Label(supplier_window, text="CNPJ:").pack()
    entry_supplier_cnpj = tk.Entry(supplier_window)
    entry_supplier_cnpj.pack()
    tk.Label(supplier_window, text="Nome do Vendedor:").pack()
    entry_seller_name = tk.Entry(supplier_window)
    entry_seller_name.pack()
    tk.Button(supplier_window, text="Cadastrar", command=register_supplier).pack()

# Carregar o fundo ao iniciar
load_background()

# Interface gráfica
tk.Label(root, text="Descrição:", bg="white").pack()
entry_description = tk.Entry(root)
entry_description.pack()

tk.Label(root, text="Código:", bg="white").pack()
entry_code = tk.Entry(root)
entry_code.pack()

tk.Label(root, text="Fornecedor:", bg="white").pack()
entry_supplier = tk.Entry(root)
entry_supplier.pack()

tk.Label(root, text="Preço:", bg="white").pack()
entry_price = tk.Entry(root)
entry_price.pack()

tk.Button(root, text="Adicionar Item", command=add_item).pack()

# Lista de itens
list_items = tk.Listbox(root, height=15, width=50)
list_items.pack()
update_item_list()

# Botões de gerenciamento
tk.Button(root, text="Marcar como Comprado", command=mark_as_purchased).pack()
tk.Button(root, text="Marcar como Parcialmente Comprado", command=mark_as_partially_purchased).pack()

# Filtros
tk.Label(root, text="Filtrar por Status:", bg="white").pack()
combo_status = ttk.Combobox(root, values=["A Comprar", "Comprado", "Parcialmente Comprado"])
combo_status.pack()

tk.Label(root, text="Filtrar por Fornecedor:", bg="white").pack()
combo_supplier = ttk.Combobox(root, values=database.get_suppliers())
combo_supplier.pack()

tk.Button(root, text="Filtrar", command=filter_items).pack()

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

cadastro_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Cadastro", menu=cadastro_menu)
cadastro_menu.add_command(label="Cadastrar Empresa", command=open_company_window)
cadastro_menu.add_command(label="Cadastrar Fornecedor", command=open_supplier_window)

compras_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Compras", menu=compras_menu)
compras_menu.add_command(label="Gerar Planilha Excel", command=generate_excel)
compras_menu.add_command(label="Importar Planilha Preenchida", command=import_excel)
compras_menu.add_command(label="Gerar Pedido em PDF", command=generate_pdf)

root.mainloop()