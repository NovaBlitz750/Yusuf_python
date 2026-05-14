no=int(input("Enter the cost price: "))
selling_pr=int(input("Now, enter the selling price: "))
if selling_pr>no:
    profit=selling_pr-no
    print("You made a profit of", profit, "rupees!")
elif selling_pr<no:
    loss=no-selling_pr
    print("You made a loss of", loss, "rupees!")
else:
    print("No profit or loss!")