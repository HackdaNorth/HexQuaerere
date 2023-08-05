string = input("Enter Bytes: ")

ba = bytearray.fromhex(string)
ba.reverse()

s = ''.join(format(x, '02x') for x in ba)
print("Bytes swapped: " +  s.upper())