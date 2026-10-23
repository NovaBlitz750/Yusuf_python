box1={"chocolate", "chips", "apple", "gummy bear"}
box2={"banana, chocolate shake", "gummy bear", "juice"}
print("snacks in box1 = ", box1)
print("snacks in box2 = ", box2)
box1.add("Granola bar")
print("Granola bar has been added to box1")
share= box1.intersection(box2)
print("Common snacks between box1 and bix2 are the following:", share)
snack_co=[2,5,7,9,6]
print("Snack count = ",snack_co)
snack_co.append(3)
snack_co.append(5)
no5=snack_co.count(5)
print("5 appears", no5, "times in snacks count")
snack_co.reverse()
print("Reversed snack count = ",snack_co)