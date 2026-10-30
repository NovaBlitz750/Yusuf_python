grades=input("Enter ur grades separated by spaces ")
parts =grades.split(" ")
print(parts)
ttl=0
for i in parts:
    ttl+=float(i)
print(ttl)
avg=ttl/len(parts)
rounded_off_avg=round(avg)
print(avg,"%")
print("Rounded off grade:",rounded_off_avg,"%")