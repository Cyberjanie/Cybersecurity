import textwrap

# 🔐 S-box 4 bits
S_BOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

# 🔧 Fonctions utilitaires
def to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def pad_block(block, size=128):
    return block.ljust(size, '0')

def mirror(block):
    return block[::-1]

def substitute(block):
    substituted = ''
    for i in range(0, len(block), 4):
        nibble = block[i:i+4]
        index = int(nibble, 2)
        new_val = format(S_BOX[index], '04b')
        substituted += new_val
    return substituted

def shift_left(block, n=5):
    return block[n:] + block[:n]

def mix_columns(block):
    mixed = ''
    for i in range(0, len(block), 16):
        col = block[i:i+16]
        # Rotation circulaire vers la gauche des 4 nibbles
        mixed += col[4:] + col[:4]
    return mixed


def xor(block, key):
    return ''.join('1' if b != k else '0' for b, k in zip(block, key))

def generate_subkeys(key_bin):
    return [shift_left(key_bin, i)[:128] for i in range(10)]

# 🔐 Algorithme principal
def algo3_cipher():
    print("\n🔐 ALGO5 - Chiffrement à clé 128 bits 🔐")
    key = input("Entrez une clé (max 16 caractères) : ")[:16]
    plaintext = input("Entrez le texte clair à chiffrer : ")

    key_bin = pad_block(to_binary(key), 128)
    text_bin = to_binary(plaintext)

    blocks = textwrap.wrap(text_bin, 128)
    blocks = [pad_block(b, 128) for b in blocks]

    subkeys = generate_subkeys(key_bin)
    encrypted_blocks = []

    for block_index, block in enumerate(blocks):
        print(f"\n🔹 Bloc {block_index + 1} clair              : {block}")
        for round in range(10):
            block = mirror(block)
            print(f"  ➤ Après miroir             : {block}")

            block = substitute(block)
            print(f"  ➤ Après substitution S_BOX : {block}")

            block = shift_left(block, 5)
            print(f"  ➤ Après shift left 5       : {block}")

            block = mix_columns(block)
            print(f"  ➤ Après MixColumns         : {block}")

            block = xor(block, subkeys[round])
            print(f"  ➤ Après XOR sous-clé {round+1}     : {block}")

        encrypted_blocks.append(block)

    final_cipher = ''.join(encrypted_blocks)
    print(f"\n🔐 Message chiffré final : {final_cipher}")

# ▶️ Exécution
algo3_cipher()