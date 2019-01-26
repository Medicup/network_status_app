from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import smtplib
import os
import logger
from email.message import EmailMessage

email = 'medicup@gmail.com'


def send_mail(archive_files):
    print(email)

    send_mail_status = True
    while send_mail_status is True:
        if os.listdir(logger.archive_directory):
            logger.update_log_file('Found files in the archive-directory. Preparing to email them.')
            from_email = "jest3rware@gmail.com"
            from_password = "#E1T1OAOnY#aW2"
            to_email = email

            subject = "Test data"
            message = "Hey there, your height is <strong>%s</strong>."

            msg = MIMEText(message, "html")
            msg["Subject"] = subject
            msg["To"] = to_email
            msg["From"] = from_email
            file_list = os.listdir(logger.archive_directory)
            for file in file_list:
                path = os.path.abspath(os.path.join(logger.archive_directory,file))
                #with open(file, 'rb') as export:
                print(path)
                #     csv_file = export.read()
                # msg.add_attachment(csv_file)

            gmail = smtplib.SMTP("smtp.gmail.com", 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login(from_email, from_password)

            archive_file_list = []
            for archive_file in archive_files:
                if archive_file.endswith(".zip"):
                    archive_file_list.append(archive_file)
            if archive_file_list is not None:
                logger.update_log_file(
                    "Sending the following archived files by email: {}".format(
                        archive_file_list
                    )
                )
            else:
                logger.update_log_file("There is nothing to send".format(archive_file_list))

            try:
                print('testing email send')
                #gmail.send_message(msg)
                logger.update_log_file('Archived files were sent')
                #todo delete files

            except Exception as e:
                logger.update_log_file('Sendmail error on archive export: {}'.format(e))
                send_mail_status = False
        else:
            logger.update_log_file('No files were found in the archive folder. ')
