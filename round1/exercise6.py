fullname = "Nguyen Van An"
words = fullname.split(" ")
last_name = words[len(words) - 1]
first_middle = ""
i = 0
while i < len(words) - 1:
    first_middle = first_middle + words[i]
    if i != len(words) - 2:
        first_middle = first_middle + " "
    i = i + 1
    
print(first_middle)
print(last_name)
