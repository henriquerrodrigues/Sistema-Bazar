import tkinter as tk
from tkinter.font import Font
from tkinter import *  
from tkinter import messagebox
from  models.Store import Store
from  models.ShoppingCart import ShoppingCart
from models.Client import Client

from tkinter import Scrollbar

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

global c
c = 1


def cadastrarCliente():
    global clienteWindow
    clienteWindow = tk.Tk()
    clienteWindow.title("Cadastro de Cliente")


    # Variável de controle para armazenar o novo_cliente
    novo_cliente = None

    def salvarCliente():
        nonlocal novo_cliente
        novo_cliente = Client(nameEntry.get(), cpfEntry.get(),rgEntry.get())
        clienteWindow.destroy()


    nameLabel = Label(clienteWindow, text="Nome:")
    nameLabel.grid(row=0, column=0, sticky=W, padx=10, pady=10)

    nameEntry = Entry(clienteWindow)
    nameEntry.grid(row=0, column=1, padx=10, pady=10)

    cpfLabel = Label(clienteWindow, text="CPF:")
    cpfLabel.grid(row=1, column=0, sticky=W, padx=10, pady=10)

    cpfEntry = Entry(clienteWindow)
    cpfEntry.grid(row=1, column=1, padx=10, pady=10)

    rgLabel = Label(clienteWindow, text="RG:")
    rgLabel.grid(row=2, column=0, sticky=W, padx=10, pady=10)

    rgEntry = Entry(clienteWindow)
    rgEntry.grid(row=2, column=1, padx=10, pady=10)

    cadastrarBtn = Button(clienteWindow, text="Cadastrar", command=lambda: salvarCliente())
    cadastrarBtn.grid(row=3, column=0, columnspan=2, pady=10)

    clienteWindow.mainloop()

    # Retorna o objeto novo_cliente após a janela ser fechada
    return novo_cliente

def pmm(mm):
    return mm/0.352777

