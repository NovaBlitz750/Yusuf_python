print("Running Lap tracker")
laps=int(input("Enter the number of laps: "))
points_perlap=int(input("Enter the points per lap: "))
total1=laps*points_perlap
print("Points:",total1, " \nFormula: total1=laps*points_perlap")
print("\n")

ttl=0
for i in range(laps):
    ttl+=points_perlap
print("Points: ",ttl,"\nFormula: for loop")
print("\n")


ttl1=0
for i in range(laps):
    for j in range(points_perlap):
        ttl1+=1
print("Points: ",ttl1,"\nFormula: Nested loop")