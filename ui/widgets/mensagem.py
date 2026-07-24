import customtkinter as ctk


class Mensagem:

    @staticmethod
    def mostrar(label, texto, erro=False):

        cor = "#850202" if erro else "#13E75A"

        label.configure(
            text=texto,
            text_color=cor
        )

        label.after(
            3000,
            lambda: label.configure(text="")
        )