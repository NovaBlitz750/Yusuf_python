word=input("Enter a word")
print(f"{word} is spelled as:")
for letter in word:
    print(letter)
print(f" \"{word}\" is of {len(word)} letters")