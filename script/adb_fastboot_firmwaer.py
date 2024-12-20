import platform
import os
import shutil

def init():
	print('Initialization adb/fastboot module')
	if os.path.isdir('infolog') == False:
		os.mkdir('infolog')
	else:
		pass

	if os.path.isdir('partitions') == False:
		os.mkdir('partitions')
	else:
		pass

	if os.path.isdir('music') == False:
		os.mkdir('music')
	else:
		pass

	if os.path.isdir('partitions/system') == False:
		os.mkdir('partitions/system')
	else:
		pass

	if os.path.isdir('partitions/recovery') == False:
		os.mkdir('partitions/recovery')
	else:
		pass
	
	if os.path.isdir('partitions/vbmeta') == False:
		os.mkdir('partitions/vbmeta')
	else:
		pass

	try:
		for file in os.listdir('infolog'):
			os.remove(file)
	except:
		pass
	
	print('Initialization module is OK')
	return True

def get_devices_adb():

	try:
		os.remove('infolog/device.txt')
	except:
		pass

	command = ''

	if platform.system() == 'Linux':
		command = os.system('adb devices > infolog/devices.txt')
	elif platform.system() == 'Windows':
		command = os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\adb devices > infolog\devices.txt ')

	if command != 0:
		print(f'Error receiving devices')
		return False

	device_txt = open('infolog/devices.txt', 'r+').read()
	result = device_txt.split('\n')

	devices = result[1:]
	devices = [devices.replace('\tdevice', '') for devices in devices]

	if devices[0] == '':
		return None
	else:
		return devices[0][0:16]
		
def get_devices_fastboot():

	try:
		os.remove('infolog/devices.txt')
	except:
		pass

	command = ''

	if platform.system() == 'Linux':
		command = os.system('fastboot devices > infolog/devices.txt')
	elif platform.system() == 'Windows':
		command = os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot devices > infolog\\devices.txt')

	if command != 0:
		print(f'Error receiving devices')
		return False

	device_txt = open('infolog/devices.txt', 'r+').read()
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

def reboot_phone(system, into):
    
	if platform.system() == 'Linux':
		try:
			if into == 'system':
				if os.system(f'{system} reboot') == 0:
					return True
				else:
					return False
			else:
				if os.system(f'{system} reboot {into}') == 0:
					return True
				else:
					return False
		except:
			return False
	elif platform.system() == 'Windows':
		try:
			if into == 'system':
				if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\{system} reboot') == 0:
					return True
				else:
					return False
			else:
				if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\{system} reboot {into}') == 0:
					return True
				else:
					return False
		except:
			return False
	else:
		return False

def status_unlock():

	try:
		os.remove('infolog/unlock.txt')
	except:
		pass

	command = ''

	if platform.system() == 'Linux':
		command = os.system('fastboot getvar unlocked 2> infolog/unlock.txt')
	elif platform.system() == 'Windows':
		command = os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot getvar unlocked 2> infolog\\unlock.txt')

	if command != 0:
		print(f'Error receiving unlock')
		return False
	
	unlock_txt = open('infolog/unlock.txt', 'r+').read()
	unlock = unlock_txt.split('\n')[0][10:]

	return unlock

def flash_partition(partition, file):

	try:
		shutil.copyfile(file, f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
	except:
		return False

	try:
		os.remove('infolog/partition.txt')
	except:
		pass
    
	if platform.system() == 'Linux':
		try:
			if os.system(f'fastboot flash {partition} partitions/recovery/{os.path.basename(file)} 2> infolog/partition.txt') == 0:
				os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
				return True
			else:
				os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
		except:
			os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
	elif platform.system() == 'Windows':
		try:
			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot flash {partition} partitions\\recovery\\{os.path.basename(file)} 2> infolog\\partition.txt') == 0:
				os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
				return True
			else:
				os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
		except:
			os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')
	else:
		os.remove(f'{os.getcwd()}/partitions/recovery/{os.path.basename(file)}')

def flash_system(partition, file):

	try:
		shutil.copyfile(file, f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
	except:
		return False

	try:
		os.remove('infolog/partition.txt')
	except:
		pass
    
	if platform.system() == 'Linux':
		try:
			if os.system(f'fastboot flash {partition} partitions/system/{os.path.basename(file)} 2> infolog/partition.txt') == 0:
				os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
				return True
			else:
				os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
		except:
			os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
	elif platform.system() == 'Windows':
		try:
			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot flash {partition} partitions\\system\\{os.path.basename(file)} 2> infolog\\partition.txt') == 0:
				os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
				return True
			else:
				os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
		except:
			os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')
	else:
		os.remove(f'{os.getcwd()}/partitions/system/{os.path.basename(file)}')

def flash_vbmeta(partition, file):

	try:
		shutil.copyfile(file, f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
	except:
		return False

	try:
		os.remove('infolog/partition.txt')
	except:
		pass
    
	if platform.system() == 'Linux':
		try:
			if os.system('fastboot oem cdms') == 0:
				print('OEM CDMS is worked')
			else:
				print('OEM CDMS is not worked')

			if os.system(f'fastboot --disable-verity --disable-verification flash {partition} partitions/vbmeta/{os.path.basename(file)} 2> infolog/partition.txt') == 0:
				os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
				return True
			else:
				os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
		except:
			os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
	elif platform.system() == 'Windows':
		try:
			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot oem cdms') == 0:
				print('OEM CDMS is worked')
			else:
				print('OEM CDMS is not worked')

			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot --disable-verity --disable-verification flash {partition} partitions\\vbmeta\\{os.path.basename(file)} 2> infolog\\partition.txt') == 0:
				os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
				return True
			else:
				os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
		except:
			os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
	else:
		os.remove(f'{os.getcwd()}/partitions/vbmeta/{os.path.basename(file)}')
