binary=input("Enter a binary number ")
decimal=0
if "0" not in binary and "1" not in binary:
    print("Please enter a valid input")
else:

    for i in binary:
        decimal=decimal*2+int(i)
    print(binary,"in binary form is:",decimal)
