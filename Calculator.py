while True:
    a = float(input("Enter a number"))
    b = float(input("Enter a second number"))
    operation=input("What operation should I do with these 2 numbers?(addition, subtraction, multiplication and division)")
    if operation=="+":
        print(a+b)
        
    if operation=="-":
        print(a-b)
       
    if operation=="*":
        print(a*b)
       
    if operation=="/":
        print(a/b)
    if operation == "quit":
        break