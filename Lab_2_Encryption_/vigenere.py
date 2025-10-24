# vigenere_interactif.py
import unicodedata
import string

ASCII_LETTERS = string.ascii_letters  # a-zA-Z

def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))

def _key_stream(key: str):
    key = strip_accents(key)
    letters = [ch for ch in key if ch in ASCII_LETTERS]
    if not letters:
        raise ValueError("La clé doit contenir au moins une lettre.")
    i = 0
    n = len(letters)
    while True:
        ch = letters[i % n]
        yield (ord(ch.lower()) - ord('a'))
        i += 1

def _shift_char(ch: str, k: int, decrypt: bool) -> str:
    if ch in string.ascii_lowercase:
        base = ord('a')
        offset = -k if decrypt else k
        return chr((ord(ch) - base + offset) % 26 + base)
    if ch in string.ascii_uppercase:
        base = ord('A')
        offset = -k if decrypt else k
        return chr((ord(ch) - base + offset) % 26 + base)
    return ch

def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    ks = _key_stream(key)
    out = []
    for ch in text:
        work_ch = strip_accents(ch)
        if work_ch in ASCII_LETTERS:
            k = next(ks)
            shifted = _shift_char(work_ch, k, decrypt)
            out.append(shifted.upper() if ch.isupper() else shifted.lower())
        else:
            out.append(ch)
    return "".join(out)

# Programme principal
if __name__ == "__main__":
    key = input("Entrez la clé : ")
    choix = input("Voulez-vous (C)hiffrer ou (D)échiffrer ? ").strip().lower()
    texte = input("Entrez le texte : ")

    if choix.startswith("d"):
        resultat = vigenere(texte, key, decrypt=True)
    else:
        resultat = vigenere(texte, key, decrypt=False)

    print("Résultat :", resultat)