from datetime import datetime
import json
import os


class Financeiro:
    def __init__(self, arquivo="dados_financeiros.json"):
        self.arquivo = arquivo
        self.dados = self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass

        return self.dados_padrao()

    def dados_padrao(self):
        return {
            "socios": [
                {
                    "id": 1,
                    "nome": "Jhonatan"
                },
                {
                    "id": 2,
                    "nome": "Irmao"
                }
            ],
            "servicos": [],
            "vales": []
        }

    def salvar_dados(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(
                self.dados,
                f,
                indent=2,
                ensure_ascii=False
            )

    # =====================
    # SERVIÇOS
    # =====================

    def adicionar_servico(self, descricao, valor_bruto):
        servico = {
            "id": len(self.dados["servicos"]) + 1,
            "data": datetime.now().isoformat(),
            "descricao": descricao,
            "valor_bruto": valor_bruto,
            "reserva": valor_bruto * 0.20,
            "lucro": valor_bruto * 0.80
        }

        self.dados["servicos"].append(servico)

        self.salvar_dados()

        return servico

    # =====================
    # VALES
    # =====================

    def adicionar_vale(self, nome_socio, valor, motivo):
        vale = {
            "id": len(self.dados["vales"]) + 1,
            "data": datetime.now().isoformat(),
            "nome_socio": nome_socio,
            "valor": valor,
            "motivo": motivo
        }

        self.dados["vales"].append(vale)

        self.salvar_dados()

        return vale

    # =====================
    # CÁLCULOS
    # =====================

    def obter_total_bruto(self):
        return sum(
            servico["valor_bruto"]
            for servico in self.dados["servicos"]
        )

    def obter_total_reserva(self):
        return sum(
            servico["reserva"]
            for servico in self.dados["servicos"]
        )

    def obter_total_lucro(self):
        return sum(
            servico["lucro"]
            for servico in self.dados["servicos"]
        )

    def obter_parte_socio(self):
        return self.obter_total_lucro() / 2

    def obter_total_vales(self, nome_socio):
        return sum(
            vale["valor"]
            for vale in self.dados["vales"]
            if vale["nome_socio"] == nome_socio
        )

    def obter_saldo_socio(self, nome_socio):
        return (
            self.obter_parte_socio()
            - self.obter_total_vales(nome_socio)
        )