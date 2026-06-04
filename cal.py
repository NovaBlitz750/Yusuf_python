def add(a,b):
    return a+b
def sub(a,b):
     return a-b
def mult(a,b):
      return a*b
def div(a,b):
    return a%b
while True:
    no1=float(input("Enter a number"))
    no2=float(input("Enter another number"))
    op=input(f"What operation shall be done with {no1} and {no2} \n A. Add \n B. Subtract \n C. Multiply \n D. Divide").strip().upper()
    if op=="A":
         print(add(no1,no2))
    elif op=="B":
        print(sub(no1,no2))
    elif op=="C":
        print(mult(no1,no2))
    elif op=="D":
        print(div(no1,no2))
    else:
        print("Please enter a valid input")