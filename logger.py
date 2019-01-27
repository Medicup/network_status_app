import datetime
import os.path
import shutil
import static_references

full_path = os.path.abspath("{}".format(static_references.log_directory))


def create_log_file(new_file):
    file = open(new_file, "w")
    file.close()


def update_log_file(message):
    log_line = "{}--{} \n".format(datetime.datetime.now(), message)
    file = str("{}".format(datetime.datetime.now().strftime("%y-%m-%d-%H")))
    file_name = os.path.abspath("{}{}.csv".format(static_references.log_directory, file))
    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
        try:
            os.mkdir(static_references.log_directory)
        except:
            pass # directory already exists
        create_log_file(file_name)



def delete_log_files():

    try:
        print(os.path.abspath(static_references.log_directory))
        shutil.rmtree(os.path.abspath(static_references.log_directory))
        os.mkdir(static_references.log_directory)
        update_log_file('Successfully emptied {}.'.format(static_references.log_directory))
    except Exception as e:
            update_log_file('***ERROR***,Unable to remove files from ,{},{}'.format(static_references.log_directory, e))



