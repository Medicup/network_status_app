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
    log_line = "{}--{} \n".format(datetime.datetime.now(), message)
    file = str("{}".format(datetime.datetime.now().strftime("%y-%m-%d-%H")))
    file_name = os.path.abspath("{}{}.csv".format(log_directory, file))
    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
        create_log_file(file_name)


def archive_log_file(file):
    archived_path = os.path.abspath("{}".format(archive_directory))
    archive_name = os.path.expanduser(
        os.path.join(
            "{}/archive-{}".format(
                archived_path, datetime.datetime.now().strftime("%y%m%d")
            )
        )
    )
    shutil.make_archive(archive_name, "zip", full_path)
    delete_log_files(file)


def delete_log_files(file):
    for file in os.listdir(full_path):
        os.remove(os.path.abspath("{}/{}".format(full_path, file)))
    create_log_file(file)
