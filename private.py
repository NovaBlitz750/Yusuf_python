class any:
    __priVar=7
    def __priv_method(self):
        print("Private method created successfully")
    def normal_method(self):
        print("Value of priVar = ", any.__priVar)
        any.__priv_method(self)
obj=any()
#obj.__priv_method()
obj.normal_method()