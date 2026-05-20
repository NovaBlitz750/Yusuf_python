while True:
    no=int(input("Enter a number"))
    if no>0 and no<=9:
        print("The number is of 1 digit")
    elif no>=10 and no<100:
        print("The number is of 2 digit")
    elif no>=100 and no<=999:
        print("The number is of 3 digits")
    else:
        print("The number is greater than 3 digits")