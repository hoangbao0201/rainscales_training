text = "lap trinh bang ngon ngu python"
char_counts = {}
i = 0
while i < len(text):
    current_char = text[i]
    if current_char != " ":
        if current_char not in char_counts:
            char_counts[current_char] = 1
        else:
            char_counts[current_char] = char_counts[current_char] + 1
    i = i + 1

max_char = ""
max_count = 0
keys = list(char_counts.keys())
index = 0
while index < len(keys):
    key = keys[index]
    if char_counts[key] > max_count:
        max_count = char_counts[key]
        max_char = key
    index = index + 1

print(max_char, max_count)
