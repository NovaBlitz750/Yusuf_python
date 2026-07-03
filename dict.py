dict1={ "name":"Yusuf", "age":"13", "course":"python"}
for key in dict1:
    print(key)
for i in dict1.values():
    print(i)
for l in dict1.items():
    print(l)
print(dict1["name"])
print(dict1.get("name"))
l1= list(dict1.items())
print(l1[0])