def criarPDF(cliente, produtos, valorTotal):
    try:
        cnv = canvas.Canvas(pastaApp+"\\CupomFiscal_"+str(c)+".pdf", pagesize=A4)

        # Definir fontes e estilos
        cnv.setFont("Helvetica-Bold", 16)  # Negrito, tamanho 16
        cnv.setFont("Helvetica", 12)  # Normal, tamanho 12

        w, h = A4
        ylisti = h - 215 #value for grid

        #margem_esquerda = inch
        #margem_direita = A4[0] - inch
        #margem_superior = A4[1] - inch
        #margem_inferior = inch

        # Texto "Cupom Fiscal"
        cnv.line(w-580, h-34, w-15, h-34)
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawCentredString(A4[0]/2, h - 80, "NOTA DA RECEITA FEDERAL:")

        cnv.setFont("Times-Roman", 12)
        cnv.drawString(12.5, h-100, "As mercadorias não poderão ser utilizadas para venda no comércio, sob pena de apreensão das autoridades competentes.")
        cnv.line(w-580, h-110, w-15, h-107)
        cnv.drawImage("Bazar\models\logo.png", 50, h - 80, width=100, height=80)
        cnv.rect(40, h - 195, 320, 80)
        cnv.rect(400, h - 180, 160, 60)

        cnv.setFont("Times-Roman", 9)
        cnv.drawString(50, h-130, "Nome:")
        cnv.drawString(180, h-130, cliente.name)
        cnv.drawString(50, h-150, "CPF:")
        cnv.drawString(180, h-150, cliente.cpf)
        cnv.drawString(50, h-170, "Registro Geral:")
        cnv.drawString(180, h-170, cliente.rg)
        cnv.drawString(50, h-190, "Cidade:")
        cnv.drawString(180, h-190, "Chapecó")

        valorTotal = "{:.2f}".format(valorTotal)

        cnv.setFont("Times-Roman", 18)
        cnv.drawString(440, h-145, "Valor Total:")
        cnv.setFont("Times-Roman", 18)
        cnv.drawString(460, h-170, str(valorTotal))
        cnv.drawString(420, h-170, "R$")

        cnv.line(w-580, h-200, w-15, h-203)

        linha_inicial = A4[1] - inch * 3
        altura_linha = inch * 0.4

        # Cabeçalho da tabela
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(inch*0.5, linha_inicial, "Produto/Unidade")
        #cnv.drawString(inch + inch * 1.4, linha_inicial, "Unidade(s)")
        cnv.drawString(inch + inch * 2.8, linha_inicial, "Valor Unitário")

                # Posição inicial da tabela
        x_start = 50
        y_start = h - 180
        y = (y_start - inch)*1.0005


        # Conteúdo da tabela
        cnv.setFont("Helvetica", 12)
        for produto in produtos:
            cnv.drawString(x_start + inch - 85, y, str(produto.name))
            #cnv.drawString(x_start + inch * 2.1, y, str(produto.quantity))
            cnv.drawString(x_start + inch * 3.5, y, str(produto.price))
            cnv.drawString(x_start + inch * 3.2, y, str("R$"))

            y -= (inch)*0.3


        #------------------Payment
        cnv.drawString(410, h-570, "Dinheiro")
        cnv.drawString(410, h-590, "Pix")
        cnv.drawString(410, h-610, "Associação")
        xt = [400 , 500 , w-15]
        yt = [h-555, h-575, h-595, h-615]
        cnv.grid(xt,yt)

        cnv.line(w-450, h-725, w-160, h-725)
        cnv.drawString(248, h-740, "ASSINATURA")

        cnv.drawString(400, h-630, "OBS: Todos os produtos adquiridos")
        cnv.drawString(400, h-650, "são finais e não estão sujeitos a")
        cnv.drawString(400, h-670, "devoluções.")

        #------------------ Final headers
        text = cnv.beginText(0, h-800)
        text.setFont("Times-Roman", 9)
        text.moveCursor(205, 0)
        text.textLine("Associação Hospitalar Lenoir Vargas Ferreira")
        text.moveCursor(30, 0)
        text.textLine("E-mail: direcao@hro.org.br")
        text.moveCursor(10, 0)
        text.textLine("Fone:(49)3321-6500")
        text.moveCursor(-55, 0)
        text.textLine("Rua Florianópolis, 1448-E-CEP: 89812-505-Chapecó-SC")
        cnv.drawText(text)

        # Salvar o arquivo PDF
        cnv.save()
    except:
        messagebox.showinfo(title = "ERRO", message = "Erro ao carregar o PDF")
        return
    messagebox.showinfo(title = "PDF", message = "Sucesso ao carregar o PDF")

