from script import adb_fastboot_firmwaer as ad_fas_firm
ad_fas_firm.init()

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
elif selector.select_languages == 'eng':
    from languages import eng as lang

des = CTk()
des.title(f"WALM Fastboot - {lang.fastboot_flash_firmware}")
des.geometry(f'{winaobj.WIDTH}x{winaobj.HEIGHT}')
des.resizable(False, False)

from script import imageload
from script import musicplayer
from script import firmware_complect_install as firm_comp_install

#System fix
rootfs = os.getcwd()
if platform.system() == 'Linux':
    FontManager.load_font(winaobj.FONT)
elif platform.system() == 'Windows':
    winaobj.FONT_NAME = 'Segoe UI'

themer = importlib.import_module(name=f'.{selector.theme}.{selector.theme}', package='image')

bg = themer.bg
fg = themer.fg
border = themer.border
text = themer.text
hover = themer.hover
scrollable = themer.scrollable
scrollbar_fg = themer.scrollbar_fg

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
    base_frame.place(x=0, y=0)
def menu_phone_status():
    menu_frame.place_forget()
    phone_status_frame.place(x=0,y=0)
def langswitcher():
    menu_frame.place_forget()
    langswitcher_frame.place(x=0,y=0)
def themeswitcher():

    for themepath in os.listdir('image'):
        themebut = CTkButton(themes_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=themepath, width=360, height=45, text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: themeswitch(themepath))
        themebut.pack()

    menu_frame.place_forget()
    themeswitcher_frame.place(x=0,y=0)
def menu_gsi():
    menu_frame.place_forget()
    gsi_menu_frame.place(x=0,y=0)
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
    firmwares_frame.place(x=285,y=131)
    reboot_menu_frame.place(x=0,y=0)
