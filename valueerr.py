try:
    a=int(input("Enter a number"))
    print(a)
except ValueError as ve:
    print("Exception:", ve )