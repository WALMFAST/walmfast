import platform
import os

def get_devices_adb():

	try:
		os.remove('device.txt')
	except:
		pass

	command = ''

	if platform.system() == 'Linux':
		command = os.system('adb devices > devices.txt')
	elif platform.system() == 'Windows':
		command = os.system('platform-tools-windows\\platform-tools\\adb devices > devices.txt ')

	if command != 0:
		print(f'Error receiving devices')
		return False

	device_txt = open('devices.txt', 'r+').read()
	result = device_txt.split('\n')

	devices = result[1:]
	devices = [devices.replace('\tdevice', '') for devices in devices]

	if devices[0] == '':
		return None
	else:
		return devices[0]
		
def get_devices_fastboot():

	try:
		os.remove('device.txt')
	except:
		pass

	command = ''

	if platform.system() == 'Linux':
		command = os.system('fastboot devices > devices.txt')
	elif platform.system() == 'Windows':
		command = os.system('platform-tools-windows\\platform-tools\\fastboot devices > devices.txt ')

	if command != 0:
		print(f'Error receiving devices')
		return False

	device_txt = open('devices.txt', 'r+').read()
	devices = device_txt[0:16]

	if devices == '':
		return None
	else:
		return devices
	
def partitions_is_true(path, vendor_parti):
	partioion_true = []

	for i in vendor_parti:
		if os.path.isfile(f'{path}/images/{i}') == True:
			partioion_true.append(i)
		else:
			continue

	return partioion_true