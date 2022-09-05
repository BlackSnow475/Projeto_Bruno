from Conta_poupanca import ContaPoupanca

class Banco:
    listaBancos = []
    numero = 1
    def __init__(self, nome, taxajuros, taxasaque):
        self._numero = Banco.numero
        self._nome = nome
        self._taxajuros = taxajuros
        self._taxasaque = taxasaque
        self._saldo = 0
        self._vetClientes = []

    @property
    def get_numero(self):
        return self._numero

    @property
    def nome(self):
        return self._nome

    @property
    def set_nome(self, value):
        self._nome = value

    @property
    def saldo(self):
        self._saldo = 0
        for i in range(len(self._vetClientes)):
            if self._vetClientes[i].conta != None:
                self._saldo += self._vetClientes[i].conta.saldo
        return self._saldo

    @saldo.setter
    def set_saldo(self, value):
        self._saldo = value

    @property
    def taxajuros(self):
        return self._taxajuros

    @property
    def set_taxajuros(self, value):
        self._taxajuros = value

    @property
    def taxasaque(self):
        return self._taxasaque

    @property
    def set_taxasaque(self, value):
        self._taxasaque = value

    def cadastrar_cliente(self, cliente):
        self._vetClientes.append(cliente)
        cliente._banco = self

    def atualizar_contas(self):
        for i in range(len(self._vetClientes)):
            if isinstance(self._vetClientes[i].conta, ContaPoupanca):
                self._vetClientes[i].conta.atualiza()

def abrir_banco(nome, taxajuros, taxasaque):
    banco = Banco(nome, taxajuros, taxasaque)
    return banco