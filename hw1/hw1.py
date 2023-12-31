import random

#Решето Эратосфена
def eratosphenGrid(N:int):

    arr = [i for i in range(1,N+1)]

    arr[0] = 0

    for i in range(2, N + 1):
        for j in range(i+1, N + 1):
            if arr[i-1] != 0 and arr[j-1] % arr[i-1] == 0:
                arr[j-1] = 0

    primes = [a for a in arr if a!=0]

    #подспорье для РСА шифрования
    return(primes)

#Числа Фибоначчи

def fibonacci(fib1, fib2, N, i, seeked):
    if(i == 1):
        print(fib1, "  ")
        print(fib2, "  ")
    i = i + 1
    fib3 = fib1 + fib2
    print(fib3, "  ")
    if N == i:
        seeked = fib3
    elif fib3 / (10**100) >= 1 and seeked != 140502:
        print("Ваше искомое число Фибоначчи = ", seeked)
        return
    elif fib3 / (10**100) >= 1 and seeked == 140502:
        print(N, " Не является корректным порядковым номером. Пожалуйста, повторите ввод\n")
        return
    fibonacci(fib2, fib3, N, i,seeked)
    
#Шифр Цезаря
def ceasar(plaintext: str, shift: int):
    cipher = []

    i = 0
    while i < len(plaintext):
        if ord(plaintext[i].upper()) + shift <= 90:
            cipher.append(chr(ord(plaintext[i]) + shift).upper())
        else:
             cipher.append(chr(ord(plaintext[i]) - 26 + shift).upper())
        i = i + 1
    return str(cipher)

#Шифр Виженера
def vigenere(plaintext: str, key: str):
    cipher = []
    j = 0
    i = 0

    while i < len(plaintext):
        if i % len(key) == 0:
            j = 0
            cipher.append(chr(ord(plaintext[i]) + ord(key[j]) - ord("A")).upper())
        else:
            cipher.append(chr(ord(plaintext[i]) + ord(key[j]) - ord("A")).upper())
        if ord(cipher[i]) > 90: #проверка на вхождение в алфавит
            cipher[i] = chr(ord(cipher[i]) - 26)
        i = i + 1
        j = j + 1
    return cipher

def dsearch(eulerVal, e): # алгоритм Евклида
    k = 1
    d = 1.1
    while not (int(d) == d):
        d = (k * eulerVal + 1)/e
        k = k + 1
    return int(d)


#Генерация ключей
def keyGen(firstPar: int, secondPar: int):
    n = firstPar * secondPar
    eulerVal = (firstPar - 1) * (secondPar - 1)
    while 1:
        randIndex = random.randint(1, len(eratosphenGrid(eulerVal)) - 2)
        e = eratosphenGrid(eulerVal)[randIndex]
        if(eulerVal % e == 0 and e != 1): #e и eulerval взаимнопростые
            continue
        else:
            break

    d = dsearch(eulerVal, e)
    pubKey = [e, n]
    privKey = [d, n]
    return [pubKey, privKey]

#Реализация РСА шифрования
def rsa(pubKey, plaintext: str):
    cipher = []
    i = 0
    while i < len(plaintext): #шифрование
        cipher.append(ord(plaintext[i])**pubKey[0] % pubKey[1])
        i = i + 1
    return cipher


#Реализация дешифрования РСА
def decryptRsa(privkey, cipher):
    plaintext = []
    i = 0
    while i < len(cipher): #дешифрование
        plaintext.append(chr(cipher[i]**privkey[0] % privkey[1]))
        i = i + 1
    return plaintext


def menu():
    while 1:
        ans = int(input("-------------Домашнее Задание 1-------------\n*введите номер задания:\n\n1-Решето Эратосфена\n2-Вывод чисел Фибоначчи\n3-Шифр Цезаря\n4-Шифр Виженера\n5-RSA-шифрование\n6-Дешифрование РСА\n\n*********Для выхода введите 0********\n\n"))
        match ans:
            case 1:
                N = int(input("Input a number\n"))
                print(eratosphenGrid(N))
            case 2:
                N = int(input("Введите порядковый номер числа Фибоначчи, которое хотели бы найти: "))
                fibonacci(1,1,N,1,140502)
            case 3:
                plaintext = input("\nВведите строку, которую нужно зашифровать: ")
                shift = int(input("\nВведите величину сдвига: "))
                print(ceasar(plaintext, shift))
            case 4:
                plaintext = input("\nВведите строку, которую нужно зашифровать: ")
                key = input("\nВведите ключ ")
                print(vigenere(plaintext, key))
            case 5:
                firstPar = int(input("Введите первый параметр( простое число/ желательно большое для лучшей защиты/ для выбора можете использовать функцию (1) - Решето Эратосфена):\n"))
                secondPar = int(input("Введите второй параметр( простое число/ желательно большое для лучшей защиты/ для выбра можете использовать функцию (1) - Решето Эратосфена):\n"))
                keys = keyGen(firstPar, secondPar)
                print("Ваши ключи публичный и приватный соответственно: ",keys[0] ,keys[1] )
                plaintext = input("Введите сообщение, которое нужно зашифровать:\n")
                cipher = rsa(keys[0], plaintext)
                print("_______________Зашифрованное сообщение:    ", cipher, "     _________________________")
            case 6:
                d = int(input("Введите первое значение приватного ключа: "))
                n = int(input("Введите второе значение приватного ключа: "))
                cipher = []
                i = 0

                print("Введите зашифрованное сообщение: \n*вводите по одному значению / после ввода каждого значения нажимайте ENTER / для завершения ввода сообщения введите 0")
                while 1:
                    i = i+1
                    print("Введите ", i ,"-е значение:     ")
                    a = int(input())
                    if a == 0:
                        break
                    else:
                        cipher.append(a)

                plaintext = decryptRsa([d,n], cipher)
                print("_______________Расшифрованное сообщение:   ", plaintext, "________________________")
            case 0:
                break
if __name__ == "__main__":
    menu()