from datetime import datetime, timedelta


class Utils:

    # =========================
    # 📅 DATA (BANCO)
    # =========================
    @staticmethod
    def data_banco():
        """Data atual no formato do SQLite."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =========================
    # 🔧 PARSER INTERNO SEGURO
    # =========================
    @staticmethod
    def _parse_data(data):
        """
        Converte diferentes formatos de data
        para datetime de forma segura.
        """

        if not data:
            return None

        formatos = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y"
        ]

        for f in formatos:
            try:
                return datetime.strptime(data, f)
            except ValueError:
                continue

        return None

    # =========================
    # 🇧🇷 DATA COMPLETA BR
    # =========================
    @staticmethod
    def data_br(data):
        """
        Converte:
        2026-06-27 14:35:12
        -> 27/06/2026 14:35
        """

        dt = Utils._parse_data(data)
        if not dt:
            return ""

        return dt.strftime("%d/%m/%Y %H:%M")

    # =========================
    # 📆 SÓ DATA BR
    # =========================
    @staticmethod
    def apenas_data_br(data):
        """
        Converte:
        2026-06-27 14:35:12
        -> 27/06/2026
        """

        dt = Utils._parse_data(data)
        if not dt:
            return ""

        return dt.strftime("%d/%m/%Y")

    # =========================
    # 💰 MOEDA BR
    # =========================
    @staticmethod
    def moeda(valor):
        """
        1200.5 -> R$ 1.200,50
        """

        try:
            valor = float(valor)
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "R$ 0,00"
        
    #==========================
    #⏰ Relogio Atual
    #==========================
    @staticmethod
    def relogio_atual():
        """Retorna data + hora formatada para UI."""
        return datetime.now().strftime("%d/%m/%Y  |  %H:%M:%S")
    
    #==========================
    #⏰ Semana Atual Inicio
    #==========================
    @staticmethod
    def inicio_semana():
            """
            Retorna o início da semana (segunda-feira 00:00:00)
            no formato do banco.
            """
            hoje = datetime.now()

            inicio = hoje - timedelta(days=hoje.weekday())
            inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)

            return inicio.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def intervalo_semana():
        hoje = datetime.now()

        inicio = hoje - timedelta(days=hoje.weekday())
        inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)

        fim = inicio + timedelta(days=6)
        fim = fim.replace(hour=23, minute=59, second=59, microsecond=999999)

        return inicio, fim

    @staticmethod
    def nomes_dias_semana():
        return ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    @staticmethod
    def gerar_semana_vazia():
        inicio, _ = Utils.intervalo_semana()

        return {
            (inicio + timedelta(days=i)).strftime("%Y-%m-%d"): 0
            for i in range(7)
        }