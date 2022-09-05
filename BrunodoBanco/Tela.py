import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from BANCOS import Banco, abrir_banco
from CLIENTES import cria_cliente

class Tela:
    def __init__(self, master):
        self.banco = Banco.listaBancos[0]

        self.janela = master
        self.janela.title("SISTEMA BANCÁRIO BRUNO")
        self.janela.geometry('620x300')

        self.lblbancoprincipal = tk.Label(self.janela, text=f'{self.banco.nome} | Saldo: {self.banco.saldo}R$')
        self.lblbancoprincipal.pack(side=tk.TOP)

        self.barra_menu = tk.Menu(self.janela)
        self.janela.config(menu=self.barra_menu)

        self.menu_banco = Menu(self.barra_menu, tearoff=False)
        self.menu_banco.add_command(label="Trocar banco", command=self.janela_trocar_banco)
        self.menu_banco.add_command(label="Listar bancos", command=self.janela_listar_bancos)
        self.menu_banco.add_command(label="Atualizar banco", command=self.janela_atualizar_banco)
        self.menu_banco.add_command(label="Cadastrar banco", command=self.janela_banco_cadastro)
        self.barra_menu.add_cascade(label="Banco", menu=self.menu_banco)

        self.menu_conta = Menu(self.barra_menu, tearoff=False)
        self.menu_conta.add_command(label='Mostrar contas', command=self.janela_listar_contas)
        self.menu_conta.add_command(label='Abrir conta', command=self.janela_abrir_conta)
        self.barra_menu.add_cascade(label='Contas', menu=self.menu_conta)

        self.menu_cliente = Menu(self.barra_menu, tearoff=False)
        self.menu_cliente.add_command(label='Mostrar clientes', command=self.janela_listar_clientes)
        self.menu_cliente.add_command(label='Cadastrar cliente', command=self.janela_cadastro_cliente)
        self.barra_menu.add_cascade(label='Clientes', menu=self.menu_cliente)

        self.frame_tabela = tk.Frame()
        self.frame_tabela.pack(side=tk.TOP)
        colunas_users = ['cliente', 'cpf','id_conta', 'conta', 'saldo']
        self.tvw_users = ttk.Treeview(self.frame_tabela, show='headings', columns=colunas_users, height=5)
        self.tvw_users.pack(side=tk.LEFT, fill=tk.BOTH)

        self.tvw_users.heading('id_conta', text="Numero da Conta")
        self.tvw_users.heading('cliente', text="Cliente")
        self.tvw_users.heading('cpf', text="CPF")
        self.tvw_users.heading('conta', text="Conta Bancaria")
        self.tvw_users.heading('saldo', text='Saldo')

        self.tvw_users.column('id_conta', minwidth=0, width=100)
        self.tvw_users.column('cliente', minwidth=0, width=100)
        self.tvw_users.column('cpf', minwidth=0, width=100)
        self.tvw_users.column('conta', minwidth=0, width=100)
        self.tvw_users.column('saldo', minwidth=0, width=100)

        self.scr1 = ttk.Scrollbar(self.frame_tabela, command=self.tvw_users.yview)
        self.scr1.pack(side=tk.LEFT, fill=tk.BOTH)
        self.tvw_users.configure(yscroll=self.scr1.set)

        self.cria_tabela_bancos()

        self.frame_botoes = tk.Frame(self.janela)
        self.frame_botoes.pack(side=tk.TOP)

        self.btn_cadastrar = tk.Button(self.frame_botoes, text='SAQUE',bg='black',fg='white', command=self.janela_saque)
        self.btn_cadastrar.pack(side=tk.LEFT)
        self.btn_deletar = tk.Button(self.frame_botoes, text='DEPOSITO',bg='black',fg='white', command=self.janela_deposito)
        self.btn_deletar.pack(side=tk.LEFT)
        self.btn_deletar_lista = tk.Button(self.frame_botoes, text='ATUALIZAR',bg='black',fg='white', command=self.janela_atualiza_cliente)
        self.btn_deletar_lista.pack(side=tk.LEFT)
        self.btn_deletar_todos = tk.Button(self.frame_botoes, text='ENCERRAR',bg='black',fg='white', command=self.janela_encerra)
        self.btn_deletar_todos.pack(side=tk.LEFT)
        self.btn_top_atualizar = tk.Button(self.frame_botoes, text='SALVAR',bg='black',fg='white', command=self.salva_extrato)
        self.btn_top_atualizar.pack(side=tk.LEFT)

    def salva_extrato(self):
        verifica = self.tvw_users.selection()
        if len(verifica) == 1:
            self.cliente = self.retorna_selecionado()
            arquivo = filedialog.asksaveasfilename(filetypes=[("Arquivo de Texto", ".txt")], defaultextension=".txt", initialfile=f'{self.cliente.nome}_CONTA{self.cliente.conta.id}')
            with open(arquivo, 'w') as arq:
                arq.write(f'{self.cliente.nome}, {self.cliente.conta.tipo}|ID: {self.cliente.conta.id} \n')
                for i in range(len(self.cliente.conta._extrato)):
                    arq.write((self.cliente.conta._extrato[i]+'\n'))
        else:
            messagebox.showwarning('AVISO', 'Escolha um único elemento')

    def janela_atualiza_cliente(self):
        verifica = self.tvw_users.selection()
        if len(verifica) == 1:
            self.cliente_atualizar = self.retorna_selecionado()

            #Janela Top Level
            self.top_atualiza_cliente = tk.Toplevel()
            self.top_atualiza_cliente.grab_set()
            self.top_atualiza_cliente.title('Atualizar Cliente')
            self.top_atualiza_cliente.geometry('300x150')
            self.lbl_nome_cliente = tk.Label(self.top_atualiza_cliente, text='Nome:')
            self.lbl_nome_cliente.grid(row=0, column=0)
            self.lbl_endereco = tk.Label(self.top_atualiza_cliente, text='Endereço')
            self.lbl_endereco.grid(row=1, column=0)
            self.lbl_cpf = tk.Label(self.top_atualiza_cliente, text='CPF')
            self.lbl_cpf.grid(row=2, column=0)
            self.ent_nome_cliente = tk.Entry(self.top_atualiza_cliente, width=30)
            self.ent_nome_cliente.grid(row=0, column=1)
            self.ent_endereco = tk.Entry(self.top_atualiza_cliente, width=30)
            self.ent_endereco.grid(row=1, column=1)
            self.ent_cpf = tk.Entry(self.top_atualiza_cliente, width=30)
            self.ent_cpf.grid(row=2, column=1)
            self.btn_confirmar = tk.Button(self.top_atualiza_cliente, text='Confirmar', command=self.confirma_atualizar_cliente)
            self.btn_confirmar.grid(row=3, column=0, columnspan=2)

            ###inserindo valores anteriores
            self.ent_nome_cliente.insert(0 ,str(self.cliente_atualizar.nome))
            self.ent_endereco.insert(1, self.cliente_atualizar.endereco)
            self.ent_cpf.insert(2, self.cliente_atualizar.cpf)
        else:
            messagebox.showwarning('AVISO', 'Escolha um único elemento')

    def confirma_atualizar_cliente(self):
        nome = self.ent_nome_cliente.get()
        endereco = self.ent_endereco.get()
        cpf = self.ent_cpf.get()
        if nome == '' or endereco == '' or cpf == '':
            messagebox.showinfo('Aviso', 'Todos campos são obrigatórios')
        elif nome == self.cliente_atualizar.nome and cpf == self.cliente_atualizar.cpf and endereco == self.cliente_atualizar.endereco:
            messagebox.showwarning('Aviso', 'NADA FOI ALTERADO!!!')
        else:
            confirma = messagebox.askyesno('Confirmar', 'Tem certeza que a alteração está correta?')
            if confirma == True:
                self.cliente_atualizar.atualiza_dados(nome, endereco, cpf)
                self.atualiza_tabela_bancos()
                self.top_atualiza_cliente.destroy()

    def janela_encerra(self):
        verifica = self.tvw_users.selection()
        if len(verifica) == 1:
            self.cliente = self.retorna_selecionado()
            print(self.cliente)
            if self.cliente.conta.status == False:
                encerra = messagebox.askyesno('AVISO', 'Este cliente não tem conta vinculada. Deseja encerra-lo?')
                if encerra == True:
                    resposta = messagebox.askyesno('ALERTA', f'Tem certeza que deseja encerrar o cliente {self.cliente.nome} de id {self.cliente.id}?')
                    if resposta == True:
                        confirma = messagebox.askyesno('ALERTA', 'ESSA AÇÃO NÃO PODE SER REVERTIDA. TEM CERTEZA?')
                        if confirma == True:
                            self.cliente.encerrar_cliente()
                            self.atualiza_tabela_bancos()

            elif self.cliente.conta.status == True:
                encerra = self.cliente.encerrar_conta()
                if encerra == True:
                    resposta = messagebox.askyesno('ALERTA', f'Tem certeza que deseja encerrar a conta vinculada a {self.cliente.nome} de id {self.cliente.conta.id}?')
                    if resposta == True:
                        confirma = messagebox.askyesno('ALERTA', 'ESSA AÇÃO NÃO PODE SER REVERTIDA. TEM CERTEZA?')
                        if confirma == True:
                            self.cliente.encerrar_conta()
                            self.atualiza_tabela_bancos()
                else:
                    messagebox.showinfo('AVISO', 'Uma conta deve ter saldo zero para ser zerada')
        else:
            messagebox.showwarning('AVISO', 'Escolha um único elemento')

    def janela_deposito(self):
        verifica = self.tvw_users.selection()
        if len(verifica) == 1:
            self.cliente = self.retorna_selecionado()
            print(self.cliente)
            if self.cliente.conta.status == False:
                messagebox.showwarning('AVISO', 'Este cliente não tem conta')
            elif self.cliente.conta.status == True:
                self.janela_depositar = tk.Toplevel(self.janela)
                self.janela_depositar.title('Quanto deseja depositar?')
                self.janela_depositar.geometry('300x150')
                self.janela_depositar.grab_set()
                self.lbl_mensagem = tk.Label(self.janela_depositar, text='DIGITE UM VALOR').pack(side=tk.TOP)
                self.valor_deposito = tk.Entry(self.janela_depositar, width=8)
                self.valor_deposito.pack(side=tk.TOP)
                self.botao_deposito = tk.Button(self.janela_depositar, text='DEPOSITAR', command=self.funcao_deposita)
                self.botao_deposito.pack(side=tk.TOP)
        else:
            messagebox.showwarning('AVISO', 'Escolha um único elemento')
    
    def funcao_deposita(self):
        valor = float(self.valor_deposito.get())
        self.cliente.conta.deposita(valor)
        messagebox.showinfo('DEPOSITO', 'Deposito realizado com sucesso.')
        self.atualiza_tabela_bancos()
        self.janela_depositar.destroy()

    def janela_saque(self):
        verifica = self.tvw_users.selection()
        if len(verifica) == 1:
            self.cliente = self.retorna_selecionado()
            print(self.cliente)
            if self.cliente.conta.status == False:
                messagebox.showwarning('AVISO', 'Este cliente não tem conta')
            elif self.cliente.conta.status == True:
                self.janela_sacar = tk.Toplevel(self.janela)
                self.janela_sacar.title('Quanto deseja sacar?')
                self.janela_sacar.geometry('300x150')
                self.janela_sacar.grab_set()
                self.lbl_mensagem = tk.Label(self.janela_sacar, text='DIGITE UM VALOR').pack(side=tk.TOP)
                self.valor_saque = tk.Entry(self.janela_sacar, width=8)
                self.valor_saque.pack(side=tk.TOP)
                self.botao_saque = tk.Button(self.janela_sacar, text='SACAR', command=self.funcao_saque)
                self.botao_saque.pack(side=tk.TOP)
        else:
            messagebox.showwarning('AVISO', 'Escolha um único elemento')

    def funcao_saque(self):
        valor = float(self.valor_saque.get())
        self.cliente.conta.saque(valor)
        if self.cliente.conta.saque(valor) == True:
            messagebox.showinfo('SAQUE', 'Saque realizado com sucesso.')
        else:
            messagebox.showinfo('SAQUE', 'Saldo insuficiente')
        self.atualiza_tabela_bancos()
        self.janela_sacar.destroy()

    def retorna_selecionado(self):
        id_selecionado = self.tvw_users.selection()[0]
        id_atual = self.tvw_users.index(id_selecionado)
        print('Linha atual:', id_atual)
        print('Conta atual:', self.banco._vetClientes[id_atual].nome)
        return self.banco._vetClientes[id_atual]

    def janela_trocar_banco(self):
        self.top_trocabanco = tk.Toplevel()
        self.top_trocabanco.grab_set()
        self.top_trocabanco.title('Escolha um banco para a interface')
        self.top_trocabanco.geometry('350x120')
        self.radioValue = tk.IntVar()
        for i in range(len(Banco.listaBancos)):
            string = Banco.listaBancos[i].nome
            radio = tk.Radiobutton(self.top_trocabanco, text=f'{string}', variable=self.radioValue, value=i)
            radio.pack(side=tk.TOP)
        botao_confirma = tk.Button(self.top_trocabanco, text='Confirmar', command=self.trocar_banco)
        botao_confirma.pack()
        print(self.banco.nome)

    def cria_tabela_bancos(self):
        for i in range (len(self.banco._vetClientes)):
            self.user_cliente = str(self.banco._vetClientes[i].nome)
            self.user_cpf = str(self.banco._vetClientes[i].cpf)
            self.user_id_conta = 'Sem Conta'
            self.user_conta = 'Sem Conta'
            self.user_saldo = 'Sem Conta'
            if self.banco._vetClientes[i].conta != None:
                self.user_id_conta = str(self.banco._vetClientes[i].conta.id)
                self.user_conta = self.banco._vetClientes[i].conta.tipo
                self.user_saldo = str(self.banco._vetClientes[i].conta.saldo)
            self.tvw_users.insert('', 'end', values=(self.user_cliente, self.user_cpf, self.user_id_conta, self.user_conta, self.user_saldo))

    def atualiza_tabela_bancos(self):
        for i in self.tvw_users.get_children():
            self.tvw_users.delete(i)
        self.lblbancoprincipal.config(text=f'{self.banco.nome} | Saldo: {self.banco.saldo}R$')
        self.cria_tabela_bancos()

    def trocar_banco(self):
        self.selecionado = int(self.radioValue.get())
        self.banco = Banco.listaBancos[self.selecionado]
        self.lblbancoprincipal['text'] = f'{self.banco.nome} | Saldo: {self.banco.saldo}R$'
        self.atualiza_tabela_bancos()
        self.top_trocabanco.destroy()

    def janela_banco_cadastro(self):
        self.top_banco_cadastro = tk.Toplevel()
        self.top_banco_cadastro.grab_set()
        self.top_banco_cadastro.title('Cadastro de Banco')
        self.top_banco_cadastro.geometry('300x150')
        self.lbl_nome = tk.Label(self.top_banco_cadastro, text='Nome:')
        self.lbl_nome.grid(row=0, column=0)
        self.lbl_taxajuros = tk.Label(self.top_banco_cadastro, text='Taxa de Juros')
        self.lbl_taxajuros.grid(row=1, column=0)
        self.lbl_taxasaque = tk.Label(self.top_banco_cadastro, text='Taxa de Saque')
        self.lbl_taxasaque.grid(row=2, column=0)
        self.ent_nome = tk.Entry(self.top_banco_cadastro, width=30)
        self.ent_nome.grid(row=0, column=1)
        self.ent_taxajuros = tk.Entry(self.top_banco_cadastro, width=30)
        self.ent_taxajuros.grid(row=1, column=1)
        self.ent_taxasaque = tk.Entry(self.top_banco_cadastro, width=30)
        self.ent_taxasaque.grid(row=2, column=1)
        self.btn_confirmar = tk.Button(self.top_banco_cadastro, text='Confirmar', command=self.confirmar_cadastro_banco)
        self.btn_confirmar.grid(row=3, column=1)

    def confirmar_cadastro_banco(self):
        nome = str(self.ent_nome.get())
        taxajuros = float(self.ent_taxajuros.get())
        taxasaque = float(self.ent_taxajuros.get())
        if nome == '' or taxajuros == '' or taxasaque == '':
            messagebox.showinfo('Aviso', 'Todos campos são obrigatórios')
        else:
            banco = abrir_banco(nome, taxajuros, taxasaque)
            print(banco)
            self.top_banco_cadastro.destroy()

    def janela_listar_bancos(self):
        colunas = ['nome', 'numero', 'juros', 'saque']
        self.top_listabanco = tk.Toplevel()
        self.top_listabanco.title('Bancos Cadastrados')
        self.top_listabanco.geometry('390x320')
        self.tvw_bancos = ttk.Treeview(self.top_listabanco, show='headings', columns=colunas, height=5)
        self.tvw_bancos.pack(side=tk.LEFT, fill=tk.BOTH)

        # cabeçalho
        self.tvw_bancos.heading('nome', text="Nome")
        self.tvw_bancos.heading('numero', text='Numero')
        self.tvw_bancos.heading('juros', text='Taxa de Juros')
        self.tvw_bancos.heading('saque', text='Taxa de Saque')

        self.tvw_bancos.column('nome', minwidth=0, width=120)
        self.tvw_bancos.column('numero', minwidth=0, width=90)
        self.tvw_bancos.column('juros', minwidth=0, width=90)
        self.tvw_bancos.column('saque', minwidth=0, width=90)

        for i in range(len(Banco.listaBancos)):
            nome = str(Banco.listaBancos[i].nome)
            numero = str(Banco.listaBancos[i].get_numero)
            juros = str(Banco.listaBancos[i].taxajuros)
            saque = str(Banco.listaBancos[i].taxasaque)
            self.tvw_bancos.insert('', 'end', values=(nome, numero, juros, saque))

        self.scrbancos = ttk.Scrollbar(self.top_listabanco, command=self.tvw_bancos.yview)
        self.scrbancos.pack(side=tk.LEFT, fill=tk.BOTH)
        self.tvw_bancos.configure(yscroll=self.scrbancos.set)

    def janela_atualizar_banco(self):
        self.top_atualizar_banco = tk.Toplevel()
        self.top_atualizar_banco.grab_set()
        self.top_atualizar_banco.title('Escolha um banco para atualizar')
        self.top_atualizar_banco.geometry('750x320')
        self.framebancos = tk.Frame(self.top_atualizar_banco)
        self.frameatualiza = tk.Frame(self.top_atualizar_banco)
        self.frameatualiza.pack(side=tk.LEFT)
        self.framebancos.pack(side=tk.LEFT)

        self.radioValue1 = tk.IntVar()
        for i in range(len(Banco.listaBancos)):
            string = Banco.listaBancos[i].nome
            radio = tk.Radiobutton(self.framebancos, text=f'{string}', variable=self.radioValue1, value=i)
            radio.pack(side=tk.TOP)

        self.lbl_nome = tk.Label(self.frameatualiza, text='Nome:')
        self.lbl_nome.grid(row=0, column=0)
        self.lbl_taxajuros = tk.Label(self.frameatualiza, text='Taxa de Juros')
        self.lbl_taxajuros.grid(row=1, column=0)
        self.lbl_taxasaque = tk.Label(self.frameatualiza, text='Taxa de Saque')
        self.lbl_taxasaque.grid(row=2, column=0)
        self.ent_nome = tk.Entry(self.frameatualiza, width=30)
        self.ent_nome.grid(row=0, column=1)
        self.ent_taxajuros = tk.Entry(self.frameatualiza, width=30)
        self.ent_taxajuros.grid(row=1, column=1)
        self.ent_taxasaque = tk.Entry(self.frameatualiza, width=30)
        self.ent_taxasaque.grid(row=2, column=1)

        botao_confirma = tk.Button(self.top_atualizar_banco, text='Confirmar', command=self.atualiza_banco)
        botao_confirma.pack(side=tk.BOTTOM)

    def atualiza_banco(self):
        novo_nome = str(self.ent_nome.get())
        novo_taxajuros = float(self.ent_taxajuros.get())
        novo_taxasaque = float(self.ent_taxajuros.get())
        if novo_nome == '' or novo_taxajuros == '' or novo_taxasaque == '':
            messagebox.showinfo('Aviso', 'Todos campos são obrigatórios')
        else:
            indice = int(self.radioValue1.get())
            Banco.listaBancos[indice]._nome = novo_nome
            Banco.listaBancos[indice]._taxajuros = novo_taxajuros
            Banco.listaBancos[indice]._taxasaque = novo_taxasaque
            self.top_atualizar_banco.destroy()

    def janela_cadastro_cliente(self):
        self.top_cliente_cadastro = tk.Toplevel()
        self.top_cliente_cadastro.grab_set()
        self.top_cliente_cadastro.title('Cadastro de Cliente')
        self.top_cliente_cadastro.geometry('300x150')
        self.lbl_nome_cliente = tk.Label(self.top_cliente_cadastro, text='Nome:')
        self.lbl_nome_cliente.grid(row=0, column=0)
        self.lbl_endereco = tk.Label(self.top_cliente_cadastro, text='Endereço')
        self.lbl_endereco.grid(row=1, column=0)
        self.lbl_cpf = tk.Label(self.top_cliente_cadastro, text='CPF')
        self.lbl_cpf.grid(row=2, column=0)
        self.lbl_banco = tk.Label(self.top_cliente_cadastro, text='Banco:')
        self.lbl_banco.grid(row=3, column=0)
        self.ent_nome_cliente = tk.Entry(self.top_cliente_cadastro, width=30)
        self.ent_nome_cliente.grid(row=0, column=1)
        self.ent_endereco = tk.Entry(self.top_cliente_cadastro, width=30)
        self.ent_endereco.grid(row=1, column=1)
        self.ent_cpf = tk.Entry(self.top_cliente_cadastro, width=30)
        self.ent_cpf.grid(row=2, column=1)
        self.btn_confirmar = tk.Button(self.top_cliente_cadastro, text='Confirmar', command=self.confirmar_cadastro_cliente)
        self.btn_confirmar.grid(row=4, column=1)
        self.n = tk.StringVar()
        self.bancoscbx = ttk.Combobox(self.top_cliente_cadastro, width=25, textvariable=self.n)
        bancos = []
        for i in range(len(Banco.listaBancos)):
            bancos.append(Banco.listaBancos[i].nome)
        self.bancoscbx['values'] = bancos
        self.bancoscbx.grid(row=3, column=1)

    def confirmar_cadastro_cliente(self):
        nome = str(self.ent_nome_cliente.get())
        endereco = str(self.ent_endereco.get())
        cpf = str(self.ent_cpf.get())
        self.selecinado = int(self.bancoscbx.current())
        if nome == '' or endereco == '' or cpf == '':
            messagebox.showinfo('Aviso', 'Todos campos são obrigatórios')
        else:
            cliente = cria_cliente(nome, endereco, cpf)
            Banco.listaBancos[self.selecinado].cadastrar_cliente(cliente)
            self.atualiza_tabela_bancos()
            self.top_cliente_cadastro.destroy()

    def janela_listar_clientes(self):
        colunas = ['nome', 'cpf', 'endereco', 'banco']
        self.top_listaclientes = tk.Toplevel()
        self.top_listaclientes.title('Lista de Clientes')
        self.top_listaclientes.geometry('430x320')
        self.tvw_clientes = ttk.Treeview(self.top_listaclientes, show='headings', columns=colunas, height=5)
        self.tvw_clientes.pack(side=tk.LEFT, fill=tk.BOTH)

        # cabeçalho
        self.tvw_clientes.heading('nome', text="Nome")
        self.tvw_clientes.heading('cpf', text='CPF')
        self.tvw_clientes.heading('endereco', text='Endereço')
        self.tvw_clientes.heading('banco', text='Banco')

        self.tvw_clientes.column('nome', minwidth=0, width=120)
        self.tvw_clientes.column('cpf', minwidth=0, width=90)
        self.tvw_clientes.column('endereco', minwidth=0, width=90)
        self.tvw_clientes.column('banco', minwidth=0, width=90)

        for i in range(len(Banco.listaBancos)):
            banco = Banco.listaBancos[i]
            for j in range (len(banco._vetClientes)):
                nome = banco._vetClientes[j].nome
                cpf = banco._vetClientes[j].cpf
                endereco = banco._vetClientes[j].endereco
                nome_banco = banco._vetClientes[j].banco._nome
                self.tvw_clientes.insert('', 'end', values=(nome, cpf, endereco, nome_banco))

        self.scrclientes = ttk.Scrollbar(self.top_listaclientes, command=self.tvw_clientes.yview)
        self.scrclientes.pack(side=tk.LEFT, fill=tk.BOTH)
        self.tvw_clientes.configure(yscroll=self.scrclientes.set)

    def janela_abrir_conta(self):
        self.top_abrir_conta = tk.Toplevel()
        self.top_abrir_conta.grab_set()
        self.top_abrir_conta.title('Abrir Conta Bancaria')
        self.top_abrir_conta.geometry('300x150')

        self.lbl_cliente_banco = tk.Label(self.top_abrir_conta, text=f'Abrindo conta em {self.banco.nome}')
        self.lbl_cliente_banco.grid(row=0, column=0, columnspan=2)

        self.lbl_ditocujo = tk.Label(self.top_abrir_conta, text='Cliente')
        self.lbl_ditocujo.grid(row=1, column=0)
        self.lbl_saldo = tk.Label(self.top_abrir_conta, text='Saldo')
        self.lbl_saldo.grid(row=2, column=0)
        self.lbl_limite = tk.Label(self.top_abrir_conta, text='Limite')
        self.lbl_limite.grid(row=3, column=0)
        #combobox
        self.v = tk.StringVar()
        self.clientescbx = ttk.Combobox(self.top_abrir_conta, width=25, textvariable=self.v)
        clientes = []
        for i in range(len(self.banco._vetClientes)):
            clientes.append(f'{self.banco._vetClientes[i].nome}')
        self.clientescbx['values'] = clientes
        self.clientescbx.grid(row=1, column=1)
        #combobox
        self.ent_saldo = tk.Entry(self.top_abrir_conta, width=30)
        self.ent_saldo.grid(row=2, column=1)
        self.ent_limite = tk.Entry(self.top_abrir_conta, width=30)
        self.ent_limite.grid(row=3, column=1)
        self.radioValue = tk.IntVar()
        self.contapoupanca = tk.Radiobutton(self.top_abrir_conta, text=f'Conta Poupança', variable=self.radioValue, value=1)
        self.contapoupanca.grid(row=4, column=0)
        self.contacorrente = tk.Radiobutton(self.top_abrir_conta, text=f'Conta Corrente', variable=self.radioValue, value=2)
        self.contacorrente.grid(row=4, column=1)
        self.btn_confirmar = tk.Button(self.top_abrir_conta, text='Confirmar', command=self.confirmar_abre_conta)
        self.btn_confirmar.grid(row=5, column=1, columnspan=2)

    def confirmar_abre_conta(self):
        tipo_conta = int(self.radioValue.get())
        index = int(self.clientescbx.current())
        cliente = self.banco._vetClientes[index]
        saldo = float(self.ent_saldo.get())
        limite = float(self.ent_limite.get())
        if saldo == '' or limite == '':
            messagebox.showinfo('Aviso', 'Todos campos são obrigatórios')
        elif (tipo_conta == 1):
            cliente.abrir_contaPoucanca(saldo, limite)
            self.atualiza_tabela_bancos()
            self.top_cliente_cadastro.destroy()
        elif (tipo_conta == 2):
            cliente.abrir_contaCorrente(saldo, limite)
            self.atualiza_tabela_bancos()
            self.top_abrir_conta.destroy()

    def janela_listar_contas(self):
        colunas = ['cliente', 'banco', 'id_conta', 'tipo_conta', 'saldo']
        self.top_listarcontas = tk.Toplevel()
        self.top_listarcontas.title('Lista de Clientes')
        self.top_listarcontas.geometry('510x320')
        self.tvw_contas = ttk.Treeview(self.top_listarcontas, show='headings', columns=colunas, height=5)
        self.tvw_contas.pack(side=tk.LEFT, fill=tk.BOTH)

        # cabeçalho
        self.tvw_contas.heading('cliente', text="Cliente")
        self.tvw_contas.heading('banco', text='Banco')
        self.tvw_contas.heading('id_conta', text='ID Conta')
        self.tvw_contas.heading('tipo_conta', text="Tipo da Conta")
        self.tvw_contas.heading('saldo', text="Saldo")

        self.tvw_contas.column('cliente', minwidth=0, width=120)
        self.tvw_contas.column('banco', minwidth=0, width=90)
        self.tvw_contas.column('id_conta', minwidth=0, width=90)
        self.tvw_contas.column('tipo_conta', minwidth=0, width=90)
        self.tvw_contas.column('saldo', minwidth=0, width=90)

        for i in range(len(Banco.listaBancos)):
            banco = Banco.listaBancos[i]
            for j in range(len(banco._vetClientes)):
                cliente = banco._vetClientes[j].nome
                nome_banco = banco.nome
                id_conta = banco._vetClientes[j].conta.id
                tipo_conta = banco._vetClientes[j].conta.tipo
                saldo = banco._vetClientes[j].conta.saldo
                self.tvw_contas.insert('', 'end', values=(cliente, nome_banco, id_conta, tipo_conta, saldo))

        self.scrclientes = ttk.Scrollbar(self.top_listarcontas, command=self.tvw_clientes.yview)
        self.scrclientes.pack(side=tk.LEFT, fill=tk.BOTH)
        self.tvw_contas.configure(yscroll=self.scrclientes.set)