import textwrap

# 🔐 S-box 4 bits
S_BOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

# 🔄 Inverse S-box
INV_S_BOX = [0]*16
for i, val in enumerate(S_BOX):
    INV_S_BOX[val] = i

# 🔧 Fonctions utilitaires
def pad_block(block, size=128):
    return block.ljust(size, '0')

def shift_right(block, n=5):
    return block[-n:] + block[:-n]

def inverse_substitute(block):
    substituted = ''
    for i in range(0, len(block), 4):
        nibble = block[i:i+4]
        if len(nibble) < 4:
            nibble = nibble.ljust(4, '0')
        index = int(nibble, 2)
        new_val = format(INV_S_BOX[index], '04b')
        substituted += new_val
    return substituted


def inverse_hybrid_permutation(block):
    # On inverse les moitiés
    mid = len(block) // 2
    swapped = block[mid:] + block[:mid]
    
    # Puis on inverse la rotation
    return swapped[-8:] + swapped[:-8]



def xor(block, key):
    return ''.join('1' if b != k else '0' for b, k in zip(block, key))

def inverse_mix_columns(block):
    unmixed = ''
    for i in range(0, len(block), 16):
        col = block[i:i+16]
        # Rotation circulaire vers la droite des 4 nibbles
        unmixed += col[-4:] + col[:-4]
    return unmixed


def to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if len(b) == 8)

def to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def generate_subkeys(key_bin):
    return [key_bin[i:] + key_bin[:i] for i in range(12)]

# 🔓 Algorithme principal
def algo4_decrypt():
    print("\n🔓 ALGO6 - Déchiffrement 128 bits 🔓")
    key = input("Entrez la clé utilisée (max 16 caractères) : ")[:16]
    cipher_bin = input("Entrez le message chiffré en binaire : ")

    key_bin = pad_block(to_binary(key), 128)
    blocks = textwrap.wrap(cipher_bin, 128)
    subkeys = generate_subkeys(key_bin)

    decrypted_blocks = []

    for block_index, block in enumerate(blocks):
        print(f"\n🔹 Bloc {block_index + 1} chiffré           : {block}")
        for round in reversed(range(12)):
            block = xor(block, subkeys[round])
            print(f"  ➤ Après XOR sous-clé {round+1}     : {block}")

            block = inverse_mix_columns(block)
            print(f"  ➤ Après inverse MixColumns         : {block}")

            block = shift_right(block, 5)
            print(f"  ➤ Après shift right 5              : {block}")

            block = inverse_substitute(block)
            print(f"  ➤ Après inverse S_BOX              : {block}")

            block = inverse_hybrid_permutation(block)
            print(f"  ➤ Après miroir                     : {block}")

        decrypted_blocks.append(block)
        print(f"🔸 Bloc {block_index + 1} déchiffré final : {block}")

    final_binary = ''.join(decrypted_blocks)
    final_plaintext = to_text(final_binary)
    print(f"\n📝 Texte déchiffré final : {final_plaintext}")

# ▶️ Exécution
algo4_decrypt()