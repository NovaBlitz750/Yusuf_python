input("Double loop at n=4 took 10 steps. Watch it grow. Press Enter")
for n in [10,100,1000]:
    input(" n = "+str(n)+"   Press Enter")
    print(" steps =",n*(n+1)//2)
