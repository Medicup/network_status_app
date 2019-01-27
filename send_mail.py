import datetime
import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zipfile
import smtplib
import os
import glob
from email import encoders
import static_references
import credentials_email

body = []
body.append('Initiating email log:')

def send_mail(email=static_references.default_email):
    zip_files()
    check_for_content_to_mail(email)


def message_body_update(message):
    message_body = ('log entry at {}: {} \n'.format(static_references.time_stamp, message))
    body.append(message_body)


def zip_files():
    name = 'networkLogArchive_{}.zip'.format(datetime.datetime.now().strftime('%y%m%d'))
    file_paths = get_all_file_paths(static_references.log_directory)
    func_name = '(zip_files)'
    try:
        with zipfile.ZipFile(name, 'w') as zip_file:
            for file in file_paths:
                zip_file.write(file)
                message_body_update('{} zipped'.format(file))
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


def check_for_content_to_mail(email):
    func_name = '(check_for_content_to_mail)'

    try:
        mail_list = os.listdir('.')
        zip_list = [attachment for attachment in mail_list if attachment.endswith('.zip')]
        mailer(zip_list, email)
    except IOError as e:
        message_body_update('Unable to create zip_list {}, {}'.format(e, func_name))


def create_error_log(message):
    day_stamp = datetime.datetime.now().strftime(('%y-%m-%d-%H'))
    log_line = "{}, {} \n".format(static_references.time_stamp, message)
    file_name = os.path.abspath("{}error_log{}.csv".format(static_references.log_directory, str(day_stamp)))

    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
        try:
            os.mkdir(static_references.log_directory)
        except FileExistsError:
            pass  # directory already exists


def mailer(zipped_list, email=static_references.default_email):
    func_name = zipped_list
    archive_list = zipped_list
    message_body_update('files to archive: {}'.format(archive_list))

    from_email = credentials_email.email
    from_password =credentials_email.password

    subject = "Network log files report"

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = email

    for attachment in zipped_list:
        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        try:
            with open(attachment, 'rb') as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                msg.attach(part)
        except IOError as e:
            create_error_log('{},{}'.format(e, func_name))

    message = str(body)

    msg.attach(MIMEText(message, 'plain'))
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    try:
        gmail.send_message(msg)
        message_body_update('Mail successfully sent.')
        gmail.quit()

        try:
            for f in glob.glob('*.zip'):
                os.remove(f)
            for f in glob.glob('log_files/*'):
                os.remove(f)
        except OSError as e:
            create_error_log('{}, {}'.format(e, func_name))

    except smtplib.SMTPAuthenticationError:
        create_error_log('error: SMTPAuthenticationError, {}'.format(func_name))

    except smtplib.SMTPServerDisconnected:
        create_error_log('error: The server unexpectedly disconnects, {}'.format(func_name))

    except smtplib.SMTPSenderRefused:
        create_error_log('error: Semder address refused, {}'.format(func_name))

    except smtplib.SMTPRecipientsRefused:
        create_error_log('error: All recipient addresses refused, {}'.format(func_name))

    except smtplib.SMTPDataError:
        create_error_log('error: The SMTP server refused to accept the message data, {}'.format(func_name))

    except smtplib.SMTPConnectError:
        create_error_log('error: Error occurred during establishment of a connection with the server, {}'.format(func_name))

    except smtplib.SMTPHeloError:
        create_error_log('error: The server refused our "HELO" message, {}'.format(func_name))

    except smtplib.SMTPException as e:
        create_error_log(': {}, {}'.format(e, func_name))

    except Exception as e:
        create_error_log(': {}, {}'.format(e, func_name))




