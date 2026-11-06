start=int(input("Enter a starting number "))
end=int(input("Enter an ending number "))
print(f"the prime numbers between {start} and {end} are: ")
for no in range(start,end+1):
    if no>1:
        for i in range(2,no):
            if no%i==0:
                break
        else:
            print(no,end=" ")