from globals.global_dir import ROOT_DIR
import os

upload_folder = 'uploads'
UPLOAD_PATH = os.path.join(ROOT_DIR, upload_folder)

downloads_folder = 'downloads'
DOWNLOADS_PATH = os.path.join(ROOT_DIR, downloads_folder)
print(DOWNLOADS_PATH)
