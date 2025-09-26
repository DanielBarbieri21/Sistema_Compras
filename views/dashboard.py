"""
Dashboard do Sistema de Compras
"""
import tkinter as tk
from tkinter import ttk, messagebox

# matplotlib é opcional para permitir ambiente sem numpy
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    matplotlib.use('TkAgg')
    _HAS_MATPLOTLIB = True
except Exception:
    _HAS_MATPLOTLIB = False

from models import ItemRepository, SupplierRepository, CompanyRepository
from services import BackupService


class DashboardView:
    """Classe responsável pela tela de dashboard"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.backup_service = BackupService()
        
        # Configurar matplotlib (se disponível)
        if _HAS_MATPLOTLIB:
            plt.style.use('dark_background')
        
        self.create_widgets()
        self.update_data()
    
    def create_widgets(self):
        """Cria os widgets do dashboard"""
        # Título
        title_label = ttk.Label(
            self.frame, 
            text="📊 Dashboard - Sistema de Compras", 
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # Frame principal com scroll
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame superior com estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="📈 Estatísticas Gerais", padding=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.create_stats_widgets(stats_frame)
        
        # Frame com gráficos (somente se matplotlib disponível)
        charts_frame = ttk.LabelFrame(main_frame, text="📊 Gráficos", padding=10)
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        if _HAS_MATPLOTLIB:
            self.create_charts_widgets(charts_frame)
        else:
            ttk.Label(charts_frame, text="Gráficos desativados (matplotlib não instalado)").pack(pady=10)
        
        # Frame inferior com informações do sistema
        system_frame = ttk.LabelFrame(main_frame, text="🔧 Informações do Sistema", padding=10)
        system_frame.pack(fill=tk.X, pady=5)
        
        self.create_system_widgets(system_frame)
    
    def create_stats_widgets(self, parent):
        """Cria os widgets de estatísticas"""
        # Grid para as estatísticas
        stats_grid = ttk.Frame(parent)
        stats_grid.pack(fill=tk.X)
        
        # Estatísticas dos itens
        self.total_items_var = tk.StringVar(value="0")
        self.items_to_buy_var = tk.StringVar(value="0")
        self.items_purchased_var = tk.StringVar(value="0")
        self.items_partial_var = tk.StringVar(value="0")
        self.total_value_var = tk.StringVar(value="R$ 0,00")
        
        # Total de itens
        ttk.Label(stats_grid, text="Total de Itens:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_grid, textvariable=self.total_items_var, font=('Arial', 12, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Itens a comprar
        ttk.Label(stats_grid, text="A Comprar:").grid(row=0, column=2, sticky=tk.W, padx=5)
        ttk.Label(stats_grid, textvariable=self.items_to_buy_var, font=('Arial', 12, 'bold'), foreground='red').grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Itens comprados
        ttk.Label(stats_grid, text="Comprados:").grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_grid, textvariable=self.items_purchased_var, font=('Arial', 12, 'bold'), foreground='green').grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Itens parciais
        ttk.Label(stats_grid, text="Parciais:").grid(row=1, column=2, sticky=tk.W, padx=5)
        ttk.Label(stats_grid, textvariable=self.items_partial_var, font=('Arial', 12, 'bold'), foreground='orange').grid(row=1, column=3, sticky=tk.W, padx=5)
        
        # Valor total
        ttk.Label(stats_grid, text="Valor Total:").grid(row=2, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_grid, textvariable=self.total_value_var, font=('Arial', 12, 'bold'), foreground='blue').grid(row=2, column=1, sticky=tk.W, padx=5)
    
    def create_charts_widgets(self, parent):
        """Cria os widgets dos gráficos"""
        # Frame para os gráficos
        charts_container = ttk.Frame(parent)
        charts_container.pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de status dos itens
        self.create_status_chart(charts_container)
        
        # Gráfico de fornecedores
        self.create_suppliers_chart(charts_container)
    
    def create_status_chart(self, parent):
        """Cria o gráfico de status dos itens"""
        # Frame para o gráfico de status
        status_frame = ttk.Frame(parent)
        status_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(status_frame, text="Status dos Itens", font=('Arial', 10, 'bold')).pack()
        
        # Criar figura do matplotlib
        self.status_fig, self.status_ax = plt.subplots(figsize=(4, 3))
        self.status_canvas = FigureCanvasTkAgg(self.status_fig, status_frame)
        self.status_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_suppliers_chart(self, parent):
        """Cria o gráfico de fornecedores"""
        # Frame para o gráfico de fornecedores
        suppliers_frame = ttk.Frame(parent)
        suppliers_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(suppliers_frame, text="Fornecedores", font=('Arial', 10, 'bold')).pack()
        
        # Criar figura do matplotlib
        self.suppliers_fig, self.suppliers_ax = plt.subplots(figsize=(4, 3))
        self.suppliers_canvas = FigureCanvasTkAgg(self.suppliers_fig, suppliers_frame)
        self.suppliers_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_system_widgets(self, parent):
        """Cria os widgets de informações do sistema"""
        # Grid para informações do sistema
        system_grid = ttk.Frame(parent)
        system_grid.pack(fill=tk.X)
        
        # Informações do backup
        backup_info = self.backup_service.get_backup_info()
        
        self.backup_status_var = tk.StringVar(value="✅ Ativo" if backup_info['automatic_backup_running'] else "❌ Inativo")
        self.total_backups_var = tk.StringVar(value=str(backup_info['total_backups']))
        self.latest_backup_var = tk.StringVar(value="Nenhum" if not backup_info['latest_backup'] else backup_info['latest_backup']['created'].strftime('%d/%m/%Y %H:%M'))
        
        # Status do backup
        ttk.Label(system_grid, text="Backup Automático:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(system_grid, textvariable=self.backup_status_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Total de backups
        ttk.Label(system_grid, text="Total de Backups:").grid(row=0, column=2, sticky=tk.W, padx=5)
        ttk.Label(system_grid, textvariable=self.total_backups_var).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Último backup
        ttk.Label(system_grid, text="Último Backup:").grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Label(system_grid, textvariable=self.latest_backup_var).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Botões de ação
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="🔄 Atualizar", command=self.update_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="💾 Criar Backup", command=self.create_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📋 Ver Backups", command=self.show_backups).pack(side=tk.LEFT, padx=5)
    
    def update_data(self):
        """Atualiza os dados do dashboard"""
        try:
            # Atualizar estatísticas dos itens
            item_stats = ItemRepository.get_statistics()
            
            self.total_items_var.set(str(item_stats['total_items']))
            self.items_to_buy_var.set(str(item_stats['items_to_buy']))
            self.items_purchased_var.set(str(item_stats['items_purchased']))
            self.items_partial_var.set(str(item_stats['items_partial']))
            self.total_value_var.set(f"R$ {item_stats['total_value']:,.2f}")
            
            # Atualizar gráficos se disponíveis
            if _HAS_MATPLOTLIB:
                self.update_status_chart(item_stats['status_counts'])
                self.update_suppliers_chart()
            
            # Atualizar informações do sistema
            backup_info = self.backup_service.get_backup_info()
            self.backup_status_var.set("✅ Ativo" if backup_info['automatic_backup_running'] else "❌ Inativo")
            self.total_backups_var.set(str(backup_info['total_backups']))
            
            if backup_info['latest_backup']:
                self.latest_backup_var.set(backup_info['latest_backup']['created'].strftime('%d/%m/%Y %H:%M'))
            else:
                self.latest_backup_var.set("Nenhum")
                
        except Exception as e:
            print(f"Erro ao atualizar dashboard: {e}")
    
    def update_status_chart(self, status_counts):
        """Atualiza o gráfico de status dos itens"""
        if not _HAS_MATPLOTLIB:
            return
        try:
            self.status_ax.clear()
            
            if not status_counts:
                self.status_ax.text(0.5, 0.5, 'Nenhum dado disponível', 
                                  ha='center', va='center', transform=self.status_ax.transAxes)
            else:
                labels = list(status_counts.keys())
                sizes = list(status_counts.values())
                colors = ['#ff6b6b', '#51cf66', '#ffd43b']  # Vermelho, Verde, Amarelo
                
                # Ajustar cores baseado nos labels
                color_map = {
                    'A Comprar': '#ff6b6b',
                    'Comprado': '#51cf66',
                    'Parcialmente Comprado': '#ffd43b'
                }
                
                chart_colors = [color_map.get(label, '#74c0fc') for label in labels]
                
                wedges, texts, autotexts = self.status_ax.pie(
                    sizes, labels=labels, colors=chart_colors, autopct='%1.1f%%',
                    startangle=90, textprops={'color': 'white'}
                )
                
                # Melhorar a aparência dos textos
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            
            self.status_ax.set_title('Status dos Itens', color='white', fontweight='bold')
            self.status_canvas.draw()
            
        except Exception as e:
            print(f"Erro ao atualizar gráfico de status: {e}")
    
    def update_suppliers_chart(self):
        """Atualiza o gráfico de fornecedores"""
        if not _HAS_MATPLOTLIB:
            return
        try:
            self.suppliers_ax.clear()
            
            suppliers = SupplierRepository.get_all()
            
            if not suppliers:
                self.suppliers_ax.text(0.5, 0.5, 'Nenhum fornecedor cadastrado', 
                                     ha='center', va='center', transform=self.suppliers_ax.transAxes)
            else:
                supplier_names = [s.name for s in suppliers]
                supplier_counts = [1] * len(suppliers)  # Contador simples
                
                bars = self.suppliers_ax.bar(supplier_names, supplier_counts, color='#74c0fc')
                self.suppliers_ax.set_title('Fornecedores Cadastrados', color='white', fontweight='bold')
                self.suppliers_ax.set_ylabel('Quantidade', color='white')
                
                # Rotacionar labels se necessário
                if len(supplier_names) > 3:
                    self.suppliers_ax.tick_params(axis='x', rotation=45)
                
                # Configurar cores dos textos
                self.suppliers_ax.tick_params(colors='white')
                self.suppliers_ax.yaxis.label.set_color('white')
            
            self.suppliers_canvas.draw()
            
        except Exception as e:
            print(f"Erro ao atualizar gráfico de fornecedores: {e}")
    
    def create_backup(self):
        """Cria um backup manual"""
        try:
            backup_path = self.backup_service.create_backup("manual")
            if backup_path:
                messagebox.showinfo("Sucesso", f"Backup criado com sucesso!\n{backup_path}")
                self.update_data()
            else:
                messagebox.showerror("Erro", "Falha ao criar backup")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup: {e}")
    
    def show_backups(self):
        """Mostra a janela de gerenciamento de backups"""
        try:
            backups = self.backup_service.list_backups()
            
            # Criar janela de backups
            backup_window = tk.Toplevel(self.parent)
            backup_window.title("Gerenciar Backups")
            backup_window.geometry("600x400")
            
            # Lista de backups
            tree = ttk.Treeview(backup_window, columns=('size', 'created'), show='tree headings')
            tree.heading('#0', text='Arquivo')
            tree.heading('size', text='Tamanho')
            tree.heading('created', text='Criado em')
            
            tree.column('#0', width=300)
            tree.column('size', width=100)
            tree.column('created', width=150)
            
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                tree.insert('', 'end', text=backup['filename'], 
                           values=(f"{size_mb:.2f} MB", backup['created'].strftime('%d/%m/%Y %H:%M')))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Botões
            buttons_frame = ttk.Frame(backup_window)
            buttons_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Button(buttons_frame, text="Restaurar", 
                      command=lambda: self.restore_backup(tree, backup_window)).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="Excluir", 
                      command=lambda: self.delete_backup(tree, backup_window)).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="Fechar", 
                      command=backup_window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar backups: {e}")
    
    def restore_backup(self, tree, window):
        """Restaura um backup selecionado"""
        try:
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione um backup para restaurar")
                return
            
            item = tree.item(selection[0])
            filename = item['text']
            
            # Encontrar o caminho completo do backup
            backups = self.backup_service.list_backups()
            backup_path = None
            for backup in backups:
                if backup['filename'] == filename:
                    backup_path = backup['path']
                    break
            
            if not backup_path:
                messagebox.showerror("Erro", "Backup não encontrado")
                return
            
            # Confirmar restauração
            if messagebox.askyesno("Confirmar", f"Restaurar backup {filename}?\n\nEsta ação substituirá o banco atual."):
                if self.backup_service.restore_backup(backup_path):
                    messagebox.showinfo("Sucesso", "Backup restaurado com sucesso!")
                    window.destroy()
                    self.update_data()
                else:
                    messagebox.showerror("Erro", "Falha ao restaurar backup")
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup: {e}")
    
    def delete_backup(self, tree, window):
        """Exclui um backup selecionado"""
        try:
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione um backup para excluir")
                return
            
            item = tree.item(selection[0])
            filename = item['text']
            
            # Encontrar o caminho completo do backup
            backups = self.backup_service.list_backups()
            backup_path = None
            for backup in backups:
                if backup['filename'] == filename:
                    backup_path = backup['path']
                    break
            
            if not backup_path:
                messagebox.showerror("Erro", "Backup não encontrado")
                return
            
            # Confirmar exclusão
            if messagebox.askyesno("Confirmar", f"Excluir backup {filename}?"):
                if self.backup_service.delete_backup(backup_path):
                    messagebox.showinfo("Sucesso", "Backup excluído com sucesso!")
                    window.destroy()
                    self.show_backups()  # Atualizar lista
                else:
                    messagebox.showerror("Erro", "Falha ao excluir backup")
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir backup: {e}")
    
    def pack(self, **kwargs):
        """Pack do frame principal"""
        self.frame.pack(**kwargs)
    
    def destroy(self):
        """Destrói o dashboard"""
        self.frame.destroy()

