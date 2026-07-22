class employee:
    def __init__(self,name):
        self.name=name
        print("Object created")
    def pri(self):
        print("The name is emplyee is", self.name)
    def __del__(self):
        print("Object destructed successfully")
obj= employee("Yusuf")
obj.pri()
