import showinfm.showinfm
from script import adb_fastboot_firmwaer_b as ad_fas_firm
from script import updater, ascii
from threading import Thread
ad_fas_firm.init()

from customtkinter import *
from settings import selector_b
from settings import window_and_objects_b as winaobj
from functools import partial
from showinfm import show_in_file_manager
from time import sleep

import importlib
import crossfiledialog
import webbrowser
import xdialog
import platform
import fileinput

if selector_b.select_languages == 'rus':
    from languages import rus as lang
elif selector_b.select_languages == 'eng':
    from languages import eng as lang

des = CTk()
des.title(f"WALM Fastboot - {lang.fastboot_flash_firmware}")
des.geometry(f'{winaobj.WIDTH}x{winaobj.HEIGHT}')
des.resizable(False, False)

from script import imageload_b
from script import musicplayer
from script import firmware_complect_install as firm_comp_install

#System fix
rootfs = os.getcwd()
status_update=None
partition_group = []
debug_mode = 0
phone_vendor = None
if platform.system() == 'Linux':
    FontManager.load_font(winaobj.FONT)
elif platform.system() == 'Windows':
    winaobj.FONT_NAME = 'Segoe UI'

try:
    argument_mode = sys.argv[1]
except:
    argument_mode = None

if argument_mode == '--debug-mode' or argument_mode == '--debug':
    debug_mode = 1
elif argument_mode == None:
    pass

themer = importlib.import_module(name=f'.{selector_b.theme}.{selector_b.theme}', package='image')

bg = themer.bg
bg1 = themer.bg1
fg = themer.fg
border = themer.border
text = themer.text
hover = themer.hover
scrollable = themer.scrollable
scrollbar_fg = themer.scrollbar_fg

#For flash
flash_all_status = IntVar(value=1)

os.chdir(rootfs)

#Functions
def menu_firmware():
    base_frame.place_forget()
    reboot_menu_frame.place_forget()
    phone_status_frame.place_forget()

    try:
        music_name_log_read = open('infolog/musicname.txt', 'r', encoding="utf-8")
        music_name = music_name_log_read.read()
        music_name_log_read.close()
        get_music_name_button.configure(command = lambda: xdialog.info('WALMFAST', message=music_name))
    except:
        get_music_name_button.configure(command = lambda: xdialog.info('WALMFAST', message=lang.get_music_name_error))

    menu_frame.place(x=0,y=0)
    des.update()
def menu_base():
    menu_frame.place_forget()
    reboot_menu_frame.place_forget()
    phone_status_frame.place_forget()
    phone_status_frame.place_forget()
    gsi_menu_frame.place_forget()
    about_menu_frame.place_forget()
    customboot_frame.place_forget()
    langswitcher_frame.place_forget()
    themeswitcher_frame.place_forget()
    donatos_frame.place_forget()
    gsi_frame.place_forget()
    vbmeta_frame.place_forget()
    update_frame.place_forget()
    adb_sideload_frame.place_forget()
    delete_product_frame.place_forget()
    wipe_data_frame.place_forget()
    flash_phone_frame.place_forget()
    sw_menu_frame.place_forget()
    base_frame.place(x=0, y=0)
def menu_phone_status():
    menu_frame.place_forget()
    phone_status_frame.place(x=0,y=0)
def langswitcher():
    menu_frame.place_forget()
    langswitcher_frame.place(x=0,y=0)
def themeswitcher():

    for themepath in os.listdir('image'):
        themebut = CTkButton(themes_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=themepath, width=360, height=45, text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: themeswitch(themepath))
        themebut.pack()

    menu_frame.place_forget()
    themeswitcher_frame.place(x=0,y=0)
def menu_gsi():
    menu_frame.place_forget()
    gsi_menu_frame.place(x=0,y=0)
def menu_sw():
    menu_frame.place_forget()
    sw_menu_frame.place(x=0,y=0)
def menu_about():
    menu_frame.place_forget()
    about_menu_frame.place(x=0,y=0)
def donatos():
    menu_frame.place_forget()
    donatos_frame.place(x=0,y=0)
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
    reboot_through_adb.place_forget()
    reboot_through_fastboot.place_forget()
    base_frame.place_configure()
    hader_re.place_forget()
    firmwares_frame.place(x=themer.firmwares_frame_position[0],y=themer.firmwares_frame_position[1])
    reboot_menu_frame.place(x=0,y=0)
def reboot_through(system, into):

    progressbar_re.place(x=themer.progressbar_re_position[0], y = themer.progressbar_re_position[1])
    hader_re.configure(text=lang.reboot)
    reboot_through_adb.place_forget()
    reboot_through_fastboot.place_forget()
    des.update()

    if ad_fas_firm.reboot_phone(system, into) == True:
        hader_re.configure(text=lang.reboot_is_done)
        des.update()
        sleep(1.5)
        hader_re.place_forget()
        firmwares_frame.place(x=285,y=131)
        menu_base()
    elif ad_fas_firm.reboot_phone(system, into) == False:
        hader_re.configure(text=lang.reboot_is_fail)
        des.update()
        sleep(1.5)
        hader_re.place_forget()
        firmwares_frame.place(x=285,y=131)
        menu_base()
def reboot_phone_through(into):
    hader_re.configure(text=f'{lang.reboot_through}')
    
    reboot_through_adb.configure(command=lambda: reboot_through('adb', into))
    reboot_through_fastboot.configure(command=lambda: reboot_through('fastboot', into))

    hader_re.place(x=themer.hader_re_position[0], y=themer.hader_re_position[1])
    reboot_through_adb.place(x=themer.reboot_through_adb[0], y=themer.reboot_through_adb[1])
    reboot_through_fastboot.place(x=themer.reboot_through_fastboot[0], y=themer.reboot_through_fastboot[1])
    progressbar_re.place_forget()
    firmwares_frame.place_forget()
