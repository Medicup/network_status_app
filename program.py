import requests
import requests.exceptions
from logger import update_log_file
from network_status import network_check, ping_check
import send_mail

url = "http://google.com"
ip_address = "8.8.8.8"


def main():
    send_mail.send_mail()
    update_log_file('Starting program.py')
    #ping_check(url, ip_address)


if __name__ == "__main__":
    main()


