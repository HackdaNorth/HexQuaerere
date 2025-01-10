def read_pairs_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pair_list = [line.strip().split() for line in lines]
    return pair_list

def find_similar_pairs(pair_list1, pair_list2):
    successful_matches = []
    
    for line1_idx, line1_pairs in enumerate(pair_list1):
        print(f"Processing line {line1_idx + 1}/{len(pair_list1)} from pairs1.txt")
        
        for line2_idx, line2_pairs in enumerate(pair_list2):
            for i in range(len(line1_pairs) - 3):
                for j in range(len(line2_pairs) - 3):
                    if all(byte != "00" for byte in line1_pairs[i:i+4]) and \
                       all(byte != "FF" for byte in line1_pairs[i:i+4]) and \
                       all(byte != "40" for byte in line1_pairs[i:i+4]) and \
                       all(byte != "80" for byte in line1_pairs[i:i+4]) and \
                       all(byte != "00" for byte in line2_pairs[j:j+4]) and \
                       all(byte != "FF" for byte in line2_pairs[j:j+4]) and \
                       all(byte != "40" for byte in line2_pairs[j:j+4]) and \
                       all(byte != "80" for byte in line2_pairs[j:j+4]) and \
                       line1_pairs[i:i+4] == line2_pairs[j:j+4][::-1]:
                        
                        matched_bytes = " ".join(line1_pairs[i:i+4]) + " <-> " + " ".join(line2_pairs[j:j+4])
                        ram_address1 = line1_idx * 4 + i  # Calculate RAM address for pairs1
                        ram_address2 = line2_idx * 4 + j  # Calculate RAM address for pairs2
                        successful_matches.append((line1_idx + 1, ram_address1, line2_idx + 1, ram_address2, matched_bytes))
                        print(f"    Match found: Pairs1 Line {line1_idx + 1}, RAM Address 0x{ram_address1:05x} <-> Pairs2 Line {line2_idx + 1}, RAM Address 0x{ram_address2:05x}, Matched Bytes: {match[4]}")
                        break
    
    return successful_matches

def save_matches_to_file(matches, output_file):
    with open(output_file, 'w') as file:
        for match in matches:
            file.write(f"Match Found:\n")
            file.write(f"Pairs1 Line {match[0]}, RAM Address 0x{match[1]:05x}:\n")
            file.write(f"Pairs2 Line {match[2]}, RAM Address 0x{match[3]:05x}:\n")
            file.write(f"Matched Bytes: {match[4]}\n\n")

def main():
    pairs1_path = "pairs1.txt"
    pairs2_path = "pairs2.txt"
    output_file = "matches_direct.txt"

    pair_list1 = read_pairs_from_file(pairs1_path)
    pair_list2 = read_pairs_from_file(pairs2_path)

    successful_matches = find_similar_pairs(pair_list1, pair_list2)
    save_matches_to_file(successful_matches, output_file)

    print("Matches saved to", output_file)

if __name__ == "__main__":
    main()