def phone_test_state(mode):

    if mode == 'adb':
        if ad_fas_firm.get_devices_adb() == None or ad_fas_firm.get_devices_adb() == False:
            android_phone_status.configure(text=lang.not_found)
            xdialog.error('WALMFast', f'{lang.platorm_tools_error}')
        else:
            android_phone_status.configure(text=ad_fas_firm.get_devices_adb(), font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM))
            android_phone_status.place(x=33, y=370)
    if mode == 'fastboot':
        if ad_fas_firm.get_devices_fastboot() == None or ad_fas_firm.get_devices_fastboot() == False:
            android_phone_status.configure(text=lang.not_found, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART))
            xdialog.error('WALMFast', f'{lang.platorm_tools_error}')
        else:
            android_phone_status.configure(text=ad_fas_firm.get_devices_fastboot(), font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM))
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

    if platform.system() == 'Linux':
        try:
            phone_vendor = crossfiledialog.open_file(title='Open phone vendor file for WALMFAST', start_dir=f'{os.getcwd()}/{winaobj.PHONE_VENDOR_PATH}/', filter=["*.py"])

            vendorid = str(os.path.basename(phone_vendor))[:-3]
            vendorvice = importlib.import_module(name=f'.{vendorid}.{vendorid}', package=f'{winaobj.PHONE_VENDOR_PATH}')

            try:
                importlib.reload(vendorvice)
            except:
                pass

            phone_vendor_model.configure(text=vendorvice.model)
            icon = imageload_b.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/icon.png')
            des.iconphoto(False, icon)

            try:
                android.configure(image=imageload_b.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/{vendorvice.image}'))
            except:
                android.configure(image=imageload_b.android)

            forum_firmwares_forpda_button.configure(state='normal', command=lambda: webbrowser.open_new_tab(f'{vendorvice.official_firmwares_forum_forpda}'))
            select_firmware_folder_button.configure(state='normal')
            test_state_button.configure(state='normal')
            des.update()
        except:
            pass

        
    elif platform.system() == 'Windows':
        clear_flash() 

        phone_vendor = crossfiledialog.open_file(title='Open phone vendor file for WALMFAST', start_dir=f'{os.getcwd()}/{winaobj.PHONE_VENDOR_PATH}/', filter=["*.py"])
        vendorid = str(os.path.basename(phone_vendor))[:-3]
        vendorvice = importlib.import_module(name=f'.{vendorid}.{vendorid}', package=f'{winaobj.PHONE_VENDOR_PATH}')

        try:
            importlib.reload(vendorvice)
        except:
            pass

        os.chdir(rootfs)

        phone_vendor_model.configure(text=vendorvice.model)
        icon = imageload_b.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/icon.png')
        des.iconphoto(False, icon)

        try:
            android.configure(image=imageload_b.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/{vendorvice.image}'))
        except:
            android.configure(image=imageload_b.android)

        forum_firmwares_forpda_button.configure(state='normal', command=lambda: webbrowser.open_new_tab(f'{vendorvice.official_firmwares_forum_forpda}'))
        select_firmware_folder_button.configure(state='normal')
        test_state_button.configure(state='normal')
        des.update()       
def load_firmware_folder():
    global vendorvice, flash_all_status, partition_group, phone_vendor

    clear_flash() 

    phone_vendor = crossfiledialog.choose_folder(title='Open firmware folder for WALMFAST', start_dir=f'{os.getcwd()}')

    print('Load flash_all.sh or flash_all.bat')
    if platform.system() == 'Linux':
        if os.path.isfile(f'{phone_vendor}/flash_all.sh') == True:
            flash_all_radiobutton.pack(anchor=W)
            flash_all_radiobutton.select()
        else:
            flash_partitions_radiobutton.select()
    elif platform.system() == 'Windows':
        if os.path.isfile(f'{phone_vendor}/flash_all.bat') == True:
            flash_all_radiobutton.pack(anchor=W)
            flash_all_radiobutton.select()
        else:
            flash_partitions_radiobutton.select()
    
    print('Load partitions from phone config')
    try:
        partition_group.clear()
        partitions = ad_fas_firm.partitions_is_true(phone_vendor, vendorvice.partitions) 
        print(partitions)

        for partition in partitions:
            flash_object = CTkCheckBox(firmware_partition_frame, text=partition, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), hover_color='grey', corner_radius=6, border_color='white',text_color='white' ,fg_color='black')
            flash_object.configure(command=partial(parition_group_check, name=partition, check=flash_object))
            flash_object.pack(anchor=W)  

        flash_partitions_radiobutton.pack(anchor=W)
        flash_all_status_check()
    except:
        xdialog.error('WALMFast', f'{lang.phone_config_error}')

    if platform.system() == 'Windows':
        os.chdir(rootfs)

    des.update()
def customboot():
    
    try:
        if vendorvice.twrp != None or vendorvice.twrp != '':
            twrp_button.configure(command=lambda: webbrowser.open_new_tab(f'{vendorvice.twrp}'))
            twrp_button.place(x=195, y=470)
        else:
            twrp_button.place_forget()
    except:
        twrp_button.place_forget()

    try:
        if vendorvice.pbrp != None or vendorvice.pbrp != '':
            pbrp_button.configure(command=lambda: webbrowser.open_new_tab(f'{vendorvice.pbrp}'))
            pbrp_button.place(x=themer.pbrp_button_position[0], y=themer.pbrp_button_position[1])
        else:
            pbrp_button.place_forget()
    except:
        pbrp_button.place_forget()

    try:
        if vendorvice.orangefox != None or vendorvice.orangefox != '':
            orangefox_button.configure(command=lambda: webbrowser.open_new_tab(f'{vendorvice.orangefox}'))
            orangefox_button.place(x=themer.orangefox_button_position[0], y=themer.orangefox_button_position[1])
        else:
            orangefox_button.place_forget()
    except:
        orangefox_button.place_forget()

    try:
        if vendorvice.nonuniversalboot == True:
            flashit_partition_attetion.configure(text=lang.flashit_recovery_partition)
            flashit_partition_attetion.place(x=themer.flashit_partition_attetion_position[0], y=themer.flashit_partition_attetion_position[1])
        elif vendorvice.nonuniversalboot == False:
            flashit_partition_attetion.configure(text=lang.flashit_boot_partition)
            flashit_partition_attetion.place(x=themer.flashit_partition_attetion_position[0], y=themer.flashit_partition_attetion_position[1])
    except:
        flashit_partition_attetion.place_forget()

    recovery_path_textbox.place(x=40, y=250)
    select_recovery_button.place(x=themer.select_recovery_button_position[0], y=themer.select_recovery_button_position[1])
    menu_frame.place_forget()
    customboot_frame.place(x=0,y=0)
def select_recovery_image():
    global recovery_image

    recovery_image = crossfiledialog.open_file(title='Open recovery image file for WALMFAST', filter=["*.img"])
    if recovery_image != '':
        recovery_path_textbox.configure(text=os.path.basename(recovery_image))
        flash_recovery_button.place(x=themer.flash_recovery_button_position[0], y=themer.flash_recovery_button_position[1])
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def flash_recovery():
    flash_recovery_process_hader.configure(text=f'{lang.q_start_flash_recovery_process[0]}')
    recovery_yes_button.place(x=themer.recovery_yes_button_position[0], y=themer.recovery_yes_button_position[1])
    recovery_no_button.place(x=themer.recovery_no_button_position[0], y=themer.recovery_no_button_position[1])
    flash_recovery_process_hader.place(x=themer.flash_recovery_process_hader_position[0], y=themer.flash_recovery_process_hader_position[1])
    flash_recovery_button.place_forget()
    close_button.place_forget()
def start_flash_recovery(reboot):
    global gsi_image

    recovery_yes_button.place_forget()
    recovery_no_button.place_forget()

    if reboot == True:
        flash_recovery_process_hader.configure(text=lang.q_start_flash_recovery_process[1])
        des.update()
        ad_fas_firm.reboot_phone('adb', 'bootloader')
        sleep(15)

    flash_recovery_process_hader.configure(text=lang.q_start_flash_recovery_process[2])
    des.update()

    if ad_fas_firm.status_unlock() == 'no':
        xdialog.error('WALMFAST', lang.unlock_bootloader_error)
        close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
        flash_recovery_process_hader.place_forget()
        flash_recovery_button.place(x=themer.flash_recovery_button_position[0], y=themer.flash_recovery_button_position[1])
        menu_base()
    if ad_fas_firm.status_unlock() == 'yes':
        flash_recovery_process_hader.configure(text=lang.q_start_flash_recovery_process[3])
        if vendorvice.nonuniversalboot == False:
            universal_detect_boot = 'boot'
        elif vendorvice.nonuniversalboot == True:
            universal_detect_boot = 'recovery'
        else:
            universal_detect_boot = 'boot'
        if ad_fas_firm.flash_partition(partition=universal_detect_boot, file=recovery_image) == True:
            flash_recovery_process_hader.place_forget()
            xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
            close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
            menu_base()
        elif ad_fas_firm.flash_partition(partition=universal_detect_boot, file=recovery_image) == False:
            xdialog.error('WALMFAST', lang.q_start_flash_recovery_process[4])
            close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
            flash_recovery_process_hader.place_forget()
            flash_recovery_button.place(x=themer.flash_recovery_button_position[0], y=themer.flash_recovery_button_position[1])
            menu_base()    
def write_language(language):
    for line in fileinput.input('settings/selector_b.py', inplace=True):
        print(line.replace(f"select_languages = '{selector_b.select_languages}'", f"select_languages = '{language}'"), end='')

    xdialog.info('WALMFAST', lang.program_is_exit)
    os._exit(0)
def themeswitch(theme):
    for line in fileinput.input('settings/selector_b.py', inplace=True):
        print(line.replace(f"theme = '{selector_b.theme}'", f"theme = '{theme}'"), end='')

    xdialog.info('WALMFAST', lang.program_is_exit)
    os._exit(0)
def gsi_installer():
    menu_frame.place_forget()
    gsi_descryption.place_forget()
    gsi_name.place_forget()
    flash_gsi.place_forget()
    gsi_frame.place(x=0,y=0)
def select_gsi_image():
    global gsi_image

    gsi_image = crossfiledialog.open_file(title='Open gsi image file for WALMFAST', filter=["*.img"])
    if gsi_image != '':
        gsi_name.configure(text=f'{os.path.basename(gsi_image)}')
        gsi_name.place(x=themer.gsi_name_position[0], y=themer.gsi_name_position[1])
        des.update()
        flash_gsi.place(x=themer.flash_gsi_position[0], y=themer.flash_gsi_position[1])

        reboot_fastbotd_yes_button.place_forget()
        reboot_fastbotd_no_button.place_forget()
        flash_gsi_process_hader.place_forget()
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def flash_gsi_step_one():
    flash_gsi.place_forget()
    reboot_fastbotd_yes_button.place(x=themer.reboot_fastbotd_yes_button_position[0], y=themer.reboot_fastbotd_yes_button_position[1])
    reboot_fastbotd_no_button.place(x=themer.reboot_fastbotd_no_button_position[0], y=themer.reboot_fastbotd_no_button_position[1])
    flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[0]}')
    flash_gsi_process_hader.place(x=themer.flash_gsi_process_hader_position[0], y=themer.flash_gsi_process_hader_position[1])
