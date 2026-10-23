def total_cal(bill,tip_per):
    total_bill=(bill+(bill*tip_per*0.01))
    total_bill= round(total_bill,2)
    return total_bill
bill=float(input("Enter your bill amount"))
tip=float(input("Enter the percentage of your total bill that you want to tip"))
print("Your total bill is", total_cal(bill,tip))