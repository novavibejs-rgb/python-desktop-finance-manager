"""
Módulo de serviço de email
Envia notificações por email
"""
import banco
import smtplib
import configparser
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ServicoEmail:
    def __init__(self, arquivo_config="config.ini"):
        self.arquivo_config = arquivo_config
        self.config = self.carregar_config()

    def carregar_config(self):
        """Carrega configurações de email"""
        config = configparser.ConfigParser()

        if os.path.exists(self.arquivo_config):
            config.read(self.arquivo_config, encoding="utf-8")
            return config

        return None

    def enviar_email(self, para_email, assunto, corpo):
        """Envia um email"""
        try:
            # 🔹 modo fallback (debug)
            if not self.config or not self.config.has_section("EMAIL"):
                print(f"[EMAIL SIMULADO] Para: {para_email}")
                print(f"Assunto: {assunto}")
                print(f"Mensagem:\n{corpo}\n")
                return True

            smtp_servidor = self.config.get("EMAIL", "smtp_server")
            smtp_porta = self.config.getint("EMAIL", "smtp_port")
            email_remetente = self.config.get("EMAIL", "email")
            senha = self.config.get("EMAIL", "password")

            msg = MIMEMultipart()
            msg["From"] = email_remetente
            msg["To"] = para_email
            msg["Subject"] = assunto

            msg.attach(MIMEText(corpo, "html", "utf-8"))

            with smtplib.SMTP(smtp_servidor, smtp_porta) as servidor:
                servidor.starttls()
                servidor.login(email_remetente, senha)
                servidor.send_message(msg)

            return True

        except Exception as e:
            print(f"[ERRO EMAIL] {e}")
            return False

    def enviar_notificacao_despesa(self, descricao, valor, categoria):
        """Notificação de despesa"""
        assunto = "✓ Nova Despesa Registrada"
    
        corpo = f"""
        <html>
        <body style="margin:0; padding:0; background-color:#f4f6f9; font-family:Arial, Helvetica, sans-serif;">

            <table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 0;">
                <tr>
                    <td align="center">

                        <table width="600" cellpadding="0" cellspacing="0"
                            style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,0.08);">

                            <!-- Cabeçalho -->
                            <tr>
                                <td style="background:#1f4e79; color:#ffffff; padding:25px;">
                                    <h2 style="margin:0;">💰 Nova Despesa Registrada</h2>
                                    <p style="margin:5px 0 0 0; opacity:0.9;">
                                        Sistema Financeiro
                                    </p>
                                </td>
                            </tr>

                            <!-- Conteúdo -->
                            <tr>
                                <td style="padding:30px;">

                                    <p style="color:#666; margin-top:0;">
                                        Uma nova despesa foi registrada no sistema.
                                    </p>

                                    <table width="100%" cellpadding="10" cellspacing="0"
                                        style="border-collapse:collapse;">

                                        <tr>
                                            <td style="background:#f8f9fa; border:1px solid #e5e7eb;">
                                                <strong>📅 Data</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb;">
                                                {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="background:#f8f9fa; border:1px solid #e5e7eb;">
                                                <strong>📝 Descrição</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb;">
                                                {descricao}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="background:#f8f9fa; border:1px solid #e5e7eb;">
                                                <strong>🏷️ Categoria</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb;">
                                                {categoria}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="background:#f8f9fa; border:1px solid #e5e7eb;">
                                                <strong>💵 Valor</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb; color:#c62828; font-size:18px;">
                                                <strong>R$ {valor:,.2f}</strong>
                                            </td>
                                        </tr>

                                    </table>

                                </td>
                            </tr>

                            <!-- Rodapé -->
                            <tr>
                                <td style="background:#f8f9fa; padding:20px; text-align:center; color:#777; font-size:12px;">
                                    Este é um e-mail automático gerado pelo Sistema Financeiro.<br>
                                    Não responda esta mensagem.
                                </td>
                            </tr>

                        </table>

                    </td>
                </tr>
            </table>

        </body>
        </html>
        """

        corpo = self._formatar_moeda_ptbr(corpo)

        admin_email = self.config.get("EMAIL", "admin_email") if self.config and self.config.has_option("EMAIL", "admin_email") else "admin@empresa.com"

        self.enviar_email(admin_email, assunto, corpo)

    def enviar_notificacao_vale(self, id_socio, valor, motivo, email_funcionario):
        """Notificação de vale com dados do sócio"""

        socio = banco.buscar_dados_socio(id_socio)

        if not socio:
            print("[EMAIL] Sócio não encontrado")
            return False

        nome_funcionario = socio["nome"]

        assunto = f"✓ Vale Autorizado - {nome_funcionario}"

        corpo = f"""
        <html>
            <body style="font-family: Arial; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 20px; border-radius: 8px;">
                    
                    <h2>✓ Vale Autorizado</h2>

                    <p><strong>Funcionário:</strong> {nome_funcionario}</p>

                    <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                    <p><strong>Motivo:</strong> {motivo}</p>
                    <p><strong>Valor:</strong> R$ {valor:,.2f}</p>

                    <hr>

                    <p style="color:red;">
                        ⚠ Histórico do sócio:
                    </p>

                    <p>Quantidade de vales: {socio['quantidade_vales']}</p>
                    <p>Total já retirado: R$ {socio['total_vales']:,.2f}</p>

                    <hr>

                    <small>Email automático</small>
                </div>
            </body>
        </html>
        """

        corpo = self._formatar_moeda_ptbr(corpo)

        # envia para funcionário
        self.enviar_email(email_funcionario, assunto, corpo)

        # envia para admin
        if self.config and self.config.has_option("EMAIL", "admin_email"):
            admin_email = self.config.get("EMAIL", "admin_email")
            self.enviar_email(admin_email, f"[ADMIN] {assunto}", corpo)

        return True

    def _formatar_moeda_ptbr(self, texto):
        """ formatação de moeda"""
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")