def flash_gsi_step_two(reboot):
    reboot_fastbotd_yes_button.place_forget()
    reboot_fastbotd_no_button.place_forget()
    if reboot == True:
        flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[1]}')
        des.update()
        ad_fas_firm.reboot_phone('adb', 'fastboot')
        sleep(30)
    elif reboot == False:
        flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[2]}')
        des.update()
        sleep(15)

    flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[3]}')
    des.update()
    sleep(2)

    if ad_fas_firm.status_unlock() == 'no':
        xdialog.error('WALMFAST', lang.unlock_bootloader_error)
        close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
        flash_gsi.place(x=themer.flash_gsi_position[0], y=themer.flash_gsi_position[1])
        flash_gsi_process_hader.place_forget()
        menu_base()
    elif ad_fas_firm.status_unlock() == 'yes':
        flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[4]}')
        des.update()

        if ad_fas_firm.flash_system(partition='system', file=gsi_image) == True:
            flash_recovery_process_hader.place_forget()
            xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
            close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
            flash_gsi.place(x=themer.flash_gsi_position[0], y=themer.flash_gsi_position[1])
            des.update()
            menu_base()
        elif ad_fas_firm.flash_system(partition='system', file=gsi_image) == False:
            xdialog.error('WALMFAST', lang.gsi_process_hader[5])
            close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
            flash_gsi_process_hader.place_forget()
            flash_gsi.place(x=themer.flash_gsi_position[0], y=themer.flash_gsi_position[1])
            menu_base()
def vbmeta_installer():
    base_frame.place_forget()
    vbmeta_frame.place(x=0, y=0)
def select_vbmeta_image():
    global vbmeta_image
    vbmeta_image = crossfiledialog.open_file(title='Open gsi image file for WALMFAST', filter=["*.img"])
    if vbmeta_image != '' and os.path.basename(vbmeta_image) == 'vbmeta.img':
        vbmeta_name.configure(text=f'{os.path.basename(vbmeta_image)}')
        vbmeta_name.place(x=themer.vbmeta_name_position[0], y=themer.vbmeta_name_position[1])
        flash_vbmeta.place(x=themer.flash_vbmeta_position[0], y=themer.flash_vbmeta_position[1])
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def flash_vbmeta_step_one():
    flash_vbmeta.place_forget()
    reboot_fastbot_yes_button.place(x=themer.reboot_fastbot_yes_button_position[0], y=themer.reboot_fastbot_yes_button_position[1])
    reboot_fastbot_no_button.place(x=themer.reboot_fastbot_no_button_position[0], y=themer.reboot_fastbot_no_button_position[1])
    flash_vbmeta_process_hader.configure(text=f'{lang.vbmeta_process_hader[0]}')
    flash_vbmeta_process_hader.place(x=themer.flash_vbmeta_process_hader_position[0], y=themer.flash_vbmeta_process_hader_position[1])
