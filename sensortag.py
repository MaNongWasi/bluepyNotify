from btle import UUID, Peripheral, DefaultDelegate, BTLEException
import struct
import datetime


class FineDust():
    def __init__(self, addr):
	self.p = Peripheral(addr)
	self.bleDelegate = TestBLEDelegate()
	self.p.setDelegate(self.bleDelegate)
	print ('enable Notification')
	self.enableNotification()	

    def get_data(self):
	self.p.waitForNotifications(2.0)
	print ('wait for notification')
	return self.bleDelegate.data

    def disconnect(self):
	self.p.disconnect()

    def enableNotification(self):
	try:
	    print ('write F1 start comm')
	    self.p.writeCharacteristic(0x0034, '\x07')
	    print ('write F3')
	    self.p.writeCharacteristic(0x0031, '\x01\x00')
	    print ('write F1 datetime')
	except BTLEException as err:
	    print 'Error writing char %s' % str(err)
	    self.p.disconnect()

class TestBLEDelegate(DefaultDelegate):
    def __init__(self):
	DefaultDelegate.__init__(self)
	self.data = 0

    def handleNotification(self, cHandle, data):
	self.data = data
	print('handleNotification')
	print('handler', cHandle)
	print(data)
	if cHandle == 0x0030:
	    print 'handler 30'
	else:
	    print 'other handler'

try:
    print('connecting sensortag')
    fd = FineDust('B4:99:4C:64:B2:3D')
    for i in range(10):
	print('data')
	print(fd.get_data())
#        print('data ' + fd.get_data())
except Exception as e:
    print ('Error in main %s' % str(e))
else:
    print('disconnect')
#    fd.disconnect()
