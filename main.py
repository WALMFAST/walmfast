from customtkinter import *
from settings import selector
from settings import window_and_objects as winaobj
from showinfm import show_in_file_manager
from time import sleep

import importlib
import crossfiledialog
import webbrowser
import xdialog
import platform

if selector.select_languages == 'rus':
    from languages import rus as lang

des = CTk()
des.title(f"WALM Fastboot - {lang.fastboot_flash_firmware}")
des.geometry(winaobj.WINDOW_SIZE)
des.resizable(False, False)

if platform.system() == 'Linux':
    FontManager.load_font(winaobj.FONT)
elif platform.system() == 'Windows':
    from pyglet import options, font
    options['win32_gdi_font'] = True
    font.add_file(f"{os.getcwd()}/{winaobj.FONT}")


from script import imageload
from script import musicplayer
from script import firmware_complect_install as firm_comp_install
from script import adb_fastboot_firmwaer as ad_fas_firm

#Functions
def menu_firmware():
    base_frame.place_forget()
    reboot_menu_frame.place_forget()
    phone_status_frame.place_forget()

    music_name_log_read = open('infolog/musicname.txt', 'r')
    music_name.configure(text=music_name_log_read.read())
    music_name_log_read.close()

    menu_frame.place(x=0,y=0)
def menu_base():
    menu_frame.place_forget()
    reboot_menu_frame.place_forget()
    phone_status_frame.place_forget()
    phone_status_frame.place_forget()
    gsi_menu_frame.place_forget()
    about_menu_frame.place_forget()
    base_frame.place(x=0, y=0)
def menu_phone_status():
    menu_frame.place_forget()
    phone_status_frame.place(x=0,y=0)
def menu_gsi():
    menu_frame.place_forget()
    gsi_menu_frame.place(x=0,y=0)
def menu_about():
    menu_frame.place_forget()
    about_menu_frame.place(x=0,y=0)
def firmware_complect_installer():
    global distr
    base_frame.place_forget()
    firmware_complect_installer_frame.place(x=0, y=0)
    des.update()
    
    sleep(1)

    if distr[1] == 'arch' or distr[1] == 'debian' or distr[1] == 'windows':
        haderfirm.configure(text=lang.installation_firmware_complect)
    elif distr[1] == 'no_support':
        haderfirm.configure(text=lang.back_installation_firmware_complect)

    
    des.update()

    sleep(1.5)

    if firm_comp_install.install_complect_firmware(distr[1]) == True:
        haderfirm.configure(text=lang.installation_firmware_complect_is_done)
        des.update()
    elif firm_comp_install.install_complect_firmware(distr[1]) == False:
        haderfirm.configure(text=lang.installation_firmware_complect_is_fail)
        des.update()

        sleep(1.5)

        firmware_complect_installer_frame.place_forget()
        base_frame.place(x=0,y=0)

        return False
    
    progressbar.configure(mode='determinate')
    progressbar.set(1)

    des.update()
    
    sleep(1.5)

    firmware_complect_installer_frame.place_forget()
    base_frame.place(x=0,y=0)

    return True
def reboot_menu():
    progressbar_re.place_forget()
    base_frame.place_configure()
    reboot_menu_frame.place(x=0,y=0)
def reboot_through(system, into):

    progressbar_re.place(x=100, y = 200)

    hader_re.configure(text=lang.reboot)
    reboot_through_adb.place_forget()
    reboot_through_fastboot.place_forget()
    des.update()

    if firm_comp_install.reboot_phone(system, into) == True:
        hader_re.configure(text=lang.reboot_is_done)
        des.update()
        sleep(1.5)
        hader_re.place_forget()
        firmwares_frame.place(x=285,y=131)
        menu_base()
    elif firm_comp_install.reboot_phone(system, into) == False:
        hader_re.configure(text=lang.reboot_is_fail)
        des.update()
        sleep(1.5)
        hader_re.place_forget()
        firmwares_frame.place(x=285,y=131)
        menu_base()
def reboot_phone_through(into):

    progressbar_re.place_forget()
    hader_re.configure(text=f'{lang.reboot_through}')
    
    reboot_through_adb.configure(command=lambda: reboot_through('adb', into))
    reboot_through_fastboot.configure(command=lambda: reboot_through('fastboot', into))

    firmwares_frame.place_forget()
    hader_re.place(x=240, y=100)
    reboot_through_adb.place(x=300, y=200)
    reboot_through_fastboot.place(x=500, y=202)
