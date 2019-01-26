import datetime
import os.path
import shutil
import send_mail

log_directory = "log_files\\"
archive_directory = "archived_files\\"
full_path = os.path.abspath("{}".format(log_directory))


def create_log_file(new_file):
    file = open(new_file, "w")
    file.close()

    if os.listdir(archive_directory):
        archive_list = os.listdir(archive_directory)
        update_log_file(
            "{}: files found in the archived_files folder.".format(
                os.listdir(archive_directory)
            )
        )
        send_mail.send_mail(archive_list)

    else:
        update_log_file("Archive folder is empty. Skipping email export")


def update_log_file(message):
    #delete_log_files()
    log_line = "{}--{} \n".format(datetime.datetime.now(), message)
    file = str("{}".format(datetime.datetime.now().strftime("%y-%m-%d-%H")))
    file_name = os.path.abspath("{}{}.csv".format(log_directory, file))
    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
        if os.listdir(log_directory) is not None:
            print('there are some items to archive')
            # for list_item in os.listdir(log_directory):
            #     print(list_item)
            archive_log_file()
        else:
            print('there are none')
        create_log_file(file_name)


def archive_log_file():
    archived_path = os.path.abspath("{}".format(archive_directory))
    archive_name = os.path.expanduser(
        os.path.join(
            "{}/archive-{}".format(
                archived_path, datetime.datetime.now().strftime("%y%m%d")
            )
        )
    )
    shutil.make_archive(archive_name, "zip", full_path)


def delete_log_files():

    #delete_folder = [log_directory, archive_directory]

    path = os.path.abspath("{}".format(log_directory))
    print(path)
    # for item in path:
    #     mod_time = os.path.getmtime(item)
    #     print('{} modified at {}'.format(item, mod_time))
    # path = os.path.abspath("{}".format(delete_folder))
    # print(path)
    # for the_file in os.listdir(delete_folder):
    #     try:
    #         os.remove("{}/{}".format(path, the_file))
    #         update_log_file('Successfully removed {} from {}.'.format(the_file, delete_folder))
    #     except Exception as e:
    #         update_log_file('***ERROR*** Unable to remove {} from {}.'.format(the_file, delete_folder))


