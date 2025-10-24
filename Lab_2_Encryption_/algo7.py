import textwrap


test_pairs = {
  "A?bcdefghijklmn": "A!bcdefghijklmn",
  "ab?cdefghijklmn": "ab!cdefghijklmn",
  "abc?defghijklmn": "abc!defghijklmn",
  "abcd?efghijklmn": "abcd!efghijklmn",
  "abcde?fghijklmn": "abcde!fghijklmn",
  "abcdef?ghijklmn": "abcdef!ghijklmn",
  "abcdefg?hijklmn": "abcdefg!hijklmn",
  "abcdefgh?ijklmn": "abcdefgh!ijklmn",
  "abcdefghi?jklmn": "abcdefghi!jklmn",
  "abcdefghij?klmn": "abcdefghij!klmn",
  "abcdefghijk?lmn": "abcdefghijk!lmn",
  "abcdefghijkl?mn": "abcdefghijkl!mn",
  "abcdefghijklm?n": "abcdefghijklm!n",
  "abcdefghijklmn?": "abcdefghijklmn!",
  "1?234567890abcde": "1!234567890abcde",
  "12?34567890abcde": "12!34567890abcde",
  "123?4567890abcde": "123!4567890abcde",
  "1234?567890abcde": "1234!567890abcde",
  "12345?67890abcde": "12345!67890abcde",
  "123456?7890abcde": "123456!7890abcde",
  "1234567?890abcde": "1234567!890abcde",
  "12345678?90abcde": "12345678!90abcde",
  "123456789?0abcde": "123456789!0abcde",
  "1234567890?abcde": "1234567890!abcde",
  "12345678901?bcde": "12345678901!bcde",
  "123456789012?cde": "123456789012!cde",
  "1234567890123?de": "1234567890123!de",
  "12345678901234?e": "12345678901234!e",
  "123456789012345?": "123456789012345!",
  "z?yxwvutsrqponml": "z!yxwvutsrqponml",
  "zy?xwvutsrqponml": "zy!xwvutsrqponml",
  "zyx?wvutsrqponml": "zyx!wvutsrqponml",
  "zyxw?vutsrqponml": "zyxw!vutsrqponml",
  "zyxwv?utsrqponml": "zyxwv!utsrqponml",
  "zyxwvu?tsrqponml": "zyxwvu!tsrqponml",
  "zyxwvut?srqponml": "zyxwvut!srqponml",
  "zyxwvuts?rqponml": "zyxwvuts!rqponml",
  "zyxwvutsr?qponml": "zyxwvutsr!qponml",
  "zyxwvutsrq?ponml": "zyxwvutsrq!ponml",
  "zyxwvutsrqp?onml": "zyxwvutsrqp!onml",
  "zyxwvutsrqpo?nml": "zyxwvutsrqpo!nml",
  "zyxwvutsrqpon?ml": "zyxwvutsrqpon!ml",
  "zyxwvutsrqponm?l": "zyxwvutsrqponm!l",
  "zyxwvutsrqponml?": "zyxwvutsrqponml!",
  "Q?WERTYUIOPASDFG": "Q!WERTYUIOPASDFG",
  "QW?ERTYUIOPASDFG": "QW!ERTYUIOPASDFG",
  "QWE?RTYUIOPASDFG": "QWE!RTYUIOPASDFG",
  "QWER?TYUIOPASDFG": "QWER!TYUIOPASDFG",
  "QWERT?YUIOPASDFG": "QWERT!YUIOPASDFG",
  "QWERTY?UIOPASDFG": "QWERTY!UIOPASDFG",
  "QWERTYU?IOPASDFG": "QWERTYU!IOPASDFG",
  "QWERTYUI?OPASDFG": "QWERTYUI!OPASDFG",
  "QWERTYUIO?PASDFG": "QWERTYUIO!PASDFG",
  "QWERTYUIOP?ASDFG": "QWERTYUIOP!ASDFG",
  "QWERTYUIOPA?SDFG": "QWERTYUIOPA!SDFG",
  "QWERTYUIOPAS?DFG": "QWERTYUIOPAS!DFG",
  "QWERTYUIOPASD?FG": "QWERTYUIOPASD!FG",
  "QWERTYUIOPASDF?G": "QWERTYUIOPASDF!G",
  "QWERTYUIOPASDFG?": "QWERTYUIOPASDFG!",
  "m?nOpQrStUvWxYz1": "m!nOpQrStUvWxYz1",
  "mn?OpQrStUvWxYz1": "mn!OpQrStUvWxYz1",
  "mno?QrStUvWxYz12": "mno!QrStUvWxYz12",
  "mnop?rStUvWxYz12": "mnop!rStUvWxYz12",
  "mnopq?StUvWxYz12": "mnopq!StUvWxYz12",
  "mnopqr?tUvWxYz12": "mnopqr!tUvWxYz12",
  "mnopqrs?UvWxYz12": "mnopqrs!UvWxYz12",
  "mnopqrst?vWxYz12": "mnopqrst!vWxYz12",
  "mnopqrstu?WxYz12": "mnopqrstu!WxYz12",
  "mnopqrstuv?xYz12": "mnopqrstuv!xYz12",
  "mnopqrstuvx?Yz12": "mnopqrstuvx!Yz12",
  "mnopqrstuvxy?z12": "mnopqrstuvxy!z12",
  "mnopqrstuvxyz?12": "mnopqrstuvxyz!12",
  "mnopqrstuvxyza?2": "mnopqrstuvxyza!2",
  "mnopqrstuvxyzab?": "mnopqrstuvxyzab!",
  "bonjourtoijanie!": "bonjourtoijanie?"
}




