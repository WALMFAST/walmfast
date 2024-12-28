import platform
import os
import shutil
import getpass
from settings import window_and_objects as winaobj

rootfs = os.getcwd()

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

	if platform.system() == 'Linux':
		if os.path.isfile(f'/home/{getpass.getuser()}/.fonts/{winaobj.FONT[4:]}') == False:
			shutil.copyfile(winaobj.FONT, f'/home/{getpass.getuser()}/.fonts/{winaobj.FONT[4:]}')
		else:
			pass

	if os.path.isdir('update') == False:
		os.mkdir('update')
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
	print(vendor_parti)

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
				if os.system(f'adb kill-server') == 0:
					if os.system(f'{system} reboot') == 0:
						return True
					else:
						return False
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

def sideload(file):

	if platform.system() == 'Linux':
		try:
			if os.system(f'adb sideload {file} 2> infolog/partition.txt') == 0:
				return True
			else:
				return False
		except:
			return False
	elif platform.system() == 'Windows':
		try:
			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\adb sideload {file} 2> infolog/partition.txt') == 0:
				return True
			else:
				return False
		except:
			return False
		
def get_slot():

	try:
		os.remove('infolog/slot.txt')
	except:
		pass

	command = ''

	if platform.system() == 'Linux':
		command = os.system('fastboot getvar current-slot 2> infolog/slot.txt')
	elif platform.system() == 'Windows':
		command = os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot getvar current-slot 2> infolog\\slot.txt')

	if command != 0:
		print(f'Error receiving slot')
		return False
	
	slot_txt = open('infolog/slot.txt', 'r+').read()
	slot = slot_txt.split('\n')[0][14:]
	
	return slot

def wipe_data():

	if platform.system() == 'Linux':
		try:
			if os.system(f'fastboot -w 2> infolog/partition.txt') == 0:
				if os.system(f'fastboot reboot recovery 2> infolog/partition.txt') == 0:
					return True
				else:
					return False
			else:
				return False
		except:
			return False
	elif platform.system() == 'Windows':
		try:
			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot -w  2> infolog/partition.txt') == 0:
				if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot reboot recovery 2> infolog/partition.txt') == 0:
					return True
				else:
					return False
			else:
				return False
		except:
			return False
		
def delete_product():

	if platform.system() == 'Linux':
		try:
			if os.system(f'fastboot delete-logical-partition product_{get_slot()} 2> infolog/partition.txt') == 0:
				return True
			else:
				return False
		except:
			return False
	elif platform.system() == 'Windows':
		try:
			if os.system(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\fastboot delete-logical-partition product_{get_slot()} 2> infolog/partition.txt') == 0:
				return True
			else:
				return False
		except:
			return False
		
def flash_all(firmware_path):
	global rootfs
	if platform.system() == 'Linux':
		try:
			
			os.chdir(firmware_path)
			if os.system(f'./flash_all.sh 2> {rootfs}/infolog/partition.txt') == 0:
				os.chdir(rootfs)
				return True
			else:
				os.chdir(rootfs)
				return False
		except:
			os.chdir(rootfs)
			return False
	elif platform.system() == 'Windows':
		print('Step 1 - verity fastboot files in firmware path')

		rootfs = os.getcwd()
		for i in os.listdir(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\'):
			if os.path.isfile(f'{firmware_path}/{i}') == True:
				continue
			else:
				shutil.copyfile(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\{i}', fr'{firmware_path}\\{i}')

		print('Step 2 - flash all')

		try:
			os.chdir(firmware_path)
			if os.system(fr'flash_all 2> {rootfs}/infolog/partition.txt') == 0:
				os.chdir(rootfs)
				return True
			else:
				os.chdir(rootfs)
				return False
		except:
			os.chdir(rootfs)
			return False

def flash_partition_images(firmware_path, group):
	global rootfs
	if platform.system() == 'Linux':
		try:
			os.chdir(f'{firmware_path}/images/')
			try:
				os.remove(f'{rootfs}/infolog/partition.txt')
			except:
				pass
			for i in group:
				if len(i) == 9 or len(i) > 9: 
					preloader_check = i[:9]
					if preloader_check == 'preloader':
						if os.system(f'fastboot flash preloader {i} 2>> {rootfs}/infolog/partition.txt') == 0:
							continue
						else:
							os.chdir(rootfs)
							return False
					else:
						if os.system(f'fastboot flash {i[:-4]} {i} 2>> {rootfs}/infolog/partition.txt') == 0:
							continue
						else:
							os.chdir(rootfs)
							return False
				else:
						if os.system(f'fastboot flash {i[:-4]} {i} 2>> {rootfs}/infolog/partition.txt') == 0:
							continue
						else:
							os.chdir(rootfs)
							return False
			os.chdir(rootfs)
		except:
			os.chdir(rootfs)
			return False
	elif platform.system() == 'Windows':
		print('Step 1 - verity fastboot files in firmware path')

		rootfs = os.getcwd()
		for i in os.listdir(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\'):
			if os.path.isfile(f'{firmware_path}/images{i}') == True:
				continue
			else:
				shutil.copyfile(fr'{os.getcwd()}\\platform-tools-windows\\platform-tools\\{i}', fr'{firmware_path}\\images\\{i}')

		print('Step 2 - flash all')

		try:
			os.chdir(f'{firmware_path}/images/')
			try:
				os.remove(f'{rootfs}/infolog/partition.txt')
			except:
				pass
			for i in group:
				if len(i) == 9 or len(i) > 9: 
					preloader_check = i[:9]
					if preloader_check == 'preloader':
						if os.system(f'fastboot flash preloader {i} 2>> {rootfs}/infolog/partition.txt') == 0:
							continue
						else:
							os.chdir(rootfs)
							return False
					else:
						if os.system(f'fastboot flash {i[:-4]} {i} 2>> {rootfs}/infolog/partition.txt') == 0:
							continue
						else:
							os.chdir(rootfs)
							return False
				else:
						if os.system(f'fastboot flash {i[:-4]} {i} 2>> {rootfs}/infolog/partition.txt') == 0:
							continue
						else:
							os.chdir(rootfs)
							return False
			os.chdir(rootfs)
		except:
			os.chdir(rootfs)
			return False