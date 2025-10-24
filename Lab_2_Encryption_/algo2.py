def to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def pad_block(block, size=128):
    return block.ljust(size, '0')  # Padding à la fin

def split_blocks(binary_text, block_size=128):
    blocks = [binary_text[i:i+block_size] for i in range(0, len(binary_text), block_size)]
    if len(blocks[-1]) < block_size:
        blocks[-1] = pad_block(blocks[-1], block_size)
    return blocks

def mirror(block):
    return block[::-1]

def shift_left(block, n=5):
    return block[n:] + block[:n]

def xor_blocks(block1, block2):
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(block1, block2))

def generate_subkeys(binary_key, total_keys=10):
    subkeys = []
    for i in range(total_keys):
        shifted = shift_left(binary_key, i % len(binary_key))
        subkeys.append(shifted[:128])
    return subkeys

def algo2_encrypt():
    key = input("Entrez une clé (max 16 caractères): ")[:16]
    plaintext = input("Entrez le texte clair à chiffrer: ")

    binary_key = to_binary(key).ljust(128, '0')[:128]
    binary_text = to_binary(plaintext)

    blocks = split_blocks(binary_text)
    subkeys = generate_subkeys(binary_key)

    encrypted_blocks = []

    for block_index, block in enumerate(blocks):
        print(f"\nBLOC {block_index + 1} CLAIR : {block}")
        for round in range(10):
            mirrored = mirror(block)
            print(f"BLOC {block_index + 1} APRES PERMUTATION MIROIR : {mirrored}")

            shifted = shift_left(mirrored)
            print(f"BLOC {block_index + 1} APRES SHIFT LEFT 5 : {shifted}")

            xor_result = xor_blocks(shifted, subkeys[round])
            print(f"BLOC {block_index + 1} APRES XOR SOUS CLÉ {round + 1} : {xor_result}")

            block = xor_result

        encrypted_blocks.append(block)

    final_cipher = ''.join(encrypted_blocks)
    print(f"\n🔐 MESSAGE CHIFFRÉ FINAL : {final_cipher}")

algo2_encrypt()