from passlib.handlers.misc import plaintext

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

def hybrid_permutation(block):
    # Rotation circulaire globale
    rotated = block[8:] + block[:8]
    
    # Ensuite, on échange les deux moitiés
    mid = len(rotated) // 2
    return rotated[mid:] + rotated[:mid]


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
    return [shift_left(key_bin, i)[:128] for i in range(12)]


def shiftleftblockright(i, lengthofblocks, blocks):
    # Shift each block left by i bits
    for idx in range(len(blocks)):
        blocks[idx] = shift_left(blocks[idx], i)

    # Rotate the last 'lengthofblocks' blocks to the right
    if lengthofblocks > 1:
        tail = blocks[-lengthofblocks:]
        blocks[-lengthofblocks:] = [tail[-1]] + tail[:-1]



def avalanche_test_from_binary_percentage(ciphertext1: str, ciphertext2: str, OnEstRenduOu, key, value):
    # On s'assure que les deux textes chiffrés sont en binaire et ont la même longueur
    if len(ciphertext1) != len(ciphertext2):
        raise ValueError("Les textes chiffrés doivent avoir la même longueur en binaire.")

    # Calculer la différence en bits en utilisant XOR
    diff_bits = sum(1 for b1, b2 in zip(ciphertext1, ciphertext2) if b1 != b2)

    # Calculer le pourcentage de différence
    total_bits = len(ciphertext1)
    diff_percentage = (diff_bits / total_bits) * 100

    # print(f"Texte chiffré 1 (binaire) : {ciphertext1}")
    # print(f"Texte chiffré 2 (binaire) : {ciphertext2}")
    # print(f"Différence en bits : {diff_bits}")
    print(f"{OnEstRenduOu} - {key} - {value} - Différence en pourcentage : {diff_percentage:.2f}%")

    return diff_percentage




# 🔐 Algorithme principal
def algo3_cipher(rounds, cle,shiftleft = 5, OnEstRenduOu= 1,text= "test pour projet mi session"):
    # print("\n🔐 ALGO6 - Chiffrement à clé 128 bits 🔐")
    # key = input("Entrez une clé (max 16 caractères) : ")[:16]
    key = cle
    # plaintext = input("Entrez le texte clair à chiffrer : ")
    plaintext = text

    key_bin = pad_block(to_binary(key), 128)
    text_bin = to_binary(plaintext)

    blocks = textwrap.wrap(text_bin, 128)
    blocks = [pad_block(b, 128) for b in blocks]

    subkeys = generate_subkeys(key_bin)
    encrypted_blocks = []

    for block_index, block in enumerate(blocks):
        for round_index in range(rounds):
            block = hybrid_permutation(block)
            block = substitute(block)
            block = shift_left(block, shiftleft)
            block = mix_columns(block)
            block = xor(block, subkeys[round_index])

        encrypted_blocks.append(block)

    final_cipher = ''.join(encrypted_blocks)
    # print(f"\n🔐 ROUND {OnEstRenduOu} -- Message chiffré final : {final_cipher} ")
    return final_cipher




# ▶️ Exécution
#ROUNDS
# i = 12   --- 11 - Différence en pourcentage : 52.34%
# for i in range(32):
#     cipher1 = algo3_cipher(i+1, "bonjourtoijanie!",  5 ,1)
#     cipher2 = algo3_cipher(i+1, "bonjourtoijanie?", 5 , 1)
#     avalanche_test_from_binary_percentage(cipher1, cipher2, i)

#SHIFTLEFT
# i = 2 ;   1 - Différence en pourcentage : 56.25%
# for i in range(32):
#     cipher1 = algo3_cipher(12, "bonjourtoijanie!",  i+1 ,1)
#     cipher2 = algo3_cipher(12, "bonjourtoijanie?", i+1 , 1)
#     avalanche_test_from_binary_percentage(cipher1, cipher2, i)

#
# for i in range(1):
#     cipher1 = algo3_cipher(12, "voici!une#autre$",  2 ,1)
#     cipher2 = algo3_cipher(12, "voici?une#autre$", 2 , 1)
#     avalanche_test_from_binary_percentage(cipher1, cipher2, i)
#



# Iterate over a list containing that object
def run_avalanche_test(test_pairs):
    results = []

    for count, (key, value) in enumerate(test_pairs.items(), start=1):
        cipher1 = algo3_cipher(12, key, 5, 1)
        cipher2 = algo3_cipher(12, value, 5, 1)

        # Assuming this function returns a percentage (float)
        diff = avalanche_test_from_binary_percentage(cipher1, cipher2, count, key, value)
        results.append(diff)

    average = sum(results) / len(results) if results else 0
    print(f"\n🔍 Average Avalanche Difference: {round(average, 2)}%")
    return average







# Iterate over a list containing that object
average = run_avalanche_test(test_pairs)
print(f"Final average: {average}%")

    # print(key, value)


# cipher1 = algo3_cipher(12, element[0],  5 ,1)
# cipher2 = algo3_cipher(12, element[1], 5 , 1)
# avalanche_test_from_binary_percentage(cipher1, cipher2, count)