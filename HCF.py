nolargest=int(input("Enter the largest number "))
nosmallest=int(input("Enter the smallest number "))

while (nosmallest):
    nostore=nosmallest
    nosmallest=nolargest%nosmallest
    nolargest=nostore

print("HCF is :",nolargest)