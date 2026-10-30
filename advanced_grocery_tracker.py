from colorama import Fore, Style, init

sample_input = """milk 3.50
bread 2.25
ice cream 6
stop
1"""

result = {}

while True:
    try:
        
        item = input("Enter the grocery item and its price separated by a space (type 'stop' to get total): ")
        if "stop" in item.strip().lower():
            break
        else:

            name, price = item.rsplit(" ", 1)
            result[name] = float(price)
            ttl=sum(result.values())
    except Exception as e:
        print(e)
how=input("All items in bill format or in one line? \n(Press 1 or bill format and 2 for one line format)) ")
if how=="2":
    print(result)
elif how=="1":
    for name, price in result.items():
        print(f"{name}: ${price:.2f}")
gst_ttl=ttl*1.15
print("Total: $",ttl )
print("Rounded off total: $", round(ttl) )
print("GST = $",gst_ttl)
print(f"Total with GST: {Fore.RED}${gst_ttl}")