def viewStore():
    global storeWindow 
    storeLabelFrame = LabelFrame(storeWindow, text="Produtos do Bazar")
    storeLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    storeCanvasFrame = Frame(storeLabelFrame)
    storeCanvasFrame.pack(side='left', fill='both', expand=True)

    storeItemsCanvas = Canvas(storeCanvasFrame)
    storeItemsCanvas.pack(side='left', fill='both', expand=True)

    storeScrollbar = Scrollbar(storeCanvasFrame, orient='vertical', command=storeItemsCanvas.yview)
    storeScrollbar.pack(side='right', fill='y')

    storeItemsCanvas.configure(yscrollcommand=storeScrollbar.set)
    storeItemsCanvas.bind('<Configure>', lambda e: storeItemsCanvas.configure(scrollregion=storeItemsCanvas.bbox('all')))

    storeFrame = Frame(storeItemsCanvas, pady="5")
    storeItemsCanvas.create_window((0, 0), window=storeFrame, anchor='nw')

    store = Store()
    storeItems = store.getStoreItems() 
    for item in storeItems:
        itemFrame = Frame(storeFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        codeLabel = Label(itemFrame, text="%s-"%item.code, font=("Candara", 12, "bold"), fg="black")
        codeLabel.pack(side="left")
        
        nameLabel = Label(itemFrame, text=item.name,font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="R$ %s"%item.price , font=("Candara",13),fg="red")  
        addToCartBtn = Button(itemFrame, text="Adicionar ao Carrinho",cursor="hand2", command=lambda i=item: addItemToCart(i) )        

        nameLabel.pack(side="left")
        priceLabel.pack(side="left",fill="both", expand=True )
        addToCartBtn.pack(side="right" )
        
    itemFrame = Frame(storeFrame, pady="5")

    btnGoCart = Button(storeWindow, text="Ir para o carrinho", font=("Candara",15,"bold"),fg="red",bg="white",cursor="hand2", command=viewCart )
    btnGoCart.pack(pady="6")

def viewCart():   
    cartWindow = Toplevel()
    cartWindow.title("Carrinho")
    cartWindow.grab_set()
    global cart
    cartItems = cart.getCartItems()

    cartItemsLabelFrame = LabelFrame(cartWindow, text="Carrinho de Itens")
    cartItemsLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    cartItemsCanvas = Canvas(cartItemsLabelFrame)
    cartItemsCanvas.pack(side='left', fill='both', expand=True)

    cartScrollbar = Scrollbar(cartItemsLabelFrame, orient='vertical', command=cartItemsCanvas.yview)
    cartScrollbar.pack(side='right', fill='y')

    cartItemsCanvas.configure(yscrollcommand=cartScrollbar.set)
    cartItemsCanvas.bind('<Configure>', lambda e: cartItemsCanvas.configure(scrollregion=cartItemsCanvas.bbox('all')))

    cartItemsFrame = Frame(cartItemsCanvas, padx=3, pady=3)
    cartItemsCanvas.create_window((0, 0), window=cartItemsFrame, anchor='nw')

    index = 0
    for item in cartItems:
        itemFrame = Frame(cartItemsFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        codeLabel = Label(itemFrame, text="%s-"%item.code, font=("Candara", 12, "bold"), fg="black")
        codeLabel.pack(side="left")

        nameLabel = Label(itemFrame, text=item.name,font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="R$ %s"%item.price,font=("Candara",13),fg="red")  
        addToCartBtn = Button(itemFrame, text="Remover do Carrinho", font=("Candara",11,"bold"),fg="red",bg="white",cursor="hand2", command=lambda i=index: removeFromCart(i,cartWindow) )

        nameLabel.pack(side="left")
        priceLabel.pack(side="left")
        addToCartBtn.pack(side="right" )
        index += 1

    checkOutFrame = Frame(cartWindow, pady="10")
    total_price = round(cart.getTotalPrice(), 2) # arredonda para duas casas decimais
    totalPriceLabel = Label(checkOutFrame, text="Preço Total : R$ {:.2f}".format(total_price), font=("Candara",14,"bold"),fg="indigo")
    totalPriceLabel.pack(side="left")
    buyBtn = Button(checkOutFrame, text="Comprar", font=("Candara",15,"bold"),fg="indigo",bg="white",cursor="hand2", command=lambda : buyCommand(cartWindow))
    buyBtn.pack(side="left",padx="10")
    checkOutFrame.pack()

    backToStoreBtn = Button(cartWindow, text="Voltar à Loja", font=("Candara",15,"bold"),fg="red",bg="white",cursor="hand2",command=cartWindow.destroy)
    backToStoreBtn.pack(pady="6")

    cartWindow.mainloop()

def addItemToCart(item=None):
    global cart
    cart.addToCart(item)
    messagebox.showinfo(title="Success" , message="Item %s Adicionado ao Carrinho !!"%item.name )

def removeFromCart(itemIndex=None,cartWindow=None):
    global cart
    cart.removeFromCart(itemIndex)
    messagebox.showinfo(title="success",message="Item Removido")
    cartWindow.destroy()
    viewCart()
def buyCommand(cartWindow):
    global cart
    #cart.emptyCart()
    cartWindow.destroy()    
    messagebox.showinfo(title="success",message="Compra Realizada com Sucesso")
    storeWindow.destroy()


while True:
    client = cadastrarCliente()

    storeWindow = tk.Tk()
    storeWindow.title("Bazar")

    viewStore()

    cart = ShoppingCart()

    storeWindow.mainloop()

    pastaApp = os.path.dirname(__file__)

    criarPDF(client, cart.getCartItems(), cart.getTotalPrice())
    os.startfile(pastaApp + "\\CupomFiscal_"+str(c)+".pdf")