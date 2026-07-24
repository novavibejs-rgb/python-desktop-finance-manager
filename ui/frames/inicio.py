import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import banco.banco as banco


class FrameInicio(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        self.criar_tela()


    def criar_tela(self):

        self.grid_columnconfigure(0, weight=1)

        self.rd_pe = ctk.CTkFrame(
            self,
            fg_color="#20B960",
            height=100
        )

        self.rd_pe.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=10
        )

        # SALDO TOTAL
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

        # RESERVA
        ctk.CTkLabel(
            self.rd_pe,
            text="📥 Reserva",
            font=("Arial", 25, "bold"),
            text_color="#0D0C0E"
        ).grid(row=0, column=1, padx=10, pady=10)

        self.lbl_reserva = ctk.CTkLabel(
            self.rd_pe,
            text="R$ 0,00",
            font=("Arial", 25, "bold"),
            text_color="#FCF8F8"
        )

        self.lbl_reserva.grid(row=1, column=1, padx=10)

        # LUCRO
        ctk.CTkLabel(
            self.rd_pe,
            text="📈 Lucro Líquido",
            font=("Arial", 25, "bold"),
            text_color="#0D0C0E"
        ).grid(row=0, column=2, padx=10, pady=10)

        self.lbl_lucro = ctk.CTkLabel(
            self.rd_pe,
            text="R$ 0,00",
            font=("Arial", 25, "bold"),
            text_color="#FCF8F8"
        )

        self.lbl_lucro.grid(row=1, column=2, padx=10)

        # ==========================
        # GRÁFICO
        # ==========================
        dias, valores = banco.buscar_faturamento_semanal()

        self.fig = Figure(figsize=(5, 3), dpi=100)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Faturamento da Semana")
        self.ax.bar(dias, valores)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().grid(
            row=1,
            column=0,
            columnspan=3,
            padx=10,
            pady=10,
            sticky="nsew"
        )

    def atualizar(self):

        faturamento = banco.faturamento_semana()
        reserva = faturamento * 0.20
        lucro = faturamento - reserva

        self.lbl_saldo_total.configure(text=f"R$ {faturamento:,.2f}")
        self.lbl_reserva.configure(text=f"R$ {reserva:,.2f}")
        self.lbl_lucro.configure(text=f"R$ {lucro:,.2f}")