dict={"name":"Lays chips",
      "price":"$10",
       "expiry__date":"1 jan, 2026" }
print(dict)
for i in dict:
    print(dict[i])
for l in dict.items():
    print(l)
print(dict.get("price"))
for x in dict.values():
    print(x)