def reboot_through(system, into):

    progressbar_re.place(x=100, y = 200)

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

    hader_re.place(x=80, y=110)
    reboot_through_adb.place(x=300, y=200)
    reboot_through_fastboot.place(x=500, y=202)
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
            icon = imageload.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/icon.png')
            des.iconphoto(False, icon)

            try:
                android.configure(image=imageload.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/{vendorvice.image}'))
            except:
                android.configure(image=imageload.android)

            forum_firmwares_forpda_button.configure(state='normal', command=lambda: webbrowser.open_new_tab(f'{vendorvice.official_firmwares_forum_forpda}'))
            select_firmware_folder_button.configure(state='normal')
            test_state_button.configure(state='normal')
            des.update()
        except:
            pass
    elif platform.system() == 'Windows':

        phone_vendor = crossfiledialog.open_file(title='Open phone vendor file for WALMFAST', start_dir=f'{os.getcwd()}/{winaobj.PHONE_VENDOR_PATH}/', filter=["*.py"])
        vendorid = str(os.path.basename(phone_vendor))[:-3]
        vendorvice = importlib.import_module(name=f'.{vendorid}.{vendorid}', package=f'{winaobj.PHONE_VENDOR_PATH}')

        try:
            importlib.reload(vendorvice)
        except:
            pass

        os.chdir(rootfs)

        phone_vendor_model.configure(text=vendorvice.model)
        icon = imageload.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/icon.png')
        des.iconphoto(False, icon)

        try:
            android.configure(image=imageload.load_image(f'{winaobj.PHONE_VENDOR_PATH}/{vendorid}/{vendorvice.image}'))
        except:
            android.configure(image=imageload.android)

        forum_firmwares_forpda_button.configure(state='normal', command=lambda: webbrowser.open_new_tab(f'{vendorvice.official_firmwares_forum_forpda}'))
        select_firmware_folder_button.configure(state='normal')
        test_state_button.configure(state='normal')
        des.update()     
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
            pbrp_button.place(x=350, y=470)
        else:
            pbrp_button.place_forget()
    except:
        pbrp_button.place_forget()

    try:
        if vendorvice.orangefox != None or vendorvice.orangefox != '':
            orangefox_button.configure(command=lambda: webbrowser.open_new_tab(f'{vendorvice.orangefox}'))
            orangefox_button.place(x=20, y=470)
        else:
            orangefox_button.place_forget()
    except:
        orangefox_button.place_forget()

    try:
        if vendorvice.nonuniversalboot == True:
            flashit_partition_attetion.configure(text=lang.flashit_recovery_partition)
            flashit_partition_attetion.place(x=0, y=10)
        elif vendorvice.nonuniversalboot == False:
            flashit_partition_attetion.configure(text=lang.flashit_boot_partition)
            flashit_partition_attetion.place(x=0, y=10)
    except:
        flashit_partition_attetion.place_forget()

    recovery_path_textbox.place(x=40, y=250)
    select_recovery_button.place(x=795, y=250)
    menu_frame.place_forget()
    customboot_frame.place(x=0,y=0)
def select_recovery_image():
    global recovery_image

    recovery_image = crossfiledialog.open_file(title='Open recovery image file for WALMFAST', filter=["*.img"])
    if recovery_image != '':
        recovery_path_textbox.configure(text=os.path.basename(recovery_image))
        flash_recovery_button.place(x=530, y=472)
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def flash_recovery():
    flash_recovery_process_hader.configure(text=f'{lang.q_start_flash_recovery_process[0]}')
    recovery_yes_button.place(x=640, y=340)
    recovery_no_button.place(x=790, y=340)
    flash_recovery_process_hader.place(x=50, y=340)
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
        close_button.place(x=795, y=470)
        flash_recovery_process_hader.place_forget()
        flash_recovery_button.place(x=530, y=472)
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
            close_button.place(x=795, y=470)
            menu_base()
        elif ad_fas_firm.flash_partition(partition=universal_detect_boot, file=recovery_image) == False:
            xdialog.error('WALMFAST', lang.q_start_flash_recovery_process[4])
            close_button.place(x=795, y=470)
            flash_recovery_process_hader.place_forget()
            flash_recovery_button.place(x=530, y=472)
            menu_base()
    
def write_language(language):
    with open('settings/selector.py', 'r') as f:
        for i in range(0):
            f.readline()
        x = f.readline()
    with open ('settings/selector.py', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace(f'{x}', f"select_languages =  '{language}'\n")
    with open ('settings/selector.py', 'w') as f:
        f.write(new_data)
    xdialog.info('WALMFAST', lang.program_is_exit)
    os._exit(0)
def themeswitch(theme):
    with open('settings/selector.py', 'r') as f:
        for i in range(1):
            f.readline()
        x = f.readline()
    with open ('settings/selector.py', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace(f'{x}', f"theme =  '{theme}'\n")
    with open ('settings/selector.py', 'w') as f:
        f.write(new_data)
    xdialog.info('WALMFAST', lang.program_is_exit)
    os._exit(0)
def gsi_installer():
    menu_frame.place_forget()
    gsi_frame.place(x=0,y=0)
def select_gsi_image():
    global gsi_image

    gsi_image = crossfiledialog.open_file(title='Open gsi image file for WALMFAST', filter=["*.img"])
    if gsi_image != '':
        gsi_name.configure(text=f'{os.path.basename(gsi_image)}')
        gsi_name.place(x=40, y=250)
        des.update()
        flash_gsi.place(x=585, y=470)

        reboot_fastbotd_yes_button.place_forget()
        reboot_fastbotd_no_button.place_forget()
        flash_gsi_process_hader.place_forget()
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def flash_gsi_step_one():
    flash_gsi.place_forget()
    reboot_fastbotd_yes_button.place(x=650, y=360)
    reboot_fastbotd_no_button.place(x=795, y=360)
    flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[0]}')
    flash_gsi_process_hader.place(x=40, y=356)
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
        close_button.place(x=795, y=470)
        flash_gsi.place(x=585, y=470)
        flash_gsi_process_hader.place_forget()
        menu_base()
    elif ad_fas_firm.status_unlock() == 'yes':
        flash_gsi_process_hader.configure(text=f'{lang.gsi_process_hader[4]}')
        des.update()

        if ad_fas_firm.flash_system(partition='system', file=gsi_image) == True:
            flash_recovery_process_hader.place_forget()
            xdialog.info('WALMFAST', f'{lang.score}\n\n{open('infolog/partition.txt', encoding='utf-8').read()}')
            close_button.place(x=795, y=470)
            flash_gsi.place(x=585, y=470)
            des.update()
            menu_base()
        elif ad_fas_firm.flash_system(partition='system', file=gsi_image) == False:
            xdialog.error('WALMFAST', lang.gsi_process_hader[5])
            close_button.place(x=795, y=470)
            flash_gsi_process_hader.place_forget()
            flash_gsi.place(x=585, y=470)
            menu_base()
def vbmeta_installer():
    base_frame.place_forget()
    vbmeta_frame.place(x=0, y=0)
def select_vbmeta_image():
    global vbmeta_image
    vbmeta_image = crossfiledialog.open_file(title='Open gsi image file for WALMFAST', filter=["*.img"])
    if vbmeta_image != '' and os.path.basename(vbmeta_image) == 'vbmeta.img':
        vbmeta_name.configure(text=f'{os.path.basename(vbmeta_image)}')
        vbmeta_name.place(x=40, y=250)
        flash_vbmeta.place(x=550, y=471)
    if platform.system() == 'Windows':
        os.chdir(rootfs)
    des.update()
def flash_vbmeta_step_one():
    flash_vbmeta.place_forget()
    reboot_fastbot_yes_button.place(x=650, y=360)
    reboot_fastbot_no_button.place(x=795, y=360)
    flash_vbmeta_process_hader.configure(text=f'{lang.vbmeta_process_hader[0]}')
    flash_vbmeta_process_hader.place(x=40, y=356)
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
        close_button.place(x=795, y=470)
        flash_vbmeta.place(x=585, y=470)
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
            close_button.place(x=795, y=470)
            flash_vbmeta_process_hader.place_forget()
            flash_vbmeta.place(x=585, y=470)
            menu_base()

#Loading Entity
background = CTkLabel(des, image=imageload.background, text='')
background.place(x=0,y=0)

#Entity 1
base_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color='black')

background = CTkLabel(base_frame, image=imageload.background, text='')

frame = CTkLabel(base_frame, image=imageload.frame, text='')

android = CTkLabel(base_frame, image=imageload.android, text='', justify='center', width=330, bg_color=bg)

android_phone_status = CTkLabel(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.not_found}', text_color=text, justify='center', width=327, bg_color=bg)

phone_vendor_model = CTkLabel(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.model_device}', text_color=text, justify='center', width=348, bg_color=bg)

exit_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.exit}', text_color=text, corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=228, border_width=2, command=lambda: os._exit(0))

