eng=float(input("Enter your english marks"))
mx=float(input("Enter your maths marks"))
hindi=float(input("Enter your hindi marks"))
sci=float(input("Enter your science marks"))
tt= eng+mx+hindi+sci
print("Your subject total is",tt, "out of 500")
avg= tt//5
if avg>90:
    print("You got an A!")
if avg<90 and avg>75:
    print("You got a B")
if avg<75 and avg>70:
    print("You got a C")