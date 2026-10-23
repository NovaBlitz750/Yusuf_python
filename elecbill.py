units=int(input("Enter your monthly electricity units consumed"))
if units<=50:
    amnt=units*2.6
    tax=25
elif units>50 and units<=100:
    amnt=units*3.25
    tax=35
elif units>100 and units<=200:
    amnt=units*5.26
    tax=45
elif units>200:
    amnt=units*8.45
    tax=75
print("Your cost is", amnt, "With",tax,"tax, leading the total bill to",amnt+tax,"rs")