about_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.about}',text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=228, border_width=2, command=menu_about)

select_phone_model_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.select_phone_model}',text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=276, command=load_phone_vendor)

test_state_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.test_state}',text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=232, state='disabled', command=menu_phone_status)

gsi_menu_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.gsi_boot_enabler}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=186, state='disabled', command=menu_gsi)

menu_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text='', width=25, height=25, image=imageload.menu,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_firmware)

firmware_image_frame = CTkScrollableFrame(base_frame, width=255, height=380, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2, scrollbar_button_color=scrollable, scrollbar_button_hover_color=scrollable, scrollbar_fg_color=scrollbar_fg)

select_firmware_folder_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.select_firmware_folder}',text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=276, state='disabled', command=load_firmware_folder)

forum_firmwares_forpda_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.forum_official_firmwares_forpda}',text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=228, border_width=2, state='disabled')

phone_reboot_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.phone_reboot}',text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, state='disabled', width=228, command=reboot_menu)

flash_phone_button = CTkButton(base_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), height=45, text=f'{lang.flash_device}',text_color='white',corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=228, state='disabled')

background.place(x=1, y=1)
base_frame.place(x=0,y=0)
background.place(x=1, y=1)
frame.place(x=20, y=20)
android.place(x=30, y=70)
android_phone_status.place(x=30, y=370)
phone_vendor_model.place(x=20, y=467)
select_phone_model_button.place(x=385,y=25)
test_state_button.place(x=695,y=73)
gsi_menu_button.place(x=740, y=25)
menu_button.place(x=695, y=25)
firmware_image_frame.place(x=385,y=73)
select_firmware_folder_button.place(x=385,y=470)
forum_firmwares_forpda_button.place(x=695,y=276)
phone_reboot_button.place(x=695,y=324)
flash_phone_button.place(x=695,y=372)
about_button.place(x=695,y=420)
exit_button.place(x=695,y=470)

#Entity 2
menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(menu_frame, image=imageload.background, text='')

firmwares_frame = CTkFrame(menu_frame, width=380, height=310, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2)

volume_on_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.volume_on, text_color=text, width=175, image=imageload.volume_on,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: musicplayer.volume_on())

volume_off_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.volume_off, text_color=text, width=175, image=imageload.volume_off,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: musicplayer.volume_off())

close_button = CTkButton(menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

location_music_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.location_music, width=360, text_color=text, image=imageload.location_music,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: show_in_file_manager(f'{os.getcwd()}/music/'))

install_firmware_complect_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.install_firmware_complect, width=360, text_color=text, image=imageload.install_firmware_complect,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=firmware_complect_installer)

