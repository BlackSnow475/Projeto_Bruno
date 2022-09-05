from geradorid import GeradorID
from Conta_corrente import ContaCorrente
from Conta_poupanca import ContaPoupanca

class Cliente:
    def __init__(self, nome, endereco, cpf):
        self._nome = nome
        self._endereco = endereco
        self._cpf = cpf
        self._conta = None
        self._banco = None
        self._id = GeradorID.gerar_id()

    def atualiza_dados(self, nome, endereco, cpf):
        self._nome = nome
        self._endereco = endereco
        self._cpf = cpf

    @property
    def endereco(self):
        return self._endereco

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def set_nome(self, value):
        self._nome = value

    @property
    def banco(self):
        return self._banco

    @banco.setter
    def set_banco(self, value):
        self._banco = value

    @property
    def conta(self):
        return self._conta

    @conta.setter
    def set_conta(self, value):
        self._conta = value

    @property
    def id(self):
        return self._id

    def abrir_contaPoucanca(self, saldo, limite):
        if self._banco == None:
            return False
        else:
            self._conta = ContaCorrente(saldo, limite)
            self._conta.banco = self._banco
            self._conta.titular = self
            self._banco._saldo += self._conta._saldo
            return True

    def abrir_contaCorrente(self, saldo, limite):
        if self._banco == None:
            return False
        else:
            self._conta = ContaPoupanca(saldo, limite)
            self._conta.banco = self._banco
            self._conta.titular = self
            self._banco._saldo += self._conta._saldo
            return True

    def encerrar_conta(self):
        if self._conta.saldo == 0:
            self._conta._titular = 'Conta encerrada'
            self._conta._limite = 'Conta encerrada'
            self._conta._id = 'Conta encerrada'
            self._conta.tipo = 'Conta encerrada'
            self._conta._status = False
            self.conta._banco = 'Conta encerrada'
            return True
        else:
            return False

    def encerrar_cliente(self):
        if self._conta._status == False:
            self._nome = 'Cliente encerrado'
            self._endereco = 'Cliente encerrado'
            self._cpf = 'Cliente encerrado'
            self._conta = None
            self._banco = None
            self.__id = 'Cliente encerrado'


def cria_cliente(nome, endereco, cpf):
    cliente = Cliente(nome, endereco, cpf)
    return cliente