def flash_vbmeta_step_two(reboot):
    reboot_fastbot_yes_button.place_forget()
    reboot_fastbot_no_button.place_forget()

    if reboot == True:
        flash_vbmeta_process_hader.configure(text=f'{lang.vbmeta_process_hader[1]}')
        des.update()
        ad_fas_firm.reboot_phone('adb', 'bootloader')
        sleep(10)
    elif reboot == False:
        flash_vbmeta_process_hader.configure(text=f'{lang.vbmeta_process_hader[2]}')
        des.update()

    flash_vbmeta_process_hader.configure(text=f'{lang.vbmeta_process_hader[3]}')
    des.update()
    sleep(2)

    if ad_fas_firm.status_unlock() == 'no':
        xdialog.error('WALMFAST', lang.unlock_bootloader_error)
        close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
        flash_vbmeta.place(x=themer.flash_vbmeta_position[0], y=themer.flash_vbmeta_position[1])
        flash_vbmeta_process_hader.place_forget()
        menu_base()
    elif ad_fas_firm.status_unlock() == 'yes':
        flash_vbmeta_process_hader.configure(text=f'{lang.vbmeta_process_hader[4]}')
        des.update()
        if ad_fas_firm.flash_system(partition='vbmeta', file=vbmeta_image) == True:
            flash_recovery_process_hader.configure(text=lang.vbmeta_process_hader[5])
            des.update()
            xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
            vbmeta_name.place_forget()
            flash_vbmeta_process_hader.place_forget()
            menu_base()
        elif ad_fas_firm.flash_system(partition='system', file=vbmeta_image) == False:
            xdialog.error('WALMFAST', lang.vbmeta_process_hader[6])
            close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
            flash_vbmeta_process_hader.place_forget()
            flash_vbmeta.place(x=themer.flash_vbmeta_position[0], y=themer.flash_vbmeta_position[1])
            menu_base()
def update():
    global status_update

    update_hader.configure(text=lang.update_check)
    about_menu_frame.place_forget()
    update_frame.place(x=0,y=0)

    update_close_button.configure(state='disabled')
    update_yes_button.place_forget()
    update_no_button.place_forget()
    des.update()

    sleep(3)

    status_update = updater.check_update()

    if status_update == 'Update_normal':
        update_hader.configure(text=lang.update_normal)
        update_close_button.configure(state='normal')
    elif status_update == 'Update_recommend':
        update_hader.configure(text=lang.update_recommend)
        update_yes_button.place(x=themer.update_yes_button_position[0], y=themer.update_yes_button_position[1])
        update_no_button.place(x=themer.update_no_button_position[0], y=themer.update_no_button_position[1])
    elif status_update == 'Update_required':
        update_hader.configure(text=lang.update_required)
        update_yes_button.place(x=themer.update_yes_button_position[0], y=themer.update_yes_button_position[1])
        update_no_button.place(x=themer.update_no_button_position[0], y=themer.update_no_button_position[1])
    elif status_update == False:
        update_hader.configure(text=lang.unable_update_check)
        update_close_button.configure(state='normal')
def update_start(status):
    update_yes_button.place_forget()
    update_no_button.place_forget()
    update_hader.configure(text=lang.update)
    des.update()

    if status == 'Update_recommend':
        updater.update_app(status)
        xdialog.info('WALMFAST', lang.program_is_exit)
        os._exit(0)
    elif status == 'Update_required':
        updater.update_app(status)
        xdialog.info('WALMFAST', lang.program_is_exit)
        os._exit(0)
def adb_sideload():
    gsi_frame.place_forget()
    sideload_image.place_forget()
    adb_sideload_hader.place(x=40, y=30)
    adb_sideload_descryption.place(x=40, y=120)
    select_adb_sideload_button.place(x=795, y=300)
    adb_sideload_hader.configure(text=lang.adbsideload)
    adb_sideload_descryption.configure(text=lang.adb_sideload_descryption, wraplength=950,justify=LEFT)
    adb_sideload_name.configure(width=750, wraplength=750, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART))
    adb_sideload_name.place_forget()
    contunue_sideload.place_forget()
    adb_sideload_frame.place(x=0, y=0)
def select_zip_adb_sideload():
    global zip_adb_sideload
    zip_adb_sideload = crossfiledialog.open_file(title='Open zip image file for WALMFAST', filter=["*.zip"])
    if zip_adb_sideload != '':
        adb_sideload_name.configure(text=f'{os.path.basename(zip_adb_sideload)}')
        adb_sideload_name.place(x=40, y=300)
        flash_adb_sideload.place(x=550, y=471)
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def sideload_setup():
    flash_adb_sideload.place_forget()
    adb_sideload_name.place_forget()
    select_adb_sideload_button.place_forget()
    adb_sideload_hader.place(x=560,y=30)
    adb_sideload_hader.configure(text=lang.adbsideload)
    adb_sideload_descryption.place(x=530, y=130)
    adb_sideload_descryption.configure(text=lang.adb_sideload_attettion, justify='center', width=425, wraplength=425)
    sideload_image.place(x=10, y=10)
    contunue_sideload.place(x=622, y=260)
def start_adb_sideload():
    adb_sideload_descryption.configure(text=lang.flash_zip_file, text_color='grey')
    contunue_sideload.place_forget()
    close_button.place_forget()

    sideload_y = 110
    for i in range(15):
        adb_sideload_descryption.place(x=530, y=sideload_y+5)
        sideload_y +=5
        des.update()
        sleep(0.03)

    adb_sideload_name.configure(text=lang.ended_adb_sideload, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), width=380, wraplength=380, justify='center')
    adb_sideload_name.place(x=560, y=275)
    adb_sideload_descryption.configure(text=lang.flash_zip_file, text_color=text, justify='center')
    des.update()

    if ad_fas_firm.sideload(file=zip_adb_sideload) == False:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base()
    else:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')    
        menu_base()
def delete_product():
    gsi_frame.place_forget()
    delete_product_button.configure(state='normal', text=lang.delete_product)
    close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
    delete_product_frame.place(x=0,y=0)
def delete_product_fun():
    close_button.place_forget()
    delete_product_confirm_button.configure(state='disabled', text=lang.please_wait)
    des.update()

    if ad_fas_firm.delete_product() == False:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base() 
    else:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base() 
def wipe_data():
    gsi_frame.place_forget()
    wipe_data_frame.place(x=0,y=0)
    close_button_wipe.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
    wipe_data_button.configure(state='normal', text=lang.wipe_data)
def wipe_data_fun():
    close_button_wipe.place_forget()
    wipe_data_confirm_button.configure(state='disabled', text=lang.please_wait)
    des.update()

    sleep(2)
    if ad_fas_firm.wipe_data() == False:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base()
    else:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base()
def flash_all_status_check():
    if flash_all_status.get() == 1:
        firmware_partition_frame.pack_forget()

        if android_phone_status._text != lang.not_found and phone_vendor_model._text != lang.model_device or debug_mode == 1:
            flash_phone_button.configure(state='normal')
        else:
            flash_phone_button.configure(state='disabled')
    else:
        firmware_partition_frame.pack()
        if len(partition_group) == 0:
            flash_phone_button.configure(state='disabled')
def parition_group_check(name, check):
    global partition_group

    check = check.get()

    if check == 0:
        partition_group.remove(name)
    elif check == 1:
        partition_group.append(name)

    if len(partition_group) == 0:
        flash_phone_button.configure(state='disabled')
    elif len(partition_group) > 0:
        if android_phone_status._text != lang.not_found and phone_vendor_model._text != lang.model_device or debug_mode == 1:
            flash_phone_button.configure(state='normal')
        else:
            flash_phone_button.configure(state='disabled')
    #print(f'Objects in partition group: {partition_group}. Score - {len(partition_group)}')
