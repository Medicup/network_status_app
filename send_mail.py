import time
import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import zipfile
import smtplib
import os
import logger
from email.message import EmailMessage
import socket

default_email = 'medicup@gmail.com'


def send_mail(email=default_email):
#    check_for_content_to_mail()
    zip_files()
    #mailer()


def zip_files():
    name = 'networkLogArchive_{}.zip'.format(datetime.datetime.now().strftime('%y%m%d'))
    directory = logger.log_directory
    file_paths = get_all_file_paths(directory)

    try:
        with zipfile.ZipFile(name, 'w') as zip_file:
            for file in file_paths:
                zip_file.write(file)

    except Exception as e:
        return 'Unable to zip all files as planned: {}'.format(e)

    logger.delete_log_files()
    logger.update_log_file('all files zipped')


def get_all_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def check_for_content_to_mail():
    if os.listdir(logger.archive_directory):
        print('Found files in {}. Preparing to email them.'.format(logger.archive_directory))
        logger.update_log_file('Found files in {}. Preparing to email them.'.format(logger.archive_directory))
        mailer()

    else:
        logger.update_log_file('The {} directory is empty. Skipping email. '.format(logger.archive_directory))


def mailer():
    from_email = "jest3rware@gmail.com"
    from_password = "#E1T1OAOnY#aW2"
    to_email = default_email

    subject = "Network log files report"
    message = 'Attached is an archive file from {}'.format(socket.gethostname())

    msg = MIMEBase('application', 'zip')
    #msg = MIMEMultipart()

    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    body = 'Test from body '

    msg.attach(MIMEText(body, 'plain'))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    # zip_file_list = [file for file in os.listdir(folder_path)]
    # for files in zip_file_list:
    #     print(files)
    #
    # for file_name in zip_file_list:
    #     zip_path = os.path.abspath(os.path.join(logger.archive_directory, file_name))
    #     attachment = open(zip_path, 'rb')
    #
    #     part = MIMEBase('application', 'octet-streaming')
    #     part.set_payload(attachment.read())
    #     part.add_header('Content-Disposition', 'attachment; filename= {}'.format(file_name))
    #
    #     msg.attach(part)
    #
    # if os.listdir(logger.archive_directory) is not None:
    #     try:
    #         logger.update_log_file(
    #             "Sending the following archived test by email: {}".format(
    #                 zip_file_list
    #             )
    #         )
    #
    #         print('mail sent')
    #         gmail.send_message(msg)
    #         gmail.quit()
    #         #logger.delete_log_files(logger.archive_directory)
    #
    #         print(
    #             'mail success'
    #         )
    #         time.sleep(15)
    #     except Exception as e:
    #         print(e)


def delete_files(path):
    folder_path = path

    #print('zip_file_list = {}'.format(zip_file_list))


