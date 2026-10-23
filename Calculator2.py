while True:
    a = float(input("Enter a number"))
    b = float(input("Enter a second number"))
    operation=input("What operation should be done with these 2 numbers?(+,-,*,/,^,quit)")
    if operation=="+":
        print(a,"+",b,"=",a+b)
        
    elif operation=="-":
        print(a,"-",b,"=",a-b)
       
    elif operation=="*":
        print(a,"*",b,"=",a*b)
       
    elif operation=="/":
        if b == 0:
            print("Division with 0 isn't possible")
        else:
            print(a/b)
    elif operation == "quit":
        break
    elif operation=="/" and b==0:
        print("Division by 0 isn't possible")    
    elif operation=="^" or"**":
        print(a,"^",b,"=",a**b)
            