def clear_flash():
    for widget in firmware_image_frame.winfo_children():
        widget.pack_forget()
    for widget in firmware_partition_frame .winfo_children():
        widget.pack_forget() 
    flash_phone_button.configure(state='disabled')
def flash_all_process():
    if ad_fas_firm.flash_all(phone_vendor) == False:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{lang.platorm_tools_error}')
        menu_base()
    else:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base()
def flash_partition_process():
    if ad_fas_firm.flash_partition_images(phone_vendor, partition_group) == False:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base()
    else:
        xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
        menu_base()
def flash_phone():
    flash_phone_frame.place(x=0,y=0)

    if flash_all_status.get() == 1:
        des.after(7000, flash_all_process)
    elif flash_all_status.get() == 0:
        des.after(7000, flash_partition_process)
    des.update()

#Loading Entity
background = CTkLabel(des, image=imageload_b.background, text='')
background.place(x=0,y=0)

#Entity 1
base_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')

background = CTkLabel(base_frame, image=imageload_b.background, text='')

frame = CTkLabel(base_frame, image=imageload_b.frame, text='')

android = CTkLabel(base_frame, image=imageload_b.android, text='', justify='center', width=330, bg_color=bg)

android_phone_status = CTkLabel(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.not_found}', text_color=text, justify='center', width=327, bg_color=bg)

phone_vendor_model = CTkLabel(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.model_device}', text_color=text, justify='center', width=348, bg_color=bg)

exit_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.exit}', text_color=text, corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=228, border_width=2, command=lambda: os._exit(0))

about_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.about}',text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=228, border_width=2, command=menu_about)

select_phone_model_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.select_phone_model}',text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=276, command=load_phone_vendor)

test_state_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.test_state}',text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=232, state='disabled', command=menu_phone_status)

gsi_menu_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.gsi_boot_enabler}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=186, state='disabled', command=menu_gsi)

menu_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text='', width=25, height=25, image=imageload_b.menu,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_firmware)

firmware_image_frame = CTkScrollableFrame(base_frame, width=255, height=380, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2, scrollbar_button_color=scrollable, scrollbar_button_hover_color=scrollable, scrollbar_fg_color=scrollbar_fg)

select_firmware_folder_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.select_firmware_folder}',text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=276, state='disabled', command=load_firmware_folder)

forum_firmwares_forpda_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.forum_official_firmwares_forpda}',text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=228, border_width=2, state='disabled')

phone_reboot_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.phone_reboot}',text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, state='disabled', width=228, command=reboot_menu)

flash_phone_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.flash_device}',text_color='white',corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=228, state='disabled', command=flash_phone)

flash_partitions_radiobutton = CTkRadioButton(firmware_image_frame, text=lang.select_partition, variable=flash_all_status, value=0, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), bg_color=bg, fg_color=border, text_color=text, hover_color=hover, border_color=border, command=flash_all_status_check)

flash_all_radiobutton = CTkRadioButton(firmware_image_frame, text=lang.flash_all, variable=flash_all_status, value=1, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), bg_color=bg, fg_color=border, text_color=text, hover_color=hover, border_color=border, command=flash_all_status_check)

firmware_partition_frame = CTkScrollableFrame(firmware_image_frame, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2, scrollbar_button_color=scrollable, scrollbar_button_hover_color=scrollable, scrollbar_fg_color=scrollbar_fg)

background.place(x=themer.background_position[0], y=themer.background_position[1])
base_frame.place(x=0,y=0)
frame.place(x=themer.frame_position[0], y=themer.frame_position[1])
android.place(x=themer.android_position[0], y=themer.android_position[1])
android_phone_status.place(x=themer.android_phone_status_position[0], y=themer.android_phone_status_position[1])
phone_vendor_model.place(x=themer.phone_vendor_model_position[0], y=themer.phone_vendor_model_position[1])
select_phone_model_button.place(x=themer.select_phone_model_button_position[0],y=themer.select_phone_model_button_position[1])
test_state_button.place(x=themer.test_state_button_position[0],y=themer.test_state_button_position[1])
gsi_menu_button.place(x=themer.gsi_menu_button_position[0], y=themer.gsi_menu_button_position[1])
menu_button.place(x=themer.menu_button_position[0], y=themer.menu_button_position[1])
firmware_image_frame.place(x=themer.firmware_image_frame_position[0],y=themer.firmware_image_frame_position[1])
select_firmware_folder_button.place(x=themer.select_firmware_folder_button_position[0],y=themer.select_firmware_folder_button_position[1])
forum_firmwares_forpda_button.place(x=themer.forum_firmwares_forpda_button_position[0],y=themer.forum_firmwares_forpda_button_position[1])
phone_reboot_button.place(x=themer.phone_reboot_button_position[0],y=themer.phone_reboot_button_position[1])
flash_phone_button.place(x=themer.flash_phone_button_position[0],y=themer.flash_phone_button_position[1])
about_button.place(x=themer.about_button_position[0],y=themer.about_button_position[1])
exit_button.place(x=themer.exit_button_position[0],y=themer.exit_button_position[1])

#Entity 2
menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(menu_frame, image=imageload_b.background, text='')

firmwares_frame = CTkFrame(menu_frame, width=380, height=310, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2)

volume_on_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.volume_on, text_color=text, width=175, image=imageload_b.volume_on,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: musicplayer.volume_on())

volume_off_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.volume_off, text_color=text, width=175, image=imageload_b.volume_off,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: musicplayer.volume_off())

close_button = CTkButton(menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

location_music_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.location_music, width=360, text_color=text, image=imageload_b.location_music,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: show_in_file_manager(f'{os.getcwd()}/music/'))

install_firmware_complect_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.install_firmware_complect, width=360, text_color=text, image=imageload_b.install_firmware_complect,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=firmware_complect_installer)

select_language_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.language, text_color=text, width=175, image=imageload_b.select_language,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=langswitcher)

select_theme_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.theme, text_color=text, width=175, image=imageload_b.select_theme,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=themeswitcher)

get_music_name_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.get_music_name, width=360, text_color=text, image=imageload_b.music,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

