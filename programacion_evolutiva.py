from MEF import MEF
import copy
import numpy as np


def generar_automata(cantidad):
    a = MEF(5)
    a.generar_mef()
    return a


def copiar_automata(automata):
    automata1 = copy.deepcopy(automata)
    return automata1

def generar_mutaciones( poblacion ):
    descendientes = []
    for iterador in range(len(poblacion)):
        automata = copiar_automata(poblacion[iterador])
        print(f'Mutación {iterador+1 }')
        print(automata.imprimir())
        automata.mutacion()
        print(f'Nuevo descendiente: {automata.imprimir()}')
        descendientes.append(automata)
        print('\n')
    return descendientes

def imprimir_elementos(poblacion):
    print(len(poblacion))
    for iterador in range(len(poblacion)):
        poblacion[iterador].aptitud('0111001010011100101001110010100111001010')
        print(f'{iterador+1}) {poblacion[iterador].imprimir()} - 0111001010011100101001110010100111001010 - {poblacion[iterador].salida} - {poblacion[iterador].actitud}')

def seleccionar(poblacion):
    aptitudes = []
    seleccionados = []
    for iterador in range(len(poblacion)):
        aptitudes.append( (poblacion[iterador].actitud, iterador))
    aptitudes.sort()
    iterador = len(poblacion)-1
    while( iterador >= len(poblacion)//2 ):
        seleccionados.append(poblacion[aptitudes[iterador][1]])
        iterador+= -1
    return seleccionados

def juntar(poblacion, descendientes):
    for elemento in descendientes:
        poblacion.append(elemento)
    return poblacion

if __name__ == '__main__':

    poblacion = []
    cantidad_individuos = 10
    cantidad_iteraciones = 100
    print('Parámetros:')
    print(f'Cantidad de individuos : {cantidad_individuos}')
    print(f'Cantidad Maxima de Estados: 5')
    print(f'Cantidad de iteraciones: {cantidad_iteraciones}')
    print('Poblacion inicial')

    for iterador in range(cantidad_individuos):
        poblacion.append(generar_automata(5))
        print(f'{iterador+1}) {poblacion[iterador].imprimir()}')

    print('Calcular la aptitud para cada individuo')
    imprimir_elementos(poblacion)

    for iteracion in range(200):
        print(f' **** Iteracion {iteracion+1} **** ') 
        print(' Proceso de mutación ')
        descendientes  = generar_mutaciones(poblacion)
        print('\nDescendientes')
        imprimir_elementos(descendientes)
        print('\nMejores Ascendentes')
        poblacion = seleccionar(poblacion)
        imprimir_elementos(poblacion)
        print('\nMejores Descendientes')
        descendientes = seleccionar(descendientes)
        imprimir_elementos(descendientes)
        print('\nNueva Población')
        poblacion = juntar(poblacion,descendientes)
        imprimir_elementos(poblacion)
        
    poblacion[0].diagrama()