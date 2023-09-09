#Решето Эратосфена
def eratosphenGrid():
    N = int(input("Input a number\n"))

    arr = [i for i in range(1,N+1)]

    arr[0] = 0
    print(len(arr))

    for i in range(2, N + 1):
        for j in range(i+1, N + 1):
            print(arr , "    " , j-i + (i - 2) * N ,  " -я итерация")
            if arr[i-1] != 0 and arr[j-1] % arr[i-1] == 0:
                arr[j-1] = 0

    primes = [a for a in arr if a!=0]

    print(primes)

#Числа Фибоначчи
def fibonacci():
    fibNums = []

    m = 0
    k=0
    while k <= 100:
        k = k+1
        m = 10 ** k

    print(m)
    i = 0
    while i >=0:

        if i < 2:
            fibNums.append(1)
        else:
            fibNums.append(fibNums[i-1] + fibNums[i-2])
        if fibNums[i] / m >= 1:
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
        if ord(plaintext[i].upper()) + shift <= 95:
            cipher.append(chr(ord(plaintext[i]) + shift))
        else:
             cipher.append(chr(ord(plaintext[i]) - 26 + shift))
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
            cipher.append(chr(ord(plaintext[i]) + ord(key[j]) - ord("A")))
        else:
            cipher.append(chr(ord(plaintext[i]) + ord(key[j]) - ord("A")))
        if ord(cipher[i]) > 95: #проверка на вхождение в алфавит
            cipher[i] = chr(ord(cipher[i]) - 26)
        i = i + 1
        j = j + 1
    return cipher



 
