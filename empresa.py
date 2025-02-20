

class Empresa:
    def __init__(self, nome, notaConsumidor, notaEmpresa, recRespondidas, volNegocio, indSolucao):
        self.nome = nome
        self.notaConsumidor = self.formatarDados(notaConsumidor)
        self.notaEmpresa = self.formatarDados(notaEmpresa)
        self.recRespondidas = self.formatarDados(recRespondidas)
        self.volNegocio = self.formatarDados(volNegocio)
        self.indSolucao = self.formatarDados(indSolucao)

    def __str__(self):
        return (
            f"Empresa: {self.nome}\n"
            f"Nota do Consumidor: {self.notaConsumidor}\n"
            f"Nota da Empresa: {self.notaEmpresa}\n"
            f"Reclamações Respondidas: {self.recRespondidas}\n"
            f"Voltariam a fazer negócio: {self.volNegocio}\n"
            f"Índice de solução: {self.indSolucao}"
        )

    @staticmethod
    def formatarDados(texto):
        # Tirar os textos excedentes que vieram junto na tag strong
        texto = texto.replace("das reclamações", "").replace(
            "voltariam a fazer negócio.", "").replace("/10", "").replace("recebidas", "").strip()

        texto = texto.rstrip(".")

        return texto
