import math

# ---- Fonction de chiffrement/déchiffrement ----
def cesar(text, key, mode="chiffrer"):
    result = ""
    for char in text:
        if char.isalpha():  # On chiffre seulement les lettres
            base = ord('A') if char.isupper() else ord('a')
            if mode == "chiffrer":
                result += chr((ord(char) - base + key) % 26 + base)
            else:  # déchiffrer
                result += chr((ord(char) - base - key) % 26 + base)
        else:
            # On ne modifie pas les caractères non alphabétiques
            result += char
    return result

# ---- Programme principal ----
if __name__ == "__main__":
    print("=== Chiffrement de César ===")
    texte = input("Entrez votre texte : ")
    clef = int(input("Entrez la clé (décalage entre 1 et 25) : "))
    choix = input("Voulez-vous chiffrer ou déchiffrer ? (c/d) : ")

    if choix.lower() == "c":
        resultat = cesar(texte, clef, mode="chiffrer")
        print("Texte chiffré :", resultat)
    elif choix.lower() == "d":
        resultat = cesar(texte, clef, mode="dechiffrer")
        print("Texte déchiffré :", resultat)
    else:
        print("Choix invalide !")