def phone_test_state(mode):

    if mode == 'adb':
        if ad_fas_firm.get_devices_adb() == None or ad_fas_firm.get_devices_adb() == False:
            android_phone_status.configure(text=lang.not_found)
            android_phone_status.place(x=55, y=370)
        else:
            android_phone_status.configure(text=ad_fas_firm.get_devices_adb(), font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM))
            android_phone_status.place(x=33, y=370)
    if mode == 'fastboot':
        if ad_fas_firm.get_devices_fastboot() == None or ad_fas_firm.get_devices_fastboot() == False:
            android_phone_status.configure(text=lang.not_found)
            android_phone_status.place(x=55, y=370)
        else:
            android_phone_status.configure(text=ad_fas_firm.get_devices_fastboot(), font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM))
            android_phone_status.place(x=33, y=370)

    if android_phone_status._text == lang.not_found:
        pass
    elif android_phone_status._text != lang.not_found:
        if phone_vendor_model._text == lang.model_device:
            pass
        elif phone_vendor_model._text != lang.model_device:
            gsi_menu_button.configure(state='normal')
            phone_reboot_button.configure(state='normal')
            flash_phone_button.configure(state='normal')

    des.update()
    menu_base()
def load_phone_vendor():
    global vendorvice

    try:
        phone_vendor = crossfiledialog.open_file(title='Open phone vendor file for WALMFAST', start_dir=f'{os.getcwd()}/{winaobj.PHONE_VENDOR_PATH}/', filter=["*.py"])
        vendorid = str(os.path.basename(phone_vendor))[:-3]
        vendorvice = importlib.import_module(name=f'.{vendorid}.{vendorid}', package=f'{winaobj.PHONE_VENDOR_PATH}')

        try:
            importlib.reload(vendorvice)
        except:
            pass

        phone_vendor_model.configure(text=vendorvice.model)
        icon = imageload.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/icon.png')
        des.iconphoto(False, icon)

        try:
            android.configure(image=imageload.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/{vendorvice.image}'))
        except:
            android.configure(image=imageload.android)

        select_firmware_folder_button.configure(state='normal')
        des.update()
    except:
       pass
def load_firmware_folder():
    global vendorvice

    phone_vendor = crossfiledialog.choose_folder(title='Open firmware folder for WALMFAST', start_dir=f'{os.getcwd()}/')

    try:
        partitions = ad_fas_firm.partitions_is_true(phone_vendor, vendorvice.partitions) 
        for partition in partitions:
                image_partition = CTkCheckBox(firmware_image_frame, text=partition, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), hover_color='grey', corner_radius=2, border_color='white',text_color='white' ,fg_color='black')
                image_partition.pack(anchor=W)  
    except:
        xdialog.error('WALMFast', f'{lang.phone_config_error}')

    des.update()

#Graphics

#Base Entity
background = CTkLabel(des, image=imageload.background, text='')
background.place(x=1, y=1)

#Entity 1
base_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
base_frame.place(x=0,y=0)

can = CTkCanvas(base_frame, width = winaobj.WIDTH, height = winaobj.WIDTH)
can.place(x=-1, y=-1)

background = CTkLabel(can, image=imageload.background, text='')
background.place(x=1, y=1)

frame = CTkLabel(can, image=imageload.frame, text='')
frame.place(x=20, y=20)

android = CTkLabel(can, image=imageload.android, text='')
android.place(x=60, y=70)

android_phone_status = CTkLabel(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.not_found}', text_color='white', bg_color='black')
android_phone_status.place(x=55, y=370)

phone_vendor_model = CTkLabel(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.model_device}', text_color='white', bg_color='black')
phone_vendor_model.place(x=20, y=467)

exit_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), height=45, text=f'{lang.exit}', text_color='white', corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: os._exit(0))
exit_button.place(x=800,y=467)

about_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), height=45, text=f'{lang.about}',text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_about)
about_button.place(x=650,y=467)

select_phone_model_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.select_phone_model}',text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=load_phone_vendor)
select_phone_model_button.place(x=385,y=25)

