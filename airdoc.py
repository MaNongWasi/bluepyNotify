from btle import UUID, Peripheral, DefaultDelegate, BTLEException
import struct
import datetime

def _TI_UUID(val):
    return UUID("%08X-0000-1000-8000-00805f9b34fb" % (0x00000000+val))

svcUUID_F = _TI_UUID(0xFFF0)
svcUUID_E = _TI_UUID(0xFFE0)
char_F1 = _TI_UUID(0xFFF1)
char_F3 = _TI_UUID(0xFFF3)
char_F4 = _TI_UUID(0xFFF4)
char_E1 = _TI_UUID(0XFFE1)
char_E3 = _TI_UUID(0XFFE3)
char_E4 = _TI_UUID(0xFFE4)
start_comm = struct.pack("18B", 0x00, 0x01, 0x37, 0x38, 0x32, 0x32, 0x38, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)

class FineDust():
    def __init__(self, addr):
	self.p = Peripheral(addr)
	self.bleDelegate = TestBLEDelegate()
	self.p.setDelegate(self.bleDelegate)
	self.svcF = self.p.getServiceByUUID(svcUUID_F)
	self.charF1 = self.svcF.getCharacteristics(char_F1)[0]
	self.charF3 = self.svcF.getCharacteristics(char_F3)[0]
	self.charF4 = self.svcF.getCharacteristics(char_F4)[0]
	self.svcE = self.p.getServiceByUUID(svcUUID_E)
	self.charE1 = self.svcE.getCharacteristics(char_E1)[0]
	self.charE3 = self.svcE.getCharacteristics(char_E3)[0]
	self.charE4 = self.svcE.getCharacteristics(char_E4)[0]
	print ('enable Notification')
	self.enableNotification()	

    def get_data(self):
	self.p.waitForNotifications(10.0)
	print ('wait for notification')
	return {'handle':self.bleDelegate.handle, 'data':self.bleDelegate.data}

    def disconnect(self):
	self.p.disconnect()

    def enableNotification(self):
	try:
	    print('enable f4')
	    self.p.writeCharacteristic(0x002f, '\x01\x00')
	    print('enable e3')
            self.p.writeCharacteristic(0x003e, '\x01\x00')
	    print('enable e4')
            self.p.writeCharacteristic(0x0042, '\x01\x00')
	    print('enable e1')
            self.p.writeCharacteristic(0x0037, '\x01\x00')
	    print ('write F1 start comm')
	    self.charF1.write(start_comm, withResponse=True)
#	    self.p.writeCharacteristic(0x0025, start_comm)
	    print ('write F3')
	    self.charF3.write('\x03', withResponse=True)
#	    self.p.writeCharacteristic(0x002b, "\x03")
	    print ('write F1 datetime')
	    self.charF1.write(self.currentTime(), withResponse=True)
#	    self.p.writeCharacteristic(0x0025, self.currentTime())
	except BTLEException as err:
	    print 'Error writing char %s' % str(err)
	    self.p.disconnect()

    def currentTime(self):
	current = datetime.datetime.now()
	time_comm = struct.pack('11B', int(str(current.year)[-2:]), current.month, current.day, current.hour, current.minute, current.second, 0x00, 0x06, 0x40, 0x00, 0x1E)
	return time_comm

   

class TestBLEDelegate(DefaultDelegate):
    def __init__(self):
	DefaultDelegate.__init__(self)
	self.data = 0
	self.handle = 'unknown'

    def handleNotification(self, cHandle, data):
	self.data = data
	print('handleNotification')
	print len(data)
	if cHandle == 0x0036:
	    self.data = struct.unpack('<20B', data)
	    self.handle = 'e1'
	elif cHandle == 0x002e:
	    self.data = struct.unpack('<B', data)
	    self.handle = 'f4'
	elif cHandle == 0x003d:
	    self.data = struct.unpack('<2B', data)
	    self.handle =  'e3'
	elif cHandle == 0x0041:
	    self.data = struct.unpack('<8B', data)
	    self.handle = 'e4'
	else:
	    self.handle = 'other'
	    print 'other handle'
        print 'handle ', cHandle, ' ', self.handle, ' ', data
try:
    print('connecting fd')
    fd = FineDust('20:91:48:43:AE:FD')
    for i in range(10):
	result = fd.get_data()
	print('handle: ', result['handle'], ' data: ', result['data']) 
except Exception as e:
    print ('Error in main %s' % str(e))
else:
    print('disconnect')
#    fd.disconnect()
