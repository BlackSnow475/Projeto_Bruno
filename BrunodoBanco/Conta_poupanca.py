from CONTAS import Conta

class ContaPoupanca(Conta):
    def __init__(self, saldo, limite):
        super().__init__(saldo, limite)
        self.tipo = 'Conta Poupança'

    def atualiza(self):
        self._saldo += self._saldo * self.banco.taxajuros
        return self._saldo
