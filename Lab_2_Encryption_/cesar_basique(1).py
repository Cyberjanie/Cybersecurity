majuscules = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # pas de W
minuscules = majuscules.lower()

def lettre(pos):
    compteur = 0
    for i in majuscules:
        if(compteur==pos):
            car = i
        compteur = compteur + 1
    return car

def num(caractere):
    if caractere in majuscules:
        alphabet = majuscules
    else:
        alphabet = minuscules
    position = alphabet.find(caractere)
    return position + 1

def chiffrement(message):
    chiffre = " "
    for c in message: # c comme . . .
        x = (num(c) + 3 ) % 26
        chiffre = chiffre + lettre(x)
    return chiffre
