expense=[]
b=[]
Items=int(input("How many items did you buy?"))
i=Items
def add_expense():
    buy=input("What did you buy")
    cost=int(input("How much did it cost?"))
    expense.append({"Item:",buy ,"Cost:",cost})
while i>0:
    add_expense()
    i-=1
if i == 0:
  print(expense)