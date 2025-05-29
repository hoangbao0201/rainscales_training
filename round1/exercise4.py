text = input("Nhap: ")
char_counts = {}
i = 0
while i < len(text):
    current_char = text[i]
    if current_char not in char_counts:
        char_counts[current_char] = 1
    else:
        char_counts[current_char] = char_counts[current_char] + 1
    i = i + 1

keys = list(char_counts.keys())
index = 0
while index < len(keys):
    print(keys[index], char_counts[keys[index]])
    index = index + 1
