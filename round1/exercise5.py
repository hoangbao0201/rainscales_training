text = "abc123def45gh6"
has_digit = False
digits = []
i = 0
while i < len(text):
    c = text[i]
    if c >= "0" and c <= "9":
        has_digit = True
        digits.append(c)
    i = i + 1

print(digits)
