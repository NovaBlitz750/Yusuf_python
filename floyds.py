while True:
    no=1
    line =1
    rows=int(input("Enter the number of rows you want"))
    for i in range(1, rows+1):
        print(line,".", end=" ")
        for j in range(0,i):
            print(no, end=" ")
            no+=1
        print()
        line+=1