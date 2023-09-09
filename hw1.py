#Решето Эратосфена
def eratosphenGrid():
    N = int(input("Input a number\n"))

    arr = [i for i in range(1,N+1)]

    arr[0] = 0
    print(len(arr))

    for i in range(2, N + 1):
        for j in range(i+1, N + 1):
            if arr[i-1] != 0 and arr[j-1] % arr[i-1] == 0:
                arr[j-1] = 0

    primes = [a for a in arr if a!=0]

    print(primes)

#Числа Фибоначчи
def fibonacci():
    fibNums = []

    i = 0
    while i >=0:

        if i < 2:
            fibNums.append(1)
        else:
            fibNums.append(fibNums[i-1] + fibNums[i-2])
        if fibNums[i] / 10 ** 100 >= 1:
            break
        i = i + 1

    print(fibNums)

    num = int(input("\n\n\n\nВведите порядковый номер:\n"))

    print("искомое число Фибоначчи под порядковым номером ", num, " равно:" , fibNums[num -1])

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


def menu():
    while 1:
        ans = int(input("-------------Домашнее Задание 1-------------\n*введите номер задания:\n\n1-Решето Эратосфена\n2-Вывод чисел Фибоначчи\n3-Шифр Цезаря\n4-Шифр Виженера\n\n*********Для выхода введите 0********\n\n"))
        match ans:
            case 1:
                eratosphenGrid()
            case 2:
                fibonacci()
            case 3:
                plaintext = input("\nВведите строку, которую нужно зашифровать: ")
                shift = int(input("\nВведите величину сдвига: "))
                print(ceasar(plaintext, shift))
            case 4:
                plaintext = input("\nВведите строку, которую нужно зашифровать: ")
                key = input("\nВведите ключ ")
                print(vigenere(plaintext, key))
            case 0:
                break

menu()