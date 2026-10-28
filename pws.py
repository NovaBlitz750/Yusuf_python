import time

def slow_print(text, delay=0.08):
    for character in text:
        print(character, end='', flush=True)
        time.sleep(delay)
    print()
joshua_npw="bRodi6#a"
kace_ipw="latHra#4"
leon_nguyenpw="Dryn9r!a"
charlie_waswopw="cyb!st1X"
name=input("Whose password do u want? Write their first name ").strip().capitalize()
if name=="Kace":
    slow_print(kace_ipw)
elif name=="Joshua":
    slow_print(joshua_npw)
elif name=="Leon":
    slow_print(leon_nguyenpw)
elif name=="Charlie":
    slow_print(charlie_waswopw)
elif name=="Yusuf":
    slow_print("Stfu fucking dumbass, ur not Yusuf")
else:
    slow_print("Enter a valid name")