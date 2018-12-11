from random import *

#check whether n is prime
def miller_rabin_test(n, time = 8):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1; s //= 2
        
    #trial test
    for _ in range(time):
        a = randrange(2, n - 1)
        x = mod_acc(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = mod_acc(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def prime_number_generator(n):
    p = 0
    while not miller_rabin_test(p):
        p = randint(0, 2 ** n - 1) + (1 << n)
    return p

#generator a coprime number with r
def coprime():
    e = prime_number_generator(16)
    return e

def inverse_element(e, r):
    x, y = gcd(e, r)
    return x % r

def gcd(a, b):
    if a == 0:
        return (0, 1)
    else:
        y, x = gcd(b % a, a)
        return (x - (b // a) * y, y)

def init(p, q):
    global N, e, d
    #p, q = int(p), int(q)
    N = p * q
    r = (p - 1) * (q - 1)
    e = coprime()
    d = inverse_element(e, r)
    print("----------------------------------------------")
    print("Prime Number: \np = %d,\nq = %d" %(p, q))
    print("Public Key (N, e) = (%d, %d)" %(N, e))
    print("Private Key (N, d) = (%d, %d)" %(N, d))

#a ^ b mod c
def mod_acc(a, b, c):
    s = 1
    while True:        
        t = b        
        if b % 2:
            s = s * a % c
        a = a * a % c
        b //= 2
        if t < 1:
            return s

#chinese remainder theorem
def crt(a, b, c, p, q):
    rp = a % p
    rq = a % q
    
    dp = b % (p - 1)
    dq = b % (q - 1)
    
    yp = mod_acc(rp, dp, p)
    yq = mod_acc(rq, dq, q)
    
    cp = inverse_element(q, p)
    cq = inverse_element(p, q)
    
    return ((q * cp * yp) + (p * cq * yq)) % N

#encryption
def encryption():
    print("----------------------------------------------")
    plaintext = input("Input the plaintext\n")
    ciphertext = ""

    for i in plaintext:
        ciphertext =  ciphertext + str(mod_acc(ord(i), e, N)) + ' '
    print("Plaintext is: %s" %(plaintext))
    print("Ciphertext is: %s" %(ciphertext))
    
    print("----------------------------------------------")
    selection = input('Do you want to decrypt the ciphertext? [y/n]\n')
    if selection == 'y':
        decryption()        

#decryption
def decryption():
    print("----------------------------------------------")
    ciphertext = input("Input the ciphertext\n").split()
    plaintext = ""

    for i in ciphertext:
        plaintext = plaintext + str(chr(int(crt(int(i), d, N, p, q))))
    print("Ciphertext is: %s" %("".join(ciphertext)))
    print("Plaintext is: %s" %(plaintext))

def start():
    while 1:
        print("----------------------------------------------")
        selection = input('e) Encryption\n' + 
                          'd) Decryption\n' + 
                          'n) Use Another Prime Number\n')
        if selection == 'e':
            encryption()
        elif selection == 'd':
            decryption()
        else:
            return

def main():
    global p, q
    while 1:
        print("----------------------------------------------")
        selection = input('i) Input Prime Number\n' + 
                          'g) Generate Prime Number\n' +
                          'q) Quit\n')
        if selection == 'i':
            p, q = input().split()
            p, q = int(p), int(q)
            init(p, q)
        elif selection == 'g':
            p = prime_number_generator(512)
            q = prime_number_generator(512)
            init(p, q)
        else:
            return

        start()

p = q = N = e = d = 0
main()

