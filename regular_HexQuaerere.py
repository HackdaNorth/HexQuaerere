def read_pairs_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pair_list = [line.strip().split() for line in lines]
    return pair_list

def find_similar_pairs(pair_list1, pair_list2):
    successful_matches = []
    
    for line1_idx, line1_pairs in enumerate(pair_list1):
        print(f"Processing line {line1_idx + 1}/{len(pair_list1)} from pairs1.txt")
        prev_match = False
        
        for line2_idx, line2_pairs in enumerate(pair_list2):
            for i in range(len(line1_pairs) - 1):
                for j in range(len(line2_pairs) - 1):
                    if ((line1_pairs[i] == "80" and line1_pairs[i+1] == "C0") or
                        (line1_pairs[i] == "C0" and line1_pairs[i+1] == "80")) and (
                        (line2_pairs[j] == "80" and line2_pairs[j+1] == "C0") or
                        (line2_pairs[j] == "C0" and line2_pairs[j+1] == "80")):
                        continue
                    if (line1_pairs[i] == line2_pairs[j+1] and
                        line1_pairs[i+1] == line2_pairs[j] and
                        line1_pairs[i] != "00" and line2_pairs[j] != "00" and
                        line1_pairs[i] != "40" and line2_pairs[j] != "40" and
                        line1_pairs[i] != "80" and line2_pairs[j] != "80"):
                        if not prev_match:
                            print(f"  Swapped to next four bytes from pairs1.txt")
                            prev_match = True
                        matched_bytes = f"{line1_pairs[i]} {line1_pairs[i+1]} <-> {line2_pairs[j]} {line2_pairs[j+1]}"
                        successful_matches.append((line1_idx + 1, line2_idx + 1, i, matched_bytes))
                        print(f"    Match found: Pairs1 Line {line1_idx + 1}, Index {i} <-> Pairs2 Line {line2_idx + 1}, Index {j}")
                        break
    
    return successful_matches

def save_matches_to_file(matches, output_file):
    with open(output_file, 'w') as file:
        for match in matches:
            file.write(f"Match Found:\n")
            file.write(f"Pairs1 Line {match[0]}, Index {match[2]}:\n")
            file.write(f"Pairs2 Line {match[1]}, Index {match[2]+1}:\n")
            file.write(f"Matched Bytes: {match[3]}\n\n")

def main():
    pairs1_path = "pairs1.txt"
    pairs2_path = "pairs2.txt"
    output_file = "matches.txt"

    pair_list1 = read_pairs_from_file(pairs1_path)
    pair_list2 = read_pairs_from_file(pairs2_path)

    successful_matches = find_similar_pairs(pair_list1, pair_list2)
    save_matches_to_file(successful_matches, output_file)

    print("Matches saved to", output_file)

if __name__ == "__main__":
    main()