select_language_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.language, text_color=text, width=175, image=imageload.select_language,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=langswitcher)

select_theme_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.theme, text_color=text, width=175, image=imageload.select_theme,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=themeswitcher)

get_music_name_button = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.get_music_name, width=360, text_color=text, image=imageload.music,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

background.place(x=1, y=1)
firmwares_frame.place(x=285,y=103)
volume_on_button.place(x=10, y=10)
volume_off_button.place(x=195, y=10)
close_button.place(x=795, y=470)
location_music_button.place(x=10, y=70)
install_firmware_complect_button.place(x=10, y=130)
select_language_button.place(x=10, y=190)
select_theme_button.place(x=195, y=190)
get_music_name_button.place(x=10, y=250)

#Entity 4 - Installer Firmware Complect
firmware_complect_installer_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(firmware_complect_installer_frame, image=imageload.background, text='')

distr=firm_comp_install.detect_system()

haderfirm = CTkLabel(firmware_complect_installer_frame, image=distr[0], font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.detect_operating_system}', text_color=text, compound='left', bg_color=bg)

progressbar = CTkProgressBar(firmware_complect_installer_frame, width=750, height=20, corner_radius=2, bg_color=bg, fg_color=fg, border_color=border, border_width=2, progress_color=border,mode='indeterminate', indeterminate_speed=5 )
progressbar.start()

background.place(x=1, y=1)
haderfirm.place(x=100, y=100)
progressbar.place(x=100, y = 200)

#Entity 5 - Reboot device
reboot_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(reboot_menu_frame, image=imageload.background, text='')

firmwares_frame = CTkFrame(reboot_menu_frame, width=380, height=200, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2)

close_button = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=140, border_width=2, command=menu_base)

reboot_into_recovery = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_recovery, text_color=text, image=imageload.recovery,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=lambda: reboot_phone_through('recovery'))

reboot_into_bootloader = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_bootloader, text_color=text, image=imageload.bootloader,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=lambda: reboot_phone_through('bootloader'))

reboot_into_fastbootd = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_fastboot, text_color=text, image=imageload.fastbootd,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=lambda: reboot_phone_through('fastboot'))

reboot_into_system = CTkButton(firmwares_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.reboot_into_system, text_color=text, image=imageload.system,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=lambda: reboot_phone_through(''))

hader_re = CTkLabel(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.reboot_through}', width=790, justify='center', text_color=text, bg_color=bg)

reboot_through_adb = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.adb, text_color=text, image=imageload.adb,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

reboot_through_fastboot = CTkButton(reboot_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.fastboot, text_color=text, image=imageload.bootloader,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

progressbar_re = CTkProgressBar(reboot_menu_frame, width=750, height=20, corner_radius=2, bg_color=bg, fg_color=fg, border_color=border, border_width=2, progress_color=border,mode='indeterminate', indeterminate_speed=5 )
progressbar_re.start()

background.place(x=1, y=1)
firmwares_frame.place(x=285,y=131)
close_button.place(x=795, y=470)
reboot_into_recovery.place(x=32, y=20)
reboot_into_bootloader.place(x=202, y=20)
reboot_into_fastbootd.place(x=32, y=80)
reboot_into_system.place(x=202, y=80)

#Entity 6 - Phone status through
phone_status_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(phone_status_frame, image=imageload.background, text='')

phone_status_through_adb = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.adb, text_color=text, image=imageload.adb,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: phone_test_state('adb'))

phone_status_through_fastboot = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.fastboot, text_color=text, image=imageload.bootloader,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: phone_test_state('fastboot'))

hader_state = CTkLabel(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.state_through}', text_color=text, width=790, justify=CENTER, bg_color=bg)

close_button = CTkButton(phone_status_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

background.place(x=1, y=1)
close_button.place(x=795, y=470)
hader_state.place(x=80, y=110)
phone_status_through_adb.place(x=300, y=200)
phone_status_through_fastboot.place(x=500, y=202)

#Entity 7 GSI Menu
gsi_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(gsi_menu_frame, image=imageload.background, text='')

close_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, width=150, command=menu_base)

flash_custom_partition_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.flash_custom_partition, text_color=text, image=imageload.flash,corner_radius=2, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=gsi_installer)

approve_custom_load_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.approve_custom_load, text_color=text, image=imageload.approve_custom_load,corner_radius=2, width=495, bg_color=bg, anchor=W, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=vbmeta_installer)

