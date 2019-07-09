from bluepy.btle import DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM, ADDR_TYPE_PUBLIC
import struct

class TestBLEDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.data = 0

    def handleNotification(self, cHandle, data):
        print ("handle notification")
        self.data = self.parse_encoder_data(data)
        print(self.data)


    @staticmethod
    def parse_encoder_data(data):
        print ("parse_encoder_data ", len(data))
        if len(data) == 16:
            (rawT, rawH, raw3, raw4, raw5, raw6, raw7, raw8, raw9, raw10, raw11, raw12, raw13, raw14, raw15, raw16) = struct.unpack('<16B', data)
            return [rawT, rawH, raw3, raw4, raw5, raw6, raw7, raw8, raw9, raw10, raw11, raw12, raw13, raw14, raw15, raw16]
        else:
            return False


class NewConnectionTest:
    def __init__(self, name="", mac_addr="", addr_type=ADDR_TYPE_RANDOM, iface=0):
        self.p=Peripheral(mac_addr, addrType=addr_type, iface=iface)
        self.mac_addr = mac_addr
        self.addr_type = addr_type
        self.iface = iface
        self.bleDelegate=TestBLEDelegate()
        self.p.withDelegate(self.bleDelegate)
        self.enableNotification()

    def enableNotification(self):
	print ("enable notification")
        try:
            self.p.writeCharacteristic(0x0010, '\x01\x00')
	except BTLEException as err:
	    print 'Error writing char %s' % str(err)
	    self.p.disconnect()


    def get_data(self):
        self.p.waitForNotifications(2.0)
        return self.bleDelegate.data

    def disconnect(self):
        self.p.disconnect()

print('Connecting to ec70')
try:
    a = NewConnectionTest(mac_addr = 'CC:E9:69:83:54:21')
    print ("connected")
    for i in range(0, 5):
        print a.get_data()
except Exception as e:
    print "Error %s" % str(e)
    a.disconnect()
else:
    a.disconnect()
