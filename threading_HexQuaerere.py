import concurrent.futures

def read_pairs_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pair_list = [line.strip().split() for line in lines]
    return pair_list

def compare_lines(line1_pairs, line2_pairs, line1_idx, line2_idx):
    for i in range(len(line1_pairs) - 3):
        for j in range(len(line2_pairs) - 3):
            if (line1_pairs[i:i+4] == line2_pairs[j:j+4][::-1] and
                line1_pairs[i+4:i+8] == line2_pairs[j+4:j+8][::-1]):
                return (line1_idx + 1, line2_idx + 1, i, j)
    return None

def find_similar_pairs(pair_list1, pair_list2, start_line, end_line):
    successful_matches = []
    
    for line1_idx in range(start_line, end_line):
        print(f"Processing line {line1_idx + 1}/{len(pair_list1)} from pairs1.txt")
        line1_pairs = pair_list1[line1_idx]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = []
            
            for line2_idx, line2_pairs in enumerate(pair_list2):
                results.append(executor.submit(compare_lines, line1_pairs, line2_pairs, line1_idx, line2_idx))
            
            for result in concurrent.futures.as_completed(results):
                match = result.result()
                if match:
                    successful_matches.append(match)
    
    return successful_matches

def save_matches_to_file(matches, output_file):
    with open(output_file, 'w') as file:
        for match in matches:
            file.write(f"Match Found:\n")
            file.write(f"Pairs1 Line {match[0]}, Index {match[2]}:\n")
            file.write(" ".join(match[1]) + "\n")
            file.write(f"Pairs2 Line {match[1]}, Index {match[3]}:\n")
            file.write(" ".join(match[0]) + "\n\n")

def main():
    pairs1_path = "pairs1.txt"
    pairs2_path = "pairs2.txt"
    output_file = "matches.txt"

    pair_list1 = read_pairs_from_file(pairs1_path)
    pair_list2 = read_pairs_from_file(pairs2_path)

    start_line = 0
    end_line = len(pair_list1)

    successful_matches = find_similar_pairs(pair_list1, pair_list2, start_line, end_line)
    save_matches_to_file(successful_matches, output_file)

    print("Matches saved to", output_file)

if __name__ == "__main__":
    main()
