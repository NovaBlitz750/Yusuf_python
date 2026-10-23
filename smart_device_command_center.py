from abc import ABC, abstractmethod
class smdevice:
    def show(self,name):
        self.name=name
        print("Device name:", name)
    @abstractmethod
    def on(self):
        ...
class smlight(smdevice):
    def on(self):
        print("SmartLight is now on")
class smfan(smdevice):
    def on(self):
        print("SmartFan is now on")
class smspeaker(smdevice):
    def on(self):
        print("SmartSpeaker is now on")
light=smlight()
fan=smfan()
speaker=smspeaker()
light.show("Living room light")
light.on()
fan.show("Room fan")
fan.on()
speaker.show("Party speaker")
speaker.on()
class seccam():
    def check(self):
        print("Security Camera is now recording")
class dlock:
    def check(self):
        print("Doorlock is now locked")
devices=[seccam(),dlock()]
print("SmartDevice statuses")
for i in devices:
    print(i.check())