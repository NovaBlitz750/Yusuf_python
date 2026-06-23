def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    return a%b
try:
    a=float(input("Enter a number"))
    b=float(input("Enter another number"))
    oper=input("What operation shall be done with these 2 numbers")
    if oper=="+":
        print(a,"+",b, "=",add(a,b))
    elif oper=="-":
        print(a,"-",b, "=",sub(a,b))
    elif oper=="*":
        print(a,"*",b, "=",mul(a,b))
    elif oper=="/":
        print(a,"/",b, "=",div(a,b))
except ZeroDivisionError as zde:
    print("Division by zero isnt possible")
except ValueError as ve:
    print("Please enter numbers only")