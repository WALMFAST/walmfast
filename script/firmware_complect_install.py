import wget
import os
import platform
from script import imageload
from settings import window_and_objects as winaobj
import shutil

distr = ''

def detect_system():
    global distr
    if platform.system() == 'Linux':
        if platform.freedesktop_os_release()['ID_LIKE'] == 'arch':
            distr = [imageload.arch, 'arch']
        elif platform.freedesktop_os_release()['ID_LIKE'] == 'debian' or platform.freedesktop_os_release()['ID_LIKE'] == 'ubuntu debian' or platform.freedesktop_os_release()['ID_LIKE'] == 'ubuntu':
            distr = [imageload.debian, 'debian']
        elif platform.freedesktop_os_release()['ID_LIKE'] == '':
            if os.system('apt list') == 0:
                distr = [imageload.debian, 'debian']
            elif os.system('pacman -Q') == 0:
                distr = [imageload.arch, 'arch']
            else:
                distr = [imageload.tux, 'no support'] 
        else:
            distr = [imageload.tux, 'no support']
    elif platform.system() == 'Windows':
        distr = [imageload.windows, 'windows']
    else:
        distr = [imageload.install_firmware_complect, 'no support']
    return distr

def install_complect_firmware(system):

    if system == 'arch':
        try:
            os.system('pkexec pacman -Sy --noconfirm android-tools protobuf')
            return True
        except:
            return False
    elif system == 'debian':
        try:
            os.system('pkexec apt update && pkexec apt install android-tools-adb android-tools-fastboot')
            return True
        except:
            return False
    elif system == 'windows':
        try:
            if os.path.isdir('platform-tools-windows') == True: 
                pass 
            else: 
                os.mkdir('platform-tools-windows')
            if os.path.isdir('platform-tools-windows/platform-tools'): 
                pass
            #install adb driver
            wget.download(winaobj.WINDOWS_PLATFORM_DRIVER, 'platform-tools-windows/Driver_Auto_Installer_EXE_v5.1632.00.zip')
            shutil.unpack_archive('platform-tools-windows/Driver_Auto_Installer_EXE_v5.1632.00.zip', 'platform-tools-windows/')
            os.system('platform-tools-windows\Driver_Auto_Installer_SP_Drivers_20160804\DriverInstall.exe')
            shutil.rmtree('platform-tools-windows\Driver_Auto_Installer_SP_Drivers_20160804')
            os.remove('platform-tools-windows\Driver_Auto_Installer_EXE_v5.1632.00.zip')
            #download and unpack platform-tools    
            wget.download(winaobj.WINDOWS_PLATFROM_URL, 'platform-tools-windows/platform-tools-latest-windows.zip')
            shutil.unpack_archive('platform-tools-windows/platform-tools-latest-windows.zip', 'platform-tools-windows/')
            os.remove('platform-tools-windows/platform-tools-latest-windows.zip')
            return True
        except:
            return False
    elif system == 'no support':
        return False

