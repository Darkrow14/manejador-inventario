import pymysql


class DataBase:
    def __init__(self):
        self.conecction = pymysql.connect(
            host='localhost',
            user='admin',
            password='1234',
            db='tallercostura'
        )
        self.cursor = self.conecction.cursor()

    def create_tables(self):
        tablas = [
            'CREATE TABLE IF NOT EXISTS `clientes` ( `DNI` int(11) NOT NULL, `NOMBRE(S)` varchar(50) COLLATE latin1_spanish_ci NOT NULL, `APELLIDOS` varchar(50) COLLATE latin1_spanish_ci NOT NULL, `DIRECCION` varchar(50) COLLATE latin1_spanish_ci NOT NULL, `TELEFONO` int(11) NOT NULL, `ACTIVO` varchar(1) COLLATE latin1_spanish_ci NOT NULL, PRIMARY KEY (`DNI`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci COMMENT="Tabla que contiene a los clientes"',
            'CREATE TABLE IF NOT EXISTS `equipos` ( `NUMEQ` int(10) NOT NULL AUTO_INCREMENT, `CANTEMP` int(11) NOT NULL, `ESPECIALIDAD` varchar(20) COLLATE latin1_spanish_ci NOT NULL, PRIMARY KEY (`NUMEQ`) ) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci',
            'CREATE TABLE IF NOT EXISTS `facturas` ( `ID_FACTURA` int(11) NOT NULL AUTO_INCREMENT, `NUMPED` int(11) NOT NULL, `DNI` int(11) NOT NULL, `PRECIO` float NOT NULL, `FORMA_DE_PAGO` varchar(25) COLLATE latin1_spanish_ci NOT NULL, PRIMARY KEY (`ID_FACTURA`) ) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci',
            'CREATE TABLE IF NOT EXISTS `pedidos` ( `NUMPED` int(11) NOT NULL AUTO_INCREMENT, `DNI` int(11) NOT NULL, `DESCRIPCION` varchar(50) COLLATE latin1_spanish_ci NOT NULL, `MODELO` varchar(20) COLLATE latin1_spanish_ci NOT NULL, `PARA` varchar(10) COLLATE latin1_spanish_ci NOT NULL, `MEDIDAS` varchar(50) COLLATE latin1_spanish_ci NOT NULL, `ACTIVO` varchar(1) COLLATE latin1_spanish_ci NOT NULL, PRIMARY KEY (`NUMPED`) ) ENGINE=MyISAM AUTO_INCREMENT=12336 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci',
            'CREATE TABLE IF NOT EXISTS `produccion` ( `ID_PRODUCCION` int(10) NOT NULL AUTO_INCREMENT, `NUMPED` int(11) NOT NULL, `NUMENCARGA` int(11) NOT NULL, `NUMEQUI` int(11) NOT NULL, `MAQUINA` varchar(25) COLLATE latin1_spanish_ci NOT NULL, PRIMARY KEY (`ID_PRODUCCION`) ) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci',
            'CREATE TABLE IF NOT EXISTS `telas` ( `CODIGOT` int(11) NOT NULL AUTO_INCREMENT, `TIPO` varchar(20) COLLATE latin1_spanish_ci NOT NULL, `METROS` float NOT NULL, `PRECIO_BASE` float NOT NULL, `ACTIVO` varchar(1) COLLATE latin1_spanish_ci NOT NULL, PRIMARY KEY (`CODIGOT`) ) ENGINE=MyISAM AUTO_INCREMENT=135 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci'
        ]

        for instruction in tablas:
            self.cursor.execute(instruction)

    def select_facturas(self):
        sql = "SELECT pedidos.NUMPED FROM pedidos, clientes WHERE pedidos.DNI = clientes.DNI"

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def select_factura(self, pedido):
        sql = "SELECT * FROM pedidos, clientes WHERE (pedidos.DNI = clientes.DNI AND pedidos.NUMPED = {})".format(pedido)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            raise e

    def facturas(self):
        sql = "SELECT * FROM facturas"

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall(), self.cursor.rowcount
        except Exception as e:
            raise e

    def select_client(self, DNI):
        sql = 'SELECT `NOMBRE(S)`, APELLIDOS, DIRECCION, TELEFONO, ACTIVO FROM clientes WHERE DNI = {}'.format(DNI)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            raise e

    def select_clients(self, actualizar=True, single=True):
        if single is True:
            if actualizar is not True:
                sql = "SELECT DNI FROM clientes WHERE ACTIVO = 'S' "
            else:
                sql = "SELECT DNI FROM clientes"
        else:
            sql = "SELECT * FROM clientes"
        try:
            self.cursor.execute(sql)
            if single is True:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchall(), self.cursor.rowcount
        except Exception as e:
            raise e

    def select_tela(self, codigo):
        sql = "SELECT TIPO, METROS, PRECIO_BASE, ACTIVO FROM telas WHERE CODIGOT ={}".format(codigo)
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            raise e

    def select_telas(self, actualizar=True, single=True):
        if single is True:
            if actualizar is not True:
                sql = "SELECT CODIGOT FROM telas WHERE ACTIVO = 'S' "
            else:
                sql = "SELECT CODIGOT FROM telas"
        else:
            sql = "SELECT * FROM telas"
        try:
            self.cursor.execute(sql)
            if single is True:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchall(), self.cursor.rowcount
        except Exception as e:
            raise e

    def select_equipos(self, single=True):
        if single is True:
            sql = "SELECT NUMEQ FROM equipos"
        else:
            sql = "SELECT * FROM equipos"

        try:
            self.cursor.execute(sql)
            if single is True:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchall(), self.cursor.rowcount

        except Exception as e:
            raise e

    def select_equipo(self, numero):
        sql = "SELECT CANTEMP, ESPECIALIDAD FROM equipos WHERE NUMEQ = {}".format(numero)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            raise e

    def select_producciones(self, single=True):
        if single is True:
            sql = "SELECT ID_PRODUCCION FROM produccion"
        else:
            sql = "SELECT * FROM produccion"

        try:
            self.cursor.execute(sql)
            if single is True:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchall(), self.cursor.rowcount
        except Exception as e:
            raise e

    def select_produccion(self, ID):

        sql = "SELECT NUMPED, NUMENCARGA, NUMEQUI, MAQUINA FROM produccion WHERE ID_PRODUCCION = {}".format(ID)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            raise e

    def select_pedidos(self, single=True):
        if single is True:
            sql = "SELECT NUMPED FROM pedidos"
        else:
            sql = "SELECT * FROM pedidos"
        try:
            self.cursor.execute(sql)
            if single is True:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchall(), self.cursor.rowcount
        except Exception as e:
            raise e

     #-----------Metodo para insertar un cliente en la tabla clientes---------#
    def insert_client(self, DNI, Nombre, Apellidos, Direccion, Telefono):
        sql = "INSERT INTO clientes (`DNI`, `NOMBRE(S)`, `APELLIDOS`, `DIRECCION`, `TELEFONO`, `ACTIVO`) VALUES ({}, '{}', '{}', '{}',{}, 'S')".format(DNI, Nombre, Apellidos, Direccion, Telefono)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    def insert_pedido(self, dni, Descripcion, modelo, para, medidas):

        sql = "INSERT INTO `pedidos` (`NUMPED`, `DNI`,`DESCRIPCION`, `MODELO`, `PARA`, `MEDIDAS`,`ACTIVO`) VALUES (NULL,'{}', '{}', '{}', '{}', {}, 'S')".format(dni, Descripcion, modelo, para, medidas)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Relacion entre el cliente y el pedido
    def insert_factura(self, pedido, dni, precio, metodo):
        sql = "INSERT INTO `facturas` (`ID_FACTURA`,`NUMPED`,`DNI`,`PRECIO`,`FORMA_DE_PAGO`) VALUES (NULL, {}, {}, {}, '{}')".format(pedido, dni, precio, metodo)

        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Inserción de equipo
    def insert_equipo(self, CantEmp, Especialidad):
        sql = "INSERT INTO `equipos` (`NUMEQ`, `CANTEMP`, `ESPECIALIDAD`) VALUES (NULL, {}, '{}')".format(CantEmp, Especialidad)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Insertar tela
    def insert_tela(self, tipo, metros, precioBase):
        sql = "INSERT INTO `telas` (`CODIGOT`, `TIPO`, `METROS`, `PRECIO_BASE`, `ACTIVO`) VALUES (NULL, '{}', {}, {}, 'S' )".format(tipo, metros, precioBase)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Ingresar produccion
    def insertar_produccion(self, NUMPED, dniL, numEqui, Maquinaria):
        sql = "INSERT INTO `produccion` (`ID_PRODUCCION`, `NUMPED`, `NUMENCARGA`, `NUMEQUI`, `MAQUINA`) VALUES (NULL, {}, {}, {}, '{}')".format(NUMPED, dniL, numEqui, Maquinaria)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Actualizar telas
    def update_tela(self, codigo, metros, precioBase, activo):
        sql = "UPDATE `telas` SET METROS={}, PRECIO_BASE={}, ACTIVO = '{}' WHERE CODIGOT = {}".format(metros, precioBase, activo, codigo)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Actualizar equipo
    def update_equipo(self, Num, CantEmp, Especialidad):
        sql = "UPDATE `equipos` SET CANTEMP={}, ESPECIALIDAD='{}' WHERE NUMEQ = {}".format(CantEmp, Especialidad, Num)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Actualizar produccion
    def update_produccion(self, Id, NUMPED, dniL, numEqui, Maquinaria):
        sql = "UPDATE `produccion` SET NUMPED={}, NUMENCARGA={}, NUMEQUI={}, MAQUINA='{}' WHERE ID_PRODUCCION = {}".format(NUMPED, dniL, numEqui, Maquinaria, Id)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Actualizar cliente
    def update_cliente(self, DNI, Nombre, Apellidos, Direccion, Telefono, Activo):
        sql = "UPDATE `clientes` SET `NOMBRE(S)`='{}', APELLIDOS='{}', DIRECCION='{}', TELEFONO={}, ACTIVO='{}' WHERE DNI={}".format(Nombre, Apellidos, Direccion, Telefono, Activo, DNI)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Eliminar cliente
    def delete_cliente(self, DNI):
        sql = "UPDATE `clientes` SET ACTIVO = 'N' WHERE DNI = {}".format(DNI)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    #Eliminar tela
    def delete_tela(self, CODIGOT):
        sql = "UPDATE `telas` SET `ACTIVO` = 'N' WHERE CODIGOT = {}".format(CODIGOT)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            raise e

    def close(self):
        self.conecction.close()
