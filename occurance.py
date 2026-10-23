word=input("Enter a word")
char=input("Enter any letter")
wor=word.strip().upper()
cha=char.strip().upper()
i=0
count=0
while i<len(word):
    if cha==wor[i]:
        count+=1
    i+=1
print(f"in \"{word}\" the letter \"{char}\" has occured {count} times")