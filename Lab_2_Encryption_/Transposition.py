#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

# ---------- Utilitaires ----------

def sanitize(text: str) -> str:
    """Garde uniquement les lettres, en MAJUSCULES (on enlève espaces/ponctuation)."""
    return "".join(ch for ch in text.upper() if ch.isalpha())

def key_ranks(key: str):
    """
    Renvoie (letters, ranks) où ranks sont des numéros 1..c attribués par ordre
    alphabétique, en cas de doublon on numérote de gauche à droite.
    Ex: B I B M A T H -> ranks [2,5,3,6,1,7,4]
    """
    letters = list(key.upper())
    pairs = sorted([(ch, i) for i, ch in enumerate(letters)], key=lambda x: (x[0], x[1]))
    rank_by_pos = [0] * len(letters)
    for rank, (_, i) in enumerate(pairs, start=1):
        rank_by_pos[i] = rank
    return letters, rank_by_pos

def print_table(header_letters, header_ranks, rows, title=None):
    """Affiche le tableau (clé, rangs, puis les lignes du message)."""
    if title:
        print("\n" + title)
    print("CLE : " + " ".join(header_letters))
    print("RANG: " + " ".join(str(r) for r in header_ranks))
    for r in rows:
        print("     " + " ".join(r))

def chunk(s, n=5):
    """Affiche par blocs n (par défaut 5, style classique)."""
    return " ".join([s[i:i+n] for i in range(0, len(s), n)])

# ---------- Chiffrement ----------

def build_encrypt_grid(plain: str, key: str):
    """Construit la grille ligne par ligne (sans bourrage)."""
    letters, ranks = key_ranks(key)
    c = len(letters)
    if c == 0:
        raise ValueError("La clé ne peut pas être vide.")
    rows, row = [], []
    for ch in plain:
        row.append(ch)
        if len(row) == c:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return letters, ranks, rows

def encrypt(plain_text: str, key: str, show_table=True):
    P = sanitize(plain_text)
    letters, ranks, rows = build_encrypt_grid(P, key)

    if show_table:
        print_table(letters, ranks, rows, title="Tableau de CHIFFREMENT")

    # Lire les colonnes dans l'ordre des rangs 1..c
    c = len(letters)
    order = sorted(range(c), key=lambda j: ranks[j])
    ciphertext = []
    for j in order:
        for i in range(len(rows)):
            if j < len(rows[i]):              # colonne présente sur cette ligne ?
                ciphertext.append(rows[i][j]) # prendre la lettre
    C = "".join(ciphertext)
    return C, letters, ranks, rows

# ---------- Déchiffrement (corrigé) ----------

def decrypt(cipher_text: str, key: str, show_table=True):
    C = sanitize(cipher_text)
    letters, ranks = key_ranks(key)
    c = len(letters)
    if c == 0:
        raise ValueError("La clé ne peut pas être vide.")
    n = len(C)

    # n = q*c + r  -> les r PREMIÈRES COLONNES DE GAUCHE ont hauteur q+1, les autres q
    q, r = divmod(n, c)
    heights = [q + (1 if j < r else 0) for j in range(c)]   # <-- CORRECTION ICI

    # Remplir les colonnes dans l'ordre des rangs (1..c), en respectant la hauteur de CHAQUE colonne gauche->droite
    order = sorted(range(c), key=lambda j: ranks[j])
    cols = [[] for _ in range(c)]
    pos = 0
    for j in order:
        h = heights[j]
        cols[j] = list(C[pos:pos+h])
        pos += h

    # Reconstituer le tableau ligne par ligne (de gauche à droite), puis aplatir
    max_h = max(heights) if heights else 0
    rows = []
    for i in range(max_h):
        row = []
        for j in range(c):
            if i < len(cols[j]):
                row.append(cols[j][i])
        if row:
            rows.append(row)

    if show_table:
        print_table(letters, ranks, rows, title="Tableau de DÉCHIFFREMENT")

    P = "".join(ch for r_ in rows for ch in r_)
    return P, letters, ranks, rows

# ---------- Interface CLI ----------

def main():
    print("=== Transposition rectangulaire (clé par défaut: BIBMATH) ===")
    mode = input("Mode (C pour chiffrer / D pour déchiffrer) [C]: ").strip().upper() or "C"
    key = input("Entrez la clé (laisser vide pour 'BIBMATH'): ").strip().upper() or "BIBMATH"
    text = input("Entrez le texte: ").strip()

    if mode == "C":
        C, letters, ranks, rows = encrypt(text, key, show_table=True)
        print("\nTexte chiffré:")
        print(chunk(C, 5))  # Groupes de 5, comme ton exemple
    elif mode == "D":
        P, letters, ranks, rows = decrypt(text, key, show_table=True)
        print("\nTexte déchiffré (sans espaces/punct.):")
        print(chunk(P, 5))
    else:
        print("Mode inconnu. Utilisez C ou D.")

if __name__ == "__main__":
    main()
