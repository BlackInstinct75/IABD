
#2. Comparar dos números
def ejec_2():
    num1 = int(input("Dame el primer número: "))
    num2 = int(input("Dame el segundo número: "))
    if num1 > num2:
        print(f"El número mayor es el {num1}")
    elif num2 == num1:
        print(f"Ambos números son iguales")
    else:
        print(f"El número mayor es el {num2}")

#3. Determinar si un número es par o impar
def ejec_3():
    numero = int(input("Dame un número: "))

    if numero % 2 == 0:
        print("El número es par")
    else:
        print("El número es impar")

#4.Clasificación de números según un rango
def ejec_4():
    numero = int(input("Dame un número: "))
    if numero in range(5):
        print("El alumno esta suspendo")
    elif numero in range(5,6):
        print("El alumno tiene un suficiente")
    elif numero in range(6,7):
        print("El alumno tiene un bien")
    elif numero in range(7,8):
        print("El alumno tiene un notable")
    elif numero in range(8,11):
            print("El alumno tiene un sobresaliente")
    else:
        print("El valor no es correcto")
#5.Imprime numero en la pantalla hasta que de cero
def ejec_5():
    res = []
    while True:
        numero = int(input("Dime un número: "))
        res.append(numero)
        print(f"Has introducido el {numero}, tienes una media de {sum(res)/len(res)}, y en total hace {sum(res)}")
        if numero == 0:
            break

def ejec_6():
    numero = int(input("Dime un número para calcular el factorial: "))
    res = numero
    for num in range(1,numero):
        res *= num
    print(f"El factorial de {numero} es {res}")

#13. Comprobar si una cadena tiene una longitud mayor a 5
def ejec_13():
    cadena = input("Dame un cadena: ")
    if 5 < len(cadena):
        print("La cadena es mayor a 5 caracteres")
    else:
        print("La cadena no supera la longitud de 5 caracteres")
#14. Escribir por pantalla cada carácter de una cadena introducida por teclado. 
def ejec_14():
    cadena = input("Dame un cadena: ")
    for letra in range(len(cadena)):
        print(cadena[letra])

#15.Realizar un programa que comprueba si una cadena leída por teclado comienza por otra  subcadena introducida por teclado. 
def ejec_15():
    cadena = input("Dame una cadena: ")
    subcadena = input("Dame una subcadena: ")
    if subcadena == cadena[:len(subcadena)]:
        print("La cadena empieza por la subcadena")
    else:
        print("La cadena no empieza por la subcadena")

#16. Pide una cadena y un carácter por teclado (valida que sea un carácter) y muestra cuantas veces aparece el carácter en la cadena. 
def ejec_16():
    res = 0
    cadena = input("Dame una cadena: ")
    car = input("Dame un caracter: ")
    if car.isnumeric():
        print("Esto no es un caracter")
    else:
        for c in cadena:
            if c.upper() == car.upper():
                res += 1
        print(f"El caracter {car} aparece {res} en la cadena: '{cadena}'")
#17. Suponiendo que hemos introducido una cadena por teclado que representa una frase (palabras separadas por espacios), realiza un programa que cuente cuántas palabras tiene. 
def ejec_17():
    res = 1
    cadena = input("Dame una cadena: ")
    for car in cadena:
        if car == " ":
            res += 1
    print(f"La cadena '{cadena}' contiene {res} palabras")

#18. Si tenemos una cadena con un nombre y apellidos, realizar un programa que muestre las iniciales en mayúsculas. 
def ejec_18():
    cadena = input("Dame una cadena: ")
    for car in range(len(cadena)):
        if cadena[car-1] == " " or car == 0:
           print(cadena[car].upper(),end="")
    print("\n",end="")
#19. Realizar un programa que dada una cadena de caracteres por caracteres, genere otra cadena resultado de invertir la primera. 
def ejec_19():
    cadena = input("Dame una cadena: ")
    print(cadena[::-1])
#20. Pide una cadena y dos caracteres por teclado (valida que sea un carácter), sustituye la aparición del primer carácter en la cadena por el segundo carácter. 
def ejec_20():
    res = ""
    cadena = input("Dame una cadena: ")
    car1 = input("Dame un caracter: ")
    car2 = input("Dame un caracter para sustituir el anterior: ")
    if car1.isnumeric() or car2.isnumeric():
        print("Esto no es un caracter")
    else:
        for c in cadena:
            if c.upper() == car1.upper():
                res += car2
            else:
                res += c
        print(f"{res}")

#21. Realizar un programa que lea una cadena por teclado y convierta las mayúsculas a minúsculas y viceversa. 
def ejec_21():
    cadena = input("Dame una cadena: ")
    print(cadena.swapcase())

#22. Realizar un programa que compruebe si una cadena contiene una subcadena. Las dos cadenas se introducen por teclado. 
def ejec_22():
    cadena = input("Dame una cadena: ")
    subcadena = input("Dame una subcadena: ")
    if subcadena in cadena:
        print("La subcadena esta en la cadena")
    else:
        print("La subcadena no pertenece a la cadena")

#23. Introducir una cadena de caracteres e indicar si es un palíndromo. Una palabra palíndroma es aquella que se lee igual adelante que atrás.
def ejec_23():
    cadena = input("Dame una palabra: ")
    if cadena == cadena[::-1]:
        print("Es palindromo")
    else:
        print("No es palindromo")

#24. Validar una contraseña
def ejec_24():
    num = 0
    up = 0 
    contrasena = input("Dame una contraseña: ") 
    for car in contrasena:
        if car.isnumeric():
            num += 1
        elif car.isupper():
            up += 1
    if ((len(contrasena) < 8) or (num < 1 or up < 1)):
        print("No es valida la contraseña")
    else:
        print("Contraseña valida")