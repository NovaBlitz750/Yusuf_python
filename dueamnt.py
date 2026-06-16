bill=float(input("Enter your bill amount"))
def reduce_bill(bill):
    amnpay=float(input("Enter how much you paid"))
    bill-=amnpay
    return f"You should collect {bill} worth of change"
print(reduce_bill(bill))