test_state_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.test_state}',text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_phone_status)
test_state_button.place(x=695,y=73)

gsi_menu_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.gsi_boot_enabler}', text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, state='disabled', command=menu_gsi)
gsi_menu_button.place(x=740, y=25)

menu_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text='', width=25, height=25, image=imageload.menu,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_firmware)
menu_button.place(x=695, y=25)

firmware_image_frame = CTkScrollableFrame(base_frame, width=230, height=380, bg_color='black', fg_color='black', corner_radius=3, border_color='white', border_width=2, scrollbar_button_color='white', scrollbar_button_hover_color='white', scrollbar_fg_color="black")
firmware_image_frame.place(x=385,y=73)

select_firmware_folder_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.select_firmware_folder}',text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, state='disabled', command=load_firmware_folder)
select_firmware_folder_button.place(x=385,y=470)

phone_reboot_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.phone_reboot}',text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, state='disabled', command=reboot_menu)
phone_reboot_button.place(x=695,y=373)

flash_phone_button = CTkButton(can, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.flash_device}',text_color='white',corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, state='disabled')
flash_phone_button.place(x=695,y=420)

#Entity 2
menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
menu_frame.place(x=0,y=0)

background = CTkLabel(menu_frame, image=imageload.background, text='')
background.place(x=1, y=1)

music_name = CTkLabel(menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'name of music', text_color='#212020', bg_color='black', wraplength=950,justify=LEFT)
music_name.place(x=5, y=370)

firmwares_frame = CTkFrame(menu_frame, width=380, height=250, bg_color='black', fg_color='black', corner_radius=3, border_color='white', border_width=2)
firmwares_frame.place(x=285,y=103)

volume_on_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.volume_on, text_color='white', image=imageload.volume_on,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: musicplayer.volume_on())
volume_on_button.place(x=30, y=10)

volume_off_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.volume_off, text_color='white', image=imageload.volume_off,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: musicplayer.volume_off())
volume_off_button.place(x=190, y=10)

close_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color='white', image=imageload.close,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_base)
close_button.place(x=115, y=200)

location_music_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.location_music, text_color='white', image=imageload.location_music,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: show_in_file_manager(f'{os.getcwd()}/music/'))
location_music_button.place(x=45, y=70)

install_firmware_complect_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.install_firmware_complect, text_color='white', image=imageload.install_firmware_complect,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=firmware_complect_installer)
install_firmware_complect_button.place(x=10, y=130)

#Entity 4 - Installer Firmware Complect
firmware_complect_installer_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
firmware_complect_installer_frame.place(x=0,y=0)

background = CTkLabel(firmware_complect_installer_frame, image=imageload.background, text='')
background.place(x=1, y=1)

distr=firm_comp_install.detect_system()

haderfirm = CTkLabel(firmware_complect_installer_frame, image=distr[0], font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.detect_operating_system}', text_color='white', compound='left', bg_color='black')
haderfirm.place(x=100, y=100)

progressbar = CTkProgressBar(firmware_complect_installer_frame, width=750, height=20, corner_radius=2, bg_color='black', fg_color='black', border_color='white', border_width=2, progress_color='white',mode='indeterminate', indeterminate_speed=5 )
progressbar.place(x=100, y = 200)
progressbar.start()

#Entity 5 - Reboot device
reboot_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
reboot_menu_frame.place(x=0,y=0)

background = CTkLabel(reboot_menu_frame, image=imageload.background, text='')
background.place(x=1, y=1)

firmwares_frame = CTkFrame(reboot_menu_frame, width=380, height=200, bg_color='black', fg_color='black', corner_radius=3, border_color='white', border_width=2)
firmwares_frame.place(x=285,y=131)

close_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color='white', image=imageload.close,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_base)
close_button.place(x=115, y=150)

reboot_into_recovery = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_recovery, text_color='white', image=imageload.recovery,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: reboot_phone_through('recovery'))
reboot_into_recovery.place(x=32, y=20)

reboot_into_bootloader = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_bootloader, text_color='white', image=imageload.bootloader,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: reboot_phone_through('bootloader'))
reboot_into_bootloader.place(x=202, y=20)

