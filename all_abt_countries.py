class india:
    def capital(self):
        print("New Delhi is the capital of India")
    def lan(self):
        print("Hindi is the most widely spoken language of India")
    def type(self):
        print("India is a developing country")
class USA:
    def capital(self):
        print("Washington D.C. is the capital of USA")
    def lan(self):
        print("English is the most widely spoken language of USA")
    def type(self):
        print("USA is a developed country")
obj_in=india()
obj_usa=USA()
for i in (obj_in,obj_usa):
    i.capital()
    i.lan()
    i.type()