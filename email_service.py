"""
Módulo de serviço de email
Envia notificações por email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import configparser
import os

class EmailService:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """Carrega configurações de email"""
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding='utf-8')
            return config
        return None
    
    def send_email(self, to_email, subject, body):
        """Envia um email"""
        try:
            if not self.config or not self.config.has_section('EMAIL'):
                print(f"[EMAIL] {subject} - Para: {to_email}")
                print(f"[EMAIL] {body}\n")
                return True
            
            smtp_server = self.config.get('EMAIL', 'smtp_server')
            smtp_port = self.config.getint('EMAIL', 'smtp_port')
            sender_email = self.config.get('EMAIL', 'email')
            password = self.config.get('EMAIL', 'password')
            
            # Cria mensagem
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # Envia email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False
    
    def send_expense_notification(self, description, value, percentage, category):
        """Envia notificação de despesa registrada"""
        subject = "✓ Nova Despesa Registrada - Autorização"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px;">
                        ✓ Despesa Registrada com Sucesso
                    </h2>
                    
                    <div style="margin: 20px 0;">
                        <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                        
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr style="background-color: #f0f0f0;">
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Descrição</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{description}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Categoria</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{category}</td>
                            </tr>
                            <tr style="background-color: #f0f0f0;">
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Valor Total</td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #2196F3; font-weight: bold;">R$ {value:,.2f}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Reserva para Gastos (20%)</td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #FF9800; font-weight: bold;">R$ {percentage:,.2f}</td>
                            </tr>
                            <tr style="background-color: #e8f5e9;">
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Saldo Disponível</td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #4CAF50; font-weight: bold;">R$ {value - percentage:,.2f}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p style="color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 15px;">
                        Este é um email automático de autorização. Não responda a este email.
                    </p>
                </div>
            </body>
        </html>
        """.replace(",", "X").replace(".", ",").replace("X", ".")
        
        if self.config and self.config.has_option('EMAIL', 'admin_email'):
            admin_email = self.config.get('EMAIL', 'admin_email')
            self.send_email(admin_email, subject, body)
        else:
            self.send_email("admin@empresa.com", subject, body)
    
    def send_vale_notification(self, employee_name, value, reason, employee_email):
        """Envia notificação de vale solicitado"""
        subject = f"✓ Vale Autorizado - {employee_name}"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; border-bottom: 3px solid #2196F3; padding-bottom: 10px;">
                        ✓ Vale Autorizado
                    </h2>
                    
                    <p style="font-size: 16px; margin: 20px 0;">Prezado(a) <strong>{employee_name}</strong>,</p>
                    
                    <p style="color: #666;">Seu vale foi autorizado com sucesso! As informações estão abaixo:</p>
                    
                    <div style="background-color: #e3f2fd; padding: 15px; border-left: 4px solid #2196F3; margin: 20px 0;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; font-weight: bold; color: #333;">Data/Hora:</td>
                                <td style="padding: 8px;">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold; color: #333;">Motivo:</td>
                                <td style="padding: 8px;">{reason}</td>
                            </tr>
                            <tr style="background-color: #fff8e1;">
                                <td style="padding: 8px; font-weight: bold; color: #333;">Valor do Vale:</td>
                                <td style="padding: 8px; color: #2196F3; font-weight: bold; font-size: 18px;">R$ {value:,.2f}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p style="color: #ff5722; font-weight: bold; margin-top: 20px;">
                        ⚠️ Este valor será descontado do seu próximo saldo.
                    </p>
                    
                    <p style="color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 15px; margin-top: 20px;">
                        Este é um email automático de autorização. Não responda a este email.
                    </p>
                </div>
            </body>
        </html>
        """.replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Envia para o funcionário
        self.send_email(employee_email, subject, body)
        
        # Também envia para o admin como confirmação
        if self.config and self.config.has_option('EMAIL', 'admin_email'):
            admin_email = self.config.get('EMAIL', 'admin_email')
            subject_admin = f"[ADMIN] Vale Autorizado - {employee_name}"
            self.send_email(admin_email, subject_admin, body)
