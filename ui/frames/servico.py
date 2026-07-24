import customtkinter as ctk

import banco.banco as banco
from serviços.email_service import ServicoEmail
from ui.widgets.mensagem import Mensagem



class FrameServico(ctk.CTkFrame):

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
        text="Adicionar Serviço",
        font=("Arial", 30, "bold"),
        text_color="#080808"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Entradas
        self.entry_nome = ctk.CTkEntry(
        self,
        placeholder_text="Nome",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_nome.grid(row=1, column=0, padx=10, pady=7)

        self.entry_valor = ctk.CTkEntry(
        self,
        placeholder_text="Valor",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_valor.grid(row=1, column=1, padx=10, pady=7)

        self.entry_servico = ctk.CTkEntry(
        self,
        placeholder_text="Serviço",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_servico.grid(row=2, column=0, padx=10, pady=7)

        self.entry_pagamento = ctk.CTkEntry(
        self,
        placeholder_text="Forma de pagamento",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_pagamento.grid(row=2, column=1, padx=10, pady=7)

        # Configuração das colunas
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Descrição
        ctk.CTkLabel(
        self,
        text="Descrição",
        font=("Arial", 15, "bold"),
        text_color="#080808"
        ).grid(row=3, column=0, columnspan=2, pady=7)

        self.textbox_descricao = ctk.CTkTextbox(
        self,
        border_width=2,
        border_color="#0A0A0A",
        width=420,
        height=80
        )
        self.textbox_descricao.grid(row=4, column=0, columnspan=2, pady=5)

        # Mensagem
        self.label_mensagem_serviço = ctk.CTkLabel(
        self,
        text="",
        font=("Arial", 14, "bold")
        )
        self.label_mensagem_serviço.grid(row=5, column=0, columnspan=2, pady=5)

        # Botão
        ctk.CTkButton(
        self,
        text="Adicionar",
        border_width=2,
        border_color="#0A0A0A",
        command=self.salvar_servico
        ).grid(row=6, column=0, columnspan=2, pady=20)
    
    def salvar_servico(self):
        nome_cliente = self.entry_nome.get().strip()
        servico = self.entry_servico.get().strip()
        descricao = self.textbox_descricao.get("1.0", "end").strip()
        forma_pagamento = self.entry_pagamento.get().strip()
        valor_texto = self.entry_valor.get().strip()

        if not nome_cliente or not servico or not valor_texto or not forma_pagamento:
            Mensagem.mostrar(
                self.label_mensagem_serviço,
                "Erro: Preencha todos os campos!",
                erro=True
            )
            return

        try:
            valor = float(valor_texto)

            if valor <= 0:
                Mensagem.mostrar(
                    self.label_mensagem_serviço,
                    "Erro: O valor deve ser maior que zero!",
                    erro=True
                )
                return

        except ValueError:
            Mensagem.mostrar(
                self.label_mensagem_serviço,
                "Erro: Valor inválido! 💥",
                erro=True
            )
            return


        banco.adicionar_servico(
            nome_cliente,
            servico,
            descricao,
            valor,
            forma_pagamento
        )


        self.servico_email.enviar_notificacao_servico(
            nome_cliente,
            valor,
            servico,
            forma_pagamento,
            descricao
        )


        self.entry_nome.delete(0, "end")
        self.entry_servico.delete(0, "end")
        self.entry_valor.delete(0, "end")
        self.entry_pagamento.delete(0, "end")
        self.textbox_descricao.delete("1.0", "end")


        Mensagem.mostrar(
            self.label_mensagem_serviço,
            "Serviço salvo com sucesso ✅",
            erro=False
        )
