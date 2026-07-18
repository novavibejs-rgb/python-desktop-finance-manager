
import customtkinter as ctk
from utils import Utils

from ui.frames.inicio import FrameInicio
from ui.frames.perfil import FramePerfil
from ui.frames.servico import FrameServico
from ui.frames.vale import FrameVale


class App:
# ==========================================================
# CONSTRUTOR
# ==========================================================
    def __init__(self):
    
        # SERVIÇOS
        # ==========================================================

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
        
        self.frame_inicio = FrameInicio(self.content_frame)

        self.frame_perfil = FramePerfil(self.content_frame,self)

        self.frame_servico = FrameServico(self.content_frame,self)

        self.frame_vale = FrameVale(self.content_frame,self)

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

  
# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================
    
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
# ATUALIZAÇÃO DA INTERFACE
# ==========================================================

    def atualizar_relogio(self):
        agora = Utils.relogio_atual()
        self.relogio_label.configure(text=agora)
        self.root.after(1000, self.atualizar_relogio)
    
    def atualizar_dashboard(self):
        self.frame_inicio.atualizar()
        self.frame_perfil.atualizar()