background.place(x=themer.background_position[0], y=themer.background_position[1])
firmwares_frame.place(x=themer.firmwares_frame_position[0],y=themer.firmwares_frame_position[1])
volume_on_button.place(x=themer.volume_on_button_position[0], y=themer.volume_on_button_position[1])
volume_off_button.place(x=themer.volume_off_button_position[0], y=themer.volume_off_button_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
location_music_button.place(x=themer.location_music_button_position[0], y=themer.location_music_button_position[1])
install_firmware_complect_button.place(x=themer.install_firmware_complect_button_position[0], y=themer.install_firmware_complect_button_position[1])
select_language_button.place(x=themer.select_language_button_position[0], y=themer.select_language_button_position[1])
select_theme_button.place(x=themer.select_theme_button_position[0], y=themer.select_theme_button_position[1])
get_music_name_button.place(x=themer.get_music_name_button_position[0], y=themer.get_music_name_button_position[1])

#Entity 4 - Installer Firmware Complect
firmware_complect_installer_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(firmware_complect_installer_frame, image=imageload_b.background, text='')

distr=firm_comp_install.detect_system()

haderfirm = CTkLabel(firmware_complect_installer_frame, image=distr[0], font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.detect_operating_system}', text_color=text, compound='left', bg_color=bg)

progressbar = CTkProgressBar(firmware_complect_installer_frame, width=750, height=20, corner_radius=6, bg_color=bg, fg_color=fg, border_color=border, border_width=2, progress_color=border,mode='indeterminate', indeterminate_speed=5 )
progressbar.start()

background.place(x=themer.background_position[0], y=themer.background_position[1])
haderfirm.place(x=themer.hadefirm_position[0], y=themer.hadefirm_position[1])
progressbar.place(x=themer.progressbar_position[0], y = themer.progressbar_position[1])

#Entity 5 - Reboot device
reboot_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(reboot_menu_frame, image=imageload_b.background, text='')

firmwares_frame = CTkFrame(reboot_menu_frame, width=380, height=200, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2)

close_button = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

reboot_into_recovery = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_recovery, text_color=text, image=imageload_b.recovery,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=370, border_width=2, command=lambda: reboot_phone_through('recovery'))

reboot_into_bootloader = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_bootloader, text_color=text, image=imageload_b.bootloader,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=370, border_width=2, command=lambda: reboot_phone_through('bootloader'))

reboot_into_fastbootd = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_fastboot, text_color=text, image=imageload_b.fastbootd,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=370, border_width=2, command=lambda: reboot_phone_through('fastboot'))

reboot_into_system = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_system, text_color=text, image=imageload_b.system,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=370, border_width=2, command=lambda: reboot_phone_through(''))

hader_re = CTkLabel(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.reboot_through}', width=790, justify='center', text_color=text, bg_color=bg)

reboot_through_adb = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.adb, text_color=text, image=imageload_b.adb,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

reboot_through_fastboot = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.fastboot, text_color=text, image=imageload_b.bootloader,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

progressbar_re = CTkProgressBar(reboot_menu_frame, width=750, height=20, corner_radius=6, bg_color=bg, fg_color=fg, border_color=border, border_width=2, progress_color=border,mode='indeterminate', indeterminate_speed=5 )
progressbar_re.start()

background.place(x=themer.background_position[0], y=themer.background_position[1])
firmwares_frame.place(x=themer.firmwares_frame_position[0],y=themer.firmwares_frame_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
reboot_into_recovery.pack(padx=themer.reboot_into_recovery_pad[0], pady=themer.reboot_into_recovery_pad[1])
reboot_into_bootloader.pack(padx=themer.reboot_into_bootloader_pad[0], pady=themer.reboot_into_bootloader_pad[1])
reboot_into_fastbootd.pack(padx=themer.reboot_into_fastbootd_pad[0], pady=themer.reboot_into_fastbootd_pad[1])
reboot_into_system.pack(padx=themer.reboot_into_system_pad[0], pady=themer.reboot_into_system_pad[1])


#Entity 6 - Phone status through
phone_status_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(phone_status_frame, image=imageload_b.background, text='')

phone_status_through_adb = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.adb, text_color=text, image=imageload_b.adb,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: phone_test_state('adb'))

phone_status_through_fastboot = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.fastboot, text_color=text, image=imageload_b.bootloader,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: phone_test_state('fastboot'))

hader_state = CTkLabel(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.state_through}', text_color=text, width=790, justify=CENTER, bg_color=bg)

close_button = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

background.place(x=themer.background_position[0], y=themer.background_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
hader_state.place(x=themer.hader_state_position[0], y=themer.hader_state_position[1])
phone_status_through_adb.place(x=themer.phone_status_through_adb_position[0], y=themer.phone_status_through_adb_position[1])
phone_status_through_fastboot.place(x=themer.phone_status_through_fastboot_position[0], y=themer.phone_status_through_fastboot_position[1])

#Entity 7 GSI Menu
gsi_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(gsi_menu_frame, image=imageload_b.background, text='')

close_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=150, command=menu_base)

flash_custom_partition_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.flash_custom_partition, text_color=text, image=imageload_b.flash,corner_radius=6, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=gsi_installer)

approve_custom_load_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.approve_custom_load, text_color=text, image=imageload_b.approve_custom_load,corner_radius=6, width=495, bg_color=bg, anchor=W, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=vbmeta_installer)

wipe_data_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.wipe_data, text_color=text, image=imageload_b.wipe_data,corner_radius=6, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=wipe_data)

delete_product_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.delete_product, text_color=text, image=imageload_b.product,corner_radius=6, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=delete_product)

search_gsi_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.search_gsi, text_color=text, image=imageload_b.search_gsi,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, width=315, anchor=W, border_color=border, border_width=2, command=lambda: webbrowser.open_new_tab(winaobj.SEARCH_GSI_URL))

forum_nonfirmwares_forpda_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.forum_official_firmwares_forpda}', image=imageload_b.forpda, text_color=text,corner_radius=6, width=315, anchor=W, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: webbrowser.open_new_tab(f'{vendorvice.nonofficial_firmwares_forum_forpda}'))

adbsideload_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.adbsideload}', image=imageload_b.adb, text_color=text,corner_radius=6, width=315, anchor=W, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=adb_sideload)

customboot_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.install_customboot}', image=imageload_b.customboot, text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=customboot)

switch_slot = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.swslot}', image=imageload_b.ab, text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=menu_sw)


background.place(x=themer.background_position[0], y=themer.background_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
flash_custom_partition_button.place(x=themer.flash_custom_partition_button_position[0], y=themer.flash_custom_partition_button_position[1])
approve_custom_load_button.place(x=themer.approve_custom_load_button_position[0], y=themer.approve_custom_load_button_position[1])
wipe_data_button.place(x=themer.wipe_data_button_position[0], y=themer.wipe_data_button_position[1])
delete_product_button.place(x=themer.delete_product_button_position[0], y=themer.delete_product_button_position[1])
search_gsi_button.place(x=themer.search_gsi_button_position[0], y=themer.search_gsi_button_position[1])
forum_nonfirmwares_forpda_button.place(x=themer.forum_nonfirmwares_forpda_button_position[0],y=themer.forum_nonfirmwares_forpda_button_position[1])
adbsideload_button.place(x=themer.adbsideload_button_position[0],y=themer.adbsideload_button_position[1])
customboot_button.place(x=themer.customboot_button_position[0],y=themer.customboot_button_position[1])
switch_slot.place(x=themer.switch_slot[0],y=themer.switch_slot[1])

#Entity 8 - About 
about_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(about_menu_frame, image=imageload_b.UPDATERLOCK, text='')

walmfast_logo = CTkLabel(about_menu_frame, image=imageload_b.logo, text='')

program_name = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.program_name}', text_color=text, bg_color=bg)

model_branch = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.VERSION}', text_color=text, bg_color=bg)

made_by = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.made_by}', text_color=text, bg_color=bg)

