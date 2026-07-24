import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw

import banco.banco as banco


class FramePerfil(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(
            master,
            fg_color="#686666",
            border_width=3,
            border_color="#0D0E0D"
        )

        self.app = app

        self.cards = {}

        self.criar_tela()


    def criar_tela(self):

        ctk.CTkLabel(
            self,
            text="Perfil do Usuário",
            font=("Arial", 30, "bold"),
            text_color="#0D0C0E"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10
        )


        conn = banco.conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM socios ORDER BY id LIMIT 2"
        )

        socios = cursor.fetchall()

        conn.close()


        for coluna, (id_socio,) in enumerate(socios):

            self.cards[id_socio] = self.criar_card_socio(
                col=coluna,
                id_socio=id_socio
            )


            self.grid_columnconfigure(
                coluna,
                weight=1
            )

    def criar_card_socio(self, col, id_socio):

        card = ctk.CTkFrame(
            self,
            width=200,
            height=350,
            fg_color="#0E36A3",
            corner_radius=10,
            border_width=3,
            border_color="#0D0E0D"
        )

        card.grid(
            row=1,
            column=col,
            padx=20,
            pady=10
        )

        card.grid_propagate(False)


        lbl_foto = ctk.CTkLabel(
            card,
            text="Adicionar\nFoto",
            width=150,
            height=150
        )

        lbl_foto.grid(
            row=0,
            column=0,
            padx=25,
            pady=15
        )


        btn = ctk.CTkButton(
            card,
            text="Alterar foto",
            fg_color="transparent",
            text_color="#030303",
            hover=False,
            command=lambda: self.escolher_foto(id_socio)
        )

        btn.grid(
            row=1,
            column=0
        )


        lbl_nome = ctk.CTkLabel(
            card,
            text="...",
            font=("Arial",20,"bold"),
            text_color="#F3EFEF"
        )

        lbl_nome.grid(
            row=2,
            column=0,
            pady=10
        )


        lbl_saldo = ctk.CTkLabel(
            card,
            text="💰 saldo: R$ 0,00",
            font=("Arial",20,"bold"),
            text_color="#F3EFEF"
        )

        lbl_saldo.grid(
            row=3,
            column=0
        )


        lbl_vale = ctk.CTkLabel(
            card,
            text="📝 vale: R$ 0,00",
            font=("Arial",20,"bold"),
            text_color="#F3EFEF"
        )

        lbl_vale.grid(
            row=4,
            column=0,
            pady=(5,15)
        )


        return {
            "card": card,
            "foto": lbl_foto,
            "nome": lbl_nome,
            "saldo": lbl_saldo,
            "vale": lbl_vale
        }
        
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

    def atualizar(self):
        
        faturamento = banco.faturamento_semana()
        reserva = faturamento * 0.20
        lucro = faturamento - reserva

        saldo_socios = lucro / 2

        socios = banco.listar_socios()

        for socio in socios:

            if socio["id"] not in self.cards:
                continue

            card = self.cards[socio["id"]]

            card["nome"].configure(text=socio["nome"])

            self.update_idletasks()
            self.mostrar_foto(socio["id"])

            card["saldo"].configure(
                text=f"💰 saldo: R$ {saldo_socios:.2f}"
            )

            card["vale"].configure(
                text=f"📝 vale: R$ {banco.somar_vales_semana(socio['id']):.2f}"
            )