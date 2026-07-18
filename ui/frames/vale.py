
import customtkinter as ctk

import banco
from email_service import ServicoEmail


class FrameVale(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(
            master,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        self.app = app
        self.servico_email = ServicoEmail()

        self.criar_tela()

    def criar_tela(self):

        ctk.CTkLabel(
            self,
            text="Fazer Vale",
            font=("Arial", 30, "bold"),
            text_color="#080808"
        ).grid(row=0, column=0, columnspan=3, pady=(15, 80))

        # Motivo
        self.motivo_do_vale = ctk.CTkEntry(
            self,
            placeholder_text="Motivo",
            border_width=2,
            border_color="#0A0A0A",
            width=150,
            height=30
        )
        self.motivo_do_vale.grid(row=2, column=0, padx=15)

        # Valor
        self.valor_do_vale = ctk.CTkEntry(
            self,
            placeholder_text="Valor",
            border_width=2,
            border_color="#0A0A0A",
            width=150,
            height=30
        )
        self.valor_do_vale.grid(row=2, column=1, padx=15)

        # E-mail
        self.email_do_socio = ctk.CTkEntry(
            self,
            placeholder_text="E-mail",
            border_width=2,
            border_color="#0A0A0A",
            width=150,
            height=30
        )
        self.email_do_socio.grid(row=2, column=2, padx=15)

        # Descrição
        ctk.CTkLabel(
            self,
            text="Descrição",
            font=("Arial", 15, "bold"),
            text_color="#080808"
        ).grid(row=3, column=0, columnspan=3, pady=7)

        self.textbox_descricao_vale = ctk.CTkTextbox(
            self,
            border_width=2,
            border_color="#0A0A0A",
            width=350,
            height=80
        )
        self.textbox_descricao_vale.grid(row=4, column=0, columnspan=3, pady=5)

        # Mensagem
        self.label_mensagem_vale = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 14, "bold")
        )
        self.label_mensagem_vale.grid(row=5, column=0, columnspan=3, pady=5)

        # Botão Adicionar
        ctk.CTkButton(
            self,
            text="Adicionar",
            border_width=2,
            border_color="#0A0A0A",
            command=self.salva_vales
        ).grid(row=6, column=0, columnspan=3, pady=(5, 100))

        # ID do sócio
        self.id_socio = ctk.CTkEntry(
            self,
            placeholder_text="ID sócio",
            border_width=2,
            border_color="#080808",
            width=65,
            height=30
        )
        self.id_socio.grid(row=0, column=0, pady=(20, 80), padx=(2, 80))

        ctk.CTkButton(
            self,
            text="OK",
            border_width=2,
            border_color="#0A0A0A",
            width=35,
            height=25,
            command=self.trazer_dados_id_vales
        ).grid(row=0, column=0, pady=(20, 80), padx=(50, 10))

        # Foto do sócio
        self.lbl_foto_socio = ctk.CTkLabel(
            self,
            text="",
            width=20,
            height=20
        )
        self.lbl_foto_socio.grid(row=0, column=2, pady=(5, 8), padx=10)

        # Nome do sócio
        self.lbl_nome_socio = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 20, "bold"),
            text_color="#F3EFEF"
        )
        self.lbl_nome_socio.grid(row=6, column=0, pady=(5, 50))

    def salva_vales(self):

        motivo = self.motivo_do_vale.get().strip()
        valor_do_vale = self.valor_do_vale.get().strip()
        e_mail = self.email_do_socio.get().strip()
        descricao = self.textbox_descricao_vale.get("1.0", "end").strip()
        id_socio = self.id_socio.get().strip()

        # Validação
        if not valor_do_vale or not descricao or not e_mail:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                "❌ Preencha todos os campos!",
                erro=True
            )
            return

        try:
            valor = float(valor_do_vale)

            if valor <= 0:
                self.mostrar_mensagem(
                    self.label_mensagem_vale,
                    "❌ O valor deve ser maior que zero!",
                    erro=True
                )
                return

        except ValueError:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                "❌ Valor inválido!",
                erro=True
            )
            return

        # Salvar vale
        try:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                "💾 Salvando vale...",
                erro=False
            )
            self.app.root.update_idletasks()

            banco.adicionar_vale(
                id_socio,
                valor,
                descricao
            )

        except Exception as e:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                f"❌ Erro ao salvar vale:\n{e}",
                erro=True
            )
            return

        # Enviar e-mail
        try:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                "📧 Enviando notificação por e-mail...",
                erro=False
            )
            self.app.root.update_idletasks()

            self.app.servico_email.enviar_notificacao_vale(
                id_socio,
                valor,
                motivo,
                e_mail
            )

        except Exception as e:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                f"⚠️ Vale salvo, mas o e-mail não foi enviado.\n{e}",
                erro=True
            )

        # Atualizar interface
        self.mostrar_mensagem(
            self.label_mensagem_vale,
            "🔄 Atualizando informações...",
            erro=False
        )
        self.app.root.update_idletasks()

        self.app.atualizar_dashboard()
        self.atualizar_pagina_vale()

        # Finalizado
        self.mostrar_mensagem(
            self.label_mensagem_vale,
            "✅ Vale cadastrado com sucesso!",
            erro=False
        )

    def trazer_dados_id_vales(self):
        id_socio = self.id_socio.get().strip()

        if not id_socio:
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                "Informe o ID do sócio!",
                erro=True
            )
            return

        if not banco.verificar_id(id_socio):
            self.mostrar_mensagem(
                self.label_mensagem_vale,
                "ID inválido!",
                erro=True
            )
            return

        dados = banco.buscar_dados_socio(id_socio)

        self.email_do_socio.delete(0, "end")
        self.email_do_socio.insert(0, dados["email"] or "")

        self.app.frame_perfil.mostrar_foto(
            id_socio,
            self.lbl_foto_socio
        )

        self.lbl_nome_socio.configure(
            text=dados["nome"]
        )
    