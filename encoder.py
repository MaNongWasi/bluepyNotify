from bluepy.btle import DefaultDelegate, Peripheral
import struct

class TestBLEDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.data = 0

    def handleNotification(self, cHandle, data):
        self.data = self.parse_encoder_data(data)
        print(self.data)


    @staticmethod
    def parse_encoder_data(data):
        if len(data) == 2:
            (rawT, rawH) = struct.unpack('<BB', data)
            return (((rawT & 0x07) * 256 + rawH) >> 1) * 360 / 1024  # degree
        else:
            return False


class NewConnectionTest:
    def __init__(self, name="", mac_addr="", addr_type="public", iface=0):
        self.p=Peripheral(mac_addr, addrType=addr_type, iface=iface)
        self.mac_addr = mac_addr
        self.addr_type = addr_type
        self.iface = iface
        self.bleDelegate=TestBLEDelegate()
        self.p.withDelegate(self.bleDelegate)
        self.name = name

    def get_data(self):
        self.p.waitForNotifications(1.0)
#        print ("Notification Recieved: ", self.name)
        return self.bleDelegate.data

    def disconnect(self):
        self.p.disconnect()

print('Connecting to ec70')
try:
    a = NewConnectionTest(mac_addr = '7C:EC:79:E4:5D:69', iface = 0)
    for i in range(0,10):
        print 'ec70 ', a.get_data()
except Exception as e:
    print "Error %s" % str(e)
    a.disconnect()
else:
    a.disconnect()
