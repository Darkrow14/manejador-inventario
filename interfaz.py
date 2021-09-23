from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from BB import *

import ctypes


def validate_int(text, long=None, tam=10):
    if long is not None:
        if len(long) > tam:
            return False
    return text.isdecimal()


def validate_char(text, long=None, tam=25):
    if long is not None:
        if len(long) > tam:
            return False
    return (text.isalpha() or text.isspace())


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.dataBase = DataBase()
        self.screenSize = []
        #------------------------Menus-----------------------#
        self.barraMenu = Menu(self)
        self.config(menu=self.barraMenu)
        self.crud = Menu(self, tearoff=False)
        self.imagenes = {}
        self.iconphoto(True, PhotoImage(file='./iconos/registro.png'))

        #--------------------------Crud-----------------------#Creacion de submenus
        self.crud.add_command(label="Insertar datos", command=lambda: self.insert())
        self.crud.add_command(label="Visualizar datos", command=lambda: self.show())
        self.crud.add_command(label="Actualizar datos", command=lambda: self.update())
        self.crud.add_command(label="Eliminar datos", command=lambda: self.delete())

        self.barraMenu.add_cascade(label="CRUD", menu=self.crud)
        #--------------------------- Imagen ---------------------#


        #------------------------Botones----------------------#
        self.InsertP = Button(self, text="Realizar Pedido", command=lambda: self.insert_p(), cursor="hand2")
        self.InsertP.grid(row=1, column=0, padx=5, pady=10)

        self.Factura = Button(self, text="Generar Factura", command=lambda: self.generar_F(), cursor="hand2")
        self.Factura.grid(row=1, column=2, padx=5, pady=10)

    def insert(self):
        windowI = Toplevel(self)
        windowI.title("Insertar datos")
        #windowI.iconphoto(True, PhotoImage(file='iconos')

        self.posicionar(380, 320, windowI)
        imagenEquipo = Label(windowI, image=self.imagenes["insertar"][0])
        imagenEquipo.grid(row=0, column=0, padx=10, pady=10)
        insertE = Button(windowI, text="Insertar equipo", command=lambda: self.insert_e(windowI), cursor="hand2")
        insertE.grid(row=1, column=0, padx=10, pady=5)

        imagenTela = Label(windowI, image=self.imagenes["insertar"][1])
        imagenTela.grid(row=0, column=2, padx=10, pady=10)
        insertM = Button(windowI, text="Insertar tela", command=lambda: self.insert_m(windowI), cursor="hand2")
        insertM.grid(row=1, column=2, padx=10, pady=5)

        imagenProduccion = Label(windowI, image=self.imagenes["insertar"][2])
        imagenProduccion.grid(row=2, column=1, padx=10, pady=10)
        insertPoduccion = Button(windowI, text="Ingresar produccion", command=lambda: self.insert_produccion(windowI), cursor="hand2")
        insertPoduccion.grid(row=3, column=1, padx=10, pady=5)
        self.iconify()
        windowI.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowI))

    def insert_e(self, window):

        varCanti = tkinter.StringVar()
        varEspecialidad = tkinter.StringVar()

        windowE = Toplevel(window)
        windowE.title("Insertar equipo")
        window.iconify()
        windowE.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowE, window))
        self.posicionar(400, 60, windowE)
        #---------------------------- Etiquetas --------------------------------#
        cantidadML = Label(windowE, text="Ingrese la cantidad de miembros")
        cantidadML.grid(row=0, column=0, padx=5, pady=5)
        especialidadEL = Label(windowE, text="Selecione la especialidad")
        especialidadEL.grid(row=1, column=0, padx=5, pady=5)
        #---------------------------- Entry ------------------------------------#
        cantidadM = Entry(windowE, textvariable=varCanti, validate="key",
                          validatecommand=(windowE.register(validate_int), "%S"))
        cantidadM.grid(row=0, column=1, padx=3, pady=2)
        especialidad = ttk.Combobox(windowE, state="readonly", textvariable=varEspecialidad)
        especialidad["values"] = ["Corte textil", "Patronaje"]
        especialidad.grid(row=1, column=1)

        #---------------------------- Extraccion de valores ----------------------------#
        accept = Button(windowE, text="Insertar", command=lambda: self.equipoMensaje(varCanti, varEspecialidad), cursor="hand2")
        accept.grid(row=1, column=2)

    def equipoMensaje(self, varCanti, varEspecialidad):
        if varCanti.get() == "" or varEspecialidad.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            messagebox.showinfo(message="Equipo insertado con exito", title="Información")
            self.dataBase.insert_equipo(int(varCanti.get()), varEspecialidad.get())

    def insert_m(self, window):
        varTipo = tkinter.StringVar()
        varMetros = tkinter.StringVar()
        varPrecio = tkinter.StringVar()

        windowM = Toplevel(window)
        windowM.title("Insertar telas")
        window.iconify()
        windowM.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowM, window))
        self.posicionar(350, 80, windowM)
        #--------------------------- Etiquetas ---------------------------------#
        tipoL = Label(windowM, text="Ingrese el tipo de tela:")
        tipoL.grid(row=0, column=0, padx=3, pady=2)
        metrosL = Label(windowM, text="Ingrese los metros de tela:")
        metrosL.grid(row=1, column=0, padx=3, pady=2)
        precioL = Label(windowM, text="Ingrese el precio por metro:")
        precioL.grid(row=2, column=0, padx=3, pady=2)
        #---------------------------Entradas-----------------------------------#
        tipo = Entry(windowM, textvariable=varTipo, validate="key", validatecommand=(windowM.register(validate_char), "%S", "%P"))
        tipo.grid(row=0, column=1, padx=3, pady=2)
        metros = Entry(windowM, textvariable=varMetros
                       ,validate="key", validatecommand=(windowM.register(validate_int), "%S"))
        metros.grid(row=1, column=1, padx=3, pady=2)
        precio = Entry(windowM, textvariable=varPrecio,
                       validate="key", validatecommand=(windowM.register(validate_int), "%S"))
        precio.grid(row=2, column=1, padx=3, pady=2)

        #----------------------------- Extraccion de valores --------------------------#
        accept = Button(windowM, text="Insertar", command=lambda: self.telaMensaje(varTipo, varMetros, varPrecio), cursor="hand2")
        accept.grid(row=1, column=2, padx=3, pady=2)

    def telaMensaje(self, varTipo, varMetros, varPrecio):
        if varTipo.get() == "" or varMetros.get() == "" or varPrecio.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            self.dataBase.insert_tela(varTipo.get(), float(varMetros.get()), float(varPrecio.get()))
            messagebox.showinfo(message="Tela agredada con exito", title="Información")

    def insert_produccion(self, window):

        varPedido = tkinter.StringVar()
        varEncargado = tkinter.StringVar()
        varEquipo = tkinter.StringVar()
        varMaquina = tkinter.StringVar()

        windowProduccion = Toplevel(window)
        windowProduccion.title("Insertar produccion")
        window.iconify()
        windowProduccion.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowProduccion, window))
        self.posicionar(600, 80, windowProduccion)
        #--------------------------------- Interaccion --------------------------#
        numPedidoL = Label(windowProduccion, text="Seleccione el pedido:")
        numPedidoL.grid(row=0, column=0, padx=3, pady=2)
        numPedido = ttk.Combobox(windowProduccion, textvariable=varPedido, state="readonly")
        numPedido.grid(row=0, column=1, padx=3, pady=2)
        pedidos = self.dataBase.select_pedidos()
        if len(pedidos) > 0:
            lista = []
            for ped in pedidos:
                lista.append(str(ped[0]))
            numPedido["value"] = lista
        else:
            if(messagebox.showwarning(message="No hay pedidos ingresados, ingrese alguno", title="Información") == "ok"):
                self.erase(windowProduccion, window)
                breakpoint()

        numEncargadoL = Label(windowProduccion, text="Seleccione el encargado:")
        numEncargadoL.grid(row=0, column=2, padx=3, pady=2)
        numEncargado = ttk.Combobox(windowProduccion, textvariable=varEncargado,state="readonly")
        numEncargado["values"] = ["10230124", "22412421", "42413234", "5234135"]
        numEncargado.grid(row=0, column=3, padx=3, pady=2)

        numEquipoL = Label(windowProduccion, text="Seleccione el equipo")
        numEquipoL.grid(row=1, column=0, padx=3, pady=2)
        numEquipo = ttk.Combobox(windowProduccion, textvariable=varEquipo, state="readonly")
        numEquipo.grid(row=1, column=1, padx=3, pady=2)
        numsEqui = self.dataBase.select_equipos()
        if len(numsEqui) > 0:
            lista = []
            for num in numsEqui:
                lista.append(str(num[0]))
            numEquipo["value"] = lista
        else:
            if(messagebox.showwarning(message="No hay equipos ingresados, ingrese alguno", title="Información") == "ok"):
                self.erase(windowProduccion, window)
                breakpoint()

        maquinariaL = Label(windowProduccion, text="Ingrese la maquinaria:")
        maquinariaL.grid(row=1, column=2, padx=3, pady=2)
        maquinaria = ttk.Combobox(windowProduccion, textvariable=varMaquina, state="readonly")
        maquinaria["values"] = ["CN0574", "CN0563", "CN05832", "PT9382", "PT4721", "PT9310"]
        maquinaria.grid(row=1, column=3, padx=3, pady=2)

        #--------------------------- Extraccion de valores ------------------------------#
        accept = Button(windowProduccion, text="Insertar",
                        command=lambda: self.mensajeProduccion(varPedido, varEncargado, varEquipo, varMaquina))
        accept.grid(row=2, column=1, padx=3, pady=2)

    def mensajeProduccion(self, varPedido, varEncargado, varEquipo, varMaquina):
        if varPedido.get() == "" or varEncargado.get() == "" or varEquipo.get() == "" or varMaquina.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            self.dataBase.insertar_produccion(int(varPedido.get()), int(varEncargado.get()), int(varEquipo.get()),
                                               varMaquina.get())
            messagebox.showinfo(message="Produccion agredada con exito", title="Información")

    def show(self):
        windowShow = Toplevel(self)
        windowShow.title("Tablas")
        self.iconify()
        windowShow.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowShow))
        windowShow.iconphoto(True, PhotoImage(file='./iconos/view.png'))
        self.posicionar(800, 300, windowShow,True)
        notebook = ttk.Notebook(windowShow)
        #------------------------------- Pestañas -------------------------#
        pedidos = self.tablaPedidos(notebook)
        clientes = self.tablaClientes(notebook)
        producciones = self.tablaProducciones(notebook)
        stock = self.tablaTelas(notebook)
        equipos = self.tablaEquipos(notebook)
        facturas = self.tablaFacturas(notebook)

        notebook.add(pedidos, text="Pedidos", padding=20)
        notebook.add(clientes, text="Clientes", padding=20)
        notebook.add(producciones, text="Producciones", padding=20)
        notebook.add(stock, text="Telas", padding=20)
        notebook.add(equipos, text="Equipos", padding=20)
        notebook.add(facturas, text="Facturas", padding=20)

        notebook.pack(padx=5, pady=5)

    def tablaPedidos(self, frame):
        pedidos, canti = self.dataBase.select_pedidos(False)
        tabla = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=str(canti))
        tabla.pack()
        tabla.heading(1, text="NUMPED")
        tabla.heading(2, text="DNI")
        tabla.heading(3, text="SERVICIO")
        tabla.heading(4, text="MODELO")
        tabla.heading(5, text="PARA")
        tabla.heading(6, text="MEDIDAS")
        tabla.heading(7, text="ACTIVO")

        for pedido in pedidos:
            tabla.insert("", "end", values=pedido)

        for i in range(1, len(tabla["columns"]) + 1):
            tabla.column(str(i), width=100)
        return tabla

    def tablaClientes(self, frame):
        clientes, canti = self.dataBase.select_clients(single=False)
        tabla = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6), show="headings", height=str(canti))
        tabla.pack()
        tabla.heading(1, text="DNI")
        tabla.heading(2, text="NOMBRE(S)")
        tabla.heading(3, text="APELLIDOS")
        tabla.heading(4, text="DIRECCION")
        tabla.heading(5, text="TELEFONO")
        tabla.heading(6, text="ACTIVO")

        for cliente in clientes:
            tabla.insert("","end", values=cliente)

        for i in range(1, len(tabla["columns"]) + 1):
            tabla.column(str(i), width=100)

        return tabla

    def tablaProducciones(self, frame):
        producciones, canti = self.dataBase.select_producciones(single=False)
        tabla = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), show="headings", height=str(canti))
        tabla.pack()
        tabla.heading(1, text="ID_PRODUCCION")
        tabla.heading(2, text="NUMPED")
        tabla.heading(3, text="NUMENCARGA")
        tabla.heading(4, text="NUMEQUI")
        tabla.heading(5, text="MAQUINA")

        for produccion in producciones:
            tabla.insert("", "end", values=produccion)

        for i in range(len(tabla["columns"]) + 1):
            tabla.column(str(i), width=100)

        return tabla

    def tablaTelas(self, frame):
        telas, canti = self.dataBase.select_telas(single=False)
        tabla = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), show="headings", height=str(canti))
        tabla.pack()
        tabla.heading(1, text="CODIGOT")
        tabla.heading(2, text="TIPO")
        tabla.heading(3, text="METROS")
        tabla.heading(4, text="PRECIO_BASE")
        tabla.heading(5, text="ACTIVO")

        for tela in telas:
            tabla.insert("", "end", values=tela)

        for i in range(len(tabla["columns"]) + 1):
            tabla.column(str(i), width=100)

        return tabla

    def tablaEquipos(self, frame):
        equipos, canti = self.dataBase.select_equipos(single=False)
        tabla = ttk.Treeview(frame, columns=(1, 2, 3), show="headings", height=str(canti))
        tabla.pack()
        tabla.heading(1, text="NUMEQ")
        tabla.heading(2, text="CANTEMP")
        tabla.heading(3, text="ESPECIALIDAD")

        for equipo in equipos:
            tabla.insert("", "end", values=equipo)

        for i in range(len(tabla["columns"]) + 1):
            tabla.column(str(i), width=100)

        return tabla

    def tablaFacturas(self, frame):
        facturas, canti = self.dataBase.facturas()
        tabla = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), show="headings", height=str(canti))
        tabla.pack()
        tabla.heading(1, text="ID_FACTURA")
        tabla.heading(2, text="NUMPED")
        tabla.heading(3, text="DNICLI")
        tabla.heading(4, text="PRECIO")
        tabla.heading(5, text="FORMA_DE_PAGO")

        for factura in facturas:
            tabla.insert("", "end", values=factura)

        for i in range(len(tabla["columns"]) + 1):
            tabla.column(str(i), width=100)

        return tabla

    def update(self):
        windowU = Toplevel(self)
        windowU.title("Actualizar datos")
        self.iconify()
        windowU.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowU))
        self.posicionar(400, 350, windowU)
        windowU.iconphoto(True, PhotoImage(file='./iconos/actualizacion.png'))
        #--------------------------- Botones -----------------------------#
        updateStock = Button(windowU, text="Actualizar telas", command=lambda: self.update_stock(windowU), cursor="hand2")
        updateStock.grid(row=1, column=0, padx=10, pady=5)
        imagenStock = Label(windowU, image=self.imagenes["actualizar"][0])
        imagenStock.grid(row=0, column=0, padx=50, pady=10)


        updateEquipo = Button(windowU, text="Actualizar equipo", command=lambda: self.update_equipo(windowU),cursor="hand2")
        updateEquipo.grid(row=1, column=1, padx=10, pady=5)
        imagenEquipo = Label(windowU, image=self.imagenes["actualizar"][1])
        imagenEquipo.grid(row=0, column=1, padx=50, pady=10)

        imagenProduccion = Label(windowU, image=self.imagenes["actualizar"][3])
        imagenProduccion.grid(row=2, column=0, padx=50, pady=10)
        updateProduccion = Button(windowU, text="Actualizar produccion", command=lambda: self.update_produccion(windowU), cursor="hand2")
        updateProduccion.grid(row=3, column=0, padx=10, pady=5)

        imagenCliente = Label(windowU, image=self.imagenes["actualizar"][2])
        imagenCliente.grid(row=2, column=1, padx=50, pady=10)
        updateCliente = Button(windowU, text="Actualizar cliente", command=lambda: self.update_cliente(windowU), cursor="hand2")
        updateCliente.grid(row=3, column=1, padx=10, pady=5)

    #Actualizar datos
    def update_stock(self, window):
        varCodigo = tkinter.StringVar()
        varTipo = tkinter.StringVar()
        varMetros = tkinter.StringVar()
        varPrecio = tkinter.StringVar()
        varActivo = tkinter.StringVar()

        updateStock = Toplevel(window)
        updateStock.title("Actualizar Stock")
        window.iconify()
        updateStock.protocol("WM_DELETE_WINDOW", lambda: self.erase(updateStock, window))
        self.posicionar(600, 100, updateStock)
        #------------------------- Interaccion --------------------------#
        codigoTelaL = Label(updateStock, text="Seleccione el codigo de la tela:")
        codigoTelaL.grid(row=0, column=0)
        codigoTela = ttk.Combobox(updateStock, textvariable=varCodigo, state="readonly")
        codigoTela.grid(row=0, column=1)
        #Se obtienen todos los codigos de las telas disponibles
        codigos = self.dataBase.select_telas()
        if len(codigos) > 0:
            lista = []
            for codigo in codigos:
                lista.append(str(codigo[0]))
            codigoTela["values"] = lista
        else:
            if(messagebox.showwarning(message="No hay telas ingresadas, por favor ingrese alguna", title="Información") == "ok"):
                self.erase(updateStock, window)
                breakpoint()

        tipoL = Label(updateStock, text="Tipo de tela:")
        tipoL.grid(row=0, column=3)
        tipo = Entry(updateStock, textvariable=varTipo, )
        tipo.grid(row=0, column=4)

        metrosL = Label(updateStock,  text="Metros de tela:")
        metrosL.grid(row=1, column=0)
        metros = Entry(updateStock, textvariable=varMetros)
        metros.grid(row=1, column=1)

        precioL = Label(updateStock, text="Precio por metro:")
        precioL.grid(row=1, column=3)
        precio = Entry(updateStock, textvariable=varPrecio)
        precio.grid(row=1, column=4)

        activoL = Label(updateStock, text="Activo:")
        activoL.grid(row=2, column=0)
        activo = ttk.Combobox(updateStock, textvariable=varActivo)
        activo["values"] = ["S", "N"]
        activo.grid(row=2, column=1)

        buscar = Button(updateStock, text="Buscar", command=lambda: self.mostrarStock(int(varCodigo.get()), tipo, metros,
                                                                                      precio, activo, False), cursor="hand2")
        buscar.grid(row=0, column=2)

        #----------------------- Extraccion de valores --------------------------#
        update = Button(updateStock, text="Actualizar", command=lambda: self.mensajeTelaU(varCodigo, varMetros, varPrecio, varActivo), cursor="hand2")
        update.grid(row=3, column=1)

    def mensajeTelaU(self, varCodigo, varMetros, varPrecio, varActivo):
        if varCodigo.get() == "" or varMetros.get() == "" or varPrecio.get() == "" or varActivo.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            messagebox.showinfo(message="Tela actualizada con exito", title="Información")
            self.dataBase.update_tela(int(varCodigo.get()), float(varMetros.get()), float(varPrecio.get()), varActivo.get())

    def mostrarStock(self, codigo, tipo, metros, precio, activo, elim):
        tela = self.dataBase.select_tela(codigo)
        if elim is not False:
            tipo.config(state="normal")
            metros.config(state="normal")
            precio.config(state="normal")
            activo.config(state="normal")
        else:
            tipo.config(state="normal")

        tipo.delete(0, END)
        metros.delete(0, END)
        precio.delete(0, END)
        activo.delete(0, END)

        tipo.insert(0, str(tela[0]))
        metros.insert(0, str(tela[1]))
        precio.insert(0, str(tela[2]))
        activo.insert(0, str(tela[3]))

        if elim is not False:
            tipo.config(state="readonly")
            metros.config(state="readonly")
            precio.config(state="readonly")
            activo.config(state="readonly")
        else:
            tipo.config(state="readonly")

    def update_equipo(self, window):
        varNum = tkinter.StringVar()
        varCanti = tkinter.StringVar()
        varEspecialidad = tkinter.StringVar()

        updateEquipo = Toplevel(window)
        updateEquipo.title("Actualizacion de equipo")
        window.iconify()
        updateEquipo.protocol("WM_DELETE_WINDOW", lambda: self.erase(updateEquipo, window))
        self.posicionar(630, 100, updateEquipo)
        #----------------------------Interaccion----------------------------#
        numEquipoL = Label(updateEquipo, text="Seleccione el equipo:")
        numEquipoL.grid(row=0, column=0, padx=5, pady=3)
        numEquipo = ttk.Combobox(updateEquipo, textvariable=varNum, state="readonly")
        numEquipo.grid(row=0, column=1, padx=5, pady=3)
        numsEqui = self.dataBase.select_equipos()
        if len(numsEqui) > 0:
            lista = []
            for num in numsEqui:
                lista.append(str(num[0]))
            numEquipo["value"] = lista
        else:
            if(messagebox.showwarning(message="No hay equipos ingresados, ingrese alguno", title="Información") == "ok"):
                self.erase(updateEquipo, window)
                breakpoint()

        cantidadML = Label(updateEquipo, text="Cantidad de miembros:")
        cantidadML.grid(row=0, column=3, padx=5, pady=3)
        cantidadM = Entry(updateEquipo, textvariable=varCanti, validate="key", validatecommand=(updateEquipo.register(validate_int), "%S", "%P"))
        cantidadM.grid(row=0, column=4, padx=5, pady=3)

        especialidadEL = Label(updateEquipo, text="Selecione la especialidad")
        especialidadEL.grid(row=1, column=0, padx=5, pady=3)
        especialidad = ttk.Combobox(updateEquipo, textvariable=varEspecialidad, state="readonly")
        especialidad["values"] = ["Corte textil", "Patronaje"]
        especialidad.grid(row=1, column=1, padx=5, pady=3)
        buscar = Button(updateEquipo, text="Buscar", command=lambda: self.mostrar_equipo(int(varNum.get()), cantidadM, especialidad), cursor="hand2")
        buscar.grid(row=0, column=2, padx=5, pady=3)

        #----------------------------- Extraccion de valores ------------------------------#
        update = Button(updateEquipo, text="Actualizar", command=lambda: self.equipoMensajeU(varNum, varCanti, varEspecialidad), cursor="hand2")
        update.grid(row=2, column=1, padx=5, pady=3)

    def equipoMensajeU(self, varNum, varCanti, varEspecialidad):
        if varCanti.get() == "" or varEspecialidad.get() == "" or varNum.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            messagebox.showinfo(message="Equipo actualizado con exito", title="Información")
            self.dataBase.update_equipo(int(varNum.get()), int(varCanti.get()), varEspecialidad.get())

    def mostrar_equipo(self, num, cantidad, especialidad):
        equipo = self.dataBase.select_equipo(num)
        especialidad.config(state="normal")
        cantidad.delete(0, END)
        especialidad.delete(0, END)

        cantidad.insert(0, str(equipo[0]))
        especialidad.insert(0, str(equipo[1]))
        especialidad.config(state="readonly")

    def update_produccion(self, window):
        varID = tkinter.StringVar()
        varPedido = tkinter.StringVar()
        varEncargado = tkinter.StringVar()
        varEquipo = tkinter.StringVar()
        varMaquina = tkinter.StringVar()

        updateProduccion = Toplevel(window)
        updateProduccion.title("Actualizacion de produccion")
        window.iconify()
        updateProduccion.protocol("WM_DELETE_WINDOW", lambda: self.erase(updateProduccion, window))
        self.posicionar(670, 120, updateProduccion)
        #-------------------------- Interaccion --------------------------#
        #Buscar entre la produccion
        idProduccionL = Label(updateProduccion, text="Seleccione el id de produccion:")
        idProduccionL.grid(row=0, column=0, padx=5, pady=3)
        idProduccion = ttk.Combobox(updateProduccion, textvariable=varID, state="readonly")
        idProduccion.grid(row=0, column=1, padx=5, pady=3)
        ids = self.dataBase.select_producciones()
        if len(ids) > 0:
            lista = []
            for i in ids:
                lista.append(str(i[0]))
            idProduccion["value"] = lista
        else:
            if(messagebox.showwarning(message="No hay producciones ingresadas, ingrese alguno", title="Información") == "ok"):
                self.erase(updateProduccion, window)
                breakpoint()

        numPedidoL = Label(updateProduccion, text="Numero del pedido:")
        numPedidoL.grid(row=0, column=3, padx=5, pady=3)
        numPedido = ttk.Combobox(updateProduccion, textvariable=varPedido, state="readonly")
        numPedido.grid(row=0, column=4, padx=5, pady=3)
        pedidos = self.dataBase.select_pedidos()
        if len(pedidos) > 0:
            lista = []
            for ped in pedidos:
                lista.append(str(ped[0]))
            numPedido["value"] = lista
        else:
            if(messagebox.showwarning(message="No hay pedidos ingresados, ingrese alguno", title="Información")):
                self.erase(updateProduccion, window)
                breakpoint()

        numEncargadoL = Label(updateProduccion, text="Numero del encargado:")
        numEncargadoL.grid(row=1, column=0, padx=5, pady=3)
        numEncargado = ttk.Combobox(updateProduccion, textvariable=varEncargado, state="readonly")
        numEncargado["values"] = ["10230124", "22412421", "42413234", "5234135"]
        numEncargado.grid(row=1, column=1, padx=5, pady=3)

        numEquipoL = Label(updateProduccion, text="Numero del equipo")
        numEquipoL.grid(row=1, column=3, padx=5, pady=3)
        numEquipo = ttk.Combobox(updateProduccion, textvariable=varEquipo,state="readonly")
        numEquipo.grid(row=1, column=4, padx=5, pady=3)
        numsEqui = self.dataBase.select_equipos()
        if len(numsEqui) > 0:
            lista = []
            for num in numsEqui:
                lista.append(str(num[0]))
            numEquipo["value"] = lista
        else:
            if(messagebox.showwarning(message="No hay equipos ingresados, ingrese alguno", title="Información")):
                self.erase(updateProduccion, window)
                breakpoint()

        maquinariaL = Label(updateProduccion, text="Tipo de maquinaria:")
        maquinariaL.grid(row=2, column=0, padx=5, pady=3)
        maquinaria = ttk.Combobox(updateProduccion, textvariable=varMaquina, state="readonly")
        maquinaria["values"] = ["CN0574", "CN0563", "CN05832", "PT9382", "PT4721", "PT9310"]
        maquinaria.grid(row=2, column=1, padx=5, pady=3)

        buscar = Button(updateProduccion, text="Buscar", command=lambda: self.mostrar_produccion(int(varID.get()), numPedido,
                                                                                             numEncargado, numEquipo, maquinaria), cursor="hand2")
        buscar.grid(row=0, column=2, padx=5, pady=3)

        #---------------------------- Extraccion de valores --------------------------------#
        update = Button(updateProduccion, text="Actualizar", command=lambda: self.produccionMensajeU(varID, numPedido, numEncargado, numEquipo, maquinaria), cursor="hand2")
        update.grid(row=3, column=1, padx=5, pady=3)

    def produccionMensajeU(self, varID, numPedido, numEncargado, numEquipo, maquinaria):
        if varID.get() == "" or numPedido.get() == "" or numEncargado.get() == "" or numEquipo.get() == "" or maquinaria.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            messagebox.showinfo(message="Produccion actualizada con exito", title="Información")
            self.dataBase.update_produccion(int(varID.get()), int(numPedido.get()), int(numEncargado.get()), int(numEquipo.get()), maquinaria.get())

    def mostrar_produccion(self, id, pedido, encargado, equipo, maquinaria):
        produccion = self.dataBase.select_produccion(id)
        pedido.config(state="normal")
        encargado.config(state="normal")
        equipo.config(state="normal")
        maquinaria.config(state="normal")

        pedido.delete(0, END)
        encargado.delete(0, END)
        equipo.delete(0, END)
        maquinaria.delete(0, END)

        pedido.insert(0, str(produccion[0]))
        encargado.insert(0, str(produccion[1]))
        equipo.insert(0, str(produccion[2]))
        maquinaria.insert(0, str(produccion[3]))

        pedido.config(state="readonly")
        encargado.config(state="readonly")
        equipo.config(state="readonly")

    def update_cliente(self, window):
        varDni = tkinter.StringVar()
        varNombre = tkinter.StringVar()
        varApellidos = tkinter.StringVar()
        varDireccion = tkinter.StringVar()
        varTelefono = tkinter.StringVar()
        varActivo = tkinter.StringVar()

        updateCliente = Toplevel(window)
        updateCliente.title("Actualizacion de cliente")
        window.iconify()
        updateCliente.protocol("WM_DELETE_WINDOW", lambda: self.erase(updateCliente, window))
        self.posicionar(550, 120, updateCliente)
        #------------------------------ Interaccion -----------------------------------#
        #Buscar entre los clientes
        dniL = Label(updateCliente, text="Seleccione el DNI:")
        dniL.grid(row=0, column=0, padx=5, pady=3)
        dni = ttk.Combobox(updateCliente, textvariable=varDni, state="readonly")
        dni.grid(row=0, column=1, padx=5, pady=3)
        codigos = self.dataBase.select_clients(True)
        if len(codigos) > 0:
            lista = []
            for codigo in codigos:
                lista.append(str(codigo[0]))
            dni["value"] = lista
        else:
            if (messagebox.showwarning(message="No hay clientes ingresados, ingrese alguno", title="Información")) == "ok":
                self.erase(updateCliente, window)
                breakpoint()

        nombresL = Label(updateCliente, text="Nombre(s):")
        nombresL.grid(row=0, column=3, padx=5, pady=3)
        nombres = Entry(updateCliente, textvariable=varNombre, validate="key", validatecommand=(updateCliente.register(validate_char), "%S"))
        nombres.grid(row=0, column=4, padx=5, pady=3)

        appellidosL = Label(updateCliente, text="Apellidos")
        appellidosL.grid(row=1, column=0, padx=5, pady=3)
        apellidos = Entry(updateCliente, textvariable=varApellidos, validate="key", validatecommand=(updateCliente.register(validate_char), "%S"))
        apellidos.grid(row=1, column=1, padx=5, pady=3)

        direccionL = Label(updateCliente, text="Direccion")
        direccionL.grid(row=1, column=3, padx=5, pady=3)
        direccion = Entry(updateCliente, textvariable=varDireccion)
        direccion.grid(row=1, column=4, padx=5, pady=3)

        telefonoL = Label(updateCliente, text="Telefono")
        telefonoL.grid(row=2, column=0, padx=5, pady=3)
        telefono = Entry(updateCliente, textvariable=varTelefono, validate="key", validatecommand=(updateCliente.register(validate_int), "%S", "%P"))
        telefono.grid(row=2, column=1, padx=5, pady=3)

        activoL = Label(updateCliente, text="Activo:")
        activoL.grid(row=2, column=3, padx=5, pady=3)
        activo = ttk.Combobox(updateCliente, textvariable=varActivo, state="readonly")
        activo["values"] = ["S", "N"]
        activo.grid(row=2, column=4, padx=5, pady=3)

        buscar = Button(updateCliente, text="Buscar", command=lambda: self.mostrar_cliente(int(varDni.get()),
                                                                                            nombres, apellidos, direccion
                                                                                            , telefono, activo, False), cursor="hand2")
        buscar.grid(row=0, column=2, padx=5, pady=3)
        #------------------------ Extraccion de valores ---------------------------#
        update = Button(updateCliente, text="Actualizar", command=lambda: self.clienteMensajeU(varDni, varNombre, varApellidos, varDireccion, varTelefono, varActivo), cursor="hand2")
        update.grid(row=3, column=1, padx=5, pady=3)

    def clienteMensajeU(self, varDni, varNombre, varApellidos, varDireccion, varTelefono, varActivo):
        if varDni.get() == "" or varNombre.get() == "" or varApellidos.get() == "" or varDireccion.get() == "" or varTelefono.get() == "" or varActivo.get() == "":
            messagebox.showwarning(message="Todos los campos son requeridos", title="Información")
        else:
            messagebox.showinfo(message="Cliente actualizado con exito", title="Información")
            self.dataBase.update_cliente(int(varDni.get()), varNombre.get(), varApellidos.get(), varDireccion.get(), int(varTelefono.get()), varActivo.get())

    def mostrar_cliente(self, DNI, nombre, apellidos, direccion, telefono, activo, elim):
        cliente = self.dataBase.select_client(DNI)
        if elim is not False:
            nombre.config(state="normal")
            apellidos.config(state="normal")
            direccion.config(state="normal")
            telefono.config(state="normal")
            activo.config(state="normal")
        else:
            activo.config(state="normal")
        nombre.delete(0, END)
        apellidos.delete(0, END)
        direccion.delete(0, END)
        telefono.delete(0, END)
        activo.delete(0, END)

        nombre.insert(0, str(cliente[0]))
        apellidos.insert(0, str(cliente[1]))
        direccion.insert(0, str(cliente[2]))
        telefono.insert(0, str(cliente[3]))
        activo.insert(0, str(cliente[4]))

        if elim is not False:
            nombre.config(state="readonly")
            apellidos.config(state="readonly")
            direccion.config(state="readonly")
            telefono.config(state="readonly")
            activo.config(state="readonly")
        else:
            activo.config(state="readonly")

    def delete(self):
        windowD = Toplevel(self)
        windowD.title("Eliminación de datos")
        self.iconify()
        windowD.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowD))
        self.posicionar(400, 200, windowD)
        windowD.iconphoto(True, PhotoImage(file='./iconos/eliminar.png'))
        #--------------------------- Interaccion -----------------------------#

        cliente = Button(windowD, text="Eliminar cliente", command=lambda: self.eliminar_cliente(windowD), cursor="hand2")
        cliente.grid(row=1, column=0, padx=10, pady=10)
        imagenCliente = Label(windowD, image=self.imagenes["eliminar"][0])
        imagenCliente.grid(row=0, column=0, padx=50, pady=10)

        tela = Button(windowD, text="Eliminar tela", command=lambda: self.eliminar_tela(windowD), cursor="hand2")
        tela.grid(row=1, column=1, padx=10, pady=10)
        imagenTela = Label(windowD, image=self.imagenes["eliminar"][1])
        imagenTela.grid(row=0, column=1, padx=50, pady=10)

    def eliminar_cliente(self, window):
        varDni = tkinter.StringVar()

        deleteCliente = Toplevel(window)
        deleteCliente.title("Eliminación de cliente")
        window.iconify()
        deleteCliente.protocol("WM_DELETE_WINDOW", lambda: self.erase(deleteCliente, window))
        self.posicionar(550, 120, deleteCliente)
        #------------------ Interaccion---------------------#
        dniL = Label(deleteCliente, text="Seleccione del DNI")
        dniL.grid(row=0, column=0)
        dni = ttk.Combobox(deleteCliente, textvariable=varDni, state="readonly")
        dni.grid(row=0, column=1)
        codigos = self.dataBase.select_clients(False)
        if len(codigos) > 0:
            lista = []
            for codigo in codigos:
                lista.append(str(codigo[0]))
            dni["value"] = lista
        else:
            messagebox.showwarning(message="No hay clientes ingresados, ingrese alguno", title="Información")
            self.erase(deleteCliente, window)
            breakpoint()
        nombresL = Label(deleteCliente, text="Nombre(s):")
        nombresL.grid(row=0, column=3, padx=5, pady=3)
        nombres = Entry(deleteCliente)
        nombres.grid(row=0, column=4, padx=5, pady=3)

        appellidosL = Label(deleteCliente, text="Apellidos")
        appellidosL.grid(row=1, column=0, padx=5, pady=3)
        apellidos = Entry(deleteCliente)
        apellidos.grid(row=1, column=1, padx=5, pady=3)

        direccionL = Label(deleteCliente, text="Direccion")
        direccionL.grid(row=1, column=3, padx=5, pady=3)
        direccion = Entry(deleteCliente)
        direccion.grid(row=1, column=4, padx=5, pady=3)

        telefonoL = Label(deleteCliente, text="Telefono")
        telefonoL.grid(row=2, column=0, padx=5, pady=3)
        telefono = Entry(deleteCliente)
        telefono.grid(row=2, column=1, padx=5, pady=3)

        activoL = Label(deleteCliente, text="Activo:")
        activoL.grid(row=2, column=4, padx=5, pady=3)
        activo = Entry(deleteCliente)
        activo.grid(row=2, column=4, padx=5, pady=3)


        buscar = Button(deleteCliente, text="Buscar", command=lambda: self.mostrar_cliente(int(varDni.get()),
                                                                                            nombres, apellidos, direccion
                                                                                            , telefono, activo, True), cursor="hand2")
        buscar.grid(row=0, column=2, padx=5, pady=3)

        #-------------------------- Extraccion de valores --------------------------------#
        if len(codigos) > 0:
            borrar = Button(deleteCliente, text="Eliminar", command=lambda: self.clienteEM(varDni), cursor="hand2")
            borrar.grid(row=3, column=1, padx=5, pady=3)

    def clienteEM(self, varDni):
        if varDni.get() == "":
            messagebox.showwarning(message="El DNI es requerido", title="Información")
        else:
            messagebox.showinfo(message="Cliente eliminado con exito", title="Información")
            self.dataBase.delete_cliente(int(varDni.get()))

    def eliminar_tela(self, window):
        varTela = tkinter.StringVar()
        deleteTela = Toplevel(window)
        deleteTela.title("Eliminación de tela")
        window.iconify()
        deleteTela.protocol("WM_DELETE_WINDOW", lambda: self.erase(deleteTela, window))
        self.posicionar(640, 120, deleteTela)
        #---------------------------- Interaccion-----------------------------#
        codigoTelaL = Label(deleteTela, text="Seleccione el codigo de la tela:")
        codigoTelaL.grid(row=0, column=0, padx=5, pady=3)
        codigoTela = ttk.Combobox(deleteTela, textvariable=varTela, state="readonly")
        codigoTela.grid(row=0, column=1, padx=5, pady=3)
        codigos = self.dataBase.select_telas(False)
        if len(codigos) > 0:
            lista = []
            for codigo in codigos:
                lista.append(str(codigo[0]))
            codigoTela["values"] = lista
        else:
            messagebox.showwarning(message="No hay telas ingresadas, ingrese alguna", title="Información")
            self.erase(deleteTela, window)
            breakpoint()
        tipoL = Label(deleteTela, text="Tipo de tela:")
        tipoL.grid(row=0, column=3, padx=5, pady=3)
        tipo = Entry(deleteTela, state="readonly")
        tipo.grid(row=0, column=4, padx=5, pady=3)

        metrosL = Label(deleteTela, text="Metros de tela:")
        metrosL.grid(row=1, column=0, padx=5, pady=3)
        metros = Entry(deleteTela, state="readonly")
        metros.grid(row=1, column=1, padx=5, pady=3)

        precioL = Label(deleteTela, text="Precio por metro:")
        precioL.grid(row=1, column=3, padx=5, pady=3)
        precio = Entry(deleteTela, state="readonly")
        precio.grid(row=1, column=4, padx=5, pady=3)

        activoL = Label(deleteTela, text="Activo:")
        activoL.grid(row=2, column=0, padx=5, pady=3)
        activo = Entry(deleteTela)
        activo.grid(row=2, column=1, padx=5, pady=3)

        buscar = Button(deleteTela, text="Buscar", command=lambda: self.mostrarStock(int(varTela.get()), tipo, metros, precio,
                                                                                     activo, True), cursor="hand2")
        buscar.grid(row=0, column=2, padx=5, pady=3)

        #---------------------------- Extraccion de valores -------------------------#
        borrar = Button(deleteTela, text="Eliminar", command=lambda: self.telaEM(varTela), cursor="hand2")
        borrar.grid(row=3, column=1, padx=5, pady=3)

    def telaEM(self, varTela):
        if varTela.get() == "":
            messagebox.showwarning(message="El codigo de la tela es requerido", title="Información")
        else:
            messagebox.showinfo(message="Tela eliminada con exito", title="Información")
            self.dataBase.delete_tela(int(varTela.get()))

    def insert_p(self):
        varCedula = tkinter.StringVar()
        varNombre = tkinter.StringVar()
        varApellidos = tkinter.StringVar()
        varDireccion = tkinter.StringVar()
        varTelefono = tkinter.StringVar()
        varServicio = tkinter.StringVar()
        varPrenda = tkinter.StringVar()
        varSexo = tkinter.StringVar()
        varMedidas = tkinter.StringVar()

        windowP = Toplevel(self)
        windowP.title("Realizar pedido")
        self.iconify()
        windowP.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowP))
        self.posicionar(540, 150, windowP)
        #------------------------------- Interaccion -----------------------------#
        cedulaL = Label(windowP, text="Ingrese cedula:")
        cedulaL.grid(row=0, column=0, padx=5, pady=3)
        cedula = Entry(windowP, textvariable=varCedula, validate="key", validatecommand=(windowP.register(validate_int), "%S", "%P"))
        cedula.grid(row=0, column=1)

        nombresL = Label(windowP, text="Ingrese nombre(s):")
        nombresL.grid(row=1, column=0, padx=5, pady=3)
        nombres = Entry(windowP, textvariable=varNombre, validate="key", validatecommand=(windowP.register(validate_char), "%S", "%P"))
        nombres.grid(row=1, column=1)

        appellidosL = Label(windowP, text="Ingrese apellidos")
        appellidosL.grid(row=0, column=2, padx=5, pady=3)
        apellidos = Entry(windowP, textvariable=varApellidos, validate="key", validatecommand=(windowP.register(validate_char), "%S", "%P"))
        apellidos.grid(row=0, column=3)

        direccionL = Label(windowP, text="Ingrese direccion")
        direccionL.grid(row=2, column=0, padx=5, pady=3)
        direccion = Entry(windowP, textvariable=varDireccion)
        direccion.grid(row=2, column=1)

        telefonoL = Label(windowP, text="Ingrese telefono")
        telefonoL.grid(row=1, column=2, padx=5)
        telefono = Entry(windowP, textvariable=varTelefono, validate="key", validatecommand=(windowP.register(validate_int), "%S"))
        telefono.grid(row=1, column=3)

        productoL = Label(windowP, text="Servicio:")
        productoL.grid(row=3, column=0)
        servicio = ttk.Combobox(windowP, textvariable=varServicio, state="readonly")
        servicio["values"] = ["Corte textil", "Patronaje"]
        servicio.grid(row=3, column=1)

        prendaL = Label(windowP, text="Prenda:")
        prendaL.grid(row=2, column=2)
        prenda = ttk.Combobox(windowP, textvariable=varPrenda, state="readonly")
        prenda["values"] = ["vestido", "camisa", "pantalon", "blusa", "chaqueta", "abrigo"]
        prenda.grid(row=2, column=3)

        paraL = Label(windowP, text="Sexo:")
        paraL.grid(row=3, column=2)
        para = ttk.Combobox(windowP, textvariable=varSexo,state="readonly")
        para["values"] = ["Niña", "Niño", "Hombre", "Mujer"]
        para.grid(row=3, column=3)

        medidasL = Label(windowP, text="Medidas:")
        medidasL.grid(row=4, column=0)
        medidas = Entry(windowP, textvariable=varMedidas, validate="key", validatecommand=(windowP.register(validate_int), "%S"))
        medidas.grid(row=4, column=1)

        #------------------------------ Extraccion de valores --------------------------------#
        accept = Button(windowP, text="Insertar", command=lambda: self.mensajePedido(varCedula, varNombre,
                                                                             varApellidos,
                                                                                varTelefono, varDireccion, varServicio,
                                                                                varPrenda, varSexo, varMedidas), cursor="hand2")
        accept.grid(row=5, column=1)

    def mensajePedido(self, varCedula, varNombre, varApellidos, varTelefono, varDireccion, varServicio,
                      varPrenda, varSexo, varMedidas):
        if varCedula.get() == "" or varNombre.get() == "" or varApellidos.get() == "" or varTelefono.get() == "" or varDireccion.get() == "" or varServicio.get() == "" or varPrenda.get() == "" or varSexo.get() == "" or varMedidas.get() == "":
            messagebox.showwarning(message="!Todos los campos son requeridos¡", title="Información")
        else:
            self.dataBase.insert_client(int(varCedula.get()), varNombre.get(), varApellidos.get(), varDireccion.get(), int(varTelefono.get()))
            self.dataBase.insert_pedido(int(varCedula.get()), varServicio.get(), varPrenda.get(), varSexo.get(), int(varMedidas.get()))
            messagebox.showinfo(message="!Pedido y cliente agregados con exito¡", title="Información")

    def generar_F(self):
        varPedido = tkinter.StringVar()
        varCedula = tkinter.StringVar()
        varNombre = tkinter.StringVar()
        varApellidos = tkinter.StringVar()
        varDireccion = tkinter.StringVar()
        varTelefono = tkinter.StringVar()
        varServicio = tkinter.StringVar()
        varPrenda = tkinter.StringVar()
        varSexo = tkinter.StringVar()
        varMedidas = tkinter.StringVar()
        varCosto = tkinter.StringVar()
        varMetodo = tkinter.StringVar()

        windowFactura = Toplevel(self)
        windowFactura.title("Factura")
        self.iconify()
        windowFactura.protocol("WM_DELETE_WINDOW", lambda: self.erase(windowFactura))
        self.posicionar(580, 200, windowFactura)
        #------------------------------- Interaccion ----------------------------------#
        numPedidoL = Label(windowFactura, text="Numero del pedido:")
        numPedidoL.grid(row=0, column=0)
        numPedido = ttk.Combobox(windowFactura, textvariable=varPedido, state="readonly")
        numPedido.grid(row=0, column=1)

        valores = self.dataBase.select_facturas()
        if len(valores) > 0:
            lista1 = []
            for valor in valores:
                lista1.append(str(valor[0]))
            numPedido["values"] = lista1
        else:
            self.erase(windowProduccion, window)
            breakpoint()

        dniL = Label(windowFactura, text="DNI del cliente:")
        dniL.grid(row=0, column=2)
        dni = Entry(windowFactura, textvariable=varCedula)
        dni.grid(row=0, column=3)

        nombresL = Label(windowFactura, text="Nombre(s) cliente:")
        nombresL.grid(row=1, column=0, padx=3, pady=3)
        nombres = Entry(windowFactura, textvariable=varNombre, validate="key", validatecommand=(windowFactura.register(validate_char), "%S", "%P"))
        nombres.grid(row=1, column=1)

        appellidosL = Label(windowFactura, text="Apellidos cliente:")
        appellidosL.grid(row=1, column=2, padx=3, pady=3)
        apellidos = Entry(windowFactura, textvariable=varApellidos)
        apellidos.grid(row=1, column=3)

        direccionL = Label(windowFactura, text="Direccion cliente:")
        direccionL.grid(row=2, column=0, padx=3, pady=3)
        direccion = Entry(windowFactura, textvariable=varDireccion)
        direccion.grid(row=2, column=1)

        telefonoL = Label(windowFactura, text="Telefono cliente:")
        telefonoL.grid(row=2, column=2, padx=5, pady=3)
        telefono = Entry(windowFactura, textvariable=varTelefono, validate="key", validatecommand=(windowFactura.register(validate_int), "%S"))
        telefono.grid(row=2, column=3)

        productoL = Label(windowFactura, text="Servicio:")
        productoL.grid(row=3, column=0, padx=5, pady=3)
        servicio = Entry(windowFactura, textvariable=varServicio)
        servicio.grid(row=3, column=1, padx=5, pady=3)

        prendaL = Label(windowFactura, text="Prenda:")
        prendaL.grid(row=3, column=2, padx=5, pady=3)
        prenda = Entry(windowFactura, textvariable=varPrenda)
        prenda.grid(row=3, column=3, padx=5, pady=3)

        paraL = Label(windowFactura, text="Sexo:")
        paraL.grid(row=5, column=0, padx=5, pady=3)
        para = Entry(windowFactura, textvariable=varSexo)
        para.grid(row=5, column=1, padx=5, pady=3)

        medidasL = Label(windowFactura, text="Medidas:")
        medidasL.grid(row=4, column=0, padx=5, pady=3)
        medidas = Entry(windowFactura, textvariable=varMedidas)
        medidas.grid(row=4, column=1, padx=5, pady=3)

        costoL = Label(windowFactura, text="Precio")
        costoL.grid(row=4, column=2, padx=5, pady=3)
        costo = Entry(windowFactura, textvariable=varCosto, validate="key", validatecommand=(windowFactura.register(validate_int), "%S"))
        costo.grid(row=4, column=3, padx=5, pady=3)

        metodoL = Label(windowFactura, text="Metodo de pago:")
        metodoL.grid(row=5, column=2, padx=5, pady=3)
        metodo = ttk.Combobox(windowFactura, textvariable=varMetodo, state="readonly")
        metodo.grid(row=5, column=3, padx=5, pady=3)
        metodo["values"] = ["Efectivo", "Credito", "Tarjeta de credito"]

        #---------------------------Busqueda------------------------------#
        buscar = Button(windowFactura, text="Buscar", command= lambda: self.mostrar_datos(int(varPedido.get()),
                                                                                          dni, nombres,
                                                                                          apellidos, direccion,
                                                                                          telefono, servicio, prenda,
                                                                                          para, medidas), cursor="hand2")
        buscar.grid(row=0, column=4)

        accept = Button(windowFactura, text="Generar factura", command= lambda: self.mensaje_factura(varPedido, varCedula, varCosto, varMetodo), cursor="hand2")
        accept.grid(row=6, column=1, padx=5, pady=5)

    def mensaje_factura(self, varPedido, varCedula, varCosto, varMetodo):

        if varPedido.get() == "" or varCedula.get() == "" or varCosto.get() == "" or varMetodo == "":
            messagebox.showwarning(message="!Todos los campos son requeridos¡",title="Información")
        else:
            self.dataBase.insert_factura(int(varPedido.get()), int(varCedula.get()), float(varCosto.get()), varMetodo.get())
            messagebox.showinfo(message="!Factura agregada con exito¡", title="Información")

    def mostrar_datos(self, numPedido, dni, nombres, apellidos, direccion, telefono, servicio, prenda, para, medidas):

        datos = self.dataBase.select_factura(int(numPedido))

        dni.config(state="normal")
        nombres.config(state="normal")
        apellidos.config(state="normal")
        direccion.config(state="normal")
        telefono.config(state="normal")
        servicio.config(state="normal")
        prenda.config(state="normal")
        para.config(state="normal")
        medidas.config(state="normal")

        dni.delete(0, END)
        nombres.delete(0, END)
        apellidos.delete(0, END)
        direccion.delete(0, END)
        telefono.delete(0, END)
        servicio.delete(0, END)
        prenda.delete(0, END)
        para.delete(0, END)
        medidas.delete(0, END)

        dni.insert(0, str(datos[1]))
        servicio.insert(0, str(datos[2]))
        prenda.insert(0, str(datos[3]))
        para.insert(0, str(datos[4]))
        medidas.insert(0, str(datos[5]))
        nombres.insert(0, str(datos[8]))
        apellidos.insert(0, str(datos[9]))
        direccion.insert(0, str(datos[10]))
        telefono.insert(0, str(datos[11]))

        dni.config(state="readonly")
        nombres.config(state="readonly")
        apellidos.config(state="readonly")
        direccion.config(state="readonly")
        telefono.config(state="readonly")
        servicio.config(state="readonly")
        prenda.config(state="readonly")
        para.config(state="readonly")
        medidas.config(state="readonly")

    #Metodo para abrir ventana padre cuando se cierra la ventana hija
    def erase(self, windowH, windowP=None):
        if windowP is None:
            self.deiconify()
            windowH.destroy()
        else:
            windowP.deiconify()
            windowH.destroy()
        self.iconphoto(True, PhotoImage(file='./iconos/registro.png'))

    def posicionar(self, tamx, tamy, window, resize=False):
        screen = self.screenSize
        posx = (screen[0] // 2) - tamx // 2
        posy = (screen[1] // 2) - tamy // 2
        window.geometry("{}x{}+{}+{}".format(tamx, tamy, posx, posy))
        if resize is False:
            window.maxsize(tamx, tamy)
        else:
            window.maxsize(tamx, 2 * tamy)

        window.minsize(tamx, tamy)


if __name__ == '__main__':
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    app = App()
    imagenes = {"insertar": [PhotoImage(file='fondos/equipos.png'), PhotoImage(file='fondos/telas.png'), PhotoImage(file='fondos/produccion.png')],
                "actualizar": [PhotoImage(file='fondos/telasA.png'), PhotoImage(file='fondos/equipoA.png'),
                               PhotoImage(file='fondos/clienteA.png'), PhotoImage(file='fondos/produccionA.png')],
                "eliminar": [PhotoImage(file='fondos/clienteD.png'), PhotoImage(file='fondos/telas.png')]}
    app.imagenes = imagenes
    app.title("Taller de costura")
    app.screenSize.append(ancho)
    app.screenSize.append(alto)
    app.posicionar(470, 300, app)
    imagen = PhotoImage(file='fondos/maquina.png')
    imgLb = Label(app, image=imagen)
    imgLb.grid(row=0, column=1)
    app.mainloop()
    app.dataBase.close()