wipe_data_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.wipe_data, text_color=text, image=imageload.wipe_data,corner_radius=2, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2)

delete_product_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.delete_product, text_color=text, image=imageload.product,corner_radius=2, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2)

search_gsi_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=lang.search_gsi, text_color=text, image=imageload.search_gsi,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, width=315, anchor=W, border_color=border, border_width=2, command=lambda: webbrowser.open_new_tab(winaobj.SEARCH_GSI_URL))

forum_nonfirmwares_forpda_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.forum_official_firmwares_forpda}', image=imageload.forpda, text_color=text,corner_radius=2, width=315, anchor=W, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: webbrowser.open_new_tab(f'{vendorvice.nonofficial_firmwares_forum_forpda}'))

adbsideload_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.adbsideload}', image=imageload.adb, text_color=text,corner_radius=2, width=315, anchor=W, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2)

customboot_button = CTkButton(gsi_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), height=45, text=f'{lang.install_customboot}', image=imageload.customboot, text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, width=495, anchor=W, hover_color=hover, border_color=border, border_width=2, command=customboot)

background.place(x=1, y=1)
close_button.place(x=795, y=470)
flash_custom_partition_button.place(x=40, y=110)
approve_custom_load_button.place(x=40, y=163)
wipe_data_button.place(x=40, y=216)
delete_product_button.place(x=40, y=269)
search_gsi_button.place(x=580, y=110)
forum_nonfirmwares_forpda_button.place(x=580,y=163)
adbsideload_button.place(x=580,y=226)
customboot_button.place(x=40,y=322)

#Entity 8 - About 
about_menu_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(about_menu_frame, image=imageload.background, text='')

walmfast_logo = CTkLabel(about_menu_frame, image=imageload.logo, text='')

program_name = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.program_name}', text_color=text, bg_color=bg)

model_branch = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{winaobj.VERSION} - {winaobj.BRANCH}', text_color=text, bg_color=bg)

made_by = CTkLabel(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.made_by}', text_color=text, bg_color=bg)

close_button = CTkButton(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

extended_button = CTkButton(about_menu_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.extended, text_color=text, image=imageload.extended,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=390, border_width=2, command=donatos)

background.place(x=1, y=1)
walmfast_logo.place(x=120, y=100)
program_name.place(x=400, y=100)
model_branch.place(x=400, y=150)
made_by.place(x=400, y=200)
close_button.place(x=795, y=470)
extended_button.place(x=400, y=270)

#Entity 9 - Customboot installer 
customboot_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(customboot_frame, image=imageload.background, text='')

customboot_hader = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.customboot_hader}', text_color=text, bg_color=bg)

customboot_descryption = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.customboot_description}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

twrp_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.twrp}', text_color=text, image=imageload.twrp,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_base)
orangefox_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.orangefox}', text_color=text, image=imageload.orangefox,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_base)
pbrp_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.pbrp}', text_color=text, image=imageload.pbrp,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=menu_base)

flash_recovery_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=f'{lang.flash_recovery}', text_color=text, image=imageload.flash,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=flash_recovery)

recovery_path_textbox = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='center', width=750, wraplength=750)

select_recovery_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_recovery_image)

flash_recovery_process_hader = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.q_start_flash_recovery_process}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

recovery_yes_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: start_flash_recovery(reboot=True))
recovery_no_button = CTkButton(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: start_flash_recovery(reboot=False))

flashit_partition_attetion = CTkLabel(customboot_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), width=winaobj.WIDTH, height=18, justify='center', text=f'partition', text_color='red', bg_color=bg)

background.place(x=1, y=1)
customboot_hader.place(x=40, y=30)
customboot_descryption.place(x=40, y=120)
close_button.place(x=795, y=470)

#Entity 10 - Задонать пж
donatos_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(donatos_frame, image=imageload.background, text='')

donatos_destination = CTkLabel(donatos_frame, image=imageload.donat_destination, text='')

donatos_me = CTkLabel(donatos_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.program_name}', text_color=text, bg_color=bg)

destination_and_number_card = CTkLabel(donatos_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.donat_me}\n{lang.donat_destination}\n{lang.card_number}', text_color=text, bg_color=bg, justify = LEFT)