reboot_into_fastbootd = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_fastboot, text_color='white', image=imageload.fastbootd,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: reboot_phone_through('fastboot'))
reboot_into_fastbootd.place(x=32, y=80)

reboot_into_system = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_system, text_color='white', image=imageload.system,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: reboot_phone_through(''))
reboot_into_system.place(x=202, y=80)

hader_re = CTkLabel(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.reboot_through}', text_color='white', bg_color='black')

reboot_through_adb = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.adb, text_color='white', image=imageload.adb,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)

reboot_through_fastboot = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.fastboot, text_color='white', image=imageload.bootloader,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)

progressbar_re = CTkProgressBar(reboot_menu_frame, width=750, height=20, corner_radius=2, bg_color='black', fg_color='black', border_color='white', border_width=2, progress_color='white',mode='indeterminate', indeterminate_speed=5 )
progressbar_re.start()

#Entity 6 - Phone status through
phone_status_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
phone_status_frame.place(x=0,y=0)

background = CTkLabel(phone_status_frame, image=imageload.background, text='')
background.place(x=1, y=1)

phone_status_through_adb = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.adb, text_color='white', image=imageload.adb,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: phone_test_state('adb'))

phone_status_through_fastboot = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.fastboot, text_color='white', image=imageload.bootloader,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: phone_test_state('fastboot'))

hader_state = CTkLabel(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.state_through}', text_color='white', bg_color='black')

close_button = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color='white', image=imageload.close,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_base)

close_button.place(x=400, y=250)
hader_state.place(x=160, y=100)
phone_status_through_adb.place(x=300, y=200)
phone_status_through_fastboot.place(x=500, y=202)

#Entity 7 GSI Menu
gsi_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
gsi_menu_frame.place(x=0,y=0)

background = CTkLabel(gsi_menu_frame, image=imageload.background, text='')
background.place(x=1, y=1)

close_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color='white', image=imageload.close,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_base)
close_button.place(x=795, y=470)

unlock_bootloader_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.unlock_bootloader, text_color='white', image=imageload.unlock_bootloader,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)
unlock_bootloader_button.place(x=100, y=110)

lock_bootloader_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.lock_bootloader, text_color='white', image=imageload.lock_bootloader,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)
lock_bootloader_button.place(x=100, y=165)

flash_custom_partition_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.flash_custom_partition, text_color='white', image=imageload.flash,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)
flash_custom_partition_button.place(x=100, y=220)

approve_custom_load_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.approve_custom_load, text_color='white', image=imageload.approve_custom_load,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)
approve_custom_load_button.place(x=100, y=275)

wipe_data_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.wipe_data, text_color='white', image=imageload.wipe_data,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)
wipe_data_button.place(x=100, y=330)

delete_product_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.delete_product, text_color='white', image=imageload.product,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2)
delete_product_button.place(x=100, y=385)

search_gsi_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.search_gsi, text_color='white', image=imageload.search_gsi,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=lambda: webbrowser.open_new_tab(winaobj.SEARCH_GSI_URL))
search_gsi_button.place(x=560, y=110)

#Entity 8 - About 
about_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')
about_menu_frame.place(x=0,y=0)

background = CTkLabel(about_menu_frame, image=imageload.background, text='')
background.place(x=1, y=1)

walmfast_logo = CTkLabel(about_menu_frame, image=imageload.logo, text='')
walmfast_logo.place(x=120, y=100)

program_name = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.program_name}', text_color='white', bg_color='black')
program_name.place(x=400, y=100)

model_branch = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{winaobj.VERSION} - {winaobj.BRANCH}', text_color='white', bg_color='black')
model_branch.place(x=400, y=150)

model_branch = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.made_by}', text_color='white', bg_color='black')
model_branch.place(x=400, y=200)

close_button = CTkButton(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color='white', image=imageload.close,corner_radius=2, bg_color='black', fg_color='black', hover_color='grey', border_color='white', border_width=2, command=menu_base)
close_button.place(x=400, y=250)

#Required actions
des.wm_protocol('WM_DELETE_WINDOW', lambda: os._exit(0))

#Startup
menu_frame.place_forget()
reboot_menu_frame.place_forget()
firmware_complect_installer_frame.place_forget()
phone_status_frame.place_forget()
gsi_menu_frame.place_forget()
about_menu_frame.place_forget()
des.mainloop()