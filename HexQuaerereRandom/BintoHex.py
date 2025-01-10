def binary_to_hex(binary_data):
    hex_string = binary_data.hex().upper()
    return hex_string

def swap_byte_pairs(hex_string):
    hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    swapped_pairs = [pair[2:4] + pair[0:2] for pair in hex_pairs]
    return ' '.join(swapped_pairs)

def save_hex_to_file(hex_string, output_file):
    with open(output_file, 'w') as file:
        columns = [hex_string[i:i+48] for i in range(0, len(hex_string), 48)]
        for column in columns:
            file.write(column + '\n')

def main():
    input_file = "file3.bin"  # Replace this with the path to your .bin file
    output_file = "output_hex.txt"  # Replace this with the desired output file name

    with open(input_file, 'rb') as file:
        binary_data = file.read()

    hex_string = binary_to_hex(binary_data)
    swapped_hex = swap_byte_pairs(hex_string)
    save_hex_to_file(swapped_hex, output_file)
    print(f"Hexadecimal data with swapped byte pairs saved to '{output_file}'.")

if __name__ == "__main__":
    main()
