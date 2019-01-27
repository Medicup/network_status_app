import datetime
import os.path
import shutil

log_directory = "log_files\\"
archive_directory = "archived_files\\"
full_path = os.path.abspath("{}".format(log_directory))


def create_log_file(new_file):
    file = open(new_file, "w")
    file.close()


def update_log_file(message):
    log_line = "{}--{} \n".format(datetime.datetime.now(), message)
    file = str("{}".format(datetime.datetime.now().strftime("%y-%m-%d-%H")))
    file_name = os.path.abspath("{}{}.csv".format(log_directory, file))
    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
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

    try:
        print(os.path.abspath(log_directory))
        shutil.rmtree(os.path.abspath(log_directory))
        os.mkdir(log_directory)
        update_log_file('Successfully emptied {}.'.format(log_directory))
    except Exception as e:
            update_log_file('***ERROR***,Unable to remove files from ,{},{}'.format(log_directory, e))



