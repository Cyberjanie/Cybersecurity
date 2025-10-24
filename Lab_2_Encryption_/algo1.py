def to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def pad_block(block, size=128):
    return block.ljust(size, '0')  # Padding à la fin

def mirror(block):
    return block[::-1]

def shift_left(block, n=5):
    return block[n:] + block[:n]

def xor_blocks(block1, block2):
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(block1, block2))

def split_blocks(binary_text, block_size=128):
    blocks = [binary_text[i:i+block_size] for i in range(0, len(binary_text), block_size)]
    if len(blocks[-1]) < block_size:
        blocks[-1] = pad_block(blocks[-1], block_size)
    return blocks

def algo1_encrypt():
    key_input = input("Entrez une clé (max 16 caractères) : ")[:16]
    plain_text = input("Entrez le texte clair à chiffrer : ")

    key_bin = to_binary(key_input).ljust(128, '0')[:128]
    text_bin = to_binary(plain_text)
    blocks = split_blocks(text_bin)

    encrypted_blocks = []

    for i, block in enumerate(blocks):
        print(f"\n🔹 Bloc {i+1} clair       : {block}")
        mirrored = mirror(block)
        print(f"🔸 Bloc {i+1} miroir      : {mirrored}")
        shifted = shift_left(mirrored)
        print(f"🔸 Bloc {i+1} shift left 5: {shifted}")
        xored = xor_blocks(shifted, key_bin)
        print(f"🔸 Bloc {i+1} XOR clé     : {xored}")
        encrypted_blocks.append(xored)

    final_cipher = ''.join(encrypted_blocks)
    print(f"\n🔐 Message chiffré final : {final_cipher}")

algo1_encrypt()