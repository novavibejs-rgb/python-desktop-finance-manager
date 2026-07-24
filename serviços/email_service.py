"""
Módulo de serviço de email
Envia notificações por email
"""
import banco.banco as banco
import smtplib
import configparser
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.utils import Utils
from email.mime.image import MIMEImage
from email.utils import make_msgid


class ServicoEmail:

    def __init__(self, arquivo_config="config.ini"):

        self.pasta = os.path.dirname(__file__)

        self.arquivo_config = os.path.join(
            self.pasta,
            arquivo_config
        )

        self.caminho_logo = os.path.join(
            self.pasta,
            "logo.png"
        )

        self.config = self.carregar_config()


    def carregar_config(self):
        """Carrega o arquivo de configuração."""

        config = configparser.ConfigParser()

        if os.path.exists(self.arquivo_config):
            config.read(self.arquivo_config, encoding="utf-8")
            return config

        return None


    def enviar_email(self, para_email, assunto, corpo):
        """Envia um e-mail."""

        try:

            if not self.config or not self.config.has_section("EMAIL"):
                print(f"[EMAIL SIMULADO] Para: {para_email}")
                print(corpo)
                return True

            smtp_servidor = self.config.get("EMAIL", "smtp_server")
            smtp_porta = self.config.getint("EMAIL", "smtp_port")
            email_remetente = self.config.get("EMAIL", "email")
            senha = self.config.get("EMAIL", "password")

            msg = MIMEMultipart("related")
            msg["From"] = email_remetente
            msg["To"] = para_email
            msg["Subject"] = assunto

            corpo = corpo.replace("cid_logo", "logo")
            msg.attach(MIMEText(corpo, "html", "utf-8"))

            if os.path.exists(self.caminho_logo):
                with open(self.caminho_logo, "rb") as img:
                    imagem = MIMEImage(img.read())
                    imagem.add_header("Content-ID", "<logo>")
                    imagem.add_header(
                        "Content-Disposition",
                        "inline",
                        filename="logo.png"
                    )
                    msg.attach(imagem)

            with smtplib.SMTP(smtp_servidor, smtp_porta) as servidor:
                servidor.starttls()
                servidor.login(email_remetente, senha)
                servidor.send_message(msg)

            return True

        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
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


    def enviar_notificacao_vale(self, id_socio, valor, motivo, email_socio):
        """Notificação de vale com dados do sócio"""

        socio = banco.buscar_dados_socio(id_socio)
        faturamento = banco.faturamento_semana() / 2

        reserva = faturamento * 0.20
        saldo_socio = faturamento - reserva
        

        if not socio:
            print("[EMAIL] Sócio não encontrado")
            return False

        nome_funcionario = socio["nome"]

        assunto = f"✓ Retirada De valor - {nome_funcionario}"

        corpo = f"""
        <html>
            <body style="font-family: Arial; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 20px; border-radius: 8px;">
                    
                   <h2 style="background:#1f4e79;color:#ffffff;padding:20px;border-radius:8px;margin:0;">✅ Adiantamento</h2>

                    <p><strong>ID -> {id_socio} :</strong> {nome_funcionario}</p>

                    <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                    <p><strong>Motivo:</strong> {motivo}</p>
                    <p><strong>Valor:</strong> R$ {valor:,.2f}</p>

                    <hr>

                    <p style="color:red;">
                        ⚠ Histórico do sócio:
                    </p>

                    <p>Quantidade de vales: {socio['quantidade_vales']}</p>
                    <p>Total já retirado: R$ {socio['total_vales']:,.2f}</p>
                    <p> 💰 Saldo: R$ {saldo_socio:,.2f}</p>

                    <hr>

                    <small>Email automático</small>
                </div>
            </body>
        </html>
        """

        corpo = self.formatar_moeda_ptbr(corpo)

        # envia para socio
        self.enviar_email(email_socio, assunto, corpo)

        # Envia para o administrador (se for diferente do funcionário)
        if self.config and self.config.has_option("EMAIL", "admin_email"):
            admin_email = self.config.get("EMAIL", "admin_email")

            if admin_email.lower() != email_socio.lower():
                self.enviar_email(admin_email, f"[ADMIN] {assunto}", corpo)

        return True
    

    def enviar_notificacao_servico(self,cliente,valor,servico,forma_pagamento,descricao):    
        """Notificação de serviço registrado"""

        assunto = f"✓ Novo Serviço Registrado - {cliente}"

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
                                    <h2 style="margin:0;"> 🏠 Novo Serviço Registrado</h2>
                                    <p style="margin:5px 0 0 0; opacity:0.9;">
                                        Sistema Financeiro
                                    </p>
                                </td>
                            </tr>

                            <!-- Conteúdo -->
                            <tr>
                                <td style="padding:30px;">

                                    <p style="color:#666; margin-top:0;">
                                        Um novo serviço foi registrado no sistema.
                                    </p>

                                    <table width="100%" cellpadding="10" cellspacing="0"
                                        style="border-collapse:collapse;">

                                        <tr>
                                            <td style="background:#f8f9fa; border:1px solid #e5e7eb;">
                                                <strong>👤 Cliente</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb;">
                                                {cliente}
                                            </td>
                                        </tr>

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
                                                <strong>🔧 Serviço</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb;">
                                                {servico}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="background:#f8f9fa; border:1px solid #e5e7eb;">
                                                <strong>💳 Pagamento</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb;">
                                                {forma_pagamento}
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
                                                <strong>💰 Valor</strong>
                                            </td>
                                            <td style="border:1px solid #e5e7eb; color:#2e7d32; font-size:18px;">
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

        corpo = self.formatar_moeda_ptbr(corpo)

        socios = banco.listar_socios()

        for socio in socios:
            if socio["email"]:
                self.enviar_email(socio["email"], assunto, corpo)

        return True


    def gerar_tabela_servicos(self, servicos):
        
        """Gera as linhas da tabela de serviços em HTML"""

        linhas = ""

        for data, servico, descricao, pagamento, valor in servicos:

            valor = self.formatar_moeda_ptbr(f"{valor:,.2f}")
            

            linhas += f"""
            <tr>
                <td style="padding:10px; border:1px solid #e5e7eb;">{data}</td>

                <td style="padding:10px; border:1px solid #e5e7eb;">
                    {servico}
                </td>

                <td style="padding:10px; border:1px solid #e5e7eb;">
                    {descricao}
                </td>

                <td style="padding:10px; border:1px solid #e5e7eb;">
                    {pagamento}
                </td>

              <td style="
                width:120px;
                min-width:120px;
                padding:10px;
                border:1px solid #e5e7eb;
                text-align:right;
                white-space:nowrap;
                color:#2e7d32;
                font-weight:bold;
            ">
                R$ {valor}
            </td>
            </tr>
            """

        return linhas


    def gerar_html_fechamento(self, cliente, periodo, total_servicos, faturamento, linhas_servicos):
        """Gera o HTML do relatório de fechamento semanal"""

        inicio, fim = periodo

        inicio = Utils.data_br(inicio)
        fim = Utils.data_br(fim)

        faturamento = self.formatar_moeda_ptbr(f"{faturamento:,.2f}")

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
        </head>

        <body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;">

            <table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 0;">
                <tr>
                    <td align="center">

                        <table width="650" cellpadding="0" cellspacing="0"
                            style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.08);">

                            <!-- Cabeçalho -->
                            <tr>
                                <td style="background:#1f4e79;color:#ffffff;padding:25px;">

                                    <table cellpadding="0" cellspacing="0">
                                        <tr>

                                            <td>
                                                <img src="cid:logo"
                                                    width="80"
                                                    height="80"
                                                    style="
                                                        display:block;
                                                        border-radius:50%;
                                                        width:80px;
                                                        height:80px;
                                                        object-fit:cover;
                                                    ">
                                            </td>

                                            <td style="padding-left:20px;">

                                                <h2 style="margin:0;">
                                                    📊 Relatório de Fechamento Semanal
                                                </h2>

                                                <p style="margin:5px 0 0 0;">
                                                    Sistema Financeiro<br>
                                                    IRMÃOS J CONSTRUÇÃO E REFORMAS
                                                </p>

                                            </td>

                                        </tr>
                                    </table>

                                </td>
                            </tr>


                            <!-- Conteúdo -->
                            <tr>
                                <td style="padding:30px;">

                                    <p>
                                        Olá,
                                        <strong>{cliente}</strong>.
                                    </p>

                                    <p>
                                        <strong>
                                            Segue abaixo o resumo dos serviços realizados nesta semana.
                                        </strong>
                                    </p>


                                    <table width="100%"
                                        cellpadding="12"
                                        cellspacing="0"
                                        style="border-collapse:collapse;margin-top:20px;">

                                        <tr>
                                            <td style="background:#f8f9fa;border:1px solid #e5e7eb;">
                                                👤 <strong>Cliente</strong>
                                            </td>

                                            <td style="border:1px solid #e5e7eb;">
                                                {cliente}
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="background:#f8f9fa;border:1px solid #e5e7eb;">
                                                📅 <strong>Período</strong>
                                            </td>

                                            <td style="border:1px solid #e5e7eb;">
                                                {inicio} até {fim}
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="background:#f8f9fa;border:1px solid #e5e7eb;">
                                                🛠 <strong>Total de Serviços</strong>
                                            </td>

                                            <td style="border:1px solid #e5e7eb;">
                                                {total_servicos}
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="background:#f8f9fa;border:1px solid #e5e7eb;">
                                                💰 <strong>Faturamento</strong>
                                            </td>

                                            <td style="
                                                border:1px solid #e5e7eb;
                                                color:#2e7d32;
                                                font-size:22px;
                                                font-weight:bold;
                                            ">
                                                R$ {faturamento}
                                            </td>
                                        </tr>

                                    </table>


                                    <h3 style="margin-top:35px;color:#1f4e79;">
                                        📋 Serviços realizados
                                    </h3>


                                    <table width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        style="border-collapse:collapse;border:1px solid #dcdcdc;">

                                        <tr style="background:#1f4e79;color:#ffffff;">

                                            <th style="padding:10px;border:1px solid #dcdcdc;">
                                                Data
                                            </th>

                                            <th style="padding:10px;border:1px solid #dcdcdc;">
                                                Serviço
                                            </th>

                                            <th style="padding:10px;border:1px solid #dcdcdc;">
                                                Descrição
                                            </th>

                                            <th style="padding:10px;border:1px solid #dcdcdc;">
                                                Pagamento
                                            </th>

                                            <th style="padding:10px;border:1px solid #dcdcdc;text-align:right;">
                                                Valor
                                            </th>

                                        </tr>

                                        {linhas_servicos}

                                    </table>


                                    <p style="margin-top:25px;color:#555;">
                                        Obrigado pela confiança em nosso trabalho.
                                    </p>

                                </td>
                            </tr>


                            <!-- Rodapé -->
                            <tr>
                                <td style="
                                    background:#f8f9fa;
                                    text-align:center;
                                    padding:20px;
                                    color:#777;
                                    font-size:12px;
                                ">

                                    Sistema Financeiro © {datetime.now().year}<br>
                                    Relatório gerado automaticamente.

                                </td>
                            </tr>


                        </table>

                    </td>
                </tr>
            </table>

        </body>
        </html>
        """

        return html


    def enviar_fechamento_semana(self, email, cliente):

        periodo = Utils.intervalo_semana_sql()

        servicos = banco.buscar_servicos_cliente_semana( cliente)

        faturamento = sum(valor for _, _,_, _, valor in servicos)

        total_servicos = len(servicos)

        linhas_servicos = self.gerar_tabela_servicos(servicos)

        html = self.gerar_html_fechamento(
            cliente=cliente,
            periodo=periodo,
            total_servicos=total_servicos,
            faturamento=faturamento,
            linhas_servicos=linhas_servicos
        )

        assunto = f"✓ Fechamento da Semana - {cliente}"

        return self.enviar_email(email, assunto, html)


    def formatar_moeda_ptbr(self, texto):
        """ formatação de moeda"""
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")