from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from PIL import Image,ImageDraw
from matplotlib.figure import Figure
import customtkinter as ctk
import banco
from email_service import  ServicoEmail
from utils import Utils
from Theme import Tema


class App:
# ==========================================================
# CONSTRUTOR
# ==========================================================
    def __init__(self):
    
        # SERVIÇOS
        # ==========================================================
        self.servico_email = ServicoEmail()

        
        # CONFIGURAÇÃO DA JANELA
        # ==========================================================
        self.configurar_janela()
        self.configurar_grid()

    
        # ESTRUTURA PRINCIPAL
        # ==========================================================
        self.criar_top_bar()
        self.criar_menu()
        self.criar_content()
        self.criar_frames()

        
        # TELAS
        # ==========================================================
        self.criar_inicio()
        self.criar_perfil()
        self.criar_servico()
        self.criar_vale()

    
        # TELA INICIAL
        # ==========================================================
        self.mostrar_inicio()

    
        # ATUALIZAÇÕES AUTOMÁTICAS
        # ==========================================================
        self.atualizar_relogio()
        self.atualizar_dashboard()

        # INICIAR APLICAÇÃO
        # ==========================================================
        self.root.mainloop()
   
# ==========================================================
# CONFIGURAÇÃO DA JANELA (chamadas do __init__)
# ==========================================================

    def configurar_janela(self):

        self.root = ctk.CTk()
        self.root.title("IRMÃOS J Sistema Financeiro",)
        self.root.geometry("800x520")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#0E36A3")
    
    def configurar_grid(self):
        # ===== CONFIG GRID PRINCIPAL =====
        self.root.grid_rowconfigure(0, weight=0)  # topo
        self.root.grid_rowconfigure(1, weight=1)  # conteúdo

        self.root.grid_columnconfigure(0, minsize=200)
        self.root.grid_columnconfigure(1, weight=1)  # dashboard

    def criar_top_bar(self):
         # ===== TOP BAR (RELÓGIO) =====
        self.top_frame = ctk.CTkFrame(self.root, fg_color="#686666",border_width=3,border_color="#0A0A0A")
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.relogio_label = ctk.CTkLabel(
            self.top_frame,
            text="relogio",
            font=("Segoe UI Emoji", 24,),
            text_color="#F8F5F5"
        )
        self.relogio_label.pack(pady=10)

    def criar_menu(self):
        self.menu_frame = ctk.CTkFrame(
            self.root,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D",
            width=250
        )
        self.menu_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.menu_frame.grid_propagate(False)

        ctk.CTkLabel(
            self.menu_frame,
            text="MENU",
            font=("Arial", 30, "bold"),
            text_color="#0A0404"
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu_frame,
            text="Início",
            border_width=2,
            border_color="#0D0E0D",
            text_color="#0D0E0D",
            fg_color="#0E36A3",
            command=self.mostrar_inicio
        ).pack(pady=20)

        ctk.CTkButton(
            self.menu_frame,
            text="Perfil",
            border_width=2,
            border_color="#0A0A0A",
            text_color="#0A0A0A",
            fg_color="#0E36A3",
            command=self.mostrar_perfil
        ).pack(pady=20)

        ctk.CTkButton(
            self.menu_frame,
            text="Adicionar serviço",
            border_width=2,
            border_color="#0A0A0A",
            text_color="#0A0A0A",
            fg_color="#0E36A3",
            command=self.mostrar_servico
        ).pack(pady=20)

        ctk.CTkButton(
            self.menu_frame,
            text="Fazer vale",
            border_width=2,
            border_color="#0A0A0A",
            text_color="#0A0A0A",
            fg_color="#0E36A3",
            command=self.mostrar_vale
        ).pack(pady=20)

    def criar_content(self):

        self.content_frame = ctk.CTkFrame(self.root)

        self.content_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def criar_frames(self):
        self.frame_inicio = ctk.CTkFrame(
            self.content_frame,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        self.frame_perfil = ctk.CTkFrame(
            self.content_frame,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        self.frame_servico = ctk.CTkFrame(
            self.content_frame,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        self.frame_vale = ctk.CTkFrame(
            self.content_frame,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        for frame in (
            self.frame_inicio,
            self.frame_perfil,
            self.frame_servico,
            self.frame_vale,
        ):
            frame.grid(row=0, column=0, sticky="nsew")

# ==========================================================
# EXIBIÇÃO DAS TELAS
# ==========================================================
    
    def mostrar_servico(self):
        self.frame_servico.tkraise()

    def mostrar_vale(self):
        self.frame_vale.tkraise()
        
    def mostrar_perfil(self):
        self.frame_perfil.tkraise()
        
    def mostrar_inicio(self):
        self.frame_inicio.tkraise()

    def criar_menu(self):
        self.menu_frame = ctk.CTkFrame(
            self.root,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D",
            width=250
        )
        self.menu_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.menu_frame.grid_propagate(False)

        ctk.CTkLabel(
            self.menu_frame,
            text="MENU",
            font=("Arial", 30, "bold"),
            text_color="#0A0404"
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu_frame,
            text="Início",
            border_width=2,
            border_color="#0D0E0D",
            text_color="#0D0E0D",
            fg_color="#0E36A3",
            command=self.mostrar_inicio
        ).pack(pady=20)

        ctk.CTkButton(
            self.menu_frame,
            text="Perfil",
            border_width=2,
            border_color="#0A0A0A",
            text_color="#0A0A0A",
            fg_color="#0E36A3",
            command=self.mostrar_perfil
        ).pack(pady=20)

        ctk.CTkButton(
            self.menu_frame,
            text="Adicionar serviço",
            border_width=2,
            border_color="#0A0A0A",
            text_color="#0A0A0A",
            fg_color="#0E36A3",
            command=self.mostrar_servico
        ).pack(pady=20)

        ctk.CTkButton(
            self.menu_frame,
            text="Fazer vale",
            border_width=2,
            border_color="#0A0A0A",
            text_color="#0A0A0A",
            fg_color="#0E36A3",
            command=self.mostrar_vale
        ).pack(pady=20)

# ==========================================================
# CRIAÇÃO DAS TELAS
# ==========================================================

    def criar_inicio(self):
        self.rd_pe = ctk.CTkFrame(self.frame_inicio, fg_color="#20B960", height=100)
        self.rd_pe.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            self.rd_pe,
            text="💰 Saldo Total",
            font=("Arial", 25, "bold"),
            text_color="#0D0C0E"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.lbl_saldo_total = ctk.CTkLabel(
            self.rd_pe,
            text="R$ 0",
            font=("Arial", 25, "bold"),
            text_color="#FCF8F8"
        )
        self.lbl_saldo_total.grid(row=1, column=0, padx=10)
        

        ctk.CTkLabel(
            self.rd_pe,
            text="📥 Reserva",
            font=("Arial", 25, "bold"),
            text_color="#0D0C0E"
        ).grid(row=0, column=1, padx=10)

        self.lbl_reserva = ctk.CTkLabel(
            self.rd_pe,
            text="R$ 0,00",
            font=("Arial", 25, "bold"),
            text_color="#FCF8F8"
        )
        self.lbl_reserva.grid(row=1, column=1)
        

        ctk.CTkLabel(
            self.rd_pe,
            text="📈 Lucro Líquido",
            font=("Arial", 25, "bold"),
            text_color="#0D0C0E"
        ).grid(row=0, column=2, padx=10)

        self.lbl_lucro = ctk.CTkLabel(
            self.rd_pe,
            text="R$ 0,00",
            font=("Arial", 25, "bold"),
            text_color="#FCF8F8"
        )
        self.lbl_lucro.grid(row=1, column=2)

        # gráfico
        dias, valores = banco.buscar_faturamento_semanal()

        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Faturamento da Semana")
        self.ax.bar(dias, valores)


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_inicio)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, pady=10)

    def criar_perfil(self):

        ctk.CTkLabel(
            self.frame_perfil,
            text="Perfil do Usuário",
            font=("Arial", 30, "bold"),
            text_color="#0D0C0E"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        self.cards = {}

        conn = banco.conectar()
        cursor = conn.cursor()

        # Busca no máximo 2 sócios
        cursor.execute("SELECT id FROM socios ORDER BY id LIMIT 2")
        socios = cursor.fetchall()

        conn.close()

        for coluna, (id_socio,) in enumerate(socios):
            self.cards[id_socio] = self.criar_card_socio(
                col=coluna,
                id_socio=id_socio
            )

            self.frame_perfil.grid_columnconfigure(coluna, weight=1)
    
    def criar_servico(self):
            
        ctk.CTkLabel(
        self.frame_servico,
        text="Adicionar Serviço",
        font=("Arial", 30, "bold"),
        text_color="#080808"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Entradas
        self.entry_nome = ctk.CTkEntry(
        self.frame_servico,
        placeholder_text="Nome",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_nome.grid(row=1, column=0, padx=10, pady=7)

        self.entry_valor = ctk.CTkEntry(
        self.frame_servico,
        placeholder_text="Valor",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_valor.grid(row=1, column=1, padx=10, pady=7)

        self.entry_servico = ctk.CTkEntry(
        self.frame_servico,
        placeholder_text="Serviço",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_servico.grid(row=2, column=0, padx=10, pady=7)

        self.entry_pagamento = ctk.CTkEntry(
        self.frame_servico,
        placeholder_text="Forma de pagamento",
        border_width=2,
        border_color="#0A0A0A",
        width=200,
        height=30
        )
        self.entry_pagamento.grid(row=2, column=1, padx=10, pady=7)

        # Configuração das colunas
        self.frame_servico.grid_columnconfigure(0, weight=1)
        self.frame_servico.grid_columnconfigure(1, weight=1)

        # Descrição
        ctk.CTkLabel(
        self.frame_servico,
        text="Descrição",
        font=("Arial", 15, "bold"),
        text_color="#080808"
        ).grid(row=3, column=0, columnspan=2, pady=7)

        self.textbox_descricao = ctk.CTkTextbox(
        self.frame_servico,
        border_width=2,
        border_color="#0A0A0A",
        width=420,
        height=80
        )
        self.textbox_descricao.grid(row=4, column=0, columnspan=2, pady=5)

        # Mensagem
        self.label_mensagem_serviço = ctk.CTkLabel(
        self.frame_servico,
        text="",
        font=("Arial", 14, "bold")
        )
        self.label_mensagem_serviço.grid(row=5, column=0, columnspan=2, pady=5)

        # Botão
        ctk.CTkButton(
        self.frame_servico,
        text="Adicionar",
        border_width=2,
        border_color="#0A0A0A",
        command=self.salvar_servico
        ).grid(row=6, column=0, columnspan=2, pady=20)

    def criar_vale(self):
    
        ctk.CTkLabel(
            self.frame_vale,
            text="Fazer Vale",
            font=("Arial", 30, "bold"),  
            text_color="#080808"
        ).grid(row=0, column=0, columnspan=3, pady=(15,80))

        # Nome
        self.motivo_do_vale = ctk.CTkEntry(

            self.frame_vale,
            placeholder_text="motivo",
            border_width=2,
            border_color="#0A0A0A",
            width=150,
            height=30
        )
        self.motivo_do_vale.grid(row=2, column=0, padx=15)

        # Valor
        self.valor_do_vale = ctk.CTkEntry(
            self.frame_vale,
            placeholder_text="Valor",
            border_width=2,
            border_color="#0A0A0A",
            width=150,
            height=30
        )
        self.valor_do_vale.grid(row=2, column=1, padx=15)

        # E-mail
        self.email_do_socio = ctk.CTkEntry(
            self.frame_vale,
            placeholder_text="E-mail",
            border_width=2,
            border_color="#0A0A0A",
            width=150,
            height=30
        )
        self.email_do_socio.grid(row=2, column=2, padx=15)

        # Descrição
        ctk.CTkLabel(
            self.frame_vale,
            text="Descrição",
            font=("Arial", 15, "bold"),
            text_color="#080808"
        ).grid(row=3, column=0, columnspan=3, pady=7)

        self.textbox_descricao_vale = ctk.CTkTextbox(
            self.frame_vale,
            border_width=2,
            border_color="#0A0A0A",
            width=350,
            height=80
        )
        self.textbox_descricao_vale.grid(row=4, column=0, columnspan=3, pady=5)

        # Mensagem
        self.label_mensagem_vale = ctk.CTkLabel(
            self.frame_vale,
            text="",
            font=("Arial", 14, "bold")
        )
        self.label_mensagem_vale.grid(row=5, column=0, columnspan=3, pady=5)

        # Botão
        ctk.CTkButton(
            self.frame_vale,
            text="Adicionar",
            border_width=2,
            border_color="#0A0A0A",
            command=self.salva_vales
        ).grid(row=6, column=0, columnspan=3, pady=(5,100))

        self.id_socio = ctk.CTkEntry(
            self.frame_vale,
            placeholder_text="ID socio",
            border_width=2,
            border_color="#080808",
            width=65,
            height=30
        )
        self.id_socio.grid(row=0,column=0,pady=(20,80),padx=(2,80))

        ctk.CTkButton(
            self.frame_vale,
            text="ok",
            border_width=2,
            border_color="#0A0A0A",
            width=35,
            height=25,
            command=self.trazer_dados_id_vales
        ).grid(row=0,column=0,pady=(20,80),padx=(50,10))

        #imagem do Id informado
        self.lbl_foto_socio = ctk.CTkLabel(
            self.frame_vale,
            text="",
            width=20,
            height=20
        )
        self.lbl_foto_socio.grid(row=0, column=2,pady=(5,8),padx=(10,10))

        # nome socio
        self.lbl_nome_socio = ctk.CTkLabel(
            self.frame_vale,
            text="",
            font=("Arial", 20, "bold"),
            text_color="#F3EFEF"
        )
        self.lbl_nome_socio.grid(row=6, column=0, pady=(5,50))


# ==========================================================
# CRIAÇÃO DOS COMPONENTES
# ==========================================================

    def criar_card_socio(self, col, id_socio):

        card = ctk.CTkFrame(
            self.frame_perfil,
            width=200,
            height=350,
            fg_color="#0E36A3",
            corner_radius=10,
            border_width=3,
            border_color="#0D0E0D"
        )
        card.grid(row=1, column=col, padx=20, pady=10)
        card.grid_propagate(False)

        lbl_foto = ctk.CTkLabel(
            card,
            text="Adicionar\nFoto",
            width=150,
            height=150
        )
        lbl_foto.grid(row=0, column=0, padx=25, pady=15)

        btn = ctk.CTkButton(
            card,
            text="Alterar foto",
            fg_color="transparent",
            text_color="#030303",
            hover=False,
            command=lambda: self.escolher_foto(id_socio)
        )
        btn.grid(row=1, column=0)

        lbl_nome = ctk.CTkLabel(card, text="...",font=("Arial", 20, "bold"),text_color="#F3EFEF")
        lbl_nome.grid(row=2, column=0, pady=(10, 5))

        lbl_saldo = ctk.CTkLabel(card, text="💰 saldo: R$ 0,00",font=("Arial", 20, "bold"),text_color="#F3EFEF")
        lbl_saldo.grid(row=3, column=0,pady=5)

        lbl_vale = ctk.CTkLabel(card, text="📝 vale: R$ 0,00",font=("Arial", 20, "bold"),text_color="#F3EFEF")
        lbl_vale.grid(row=4, column=0,pady=(5,15))

        return {
            "card": card,
            "foto": lbl_foto,
            "nome": lbl_nome,
            "saldo": lbl_saldo,
            "vale": lbl_vale
        }



# ==========================================================
# FOTOS DOS SÓCIOS
# ==========================================================

    def escolher_foto(self, id_socio):
        caminho = filedialog.askopenfilename(
            title="Escolha uma foto",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )


        if caminho:
            conn = banco.conectar()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE socios SET foto=? WHERE id=?",
                (caminho, id_socio)
            )

            conn.commit()
            conn.close()

            self.mostrar_foto(id_socio, self.cards[id_socio]["foto"])

    def mostrar_foto(self, id_socio, label=None):
        conn = banco.conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT foto FROM socios WHERE id=?",
            (id_socio,)
        )

        resultado = cursor.fetchone()
        conn.close()

        # Se não foi informado um label, usa o do card
        if label is None:
            label = self.cards[id_socio]["foto"]

        if resultado and resultado[0]:
            foto = self.criar_foto_redonda(resultado[0])

            label.configure(image=foto, text="")
            label.image = foto
        else:
            label.configure(image=None, text="Adicionar\nFoto")
            label.image = None
    
    def criar_foto_redonda(self,caminho):
        tamanho = 120
        borda = 8
        tamanho_total = tamanho + borda * 2

        # Foto
        foto = Image.open(caminho).convert("RGBA")
        foto = foto.resize((tamanho, tamanho))

        # Máscara circular
        mascara = Image.new("L", (tamanho, tamanho), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, tamanho, tamanho), fill=255)

        foto_redonda = Image.new("RGBA", (tamanho, tamanho))
        foto_redonda.paste(foto, (0, 0), mascara)

        # Moldura
        imagem_final = Image.new("RGBA", (tamanho_total, tamanho_total), (0, 0, 0, 0))
        draw = ImageDraw.Draw(imagem_final)

        draw.ellipse(
            (0, 0, tamanho_total-1, tamanho_total-1),
            outline="#0A0708",
            width=5
        )

        imagem_final.paste(foto_redonda, (borda, borda), foto_redonda)

        return ctk.CTkImage(
            light_image=imagem_final,
            dark_image=imagem_final,
            size=(tamanho_total, tamanho_total)
        )


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================
    
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

        self.mostrar_foto(id_socio,self.lbl_foto_socio)
        self.lbl_nome_socio.configure(text= dados["nome"])
      
    def mostrar_mensagem(self, label, texto, erro=False):
        cor = "#850202" if erro else "#13E75A"

        label.configure(
            text=texto,
            text_color=cor
        )

        label.after(
            3000,
            lambda: label.configure(text="")
        )


# ==========================================================
# SALVAMENTO DOS DADOS
# ==========================================================
 
    def salvar_servico(self):
        nome_cliente = self.entry_nome.get().strip()
        servico = self.entry_servico.get().strip()
        descricao = self.textbox_descricao.get("1.0", "end").strip()
        forma_pagamento = self.entry_pagamento.get().strip()
        valor_texto = self.entry_valor.get().strip()

        if not nome_cliente or not servico or not valor_texto or not forma_pagamento:
            self.mostrar_mensagem(self.label_mensagem_serviço,"Erro: Preencha todos os campos!", erro=True)
            return

        
        try:
            valor = float(valor_texto)
            if valor <= 0:
                self.mostrar_mensagem(self.label_mensagem_serviço,"Erro: O valor deve ser maior que zero!", erro=True)
                return
        except ValueError:
            self.mostrar_mensagem(self.label_mensagem_serviço,"Erro: Valor inválido! 💥", erro=True)
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


        self.mostrar_mensagem(self.label_mensagem_serviço,"serviço salvo com sucesso ✅",erro=False)
        
        self.atualizar_dashboard()
    
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
                erro=None
            )
            self.update_idletasks()

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
                erro=None
            )
            self.update_idletasks()

            self.servico_email.enviar_notificacao_vale(
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
            erro=None
        )
        self.update_idletasks()

        self.atualizar_dashboard()
        self.atualizar_pagina_vale()

        # Finalizado
        self.mostrar_mensagem(
            self.label_mensagem_vale,
            "✅ Vale cadastrado com sucesso!",
            erro=None
        )


# ==========================================================
# ATUALIZAÇÃO DA INTERFACE
# ==========================================================

    def atualizar_relogio(self):
        agora = Utils.relogio_atual()
        self.relogio_label.configure(text=agora)
        self.root.after(1000, self.atualizar_relogio)
    
    def atualizar_dashboard(self):

        faturamento = banco.faturamento_semana()

        reserva = faturamento * 0.20
        lucro = faturamento - reserva

        self.lbl_saldo_total.configure(text=f"R$ {faturamento:.2f}")
        self.lbl_reserva.configure(text=f"R$ {reserva:.2f}")
        self.lbl_lucro.configure(text=f"R$ {lucro:.2f}")

        saldo_socios = lucro / 2

        # Atualiza informações de cada sócio
        socios = banco.listar_socios()

        for socio in socios:

            if socio["id"] not in self.cards:
                continue

            card = self.cards[socio["id"]]

            # Nome
            card["nome"].configure(text=socio["nome"])

            # Foto
            self.mostrar_foto(socio["id"])

            # Saldo
            card["saldo"].configure(
                text=f"💰 saldo: R$ {saldo_socios:.2f}"
            )

            # Vale
            card["vale"].configure(
                text=f"📝 vale: R$ {banco.somar_vales_semana(socio['id']):.2f}"
            )

    def atualizar_pagina_vale(self):

        self.motivo_do_vale.delete(0, "end")
        self.valor_do_vale.delete(0, "end")
        self.email_do_socio.delete(0, "end")

        self.textbox_descricao_vale.delete("1.0", "end")
        self.id_socio.delete(0, "end")

        self.lbl_nome_socio.configure(text="")
        self.lbl_foto_socio.configure(image=None, text="")
        self.lbl_foto_socio.image = None
App()   

