try:
    age=int(input("Enter your age(as a integer)"))
    if age%2==0:
        print(age, "is an even number")
    else:
         print(age, "is an odd number")
except ValueError as ve:
    print(ve)
    print("Please enter a integer")