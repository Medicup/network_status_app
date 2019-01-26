import csv
import datetime
import glob
import os.path
import time
import zipfile

log_directory = "log_files/"
#(os.path.abspath('{}'.format(log_directory)))

full_path = os.path.abspath("{}".format(log_directory))


def create_log_file(file):
    print('creating file')
    open(file, 'w').close()



def update_log_file(message):
    log_line = "{}--{} \n".format(datetime.datetime.now(), message)
    file = str(datetime.datetime.now().strftime("%y-%m-%d-%H"))
    file_name = (os.path.abspath('{}{}.csv'.format(log_directory, file)))

    if os.path.isfile(file_name) is True:
        with open(file_name, 'a', newline='') as log_file:
            log_file.writelines(log_line)
    else:
        print('file does not exists')
        archive_log_file(file_name)

    print(log_line)


def archive_log_file(file):
    print('new file is {}: '.format(file))
    print('archiving')
    file_list = (os.listdir(full_path)[:-1])
    print(file_list)
    #print(file_list[:-1])
    zf = zipfile.ZipFile(os.path.abspath('{}.zip'.format(datetime.datetime.now().strftime('%y%m%d'))), 'w')
    for file in file_list:
        print(file)
        zf.write(os.path.join(full_path, file))
    create_log_file(file)
