import time
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import zipfile
import smtplib
import os
import logger
from email.message import EmailMessage

email = 'medicup@gmail.com'


def send_mail(archive_files):
    print(email)

    send_mail_status = True


    logger.update_log_file('Found files in the archive-directory. Preparing to email them.')
    from_email = "jest3rware@gmail.com"
    from_password = "#E1T1OAOnY#aW2"
    to_email = email

    subject = "Test data"
    message = "Test message."

    #msg = MIMEBase('application', 'zip')
    msg = MIMEMultipart()

    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    body = 'Test from body '

    msg.attach(MIMEText(body, 'plain'))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    zip_file_list = os.listdir(logger.archive_directory)


    if os.listdir(logger.archive_directory):
        for file_name in zip_file_list:
            zip_path = os.path.abspath(os.path.join(logger.archive_directory, file_name))
            attachment = open(zip_path, 'rb')

            part = MIMEBase('application', 'octet-streaming')
            part.set_payload(attachment.read())
            part.add_header('Content-Disposition', 'attachment; filename= {}'.format(file_name))

            msg.attach(part)

        if os.listdir(logger.archive_directory) is not None:
            try:
                logger.update_log_file(
                    "Sending the following archived test by email: {}".format(
                        zip_file_list
                    )
                )

                print('mail sent')
                gmail.send_message(msg)
                gmail.quit()
                #logger.delete_log_files(logger.archive_directory)

                print(
                    'mail success'
                )
                time.sleep(15)
            except Exception as e:
                print(e)

        else:
            logger.update_log_file("There is nothing to send from {}".format(logger.archive_directory))
