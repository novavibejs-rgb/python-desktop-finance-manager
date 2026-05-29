"""
Módulo de gerenciamento de despesas
Lógica de negócio para despesas e vales
"""

import json
import os
from datetime import datetime
from pathlib import Path

class ExpenseManager:
    def __init__(self, filename="expenses_data.json"):
        self.filename = filename
        self.data = self.load_data()
        
    def load_data(self):
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_data()
        return self.get_default_data()
    
    def get_default_data(self):
        """Retorna estrutura padrão de dados"""
        return {
            "total_balance": 0,
            "expenses": [],
            "vales": [],
            "gastos_reserve": 0
        }
    
    def save_data(self):
        """Salva dados no arquivo JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
    
    def add_expense(self, description, value, category):
        """Adiciona uma nova despesa"""
        expense = {
            "id": len(self.data["expenses"]) + 1,
            "date": datetime.now().isoformat(),
            "description": description,
            "value": value,
            "category": category,
            "percentage_20": value * 0.20,
            "available": value * 0.80,
            "status": "registered"
        }
        
        self.data["expenses"].append(expense)
        self.data["total_balance"] += value * 0.80
        self.data["gastos_reserve"] += value * 0.20
        
        self.save_data()
        return expense
    
    def add_vale(self, employee_name, value, reason, email):
        """Adiciona um vale para funcionário"""
        vale = {
            "id": len(self.data["vales"]) + 1,
            "date": datetime.now().isoformat(),
            "employee_name": employee_name,
            "value": value,
            "reason": reason,
            "email": email,
            "status": "approved",
            "discount_date": None
        }
        
        self.data["vales"].append(vale)
        self.data["total_balance"] -= value
        
        self.save_data()
        return vale
    
    def get_balance(self):
        """Retorna o saldo disponível"""
        return self.data.get("total_balance", 0)
    
    def get_pending_vales(self):
        """Retorna total de vales pendentes de desconto"""
        total = 0
        for vale in self.data.get("vales", []):
            if vale.get("status") == "approved" and vale.get("discount_date") is None:
                total += vale.get("value", 0)
        return total
    
    def get_gastos_reserve(self):
        """Retorna o valor em reserva para gastos (20%)"""
        return self.data.get("gastos_reserve", 0)
    
    def mark_vale_as_discounted(self, vale_id):
        """Marca um vale como descontado"""
        for vale in self.data.get("vales", []):
            if vale.get("id") == vale_id:
                vale["status"] = "discounted"
                vale["discount_date"] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def generate_report(self):
        """Gera um relatório completo"""
        report = []
        report.append("=" * 80)
        report.append("RELATÓRIO DE DESPESAS E VALES".center(80))
        report.append("=" * 80)
        report.append(f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        # Resumo Financeiro
        report.append("\n" + "-" * 80)
        report.append("RESUMO FINANCEIRO")
        report.append("-" * 80)
        total_balance = self.get_balance()
        gastos_reserve = self.get_gastos_reserve()
        pending_vales = self.get_pending_vales()
        
        report.append(f"Saldo Disponível:        R$ {total_balance:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        report.append(f"Reserva para Gastos (20%): R$ {gastos_reserve:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        report.append(f"Vales Pendentes:         R$ {pending_vales:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        report.append(f"{'':43} {'─' * 15}")
        report.append(f"Total:                   R$ {total_balance + gastos_reserve - pending_vales:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        # Despesas
        expenses = self.data.get("expenses", [])
        if expenses:
            report.append("\n" + "-" * 80)
            report.append("DESPESAS REGISTRADAS")
            report.append("-" * 80)
            report.append(f"{'ID':<5} {'Data':<12} {'Categoria':<15} {'Descrição':<25} {'Valor':>12}")
            report.append("-" * 80)
            
            for exp in expenses[-10:]:  # Últimas 10
                date = exp.get("date", "").split("T")[0]
                report.append(f"{exp.get('id'):<5} {date:<12} {exp.get('category', ''):<15} {exp.get('description', ''):<25} R$ {exp.get('value', 0):>10,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        # Vales
        vales = self.data.get("vales", [])
        if vales:
            report.append("\n" + "-" * 80)
            report.append("VALES SOLICITADOS")
            report.append("-" * 80)
            report.append(f"{'ID':<5} {'Data':<12} {'Funcionário':<20} {'Valor':>12} {'Status':<15}")
            report.append("-" * 80)
            
            for vale in vales[-10:]:  # Últimos 10
                date = vale.get("date", "").split("T")[0]
                status = "Descontado" if vale.get("status") == "discounted" else "Pendente"
                report.append(f"{vale.get('id'):<5} {date:<12} {vale.get('employee_name', ''):<20} R$ {vale.get('value', 0):>10,.2f} {status:<15}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
    
    def export_report(self):
        """Exporta o relatório para arquivo .txt"""
        report = self.generate_report()
        with open("relatório.txt", "w", encoding="utf-8") as f:
            f.write(report)
