import tkinter as tk
from Tela import Tela
from geradorid import GeradorID
from BANCOS import Banco
from CLIENTES import Cliente
from Conta_corrente import ContaCorrente
from Conta_poupanca import *

print(GeradorID.gerar_id())
print(GeradorID.gerar_id())
print(GeradorID.gerar_id())
print(GeradorID.gerar_id())

banco1 = Banco('Brasil', 0.01, 3)
banco2 = Banco('ITAU', 0.013, 6.50)
banco3 = Banco('Nubank', 0.05, 4.33)
banco4 = Banco('Bradesco', 1, 1)

clienteZERADO1 = Cliente('Luiz Moura', 'Tucumã', '098.342.232-56')
banco1.cadastrar_cliente(clienteZERADO1)
clienteZERADO1.abrir_contaPoucanca(0, 0)

clienteZERADO2 = Cliente('Limeira', 'UFAC', '737.838.382-96')
banco1.cadastrar_cliente(clienteZERADO2)
clienteZERADO2.abrir_contaCorrente(0, 0)

cliente1 = Cliente("Maria", 'Tucumã', '978.389.386-78')
banco1.cadastrar_cliente(cliente1)
cliente1.abrir_contaCorrente(2000, 1500)

cliente1.conta.saque(100)
cliente1.conta.deposita(200)
cliente1.conta.deposita(500)

cliente2 = Cliente('José', 'Floresta', '923.893.723-98')
banco1.cadastrar_cliente(cliente2)
cliente2.abrir_contaPoucanca(3400, 1500)

cliente2.conta.saque(200)
cliente2.conta.saque(500)
cliente2.conta.deposita(1000)
cliente2.conta.saque(1)

cliente3 = Cliente('Bruno', 'São Francisco', '983.384.342-69')
banco2.cadastrar_cliente(cliente3)
cliente3.abrir_contaPoucanca(0, 0)

cliente4 = Cliente('Paulo', 'Rui Lino', '784.934.348-67')
banco3.cadastrar_cliente(cliente4)
cliente4.abrir_contaCorrente(2400, 1500)

cliente5 = Cliente('Irisneu', 'Não sei', '784.043.488-30')
banco3.cadastrar_cliente(cliente5)
cliente5.abrir_contaPoucanca(2400, 1500)

cliente6 = Cliente('Paula', 'Bosque', '928.734.926.466-26')
banco3.cadastrar_cliente(cliente6)
cliente6.abrir_contaCorrente(2600, 1500)

cliente7 = Cliente('José Paulo', 'Rui Lino', '784.934.348-60')
banco4.cadastrar_cliente(cliente7)
cliente7.abrir_contaPoucanca(5400, 1500)

cliente8 = Cliente('Ana Paula', 'Holanda', '903.393.233-23')
banco4.cadastrar_cliente(cliente8)
cliente8.abrir_contaCorrente(2000,1500)

app = tk.Tk()
Tela(app)
app.mainloop()
