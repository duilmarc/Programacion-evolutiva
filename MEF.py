import numpy as np
import copy

# usado para representar a los estados respecto a sus letras que corresponden
letra = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']


class Estado(object):
    def __init__(self, posicion):
        self.posicion = posicion
        self.estado = 0
        self.entrada_1 = 0
        self.entrada_2 = 0
        self.salida_1 = 0
        self.salida_2 = 0
        self.estado_salida_1 = posicion
        self.estado_salida_2 = posicion

    def set_estado(self, estado):
        self.estado = estado

    def inicial(self):
        self.estado = 2

    def inactivo(self):
        self.estado = 0

    def activo(self):
        self.estado = 1

    def set_entradas(self, valor):
        if valor:
            self.entrada_1 = valor
            self.entrada_2 = 0
        else:
            self.entrada_1 = valor
            self.entrada_2 = 1

    def set_salida_1(self, valor):
        self.salida_1 = valor

    def set_salida_2(self, valor):
        self.salida_2 = valor

    def set_estado_salida1(self,  estado):
        self.estado_salida_1 = estado

    def set_estado_salida2(self,  estado):
        self.estado_salida_2 = estado

    def cambiar_entradas(self):
        self.entrada_1, self.entrada_2 = self.entrada_2, self.entrada_1

    def cambiar_salida_1(self):
        if(self.salida_1 == 0):
            self.salida_1 = 1
        else:
            self.salida_1 = 0

    def cambiar_salida_2(self):
        if(self.salida_2 == 0):
            self.salida_2 = 1
        else:
            self.salida_2 = 0

    def mostrar(self):
        string = f'{self.estado}{self.entrada_1}{self.entrada_2}{self.salida_1}{self.salida_2}{letra[self.estado_salida_1]}{letra[self.estado_salida_2]}'
        return string

    def consultar(self, valor):
        if(valor == self.entrada_1):
            return [self.estado_salida_1, self.salida_1]
        else:
            return [self.estado_salida_2, self.salida_2]


