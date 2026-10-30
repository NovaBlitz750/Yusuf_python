no_of_items=int(input("Enter ur number of items "))
result={}
for i in range(no_of_items):
    item = input("Enter the grocery item and its price separated by a space: ")
    name, price = item.rsplit(" ", 1)
    result[name] = float(price)
ttl=sum(result.values())
print(result)
print("Total: $",ttl )
print("Rounded off total: $", round(ttl) )