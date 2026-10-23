while True:
    GST = 0.15
    amt = float(input("Enter an amount: "))
    print("The bil is", amt, "and GST is 15%, so $",amt * GST + amt, "Will be the total expense with $",amt*GST, "GST")
