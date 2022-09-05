from CONTAS import Conta

class ContaCorrente(Conta):
    def __init__(self, saldo, limite):
        super().__init__(saldo, limite)
        self.tipo = 'Conta Corrente'

    def saque(self, valor):
        valor = valor + self.banco.taxasaque
        if self._saldo < valor:
            return False
        else:
            self._saldo -= valor
            string = "Saque de %.2f" % (float(valor))
            self._extrato.append(string)
            return True

    def deposita(self, valor):
        self._titular._banco._saldo += self.banco.taxasaque
        self._saldo += valor
        string = "Deposito de " + str(valor)
        self._extrato.append(string)
