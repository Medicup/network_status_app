import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import zipfile
import smtplib
import os
import logger
import glob
import pathlib
from email import encoders
import socket
import static_references


body = []


def send_mail(email=static_references.default_email):
    zip_files()
    check_for_content_to_mail()


def message_body_update(message):
    time_stamp = datetime.datetime.now().strftime('%y-%m-%d-%H: ')
    message_body = (time_stamp, message)
    body.append(message_body)
    print(message_body)


def zip_files():
    name = 'networkLogArchive_{}.zip'.format(datetime.datetime.now().strftime('%y%m%d'))
    file_paths = get_all_file_paths(static_references.log_directory)
    func_name = '(zip_files)'
    try:
        with zipfile.ZipFile(name, 'w') as zip_file:
            for file in file_paths:
                zip_file.write(file)
        message_body_update('all files zipped')
    except zipfile.BadZipFile as e:
        message_body_update('BadZipFile exception raised as {} {}'.format(e, func_name))
    except zipfile.LargeZipFile as e:
        message_body_update('LargeZipFile exception raised as {} {}'.format(e, func_name))
    except Exception as e:
        message_body_update('Unknown ZipFile error as {} {}'.format(e, func_name))


def get_all_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def check_for_content_to_mail():
    func_name = '(check_for_content_to_mail)'
    mail_list = []
    if os.listdir('.'):
        zip_list = os.listdir('.')
        for file in zip_list:
            if os.path.isfile(file) and '.zip' in file:
                mail_list.append(file)
                mailer(mail_list)
            else:
                pass
            message_body_update('Located archive file(s) for export {} {}'.format(mail_list, func_name))


def create_error_log(message):
    time_stamp = datetime.datetime.now().strftime(('%y-%m-%d-%H:%M'))
    day_stamp = datetime.datetime.now().strftime(('%y-%m-%d-%H'))
    log_line = "{}, {} \n".format(time_stamp, message)
    file_name = os.path.abspath("{}{}.csv".format(static_references.log_directory, str(day_stamp)))

    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
        try:
            os.mkdir(static_references.log_directory)
        except FileExistsError:
            pass  # directory already exists


def mailer(mail_list):
    func_name = mail_list
    archive_list = mail_list
    message_body_update('files to archive: {}'.format(archive_list))

    from_email = "jest3rware@gmail.com"
    from_password = "#E1T1OAOnY#aW2"
    to_email = static_references.default_email

    subject = "Network log files report"
    message = 'Attached is an archive file from {}'.format(socket.gethostname())

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email
    msg_body = message

    try:
        for file in mail_list:
            zf = open(file, 'rb')
            part = MIMEBase('application', "octet-stream")
            part.set_payload(zf.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='{}'.format(file))
            msg.attach(part)
    except IOError as e:
        message_body_update('{},{}'.format(e, func_name))

    msg.attach(MIMEText(msg_body, 'plain'))
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    try:
        gmail.send_message(msg)
        message_body_update('Mail successfully sent.')
        gmail.quit()

        try:
            # for p in pathlib.Path('.').glob('*.zip'):
            for f in glob.glob('*.zip'):
                os.remove(f)
            # if os.path.isfile(file):
            #     os.remove(file)
        except OSError as e:
            create_error_log('{}, {}'.format(e, func_name))

    except smtplib.SMTPException as e:
        create_error_log(': {}, {}'.format(e, func_name))

    except Exception as e:
        create_error_log(': {}, {}'.format(e, func_name))



