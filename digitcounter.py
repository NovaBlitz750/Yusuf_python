no=int(input("Enter a number"))
if no<100 and no>10:
    print("It is a 2 digit number")
elif no<1000 and no>100:
    print("It is a 3 digit number")
elif no<10:
    print("Its a 1 digit number")
else:
    print("The number is greater than 3 digits")