close_button = CTkButton(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=' ', text_color=text, image=imageload_b.close,corner_radius=8, bg_color=bg, fg_color=bg, hover_color=hover, border_color=bg, width=150, border_width=2, command=menu_base)

extended_button = CTkButton(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.extended, text_color=text, image=imageload_b.extended,corner_radius=8, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=195, border_width=2, command=donatos)

update_button = CTkButton(about_menu_frame, image=imageload_b.logo, width=370, height=150, bg_color=bg, fg_color=fg, hover_color=bg, text=' ', command=update)
update_button1 = CTkButton(about_menu_frame, width=650, height=30, bg_color=bg, fg_color=bg, hover_color=bg,font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text='Проверить наличие обновлений',text_color=text,border_color=border, corner_radius=8, border_width=2, command=update)

version = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.VERSION}', text_color=text, bg_color=bg1)

NB = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.NB}', text_color=text, bg_color=bg1)

NBD = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.NBD}', text_color=text, bg_color=bg1)

NBDR = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.NBDR}', text_color=text, bg_color=bg1)

CDNM = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.CDNM}', text_color=text, bg_color=bg1)

CDNML = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.CDNML}', text_color=text, bg_color=bg1)

NC = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.NC}', text_color=text, bg_color=bg1)

core_version = CTkButton(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{winaobj.CORE_VERSION}', text_color=text,corner_radius=8, bg_color=bg1, fg_color=bg1, hover_color=hover, border_color=bg1, width=150, border_width=2, command=menu_base)

background.place(x=1, y=1)
model_branch.place(x=400, y=193)
version.place(x=770, y=300)
NB.place(x=50, y=300)
core_version.place(x=770, y=340)
NBDR.place(x=800, y=380)
NC.place(x=50, y=340)
NBD.place(x=50, y=380)
CDNM.place(x=50, y=420)
CDNML.place(x=810, y=420)
made_by.place(x=1000, y=200)
close_button.place(x=0, y=15)
update_button.place(x=250, y=50)
update_button1.place(x=150, y=480)
walmfast_logo.place(x=250, y=50)

#Entity 9 - Customboot installer 
customboot_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(customboot_frame, image=imageload_b.background, text='')

customboot_hader = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.customboot_hader}', text_color=text, bg_color=bg)

customboot_descryption = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.customboot_description}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

twrp_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.twrp}', text_color=text, image=imageload_b.twrp,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_base)
orangefox_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.orangefox}', text_color=text, image=imageload_b.orangefox,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_base)
pbrp_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.pbrp}', text_color=text, image=imageload_b.pbrp,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_base)

flash_recovery_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.flash_recovery}', text_color=text, image=imageload_b.flash,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=flash_recovery)

recovery_path_textbox = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='center', width=750, wraplength=750)

select_recovery_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_recovery_image)

flash_recovery_process_hader = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.q_start_flash_recovery_process}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

recovery_yes_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: start_flash_recovery(reboot=True))
recovery_no_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: start_flash_recovery(reboot=False))

flashit_partition_attetion = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), width=winaobj.WIDTH, height=18, justify='center', text=f'partition', text_color='red', bg_color=bg)

background.place(x=themer.background_position[0], y=themer.background_position[1])
customboot_hader.place(x=themer.customboot_hader_position[0], y=themer.customboot_hader_position[1])
customboot_descryption.place(x=themer.customboot_descryption_position[0], y=themer.customboot_descryption_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])

#Entity 10 - Задонать пж
donatos_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(donatos_frame, image=imageload_b.background, text='')

donatos_destination = CTkLabel(donatos_frame, image=imageload_b.donat_destination, text='')

donatos_me = CTkLabel(donatos_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.program_name}', text_color=text, bg_color=bg)

destination_and_number_card = CTkLabel(donatos_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.donat_me}\n{lang.donat_destination}\n{lang.card_number}', text_color=text, bg_color=bg, justify = LEFT)

close_button = CTkButton(donatos_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

background.place(x=themer.background_position[0], y=themer.background_position[1])
donatos_destination.place(x=themer.donatos_destination_position[0], y=themer.donatos_destination_position[1])
donatos_me.place(x=themer.donatos_me_position[0], y=themer.donatos_me_position[1])
destination_and_number_card.place(x=themer.destination_and_number_card[0], y=themer.destination_and_number_card[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])

#Entity 11 - Language switcher
langswitcher_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(langswitcher_frame, image=imageload_b.background, text='')

langswitcher_hader = CTkLabel(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.choose_language}', width=950, text_color=text, bg_color=bg)

close_button = CTkButton(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

russian_language = CTkButton(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.russian_language, text_color=text, image=imageload_b.russian_flag,corner_radius=6, bg_color=bg, height=45, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: write_language('rus'))

english_language = CTkButton(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.english_language, text_color=text, image=imageload_b.english_flag,corner_radius=6, bg_color=bg, height=45, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: write_language('eng'))

background.place(x=themer.background_position[0], y=themer.background_position[1])
langswitcher_hader.place(x=themer.langswitcher_hader_position[0], y=themer.langswitcher_hader_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
russian_language.place(x=themer.russian_language_position[0], y=themer.russian_language_position[1])
english_language.place(x=themer.english_language_position[0], y=themer.english_language_position[1])

#Entity 12 - Theme switcher
themeswitcher_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(themeswitcher_frame, image=imageload_b.background, text='')

themeswitcher_hader = CTkLabel(themeswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.choose_theme}', width=950, text_color=text, bg_color=bg)

close_button = CTkButton(themeswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

themes_frame = CTkScrollableFrame(themeswitcher_frame, width=380, height=310, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2)

background.place(x=themer.background_position[0], y=themer.background_position[1])
themeswitcher_hader.place(x=themer.themeswitcher_hader_position[0], y=themer.themeswitcher_hader_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
themes_frame.place(x=themer.themes_frame_position[0],y=themer.themes_frame_position[1])

#Entity 13 - GSI System Installer
gsi_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(gsi_frame, image=imageload_b.background, text='')

gsi_hader = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.gsi_hader}', text_color=text, bg_color=bg)

gsi_descryption = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.gsi_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

select_gsi_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_gsi_image)

gsi_name = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='left', width=750, wraplength=750)

flash_gsi = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.flash_gsi}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=200, command=flash_gsi_step_one)

flash_gsi_process_hader = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.gsi_process_hader}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

reboot_fastbotd_yes_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: flash_gsi_step_two(reboot=True))
reboot_fastbotd_no_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, width=150, border_color=border, border_width=2, command=lambda: flash_gsi_step_two(reboot=False))

background.place(x=themer.background_position[0], y=themer.background_position[1])
gsi_hader.place(x=themer.gsi_hader_position[0], y=themer.gsi_hader_position[1])
gsi_descryption.place(x=themer.gsi_descryption_position[0], y=themer.gsi_descryption_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
select_gsi_button.place(x=themer.select_gsi_button_position[0], y=themer.select_gsi_button_position[1])

#Entity 14 - Vbmeta Fix Installer
vbmeta_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(vbmeta_frame, image=imageload_b.background, text='')

vbmeta_hader = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.vbmeta_hader}', text_color=text, bg_color=bg)

