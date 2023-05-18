def cargar():
    lista=[]
    for x in range(5):
        num=int(input("Ingrese un valor:"))
        lista.append(num)
    return lista


def imprimir(lista):
    print("Lista completa")
    for elemento in lista:
        print(elemento)


def mayor(lista):
    may=lista[0]
    for elemento in lista:
        if elemento>may:
            may=elemento
    print("El elemento mayor de la lista es",may)            
        

def sumar_elementos(lista):
    suma=0
    for elemento in lista:
        suma=suma+elemento
    print("La suma de todos sus elementos es",suma)

def recorrer(lista):
    for x in range(len(lista)):   
         print('uno a uno', lista[x])

# bloque principal

lista=cargar()
imprimir(lista)
mayor(lista)
sumar_elementos(lista)
recorrer(lista)
