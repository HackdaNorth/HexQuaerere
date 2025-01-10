def read_pairs_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pair_list = [line.strip().split() for line in lines]
    return pair_list

def find_similar_pairs(pair_list1, pair_list2):
    successful_matches = []

    unique_segments = set()
    for line2_pairs in pair_list2:
        for j in range(len(line2_pairs) - 3):
            segment = tuple(line2_pairs[j:j+4][::-1])
            if all(byte != "00" for byte in segment) and \
               all(byte != "FF" for byte in segment) and \
               all(byte != "40" for byte in segment) and \
               all(byte != "80" for byte in segment):
                unique_segments.add(segment)

    for line1_idx, line1_pairs in enumerate(pair_list1):
        print(f"Processing line {line1_idx + 1}/{len(pair_list1)} from pairs1.txt")

        for i in range(len(line1_pairs) - 3):
            segment = tuple(line1_pairs[i:i+4])
            if all(byte != "00" for byte in segment) and \
               all(byte != "FF" for byte in segment) and \
               all(byte != "40" for byte in segment) and \
               all(byte != "80" for byte in segment):
                if segment in unique_segments:
                    matched_bytes = " ".join(segment[::-1]) + " <-> " + " ".join(segment)
                    hex_offset1 = "{:08x}".format(line1_idx * 16 + i)  # Calculate HEX offset for pairs1

                    # Find the corresponding Pairs2 Line and HEX Offset
                    for line2_idx, line2_pairs in enumerate(pair_list2):
                        for j in range(len(line2_pairs) - 3):
                            if segment == tuple(line2_pairs[j:j+4][::-1]):
                                hex_offset2 = "{:08x}".format(line2_idx * 16 + j)  # Calculate HEX offset for pairs2
                                successful_matches.append((line1_idx + 1, hex_offset1, line2_idx + 1, hex_offset2, segment, matched_bytes))
                                print(f"Match found: Pairs1 Line {line1_idx + 1}, HEX Offset {hex_offset1} , Pairs2 Line {line2_idx + 1}, HEX Offset {hex_offset2}, Matched Bytes: Pairs1: {segment[::-1]} <->  Pairs2: {segment}")
                                break

    return successful_matches

def save_matches_to_file(matches, output_file):
    with open(output_file, 'w') as file:
        for match in matches:
            file.write(f"Match Found:\n")
            file.write(f"Pairs1 Line {match[0]}, HEX Offset {match[1]}:\n")
            file.write(f"Pairs2 Line {match[2]}, HEX Offset {match[3]}:\n")
            file.write(f"Matched Bytes: Pairs1: {match[5]} <->  Pairs2: {match[4]}\n\n")

def main():
    pairs1_path = "pairs1.txt"
    pairs2_path = "pairs2.txt"
    output_file = "matches_with_hex_offset_v4.txt"

    pair_list1 = read_pairs_from_file(pairs1_path)
    pair_list2 = read_pairs_from_file(pairs2_path)

    successful_matches = find_similar_pairs(pair_list1, pair_list2)
    save_matches_to_file(successful_matches, output_file)

    print("Matches saved to", output_file)

if __name__ == "__main__":
    main()

