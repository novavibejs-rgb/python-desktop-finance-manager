from datetime import datetime, timedelta


class Utils:

    # =====================================================
    # 🔧 PARSER INTERNO
    # =====================================================

    @staticmethod
    def _parse_data(data):
        """
        Converte string ou datetime para objeto datetime.
        """

        if isinstance(data, datetime):
            return data

        if not isinstance(data, str):
            return None

        formatos = (
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y",
            "%d/%m/%Y %H:%M"
        )

        for formato in formatos:
            try:
                return datetime.strptime(data, formato)
            except ValueError:
                pass

        return None

    # =====================================================
    # 📅 DATAS
    # =====================================================

    @staticmethod
    def data_banco():
        """Retorna a data atual no formato do banco."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def data_sql(data, hora=False):
        """
        Converte uma data para o formato SQL.
        """

        dt = Utils._parse_data(data)

        if not dt:
            return ""

        if hora:
            return dt.strftime("%Y-%m-%d %H:%M:%S")

        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def data_br(data, hora=False):
        """
        Converte para formato brasileiro.
        """

        dt = Utils._parse_data(data)

        if not dt:
            return ""

        if hora:
            return dt.strftime("%d/%m/%Y %H:%M")

        return dt.strftime("%d/%m/%Y")

    @staticmethod
    def apenas_data_br(data):
        """
        Retorna somente a data em formato brasileiro.
        """

        dt = Utils._parse_data(data)

        if not dt:
            return ""

        return dt.strftime("%d/%m/%Y")

    # =====================================================
    # 💰 FORMATAÇÃO
    # =====================================================

    @staticmethod
    def moeda(valor):
        """Formata moeda brasileira."""

        try:
            valor = float(valor)
            return (
                f"R$ {valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        except (ValueError, TypeError):
            return "R$ 0,00"

    @staticmethod
    def relogio_atual():
        """Data e hora para interface."""
        return datetime.now().strftime("%d/%m/%Y | %H:%M:%S")

    # =====================================================
    # 📅 SEMANA
    # =====================================================

    @staticmethod
    def intervalo_semana_dt():
        """
        Retorna início e fim da semana como datetime.
        """

        hoje = datetime.now()

        inicio = hoje - timedelta(days=hoje.weekday())
        inicio = inicio.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        fim = inicio + timedelta(days=6)
        fim = fim.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999
        )

        return inicio, fim

    @staticmethod
    def inicio_semana():
        """Retorna o início da semana."""
        return Utils.intervalo_semana_dt()[0]

    @staticmethod
    def fim_semana():
        """Retorna o fim da semana."""
        return Utils.intervalo_semana_dt()[1]

    @staticmethod
    def intervalo_semana_sql():
        """
        Retorna o início e fim da semana em formato SQL.
        """
        inicio, fim = Utils.intervalo_semana_dt()

        return (
            Utils.data_sql(inicio, hora=True),
            Utils.data_sql(fim, hora=True)
        )

    @staticmethod
    def gerar_semana_vazia():
        """
        Retorna um dicionário com os sete dias da semana.
        """

        inicio = Utils.inicio_semana()

        return {
            (inicio + timedelta(days=i)).strftime("%Y-%m-%d"): 0
            for i in range(7)
        }

    @staticmethod
    def nomes_dias_semana():
        """Nomes abreviados dos dias da semana."""

        return [
            "Seg",
            "Ter",
            "Qua",
            "Qui",
            "Sex",
            "Sáb",
            "Dom"
        ]