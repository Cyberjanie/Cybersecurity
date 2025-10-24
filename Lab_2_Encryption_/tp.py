

#### Convert to ASCII ################

word = "Bonjour"
ascii_values = [ord(char) for char in word]
print(ascii_values)  # Output: [72, 101, 108, 108, 111]

#### Convert Ascii to Binary ################

nombreBinaire = 16
def ascii_list_to_binary(ascii_list):
    return [format(num, f"0{nombreBinaire}b") for num in ascii_list]

# Example usage
binary_output = ascii_list_to_binary(ascii_values)


string = []
for element in binary_output:
    string.append(element)

string_binaire = ''.join(string)
string_temp = ' '.join(string)

print(string_binaire)
#### Permutation ################


def binary_permutation_blocks(binary_str, block_size=16):
    """
    Permutes each block of binary_str using a fixed permutation pattern.

    :param binary_str: A string of binary digits (e.g., '1101010111001100...')
    :param block_size: Size of each block to permute (default is 16)
    :return: Binary string with each block permuted
    """
    if len(binary_str) % block_size != 0:
        raise ValueError("Binary string length must be a multiple of block size.")

    # Define a permutation pattern for each block (e.g., reverse)
    permutation_pattern = list(reversed(range(block_size)))

    permuted_blocks = []
    for i in range(0, len(binary_str), block_size):
        block = binary_str[i:i + block_size]
        permuted_block = ''.join(block[j] for j in permutation_pattern)
        permuted_blocks.append(permuted_block)

    return ' '.join(permuted_blocks)



permutation_size = len(string_binaire)

result = binary_permutation_blocks(string_binaire)

print("Original binary: ", string_temp)
print("Permuted binary: ", result)



