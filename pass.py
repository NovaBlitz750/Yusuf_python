for no in range(20):
    if no%20==0:
        print("twist")
    elif no%15==0:
        pass
    elif no%5==0:
        print("buzz")
    elif no%3==0:
        print("fizz")
    else:
        print(no)