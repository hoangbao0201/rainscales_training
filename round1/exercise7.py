name = "nGuYen vAN a"

list_word = name.strip().split()
list_word = [word[0].upper() + word[1:] for word in list_word]

print(' '.join(list_word))