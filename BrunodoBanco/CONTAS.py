from geradorid import GeradorID

class Conta:
    def __init__(self, saldo, limite):
        self._titular = ''
        self._saldo = saldo
        self._limite = limite
        self._id = GeradorID.gerar_id()
        self._extrato = []
        self._status = True
        self.banco = ''

    @property
    def id(self):
        return self._id

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def set_saldo(self, value):
        self._saldo = value
        pass

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, value):
        self._titular = value

    @property
    def status(self):
        return self._status

    def __str__(self):
        return f'{self.titular}, {self.saldo}'

    def saque(self, valor):
        if self._saldo < valor:
            return False
        else:
            self._saldo -= valor
            string = "Saque de %.2f" % (float(valor))
            self._extrato.append(string)
            return True

    def deposita(self, valor):
        self._saldo += valor
        string = "Deposito de " + str(valor)
        self._extrato.append(string)