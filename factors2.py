no=int(input("Enter a number to check its factors "))
print("Factors of",no,"are: ")
for i in range(1,no+1):
    if no%i==0:
        print(i,end=" ")
    else: pass