vbmeta_descryption = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.vbmeta_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

select_vbmeta_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_vbmeta_image)

vbmeta_name = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='center', width=750, wraplength=750)

flash_vbmeta = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.flash_vbmeta}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=200, command=flash_vbmeta_step_one)

flash_vbmeta_process_hader = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.gsi_process_hader}', text_color=text,  bg_color=bg, wraplength=950,justify=LEFT)

reboot_fastbot_yes_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: flash_vbmeta_step_two(reboot=True))
reboot_fastbot_no_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, width=150, border_color=border, border_width=2, command=lambda: flash_vbmeta_step_two(reboot=False))

background.place(x=themer.background_position[0], y=themer.background_position[1])
vbmeta_hader.place(x=themer.vbmeta_hader_position[0], y=themer.vbmeta_hader_position[1])
vbmeta_descryption.place(x=themer.vbmeta_descryption_position[0], y=themer.vbmeta_descryption_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
select_vbmeta_button.place(x=themer.select_vbmeta_button_position[0], y=themer.select_vbmeta_button_position[1])

#Entity 15 - Update
update_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(update_frame, image=imageload_b.background, text='')

update_close_button = CTkButton(update_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

update_hader = CTkLabel(update_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.update_check}', width=winaobj.WIDTH, justify='center', text_color=text, bg_color=bg)

update_yes_button = CTkButton(update_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: update_start(status_update))
update_no_button = CTkButton(update_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, width=150, border_color=border, border_width=2, command=menu_base)

background.place(x=themer.background_position[0], y=themer.background_position[1])
update_close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
update_hader.place(x=themer.update_hader_position[0], y=themer.update_hader_position[1])

#Entity 16 - ADB Sideload
adb_sideload_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(adb_sideload_frame, image=imageload_b.background, text='')

close_button = CTkButton(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

adb_sideload_hader = CTkLabel(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.adbsideload}', text_color=text, bg_color=bg)

adb_sideload_descryption = CTkLabel(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.adb_sideload_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

select_adb_sideload_button = CTkButton(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_zip_adb_sideload)

adb_sideload_name = CTkLabel(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='center', width=750, wraplength=750)

flash_adb_sideload = CTkButton(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.flash_zip_adb_sideload}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=200, command=sideload_setup)

sideload_image = CTkLabel(adb_sideload_frame, image=imageload_b.sideload, text='')

contunue_sideload = CTkButton(adb_sideload_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.l_continue}', image=imageload_b.right, text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=200, command=start_adb_sideload)

background.place(x=themer.background_position[0], y=themer.background_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
adb_sideload_hader.place(x=themer.adb_sideload_hader_position[0], y=themer.adb_sideload_hader_position[1])
adb_sideload_descryption.place(x=themer.adb_sideload_descryption_position[0], y=themer.adb_sideload_descryption_position[1])
select_adb_sideload_button.place(x=themer.select_adb_sideload_button_position[0], y=themer.select_adb_sideload_button_position[1])

#Entity 17 Delete Product
delete_product_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(delete_product_frame, image=imageload_b.background, text='')

delete_product_hader = CTkLabel(delete_product_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.clean_storage_gsi}', text_color=text, bg_color=bg)

delete_product_descryption = CTkLabel(delete_product_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.clean_storage_gsi_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(delete_product_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

delete_product_confirm_button = CTkButton(delete_product_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.delete_product}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=600, command=delete_product_fun)

background.place(x=themer.background_position[0], y=themer.background_position[1])
close_button.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
delete_product_hader.place(x=themer.delete_product_hader_position[0], y=themer.delete_product_hader_position[1])
delete_product_descryption.place(x=themer.delete_product_descryption_position[0], y=themer.delete_product_descryption_position[1])
delete_product_confirm_button.place(x=themer.delete_product_confirm_button_position[0], y=themer.delete_product_confirm_button_position[1])

#Entity 18 Wipe Data
wipe_data_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(wipe_data_frame, image=imageload_b.background, text='')

wipe_data_hader = CTkLabel(wipe_data_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.clean_user_partition}', text_color=text, bg_color=bg)

wipe_data_descryption = CTkLabel(wipe_data_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.clean_user_partition_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button_wipe = CTkButton(wipe_data_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload_b.close,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

wipe_data_confirm_button = CTkButton(wipe_data_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.wipe_data}', text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=600, command=wipe_data_fun)

wipe_data_hader.place(x=themer.wipe_data_hader_position[0], y=themer.wipe_data_hader_position[1])
wipe_data_descryption.place(x=themer.wipe_data_descryption_position[0], y=themer.wipe_data_descryption_position[1])
background.place(x=themer.background_position[0], y=themer.background_position[1])
close_button_wipe.place(x=themer.close_button_position[0], y=themer.close_button_position[1])
wipe_data_confirm_button.place(x=themer.wipe_data_confirm_button_position[0], y=themer.wipe_data_confirm_button_position[1])

#Entity 19 Flash Phone
flash_phone_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(flash_phone_frame, image=imageload_b.background, text='')

flash_phone_hader = CTkLabel(flash_phone_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.flash_phone}', width=winaobj.WIDTH, text_color=text, bg_color=bg)

progressbar_fp = CTkProgressBar(flash_phone_frame, width=750, height=20, corner_radius=6, bg_color=bg, fg_color=fg, border_color=border, border_width=2, progress_color=border,mode='indeterminate', indeterminate_speed=0.8)
progressbar_fp.start()

background.place(x=themer.background_position[0], y=themer.background_position[1])
flash_phone_hader.place(x=themer.flash_phone_hader_position[0], y=themer.flash_phone_hader_position[1])
progressbar_fp.place(x=themer.progressbar_fp_position[0], y=themer.progressbar_fp_position[1])


# 20 Смена слота
sw_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)
background = CTkLabel(sw_menu_frame, image=imageload_b.background, text='')
slot_a = CTkButton(sw_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.a}', image=imageload_b.ab, text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, width=25, anchor=W, hover_color=hover, border_color=border, border_width=2, command=lambda:set_A)
slot_b = CTkButton(sw_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.b}', image=imageload_b.ab, text_color=text,corner_radius=6, bg_color=bg, fg_color=fg, width=25, anchor=W, hover_color=hover, border_color=border, border_width=2, command=lambda:set_B)


slot_a.place(x=themer.russian_language_position[0], y=themer.russian_language_position[1])
slot_b.place(x=themer.english_language_position[0], y=themer.english_language_position[1])
background.place(x=themer.background_position[0], y=themer.background_position[1])
#Required actions

des.wm_protocol('WM_DELETE_WINDOW', lambda: os._exit(0))

#Debug
if debug_mode == 1:
    gsi_menu_button.configure(state='normal')
    phone_reboot_button.configure(state='normal')
    flash_phone_button.configure(state='normal')

#Startup
des.mainloop()
