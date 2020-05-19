import numpy as np

#usado para representar a los estados respecto a las letras que corresponden
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

    def cambiar_simbolo_entrada(self):
        self.entrada_1, self.entrada_2 = self.entrada_2, self.entrada_1

    def mostrar(self):
        string = f'{self.estado} {self.entrada_1} {self.entrada_2} {self.salida_1} {self.salida_2} {letra[self.estado_salida_1]} {letra[self.estado_salida_2]}'
        return string

    def consultar(self , valor):
        if( valor == self.entrada_1 ):
            return [self.estado_salida_1,self.salida_1]
        else:
            return [self.estado_salida_2,self.salida_2]


class MEF():
    activos = []
    inactivos = []
    inicial = -1

    def __init__(self, cantidad_estados):
        self.estados = []
        self.cantidad_estados = cantidad_estados
        for iterador in range(cantidad_estados):
            nuevo_estado = Estado(iterador)
            self.estados.append(nuevo_estado)
            self.matriz_transicion = np.zeros(
                [cantidad_estados, cantidad_estados])

    def imprimir(self):
        cadena = ''
        for iterador in range(self.cantidad_estados):
            cadena += f'{self.estados[iterador].mostrar()} '
        return cadena

    def set_inicial(self):
        pos_elegido = self.activos[np.random.randint(0, len(self.activos))]
        elegido = self.estados[pos_elegido]
        while(elegido.posicion == self.inicial):
            pos_elegido = self.activos[np.random.randint(
                0, self.cantidad_estados)][0]
            elegido = self.estados[pos_elegido]
        self.inicial = elegido.posicion
        elegido.inicial()

    def set_estados(self):
        np.random.seed(0)
        apuntador = 0
        for estado in self.estados:
            posicion_aleatorio1 = np.random.randint(0, len(self.activos))
            posicion_aleatorio2 = np.random.randint(0, len(self.activos))
            while(apuntador == posicion_aleatorio1 and apuntador == posicion_aleatorio2):
                posicion_aleatorio1 = np.random.randint(0, len(self.activos))
                posicion_aleatorio2 = np.random.randint(0, len(self.activos))
            estado.set_estado_salida1(posicion_aleatorio1)
            estado.set_estado_salida2(posicion_aleatorio2)
            self.matriz_transicion[apuntador][posicion_aleatorio1] += 1
            self.matriz_transicion[apuntador][posicion_aleatorio2] += 1
            apuntador += 1

    def generar_mef(self):
        for iterador in range(self.cantidad_estados):
            estado_activo = np.random.uniform()
            nodo = self.estados[iterador]
            entradas = np.random.randint(0, 2)
            salida1 = np.random.randint(1, 10)
            salida2 = np.random.randint(1, 10)
            nodo.set_entradas(entradas)
            nodo.set_salida_1(salida1 % 2)
            nodo.set_salida_2(salida2 % 2)
            if estado_activo < 0.8:
                nodo.activo()
                self.activos.append(iterador) 
            else:
                nodo.inactivo()
                self.inactivos.append(iterador) 
        self.set_inicial()
        self.set_estados()

    def aptitud(self, entrada):
        estado_actual = self.estados[self.inicial]
        tamanio = len(entrada)
        contador_exitos = 0 
        self.salida = []
        for iterador in range(tamanio):
            digito = int(entrada[iterador])
            estado_siguiente , salida =  estado_actual.consultar(digito)
            if( iterador < tamanio-1):
                if salida == int(entrada[iterador+1]):
                    print(f'posicion: {iterador}')
                    contador_exitos += 1
            self.salida.append(salida)
            estado_actual = self.estados[estado_siguiente]
            print(letra[estado_siguiente])
        self.actitud = contador_exitos*1.0/(tamanio-1)
        print(f'actitud: {self.actitud}')
        print(f'entrada: {entrada}')
        print(f'salida:  {self.salida}')
           


def representar(cadena):
    estados = 4
    print('digraph finite_state_machine')
    print(' rankdir = LR;')
    print(' size= "8,5"')
    estado = 0
    for iterador in range(estados):
        estado_l = cadena[estado:(estado+7)]
        if(estado_l[0] == '0'):
            estado = estado+7
            continue
        estado = estado+7
        pos1[estado_l][0]
        print(estado_l)
        print('activo')


if __name__ == '__main__':
    franco = MEF(5)
    franco.generar_mef()
    print(franco.imprimir())
    franco.aptitud('0001101')