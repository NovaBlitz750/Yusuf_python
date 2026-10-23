try:
    no1,no2=eval(input("Enter 2 numbers, separated by commas"))
    print(no1/no2)
except ZeroDivisionError as zde:
    print("Division with 0 isn't possible")
except SyntaxError:
    print("Separate numbers with a comma")
except:
    print("Something went wrong")
finally:
    print("This will execute")