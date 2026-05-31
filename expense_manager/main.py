""""
Gerenciador de Despesas e Vales
Interface gráfica para gerenciar despesas da empresa e vales de funcionários
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from expense_manager import ExpenseManager
from email_service import EmailService
import json
from datetime import datetime
import os
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class ExpenseManagerApp:
    def __init__(self, root):
            
        self.root = root
        self.root.title("Gerenciador de Despesas e Vales")
        self.root.geometry("900x600")

        # Carrega dados
        self.expense_manager = ExpenseManager()
        self.email_service = EmailService()

        # Define estilo
        self.setup_styles()

        # STATUS BAR PRIMEIRO
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")

        status_bar = ttk.Label(
            root,
            textvariable=self.status_var,
            relief=tk.SUNKEN
        )

        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria abas
        self.create_expense_tab()
        self.create_vale_tab()
        self.create_report_tab()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_expense_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Lançar Despesa")
        
        # Título
        title_label = ttk.Label(frame, text="Registrar Nova Despesa", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(frame, text="Dados da Despesa", padding=20)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Descrição
        ttk.Label(input_frame, text="Descrição:").grid(row=0, column=0, sticky="w", pady=5)
        self.expense_desc = ttk.Entry(input_frame, width=40)
        self.expense_desc.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Valor
        ttk.Label(input_frame, text="Valor (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.expense_value = ttk.Entry(input_frame, width=40)
        self.expense_value.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Categoria
        ttk.Label(input_frame, text="Categoria:").grid(row=2, column=0, sticky="w", pady=5)
        self.expense_category = ttk.Combobox(input_frame, values=["Salário", "Insumos", "Aluguel", "Utilitários", "Outro"], width=38)
        self.expense_category.grid(row=2, column=1, sticky="ew", pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Frame de informações
        info_frame = ttk.LabelFrame(frame, text="Cálculo Automático", padding=20)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(info_frame, text="Valor Total:").grid(row=0, column=0, sticky="w")
        self.expense_total = ttk.Label(info_frame, text="R$ 0,00", foreground="blue", font=("Arial", 12, "bold"))
        self.expense_total.grid(row=0, column=1, sticky="w")
        
        ttk.Label(info_frame, text="Percentual para Gastos (20%):").grid(row=1, column=0, sticky="w", pady=5)
        self.expense_percentage = ttk.Label(info_frame, text="R$ 0,00", foreground="green", font=("Arial", 12, "bold"))
        self.expense_percentage.grid(row=1, column=1, sticky="w")
        
        ttk.Label(info_frame, text="Saldo Disponível:").grid(row=2, column=0, sticky="w", pady=5)
        self.expense_balance = ttk.Label(info_frame, text="R$ 0,00", foreground="red", font=("Arial", 12, "bold"))
        self.expense_balance.grid(row=2, column=1, sticky="w")
        
        # Botões
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Calcular", command=self.calculate_expense).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Lançar Despesa", command=self.register_expense).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_expense_fields).pack(side="left", padx=5)
        
        self.update_expense_info()
        
    def create_vale_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Solicitar Vale")
        
        # Título
        title_label = ttk.Label(frame, text="Solicitar Vale para Funcionário", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(frame, text="Dados do Vale", padding=20)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Nome do funcionário
        ttk.Label(input_frame, text="Nome do Funcionário:").grid(row=0, column=0, sticky="w", pady=5)
        self.employee_name = ttk.Entry(input_frame, width=40)
        self.employee_name.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Valor do vale
        ttk.Label(input_frame, text="Valor do Vale (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.vale_value = ttk.Entry(input_frame, width=40)
        self.vale_value.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Motivo
        ttk.Label(input_frame, text="Motivo:").grid(row=2, column=0, sticky="w", pady=5)
        self.vale_reason = ttk.Entry(input_frame, width=40)
        self.vale_reason.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Email do funcionário
        ttk.Label(input_frame, text="Email do Funcionário:").grid(row=3, column=0, sticky="w", pady=5)
        self.employee_email = ttk.Entry(input_frame, width=40)
        self.employee_email.grid(row=3, column=1, sticky="ew", pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Frame de informações
        info_frame = ttk.LabelFrame(frame, text="Informações da Conta", padding=20)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(info_frame, text="Saldo Disponível:").grid(row=0, column=0, sticky="w")
        self.vale_balance = ttk.Label(info_frame, text="R$ 0,00", foreground="blue", font=("Arial", 12, "bold"))
        self.vale_balance.grid(row=0, column=1, sticky="w")
        
        ttk.Label(info_frame, text="Total de Vales Pendentes:").grid(row=1, column=0, sticky="w", pady=5)
        self.vale_pending = ttk.Label(info_frame, text="R$ 0,00", foreground="orange", font=("Arial", 12, "bold"))
        self.vale_pending.grid(row=1, column=1, sticky="w")
        
        # Botões
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Solicitar Vale", command=self.request_vale).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_vale_fields).pack(side="left", padx=5)
        
        self.update_vale_info()
        
    def create_report_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Relatório")
        
        # Título
        title_label = ttk.Label(frame, text="Relatório de Despesas e Vales", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame de botões
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Atualizar", command=self.update_report).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exportar", command=self.export_report).pack(side="left", padx=5)
        
        # Text widget para relatório
        self.report_text = tk.Text(frame, height=20, width=100)
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.report_text)
        scrollbar.pack(side="right", fill="y")
        self.report_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.report_text.yview)
        
        self.update_report()
        
    def calculate_expense(self):
        try:
            value = float(self.expense_value.get().replace(",", "."))
            percentage = value * 0.20
            balance = value - percentage
            
            self.expense_total.config(text=f"R$ {value:,.2f}".replace(",", ".").replace(".", ","))
            self.expense_percentage.config(text=f"R$ {percentage:,.2f}".replace(",", ".").replace(".", ","))
            self.expense_balance.config(text=f"R$ {balance:,.2f}".replace(",", ".").replace(".", ","))
            
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido")
            
    def register_expense(self):
        try:
            desc = self.expense_desc.get()
            value = float(self.expense_value.get().replace(",", "."))
            category = self.expense_category.get()
            
            if not desc or not category:
                messagebox.showwarning("Aviso", "Preencha todos os campos")
                return
                
            self.expense_manager.add_expense(desc, value, category)
            
            # Envia email de notificação
            percentage = value * 0.20
            self.email_service.send_expense_notification(
                desc, value, percentage, category
            )
            
            messagebox.showinfo("Sucesso", f"Despesa registrada!\n\n20% para gastos: R$ {percentage:.2f}")
            self.clear_expense_fields()
            self.update_expense_info()
            self.update_vale_info()
            self.status_var.set(f"Despesa registrada: {desc}")
            
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar despesa: {str(e)}")
            
    def request_vale(self):
        try:
            employee = self.employee_name.get()
            vale_value = float(self.vale_value.get().replace(",", "."))
            reason = self.vale_reason.get()
            email = self.employee_email.get()
            
            if not employee or not reason or not email:
                messagebox.showwarning("Aviso", "Preencha todos os campos")
                return
                
            # Verifica saldo disponível
            current_balance = self.expense_manager.get_balance()
            if vale_value > current_balance:
                messagebox.showerror("Erro", f"Saldo insuficiente!\nSaldo disponível: R$ {current_balance:.2f}")
                return
                
            self.expense_manager.add_vale(employee, vale_value, reason, email)
            
            # Envia email de autorização
            self.email_service.send_vale_notification(
                employee, vale_value, reason, email
            )
            
            messagebox.showinfo("Sucesso", f"Vale autorizado para {employee}!\nValor: R$ {vale_value:.2f}")
            self.clear_vale_fields()
            self.update_vale_info()
            self.update_expense_info()
            self.status_var.set(f"Vale autorizado: {employee} - R$ {vale_value:.2f}")
            
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao solicitar vale: {str(e)}")
            
    def clear_expense_fields(self):
        self.expense_desc.delete(0, tk.END)
        self.expense_value.delete(0, tk.END)
        self.expense_category.delete(0, tk.END)
        self.expense_total.config(text="R$ 0,00")
        self.expense_percentage.config(text="R$ 0,00")
        self.expense_balance.config(text="R$ 0,00")
        
    def clear_vale_fields(self):
        self.employee_name.delete(0, tk.END)
        self.vale_value.delete(0, tk.END)
        self.vale_reason.delete(0, tk.END)
        self.employee_email.delete(0, tk.END)
        
    def update_expense_info(self):
        balance = self.expense_manager.get_balance()
        self.expense_balance.config(text=f"R$ {balance:,.2f}".replace(".", ","))
        
    def update_vale_info(self):
        balance = self.expense_manager.get_balance()
        pending = self.expense_manager.get_pending_vales()
        self.vale_balance.config(text=f"R$ {balance:,.2f}".replace(".", ","))
        self.vale_pending.config(text=f"R$ {pending:,.2f}".replace(".", ","))
        
    def update_report(self):
        report = self.expense_manager.generate_report()
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
        self.status_var.set("Relatório atualizado")
        
    def export_report(self):
        try:
            self.expense_manager.export_report()
            messagebox.showinfo("Sucesso", "Relatório exportado para relatório.txt")
            self.status_var.set("Relatório exportado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManagerApp(root)
    root.mainloop()
