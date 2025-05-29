text = "lap trinh bang ngon ngu python"
words = text.split(" ")
reversed_words = []
i = len(words) - 1

while i >= 0:
    reversed_words.append(words[i])
    i = i - 1
    
result = " ".join(reversed_words)
print(result)
