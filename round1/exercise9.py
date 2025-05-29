text = input("Nhap: ")
i = 0
is_palindrome = True
j = len(text) - 1
while i < j:
    if text[i] != text[j]:
        is_palindrome = False
        break
    i = i + 1
    j = j - 1
print(is_palindrome)