close_button = CTkButton(donatos_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

background.place(x=1, y=1)
donatos_destination.place(x=120, y=115)
donatos_me.place(x=400, y=100)
destination_and_number_card.place(x=400, y=150)
close_button.place(x=795, y=470)

#Entity 11 - Language switcher
langswitcher_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(langswitcher_frame, image=imageload.background, text='')

langswitcher_hader = CTkLabel(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.choose_language}', width=950, text_color=text, bg_color=bg)

close_button = CTkButton(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

russian_language = CTkButton(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.russian_language, text_color=text, image=imageload.russian_flag,corner_radius=2, bg_color=bg, height=45, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: write_language('rus'))

english_language = CTkButton(langswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.english_language, text_color=text, image=imageload.english_flag,corner_radius=2, bg_color=bg, height=45, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: write_language('eng'))

background.place(x=1, y=1)
langswitcher_hader.place(x=5, y=100)
close_button.place(x=795, y=470)
russian_language.place(x=300, y=200)
english_language.place(x=500, y=202)

#Entity 12 - Theme switcher
themeswitcher_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(themeswitcher_frame, image=imageload.background, text='')

themeswitcher_hader = CTkLabel(themeswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text=f'{lang.choose_theme}', width=950, text_color=text, bg_color=bg)

close_button = CTkButton(themeswitcher_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

themes_frame = CTkScrollableFrame(themeswitcher_frame, width=380, height=310, bg_color=bg, fg_color=fg, corner_radius=3, border_color=border, border_width=2)

background.place(x=1, y=1)
themeswitcher_hader.place(x=5, y=100)
close_button.place(x=795, y=470)
themes_frame.place(x=285,y=180)

#Entity 13 - GSI System Installer
gsi_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(gsi_frame, image=imageload.background, text='')

gsi_hader = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.gsi_hader}', text_color=text, bg_color=bg)

gsi_descryption = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.gsi_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

select_gsi_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_gsi_image)

gsi_name = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='left', width=750, wraplength=750)

flash_gsi = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.flash_gsi}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=200, command=flash_gsi_step_one)

flash_gsi_process_hader = CTkLabel(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.gsi_process_hader}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

reboot_fastbotd_yes_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: flash_gsi_step_two(reboot=True))
reboot_fastbotd_no_button = CTkButton(gsi_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, width=150, border_color=border, border_width=2, command=lambda: flash_gsi_step_two(reboot=False))

background.place(x=1, y=1)
gsi_hader.place(x=40, y=30)
gsi_descryption.place(x=40, y=120)
close_button.place(x=795, y=470)
select_gsi_button.place(x=795, y=250)

#Entity 14 - Vbmeta Fix Installer
vbmeta_frame = CTkFrame(des, width=winaobj.WIDTH, height=winaobj.HEIGHT, bg_color=bg)

background = CTkLabel(vbmeta_frame, image=imageload.background, text='')

vbmeta_hader = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_BIG), text=f'{lang.vbmeta_hader}', text_color=text, bg_color=bg)

vbmeta_descryption = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.vbmeta_descryption}', text_color=text, bg_color=bg, wraplength=950,justify=LEFT)

close_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_SMALL), text=lang.close, text_color=text, image=imageload.close,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, width=150, border_width=2, command=menu_base)

select_vbmeta_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.select}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=150, command=select_vbmeta_image)

vbmeta_name = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART), text='', text_color=text, bg_color=bg, justify='center', width=750, wraplength=750)

flash_vbmeta = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.flash_vbmeta}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, height=50, width=200, command=flash_vbmeta_step_one)

flash_vbmeta_process_hader = CTkLabel(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.gsi_process_hader}', text_color=text,  bg_color=bg, wraplength=950,justify=LEFT)

reboot_fastbot_yes_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.yes}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, border_color=border, border_width=2, command=lambda: flash_vbmeta_step_two(reboot=True))
reboot_fastbot_no_button = CTkButton(vbmeta_frame, font=(winaobj.FONT_NAME, winaobj.FONT_SIZE_STANDART_MEDIUM), text=f'{lang.no}', text_color=text,corner_radius=2, bg_color=bg, fg_color=fg, hover_color=hover, width=150, border_color=border, border_width=2, command=lambda: flash_vbmeta_step_two(reboot=False))

background.place(x=1, y=1)
vbmeta_hader.place(x=40, y=30)
vbmeta_descryption.place(x=40, y=120)
close_button.place(x=795, y=470)
select_vbmeta_button.place(x=795, y=250)

#Required actions
des.wm_protocol('WM_DELETE_WINDOW', lambda: os._exit(0))

#Debug
gsi_menu_button.configure(state='normal')

#Startup
des.mainloop()