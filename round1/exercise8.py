word = "ABCDEfgh"
result = []
for i, ch in enumerate(word):
    if i % 2 == 0:
        result.append(ch.upper())
    else:
        result.append(ch.lower())

print(''.join(result))