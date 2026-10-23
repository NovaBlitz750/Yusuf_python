medc=input("Do you have any medical condition?(Y/N)").strip().upper()
if medc=="Y":
    print("You are eligible for the exam")
elif medc=="N":
    att=float(input("Enter you attendance"))
    if att>=75:
        print("You are eligible for the exam")
    else:
        print("You aren't eligible for the exam")
else:
    print("Please enter a valid option")