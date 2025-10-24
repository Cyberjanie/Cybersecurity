# Transposition rectangulaire avec colonnes completes

from random import choice
import random
import math


def msg_clair(msg):
    # supprime les caracteres speciaux
    msg = msg.upper()
    msg = msg.replace("À", "A")
    msg = msg.replace("Â", "A")
    msg = msg.replace("Ä", "A")
    msg = msg.replace("Ç", "C")
    msg = msg.replace("É", "E")
    msg = msg.replace("È", "E")
    msg = msg.replace("Ê", "E")
    msg = msg.replace("Ë", "E")
    msg = msg.replace("Î", "I")
    msg = msg.replace("Ï", "I")
    msg = msg.replace("Ô", "O")
    msg = msg.replace("Ö", "O")
    msg = msg.replace("Ù", "U")
    msg = msg.replace("Û", "U")
    msg = msg.replace("Ü", "U")
    msg = msg.replace("Ÿ", "Y")
    for ch in msg :
        if ord(ch)<65 or ord(ch)>90:
            msg = msg.replace(ch,"")
    return msg


def clef_numerique_dechiffrement(clef):
    # donne la permuation des colonnes d'apres une clef textuelle
    clef = msg_clair(clef)
    lst_clef = list(clef)
    clef_ordre = sorted(list(clef))             # sorted met la liste dans l'ordre alphabétique
    permutation = []
    col = len(clef)
    for x in range(col):                        # remettre les listes dans l'ordre alphabetique de la clef
        indice = clef_ordre.index(lst_clef[x])  # index = donne la position de la lettre recherchee
        clef_ordre[indice] = "0"
        lst_clef[x] = "0"
        permutation.append(indice)
    return permutation


def dechiffrer_message(msg_code,clef) :

    msg = ""
    long_msg = len(msg_code)
    lst_msg_code = list(msg_code)
    col = len(clef)
    ligne = int(math.ceil(long_msg / col))

    liste = []
    lst_msg_decode = []

    for x in range(col): # créer plusieurs listes avec le message codé en fonction du nombre de ligne du message
        j = ligne*x
        liste_1 = []
        while j<(ligne*(x+1)) and (ligne*(x+1))<=long_msg:
            liste_1.append(lst_msg_code[j])
            j+=1
        liste.append(liste_1)

    ordre = clef_numerique_dechiffrement(clef)
    for x in range(col):
        lst_msg_decode.append(liste[ordre[x]])

    y = 0
    while y < ligne :
        for x in range(col) : #transformer les listes en chaines de caractères
            msg += ' '.join(lst_msg_decode[x][y])
        y+=1

    msg_decode = msg.replace("_","")

    return msg_decode


def clef_numerique_chiffrement(clef):
    # donne la permuation des colonnes d'apres une clef textuelle
    clef = msg_clair(clef)
    lst_clef = list(clef)
    clef_ordre = sorted(list(clef)) # sorted met la liste dans l'ordre alphabétique
    permutation = []
    col = len(clef)
    for x in range(col):                            # remettre les listes dans l'ordre alphabétique de la clef
        indice = clef.index(clef_ordre[x])          # index = donne la position de la lettre recherchée
        clef = clef.replace(clef_ordre[x], "0",1)   # on remplèce les lettres par 0 pour pourvoir utiliser une clef qui contient plusieurs fois la même lettre
        clef_ordre[x] = "0"
        permutation.append(indice)
    return permutation


def chiffrer_message(msg, clef):

    msg_code = ""
    msg = msg_clair(msg)
    long_msg = len(msg)
    lst_msg = list(msg)         # message sous forme de liste de lettres majuscules sans accents

    col = len(clef)             # nombre de colonnes du tableau
    lig = long_msg // col + 1   # nombre de lignes du tableau

    liste = []
    lst_msg_code = []
    liste_lettre = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    espaces_a_combler = int((lig * col) - long_msg)     # ajouter des lettres pour combler les trous
    for x in range(espaces_a_combler):
        lst_msg.extend(choice(liste_lettre))

    for x in range(col): # creer une liste de colonnes avec le message en fonction de la longueur de la clef
        j = x
        colonne = []
        while j<(long_msg + espaces_a_combler):
            colonne.append(lst_msg[j])
            j += col
        liste.append(colonne)

    ordre = clef_numerique_chiffrement(clef)
    for x in range(col):
        lst_msg_code.append(liste[ordre[x]])

    for x in range(col) : # transformer les listes en chaines de caracteres
        y = 0
        while y < lig :
            msg_code += ' '.join(lst_msg_code[x][y])
            y+=1

    return msg_code

clair = "TRANSPOSITIONSRECTANGULAIRES"
clef = "pouce"
print("cryptogramme")
txt_chiffre = chiffrer_message(clair, clef)
print(txt_chiffre)
print("clair")
txt_dechiffre = dechiffrer_message(txt_chiffre,clef)
print(txt_dechiffre)