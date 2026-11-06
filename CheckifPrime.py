no=int(input("Enter a number to check wheather its prime or not "))
if no<=1:
    print(no,"isnt a prime number")
else: 
    for i in range(2,no):
        if no%i==0:
            print("Number isn't a prime number")
            break
    else:
            print("Number is a prime number")
