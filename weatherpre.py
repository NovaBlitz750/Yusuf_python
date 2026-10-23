weather=(1,0,0,1,1,0,1,0,1,1,0)
r=0
s=0
for i in range(0,len(weather)):
    if weather[i]==1:
        r+=1
    else:
        s=+1
if r>s:
    print("It will be rainy ")
else:
    print("It will be sunny")