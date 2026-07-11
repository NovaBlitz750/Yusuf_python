import random
x=0
y=0
mode=input("Quiz mode or learning mode?")
if mode.strip().upper()=="LEARN"  or mode.strip().upper()=="LEARNING":
    no=int(input("Enter a number"))
    no2=int(input("Enter another number"))
    op=input("Cubes or squares?").strip().upper()
    if op=="CUBES":
        for i in range(no,no2+1):
            print(i,"^ 3 =",i**3)
    elif op=="SQUARES":
     for i in range(no,no2+1):
          print(i,"^ 2= ",i**2)
    else:
        print("Please enter a valid option")
elif mode.strip().upper()=="QUIZ":
    no=int(input("Enter a number"))
    no2=int(input("Enter another number"))
    op=input("Cubes or squares?").strip().upper()
    ques=int(input("How many questions"))
    if op=="CUBES" or op=="CUBE":
        while y<ques:
            cubeask=random.randint(no,no2)
            ask=int(input(f"Whats the cube of {cubeask}"))
            if ask== cubeask**3:
                print("Correct answer")
                x+=1
            else:
                print("Wrong answer, the correct answer is", cubeask**3)
            y+=1
        print("Your score was",x,"out of",ques )
    elif op=="SQUARES" or op=="SQUARE":
        while y<ques:
            cubeask=random.randint(no,no2)
            ask=int(input(f"Whats the square of {cubeask}"))
            if ask== cubeask**2:
                print("Correct answer")
                x+=1
            else:
                print("Wrong answer, the correct answer is", cubeask**2)
            y+=1
        print("Your score was",x,"out of",ques )