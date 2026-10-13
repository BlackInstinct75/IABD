def num_mayor(num1,num2):
    if num1 > num2:
        return print(f"El numero mayor es: {num1}")
    return print(f"El numero mayor es: {num2}")
num_mayor(2,3)

#Facil de mantener
def sum_pos_pro(lista):
    res = []
    for numero in lista:
        if numero > 0:
            res.append(numero)
    return print(f"Suma de positivos: {sum(res)}, Promedio: {sum(res)/len(res)}")
#Más eficiente
def sum_pos_pro_ef(lista):
    return print(f"Suma de positivos: {sum([numero for numero in lista if numero > 0])}, Promedio: {sum([numero for numero in lista if numero > 0])/len([numero for numero in lista if numero > 0])}")

def palindromo(cadena):
    if cadena == cadena[::-1]:
        print("La cadena es palíndromo")
    else:
        print("La cadena no es palíndromo")

palindromo("radar")

def fibonacci(longitud):
    res = [0,1]
    while longitud > len(res):
        res.append(res[-1]+res[-2])
    print(res[:longitud])

fibonacci(2)

def sub_array(lista,tamaño):
    res = []
    valor = 0
    for posicion,num in enumerate(lista[:-(tamaño-1)]):
        if sum(lista[posicion:posicion+tamaño]) > valor:
            res = [lista[posicion:posicion+tamaño]]
            valor = sum(lista[posicion:posicion+tamaño])
    print(f"La suma máxima: {valor} (subarray: {res})")

sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4],4)

def sum_matriz(matriz1,matriz2):
    res = matriz1
    for fila in range(len(matriz2)):
        for columna in range(len(matriz2[fila])):
            res[fila][columna] += matriz2[fila][columna]
    return print(res)
sum_matriz([[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[4,5,6],[7,8,9]])

def longitud_sub(cadena1,cadena2):
    res = ""
    for x in range(len(cadena1)):
        con = ""
        for y in range(len(cadena2)):
            if cadena1[x+len(con)] == cadena2[y] and (cadena1[x-1+len(con)] == cadena2[y-1] or cadena1[x+len(con)+1] == cadena2[y+1]):
                con += cadena2[y]
        if len(con) > len(res):
            res = con
    return print(f'Longitud LCS: {len(res)} cadena "{res}"')
longitud_sub("no mover","deposito moviles")
    

