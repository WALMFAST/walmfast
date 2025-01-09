from wget import download
from settings import window_and_objects as winaobj
from settings import version
import os
import shutil
import importlib


def check_update():
    global update

    try:
        os.remove('update/update.py')
    except:
        pass

    try:
        download(winaobj.meta_info_update, 'update/')
    except:
        return False

    try:
        importlib.reload(update)
    except:
        from update import update

    patch_version = update.patch - version.patch

    if update.version == version.version or update.version < version.version:
        if update.patch == version.patch or update.patch < version.patch:
            os.remove('update/update.py')
            return 'Update_normal'
        elif update.patch > version.patch:
            if patch_version < 1 or patch_version > -1:
                return 'Update_recommend'
            elif patch_version > 1:
                return 'Update_required'
    elif update.version > version.version:
        return 'Update_required'
    
def update_app(status):

    rootfs = os.getcwd()

    if status == 'Update_recommend':

        if os.path.isdir(f'{rootfs}/backup') == True:
            if os.path.isdir(f'{rootfs}/backup/{os.path.basename(rootfs)}') == True:
                shutil.rmtree(f'{rootfs}/backup/{os.path.basename(rootfs)}')
            else:
                pass
        else:
            try:
                os.mkdir(f'{rootfs}/backup')
            except:
                pass

        for file_backup in os.listdir(rootfs):    

            if file_backup == 'backup':
                continue
            else:
                pass         

            if os.path.isdir(f'{rootfs}/{file_backup}') == True:
                shutil.copytree(f'{rootfs}/{file_backup}', f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_backup}')
            else:
                pass
            
            if os.path.isfile(f'{rootfs}/{file_backup}') == True:
                shutil.copyfile(f'{rootfs}/{file_backup}', f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_backup}')
            else:
                pass
        
        for update_file in update.update_packages:
            
            os.remove(update_file)
            
            try:
                download(f'{update.repository}{update.branch}/{update_file}', f'{rootfs}/{update_file}')
            except:
                shutil.copyfile(f'{rootfs}/backup/{os.path.basename(rootfs)}/{update_file}', f'{rootfs}/{update_file}')
                shutil.rmtree(f'{rootfs}/backup/')
                os.remove(f'{rootfs}/update/update.py')
                return False

        try:    
            os.remove(f'{rootfs}/update/update.py')
        except:
            pass
            
        return True
    
    if status == 'Update_required':

        if os.path.isdir(f'{rootfs}/backup') == True:
            if os.path.isdir(f'{rootfs}/backup/{os.path.basename(rootfs)}') == True:
                shutil.rmtree(f'{rootfs}/backup/{os.path.basename(rootfs)}')
            else:
                pass
        else:
            try:
                os.mkdir(f'{rootfs}/backup')
            except:
                pass
        
        for file_backup in os.listdir(rootfs):

            if file_backup == 'backup':
                continue
            else:
                pass              

            if os.path.isdir(f'{rootfs}/{file_backup}') == True:
                shutil.copytree(f'{rootfs}/{file_backup}', f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_backup}')
            else:
                pass
            
            if os.path.isfile(f'{rootfs}/{file_backup}') == True:
                shutil.copyfile(f'{rootfs}/{file_backup}', f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_backup}')
            else:
                pass
        
        for file_remove in os.listdir(rootfs):

            if file_remove == 'backup':
                continue
            else:
                pass

            if os.path.isdir(f'{rootfs}/{file_remove}') == True:
                shutil.rmtree(f'{rootfs}/{file_remove}')    

            if os.path.isfile(f'{rootfs}/{file_remove}') == True:
                os.remove(f'{rootfs}/{file_remove}')

        try:
            download(f'https://github.com/WALMFAST/walmfast/archive/refs/heads/{update.branch}.zip', f'{rootfs}/walmfast.zip')
            shutil.unpack_archive(f'{rootfs}/walmfast.zip', f'{rootfs}')
            os.remove(f'{rootfs}/walmfast.zip')

            for file_copy in os.listdir(f'{rootfs}/walmfast-{update.branch}'):

                print('!!!UPDATE!!!!\n!!!UPDATE!!!!\n!!!UPDATE!!!!\n!!!UPDATE!!!!\n!!!UPDATE!!!!')
                
                if os.path.isfile(f'{rootfs}/walmfast-{update.branch}/{file_copy}') == True:
                    shutil.copyfile(f'{rootfs}/walmfast-{update.branch}/{file_copy}', f'{rootfs}/{file_copy}')  
                elif os.path.isdir(f'{rootfs}/walmfast-{update.branch}/{file_copy}') == True:
                    shutil.copytree(f'{rootfs}/walmfast-{update.branch}/{file_copy}', f'{rootfs}/{file_copy}')   

            shutil.rmtree(f'{rootfs}/walmfast-{update.branch}')
            shutil.rmtree(f'{rootfs}/backup')
            os.remove(f'{rootfs}/update.py')
            return True
        except:

            try:
                shutil.rmtree(f'{rootfs}/walmfast-{update.branch}')
            except:
                pass

            for file_return in os.listdir(f'{rootfs}/backup/{os.path.basename(rootfs)}/'):

                print('!!!ERROR!!!!\n!!!ERROR!!!!\n!!!ERROR!!!!\n!!!ERROR!!!!\n!!!ERROR!!!!')

                if file_return == 'backup':
                    continue
                
                if os.path.isdir(f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_return}') == True:
                    shutil.copytree(f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_return}', f'{rootfs}/{file_return}')
                elif os.path.isfile(f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_return}') == True:
                    shutil.copyfile(f'{rootfs}/backup/{os.path.basename(rootfs)}/{file_return}', f'{rootfs}/{file_return}')

            try:
                os.remove(f'{rootfs}/update/update.py')
            except:
                pass

            return False