class MEF():
    def __init__(self, cantidad_estados):
        self.estados = []
        self.cantidad_estados = cantidad_estados
        self.activos = []
        self.inactivos = []
        self.inicial = -1
        for iterador in range(cantidad_estados):
            nuevo_estado = Estado(iterador)
            self.estados.append(nuevo_estado)

    def imprimir(self):
        cadena = ''
        for iterador in range(self.cantidad_estados):
            cadena += f'{self.estados[iterador].mostrar()}'
        return cadena

    def set_inicial(self):
        pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
        elegido = self.estados[pos_elegido]
        while(elegido.posicion == self.inicial):
            pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
            elegido = self.estados[pos_elegido]
        self.inicial = elegido.posicion
        elegido.inicial()
        return elegido.posicion

    def cambiar_inicial(self):
        posicion = self.inicial
        pos = self.set_inicial()
        print(f'Seteando posicional inicial a estado: {letra[pos]}')
        self.estados[posicion].activo()

    def set_estados(self):
        apuntador = 0
        for estado in self.estados:
            posicion_aleatorio1 = np.random.randint(0, len(self.activos))
            posicion_aleatorio2 = np.random.randint(0, len(self.activos))
            while(apuntador == posicion_aleatorio1 and apuntador == posicion_aleatorio2):
                posicion_aleatorio1 = np.random.randint(0, len(self.activos))
                posicion_aleatorio2 = np.random.randint(0, len(self.activos))
            estado.set_estado_salida1(posicion_aleatorio1)
            estado.set_estado_salida2(posicion_aleatorio2)

            apuntador += 1
        apuntador = 0

    def desactivar_estado(self):
        pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
        print(
            f'Estado a desactivar: {letra[self.estados[pos_elegido].posicion]}')
        elegido = self.estados[pos_elegido]
        if(elegido.posicion == self.inicial):
            self.set_inicial()
        self.inactivos.append(elegido.posicion)
        self.estados[pos_elegido].inactivo()
        self.activos.remove(pos_elegido)
        self.set_estados()

    def generar_mef(self):
        for iterador in range(self.cantidad_estados):
            estado_activo = np.random.uniform()
            estado = self.estados[iterador]
            entradas = np.random.randint(0, 2)
            salida1 = np.random.randint(1, 10)
            salida2 = np.random.randint(1, 10)
            estado.set_entradas(entradas)
            estado.set_salida_1(salida1 % 2)
            estado.set_salida_2(salida2 % 2)
            if estado_activo < 0.8:
                estado.activo()
                self.activos.append(iterador)
            else:
                estado.inactivo()
                self.inactivos.append(iterador)
        self.set_inicial()
        self.set_estados()

    def cambiar_simbolos_entrada(self):
        pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
        print(f'Se esta modificando el estado: { letra[pos_elegido]}')
        self.estados[pos_elegido].cambiar_entradas()

    def cambiar_simbolo_salida1(self):
        pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
        print(f'Se esta modificando el estado: { letra[pos_elegido]}')
        self.estados[pos_elegido].cambiar_salida_1()

    def cambiar_simbolo_salida2(self):
        pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
        print(f'Se esta modificando el estado: { letra[pos_elegido]}')
        self.estados[pos_elegido].cambiar_salida_2()

    def activar_estado(self):
        if(len(self.inactivos) == 0):
            return -1
        pos_elegido = self.inactivos[np.random.randint(0, len(self.inactivos))]
        print(f'Se esta modificando el estado: { letra[pos_elegido] }')
        self.inactivos.remove(pos_elegido)
        self.activos.append(pos_elegido)
        self.estados[pos_elegido].activo()
        self.set_estados()

    def aptitud(self, entrada):
        estado_actual = self.estados[self.inicial]
        tamanio = len(entrada)
        contador_exitos = 0
        self.salida = ''
        for iterador in range(tamanio):
            digito = int(entrada[iterador])
            estado_siguiente, salida = estado_actual.consultar(digito)
            if(iterador < tamanio-1):
                if salida == int(entrada[iterador+1]):
                    contador_exitos += 1
            self.salida += str(salida)
            estado_actual = self.estados[estado_siguiente]
        self.actitud = contador_exitos*1.0/(tamanio-1)

    def diagrama(self):
        print('digraph finite_state_machine {')
        print(' rankdir = LR;')
        print(' size= "8,5"')
        for posicion in self.activos:
            print(
                f' node[shape = circle, label = "{letra[self.estados[posicion].posicion]}"] {letra[self.estados[posicion].posicion]}')
        print(f" node[shape=point];qi")
        print(f' qi -> {letra[self.inicial]}')
        for posicion in self.activos:
            print(f' {letra[self.estados[posicion].posicion]} -> {letra[self.estados[posicion].estado_salida_1]}[ label = "{self.estados[posicion].entrada_1}-{self.estados[posicion].salida_1}"];')
            print(f' {letra[self.estados[posicion].posicion]} -> {letra[self.estados[posicion].estado_salida_2]}[ label = "{self.estados[posicion].entrada_2}-{self.estados[posicion].salida_2}"];')
        print("}")

    def mutacion(self):
        estado_elegido = np.random.randint(0, len(self.activos))
        aleatorio = np.random.uniform(0, 1)
        print(f'Aleatorio : {aleatorio} ')
        if aleatorio <= 0.1:
            print('Desactivar un estado ')
            self.desactivar_estado()
        elif aleatorio <= 0.3:
            print('Cambiar estado inicial')
            self.cambiar_inicial()
        elif aleatorio <= 0.5:
            print('Cambiar símbolos de entrada')
            self.cambiar_simbolos_entrada()
        elif aleatorio <= 0.7:
            print('Cambiar salida 1')
            self.cambiar_simbolo_salida1()
        elif aleatorio <= 0.9:
            print('Cambiar salida 2')
            self.cambiar_simbolo_salida2()
        elif aleatorio <= 1.0:
            print('Activar un estado ')
            a = self.activar_estado()
        else:
            print('Error')
